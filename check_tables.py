"""Check published map aggregates and public input identities, without external packages."""
import csv
import hashlib
import math
import re
import random
from collections import Counter
from decimal import Decimal
from itertools import product
from pathlib import Path
from statistics import fmean

ROOT = Path(__file__).resolve().parent


def read(relative):
    with (ROOT / relative).open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def require(condition, message):
    if not condition:
        raise ValueError(message)

def check_uncertainty(rows, summary):
    values = [Decimal(m["mean_improvement_percent"]) for m in sorted(rows, key=lambda m: m["map_id"])]
    v = list(map(float, values))
    prng = random.Random(20261116)
    resamples = sorted(fmean(prng.choices(v, k=len(v))) for _ in range(20000))
    for probability, name in [(0.025, "ci95_low_percent"), (0.975, "ci95_high_percent")]:
        at = (len(resamples)-1) * probability
        i = int(at)
        quantile = resamples[i] + (at-i) * (resamples[i+1]-resamples[i])
        require(math.isclose(quantile, float(summary[name]), abs_tol=1e-12), summary["comparison"]+" interval")
    nz = [item for item in values if item != 0]
    observed = abs(sum(values))
    extreme_count = sum(abs(sum(s*a for s,a in zip(signs,nz))) >= observed for signs in product((-1,1), repeat=len(nz)))
    p = extreme_count / 2**len(nz)
    require(math.isclose(p, float(summary["sign_flip_p"]), abs_tol=1e-12), summary["comparison"]+" test")
    return p


def main():
    maps = read("replay/stirling_14.csv")
    require(len(maps) == len({m["map_id"] for m in maps}) == 14, "instance manifest")
    for m in maps:
        raw = (ROOT / "instances" / m["batch"] / (m["map_id"] + ".tsp")).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == m["member_sha256"], m["map_id"])
    print("14 original Stirling members matched their registered hashes.")

    by_map = read("data/R4_map_comparisons.csv")
    p_values = [(1.0, "EAX_untested", 1.0)]
    for summary in read("data/R4_summary.csv"):
        key = summary["comparison"]
        paired = [m for m in by_map if m["comparison"] == key and int(m["paired_seeds"]) > 0]
        require(len(paired) == len({m["map_id"] for m in paired}) == int(summary["maps_with_pairs"]), key)
        mean = fmean(float(m["mean_improvement_percent"]) for m in paired)
        require(math.isclose(mean, float(summary["map_equal_mean_improvement_percent"]), abs_tol=1e-12), key)
        counts = [sum(int(m[category]) for m in paired) for category in ("shorter", "tie", "longer")]
        require(counts == [int(summary["pair_" + k]) for k in ("shorter", "tie", "longer")], key)
        print(f"R4 {key}: {len(paired)} maps, {counts[0]}/{counts[1]}/{counts[2]}, {mean:+.9f}%")
        if summary["holm_p_five_main"]:
            p_values.append((check_uncertainty(paired, summary), key, float(summary["holm_p_five_main"])))
    adjusted = 0.0
    require(len(p_values) == 5, "R4 primary family size")
    for rank, (p_value, key, reported) in enumerate(sorted(p_values)):
        adjusted = max(adjusted, min(1., (len(p_values)-rank) * p_value))
        require(math.isclose(adjusted, reported, abs_tol=1e-12), key + " Holm adjustment")
    print("R4 primary intervals, sign-flip p-values and five-comparison Holm correction reproduced.")

    old = read("data/V22_20_maps_CN.csv")
    require(len(old) == len({m["地图编号"] for m in old}) == 20, "V22 map identity")
    for key in ["K对M", "K对C", "M对C"]:
        counts = [0, 0, 0]
        for m in old:
            match = re.fullmatch(r"(\d+)胜(\d+)平(\d+)负", m[key + "五次胜平负"])
            require(match is not None, m["地图编号"])
            for i, n in enumerate(match.groups()):
                counts[i] += int(n)
        mean = fmean(float(m[key + "平均相对缩短百分比"]) for m in old)
        print(f"V22 {key}: 20 maps, {counts[0]}/{counts[1]}/{counts[2]}, {mean:+.9f}%")

    outcomes = Counter()
    for p in read("data/Figure_S1_plot_coordinates.csv"):
        x = float(p["start_improvement_percent"])
        y = float(p["final_improvement_percent"])
        require(x > 0, "Figure S1 requires a shorter K start")
        outcomes["shorter" if y > 0 else "longer" if y < 0 else "tie"] += int(p["number_of_pairs"])
    require(outcomes == Counter(shorter=9, tie=5, longer=6), "Figure S1")
    print("Figure S1: among 20 shorter K starts, K finished shorter/tied/longer 9/5/6 times.")


if __name__ == "__main__":
    main()
