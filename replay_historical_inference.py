"""Replay the published V22 inference and link R4 map tables to registered seed rows."""

import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
from statistics import fmean

import numpy as np

from check_tables import ROOT, check_uncertainty, read, require
from verify_seed_export import differences, read as read_seed_rows


V22_STRATA = ("public", "uniform", "clustered", "mixed")
V22_PRIMARY = ("K_vs_C", "K_vs_M")


def agree(observed, recorded, label):
    require(math.isclose(float(observed), float(recorded), rel_tol=0, abs_tol=1e-12), label)


def pair_groups(rows, left, right):
    groups = defaultdict(list)
    for map_id, seed, delta, effect in differences(rows, left, right):
        groups[map_id].append((seed, delta, effect))
    return groups


def split_counts(pairs):
    values = [delta for _, delta, _ in pairs]
    return [sum(d > 0 for d in values), sum(d == 0 for d in values), sum(d < 0 for d in values)]


def exact_flip(values):
    nonzero = [value for value in values if value]
    denominator = math.lcm(*(value.denominator for value in nonzero))
    integers = [value.numerator * (denominator // value.denominator) for value in nonzero]
    cutoff = abs(sum(integers))
    extreme = sum(abs(sum(s * v for s, v in zip(signs, integers))) >= cutoff
                  for signs in product((-1, 1), repeat=len(integers)))
    return extreme / 2**len(integers)


def stratified_bootstrap(map_effect, order, strata):
    rng = np.random.Generator(np.random.PCG64(20261112))
    replicates = [0.0] * 20000
    for stratum in V22_STRATA:
        values = [float(map_effect[map_id]) for map_id in order if strata[map_id] == stratum]
        indexes = rng.integers(len(values), size=(len(replicates), len(values)))
        for i, row in enumerate(indexes):
            replicates[i] += sum(values[int(j)] for j in row)
    replicates.sort()
    replicates = [value / len(order) for value in replicates]
    return {name: list(np.quantile(replicates, quantiles, method="linear"))
            for name, quantiles in [("95", [0.025, 0.975]), ("97.5", [0.0125, 0.9875])]}


def holm(raw):
    previous = 0.0
    adjusted = {}
    for rank, (key, p) in enumerate(sorted(raw.items(), key=lambda item: (item[1], item[0]))):
        previous = max(previous, min(1.0, (len(raw) - rank) * p))
        adjusted[key] = previous
    return adjusted


def v22(rows):
    maps = read("data/V22_20_maps_CN.csv")
    order = [row["地图编号"] for row in maps]
    require(order == list(dict.fromkeys(row["map_id"] for row in rows)), "V22 frozen map order")
    require(len(order) == 20 and all(row["status"] == "valid" for row in rows), "V22 row inventory")
    synthetic = {row["map_id"]: row["geometry"] for row in read("generated_map_manifest.csv") if row["batch"] == "V22"}
    strata = {map_id: synthetic.get(map_id, "public") for map_id in order}
    require(Counter(strata.values()) == dict(public=8, uniform=4, clustered=4, mixed=4), "V22 map strata")
    reference = json.loads((ROOT / "data/historical_seeds/V22_frozen_inference_reference.json").read_text(encoding="utf-8"))
    output = {}
    for left, right in [("K", "C"), ("K", "M"), ("M", "C")]:
        label = f"{left}_vs_{right}"
        groups = pair_groups(rows, left, right)
        require(set(groups) == set(order) and all(len(g) == 5 for g in groups.values()), label)
        lengths = {(row["map_id"], int(row["seed"]), row["method"]): int(row["length"]) for row in rows}
        means = {}
        for item, map_id in zip(maps, order):
            exact = [Fraction(100 * delta, lengths[(map_id, seed, right)]) for seed, delta, _ in groups[map_id]]
            means[map_id] = sum(exact, Fraction(0)) / len(exact)
            agree(means[map_id], item[f"{left}对{right}平均相对缩短百分比"], f"V22 {map_id} {label}")
            s, t, l = split_counts(groups[map_id])
            require(f"{s}胜{t}平{l}负" == item[f"{left}对{right}五次胜平负"], f"V22 {map_id} {label} signs")
        result = {"map_count": len(means), "pair_count": sum(map(len, groups.values())),
                  "shorter_tied_longer": split_counts([pair for group in groups.values() for pair in group]),
                  "map_equal_mean_percent": float(sum(means.values(), Fraction(0)) / len(means))}
        target = reference["comparisons"][label]
        require(result["shorter_tied_longer"] == target["shorter_tied_longer"], label + " pair counts")
        agree(result["map_equal_mean_percent"], target["map_equal_mean_percent"], label + " mean")
        if label in V22_PRIMARY:
            result["intervals"] = stratified_bootstrap(means, order, strata)
            for level, interval in result["intervals"].items():
                for value, expected in zip(interval, target["intervals"][level]):
                    agree(value, expected, label + " interval " + level)
            result["exact_sign_flip_p"] = exact_flip(means.values())
            agree(result["exact_sign_flip_p"], target["exact_sign_flip_p"], label + " sign flip")
        output[label] = result
    adjusted = holm({label: output[label]["exact_sign_flip_p"] for label in V22_PRIMARY})
    for label, value in adjusted.items():
        output[label]["holm_p_two_primary"] = value
        agree(value, reference["comparisons"][label]["holm_p_two_primary"], label + " Holm")
    return {"method_slots": len(rows), "status_counts": dict(Counter(row["status"] for row in rows)), "comparisons": output}


def r4(rows):
    table = read("data/R4_map_comparisons.csv")
    counts = Counter(row["status"] for row in rows)
    require(counts == dict(valid=164, budget_no_delivery=15, monitor_invalid=1), "R4 state counts")
    output = {}
    p_values = {"EAX_untested": 1.0}
    for summary in read("data/R4_summary.csv"):
        label = summary["comparison"]
        groups = pair_groups(rows, summary["left"], summary["right"])
        paired = [row for row in table if row["comparison"] == label and int(row["paired_seeds"]) > 0]
        require(set(groups) == {row["map_id"] for row in paired}, label + " paired-map coverage")
        means = []
        for item in paired:
            matched = groups[item["map_id"]]
            counts_expected = [int(item[key]) for key in ("shorter", "tie", "longer")]
            require(len(matched) == int(item["paired_seeds"]) and split_counts(matched) == counts_expected,
                    label + " map/seed counts")
            mean = fmean(effect for _, _, effect in matched)
            agree(mean, item["mean_improvement_percent"], label + " map effect")
            means.append(mean)
        all_pairs = [pair for group in groups.values() for pair in group]
        result = {"map_count": len(groups), "pair_count": len(all_pairs), "shorter_tied_longer": split_counts(all_pairs),
                  "map_equal_mean_percent": fmean(means)}
        require(result["map_count"] == int(summary["maps_with_pairs"]) and result["pair_count"] == int(summary["paired_seed_count"]), label)
        require(result["shorter_tied_longer"] == [int(summary["pair_" + key]) for key in ("shorter", "tie", "longer")], label)
        agree(result["map_equal_mean_percent"], summary["map_equal_mean_improvement_percent"], label)
        if summary["holm_p_five_main"]:
            p_values[label] = check_uncertainty(paired, summary)
            result["recorded_interval_percent"] = [float(summary["ci95_low_percent"]), float(summary["ci95_high_percent"])]
            result["verified_sign_flip_p"] = p_values[label]
            result["recorded_holm_p_five_main"] = float(summary["holm_p_five_main"])
        output[label] = result
    require(len(p_values) == 5, "R4 family size")
    for label, value in holm(p_values).items():
        if label != "EAX_untested":
            agree(value, output[label]["recorded_holm_p_five_main"], label + " Holm")
    return {"method_slots": len(rows), "status_counts": dict(counts), "comparisons": output}


def main():
    v22_rows = read_seed_rows("V22_method_results_300.csv", 300)
    r4_rows = read_seed_rows("R4_method_results_180.csv", 180)
    result = {"status": "verified_numerical_replay", "V22": v22(v22_rows), "R4": r4(r4_rows), "numpy": np.__version__}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
