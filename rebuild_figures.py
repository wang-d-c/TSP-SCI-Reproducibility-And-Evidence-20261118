"""Render the manuscript figures using the public map effects and plot coordinates."""

import argparse
import csv
from pathlib import Path
from statistics import mean

import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


DATA = Path(__file__).resolve().parent / "data"


def rows(name):
    with (DATA / name).open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def save(fig, output, name):
    for ext in ("png", "pdf"):
        fig.savefig(output / (name + "." + ext), dpi=300)
    plt.close(fig)


def map_effects(output):
    maps = [r for r in rows("R4_map_comparisons.csv") if r["comparison"] == "K_vs_M"]
    if len(maps) != 12 or len({r["map_id"] for r in maps}) != 12:
        raise ValueError("Expected twelve different K/M maps.")
    values = [float(r["mean_improvement_percent"]) for r in maps]
    avg = mean(values)
    fig, ax = plt.subplots(figsize=(7.1, 5.8), layout="constrained")
    for i, value in enumerate(values):
        ax.barh(i, value, height=.68, facecolor="#333333" if value > 0 else "white",
                edgecolor="#111111", linewidth=.85, hatch="////" if value < 0 else None)
        if value == 0:
            ax.plot(0, i, marker="|", markersize=8, color="black")
    ax.set_yticks(range(len(maps)), [r["map_id"].removeprefix("V242-") for r in maps])
    ax.invert_yaxis()
    ax.axvline(0, color="black", linewidth=.8)
    ax.axvline(avg, color="black", linestyle="--", linewidth=1.3)
    ax.set_xlabel("Mean relative reduction of K versus M (%)")
    ax.grid(axis="x", color="#cccccc", linewidth=.5)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    labels = [
        Patch(facecolor="#333333", edgecolor="black", label="Positive"),
        Patch(facecolor="white", edgecolor="black", hatch="////", label="Negative"),
        Line2D([0], [0], color="black", linestyle="--",
               label="Equal-map mean: " + f"{avg:.6f}%".replace("-", "−")),
    ]
    ax.legend(handles=labels, loc="lower center", bbox_to_anchor=(.5, 1.01),
              ncol=3, frameon=False, fontsize=8)
    save(fig, output, "Figure_1_R4_K_vs_M")


def start_final(output):
    points = [(float(r["start_improvement_percent"]), float(r["final_improvement_percent"]),
               int(r["number_of_pairs"])) for r in rows("Figure_S1_plot_coordinates.csv")]
    if any(x <= 0 or n < 1 for x, _, n in points) or sum(n for _, _, n in points) != 20:
        raise ValueError("Expected twenty pairs with a shorter K start.")
    fig, ax = plt.subplots(figsize=(6.7, 4.9), layout="constrained")
    cases = [
        (1, "K final shorter", dict(marker="o", facecolors="#222222", edgecolors="#222222")),
        (0, "Final tied", dict(marker="D", facecolors="white", edgecolors="#222222")),
        (-1, "K final longer", dict(marker="x", c="#222222")),
    ]
    for sign, label, style in cases:
        selected = [(x,y) for x,y,n in points if (y > 0) - (y < 0) == sign for _ in range(n)]
        xs, ys = zip(*selected) if selected else ([], [])
        ax.scatter(xs, ys, s=46, linewidths=1.1, label=f"{label} ({len(selected)})", **style)
    ax.axhline(0, color="#555555", linewidth=.8)
    ax.axvline(0, color="#aaaaaa", linewidth=.6)
    ax.set_xlabel("Starting-tour reduction of K versus M (%)")
    ax.set_ylabel("Final-tour reduction of K versus M (%)")
    ax.grid(color="#d5d5d5", linewidth=.45)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(.5, 1.13), ncol=3, frameon=False, fontsize=8)
    for x, y, n in points:
        if n > 1:
            ax.annotate(f"{n} pairs", xy=(x, y), xytext=(6, 8), textcoords="offset points", fontsize=8)
    save(fig, output, "Figure_2_start_vs_final")


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("output", type=Path, help="a new directory for the two PDF and PNG figures")
    out = cli.parse_args().output
    out.mkdir(parents=True, exist_ok=False)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "pdf.fonttype": 42, "ps.fonttype": 42})
    map_effects(out)
    start_final(out)


if __name__ == "__main__":
    main()
