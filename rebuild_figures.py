"""Rebuild Figure 1 and Supplementary Figure S1 from the bundled public CSVs."""

import argparse
import csv
from pathlib import Path
from statistics import mean

import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, MultipleLocator


DATA = Path(__file__).resolve().parent / "data"
BLUE = "#1B5A78"
RUST = "#9F472C"
INK = "#18272E"
GRAY = "#78878C"


def rows(data, name):
    with (data / name).open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def save(fig, output, name):
    fig.savefig(output / (name + ".png"), dpi=450)
    fig.savefig(output / (name + ".pdf"), metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)


def pretty_percent(value, digits):
    return f"{value:.{digits}f}".replace("-", "−") + "%"


def style_axes(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["bottom", "left"]].set_color(GRAY)
    ax.tick_params(color=GRAY, labelcolor=INK, length=3)
    ax.set_axisbelow(True)


def map_effects(data, output):
    maps = [r for r in rows(data, "R4_map_comparisons.csv") if r["comparison"] == "K_vs_M"]
    families = ["RUE", "NETGEN", "MORPH", "uniform", "clustered", "mixed"]
    if len(maps) != 12 or len({r["map_id"] for r in maps}) != 12:
        raise ValueError("Expected twelve different K/M maps.")
    for family in families:
        if sum(r["category"] == family for r in maps) != 2:
            raise ValueError(f"Expected two maps in the {family} family.")
    maps.sort(key=lambda r: (families.index(r["category"]), r["map_id"]))
    positions = [1, 2, 3, 4, 5, 6, 8.6, 9.6, 10.6, 11.6, 12.6, 13.6]
    values = [float(r["mean_improvement_percent"]) for r in maps]
    avg = mean(values)
    most_negative = min(range(len(values)), key=values.__getitem__)

    fig = plt.figure(figsize=(7.45, 5.60))
    grid = fig.add_gridspec(1, 3, width_ratios=(1.45, 4.02, 1.05), wspace=0.07,
                            left=0.036, right=0.980, bottom=0.19, top=0.90)
    labels = fig.add_subplot(grid[0])
    ax = fig.add_subplot(grid[1], sharey=labels)
    counts = fig.add_subplot(grid[2], sharey=ax)
    for side in (labels, counts):
        side.axis("off")
    labels.set_ylim(14.15, -0.45)
    ax.set_xlim(-0.0100, 0.0061)

    for pane in (labels, ax, counts):
        for y in (1, 5, 10.6):
            pane.axhspan(y - 0.45, y + 1.45, color="#F4F7F8", ec="none", zorder=0)
    for y, label in ((0.02, "Public · 1,500–2,000"), (7.58, "Synthetic · 10,000")):
        labels.text(0, y, label, va="center", ha="left", fontsize=8.8, fontweight="bold",
                    color=INK, transform=labels.get_yaxis_transform(), clip_on=False)
    counts.text(0.5, 0.02, "Shorter / tied / longer", ha="center", va="center", fontsize=7.7,
                color=INK, transform=counts.get_yaxis_transform(), clip_on=False)

    for i, (r, y, effect) in enumerate(zip(maps, positions, values)):
        map_id = r["map_id"].removeprefix("V242-")
        if r["category"] in families[3:]:
            family = r["category"].capitalize()
            map_id = f"{family} · {map_id}"
        labels.text(0, y, map_id, ha="left", va="center", fontsize=8.6,
                    transform=labels.get_yaxis_transform(), color=INK)
        counts.text(0.5, y, f'{r["shorter"]} / {r["tie"]} / {r["longer"]}',
                    ha="center", va="center", fontsize=8.6, color=INK,
                    transform=counts.get_yaxis_transform())
        if effect == 0:
            ax.scatter(effect, y, s=25, color="white", edgecolors=INK, linewidths=0.9, zorder=4)
        elif abs(effect) < 0.0000001:
            marker = "<" if effect < 0 else ">"
            color = RUST if effect < 0 else BLUE
            ax.scatter(effect, y, marker=marker, s=35, color=color, zorder=4)
        else:
            ax.barh(y, effect, height=.55, zorder=3, linewidth=.8,
                    color=BLUE if effect > 0 else "#F9E5DB",
                    edgecolor=BLUE if effect > 0 else RUST,
                    hatch=None if effect > 0 else "////")
        if i == most_negative:
            ax.annotate(pretty_percent(effect, 5), xy=(effect, y), xytext=(5, 0),
                        textcoords="offset points", ha="left", va="center", color=INK,
                        fontsize=7.8, bbox=dict(facecolor="#F9E5DB", edgecolor="none", pad=1.2), zorder=5)

    ax.axvline(0, color=GRAY, linewidth=.85, zorder=2)
    ax.axvline(avg, color=INK, linestyle="--", linewidth=1.1, zorder=2)
    ax.xaxis.set_major_locator(MultipleLocator(.0025))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.4f}".replace("-", "−")))
    ax.tick_params(axis="y", left=False, labelleft=False)
    ax.set_xlabel("Mean relative reduction of K versus M (%)", color=INK, labelpad=7)
    ax.grid(axis="x", color="#D6DFE2", linewidth=.56)
    style_axes(ax)
    ax.spines["left"].set_visible(False)
    legend = [
        Patch(facecolor=BLUE, edgecolor=BLUE, label="K shorter on average"),
        Patch(facecolor="#F9E5DB", edgecolor=RUST, hatch="////", label="K longer on average"),
        Line2D([0], [0], color=INK, marker="o", markerfacecolor="white", linestyle="none",
               label="Exactly zero"),
        Line2D([0], [0], color=RUST, marker="<", linestyle="none",
               label="Tiny negative effect"),
        Line2D([0], [0], color=INK, linestyle="--",
               label=f"Equal-map mean {pretty_percent(avg, 6)}"),
    ]
    fig.legend(handles=legend, loc="lower center", bbox_to_anchor=(.5, .025), ncol=3,
               frameon=False, fontsize=8, columnspacing=1.65, handletextpad=.55)
    save(fig, output, "Figure_1_R4_K_vs_M")


def start_final(data, output):
    points = [(float(r["start_improvement_percent"]), float(r["final_improvement_percent"]),
               int(r["number_of_pairs"])) for r in rows(data, "Figure_S1_plot_coordinates.csv")]
    if any(x <= 0 or n < 1 for x, _, n in points) or sum(n for _, _, n in points) != 20:
        raise ValueError("Expected twenty pairs with a shorter K start.")
    fig, ax = plt.subplots(figsize=(7.1, 4.95))
    fig.subplots_adjust(left=.14, right=.975, bottom=.20, top=.93)
    xmax = max(x for x, _, _ in points) * 1.08
    ymax = max(y for _, y, _ in points) * 1.46
    ax.set_xlim(0, xmax)
    ax.set_ylim(min(y for _, y, _ in points) * 1.15, ymax)

    cases = [
        (1, "K final shorter", dict(marker="o", facecolors=BLUE, edgecolors=BLUE)),
        (0, "Final tied", dict(marker="D", facecolors="white", edgecolors=INK)),
        (-1, "K final longer", dict(marker="x", c=RUST)),
    ]
    for sign, label, style in cases:
        selected = [(x, y, n) for x, y, n in points if (y > 0) - (y < 0) == sign]
        xs, ys, multiplicities = zip(*selected) if selected else ([], [], [])
        ax.scatter(xs, ys, s=[48 + 22 * (n - 1) for n in multiplicities], linewidths=1.15,
                   label=f"{label} ({sum(multiplicities)})", zorder=3, **style)
    ax.axhline(0, color=GRAY, linewidth=.85)
    ax.plot([0, min(xmax, ymax)], [0, min(xmax, ymax)], color="#4B6C77", linewidth=1.05,
            linestyle="--", label="Equal start and final reductions")

    for x, y, n in points:
        if n > 1:
            ax.annotate(f"{n} pairs", xy=(x, y), xytext=(28, -22), textcoords="offset points",
                        ha="left", va="center", fontsize=8.4, color=INK, zorder=5,
                        arrowprops=dict(arrowstyle="->", color=GRAY, lw=.8, shrinkB=4),
                        bbox=dict(facecolor="white", edgecolor="none", alpha=.93, pad=1.2))
    decline_x, decline_y, _ = min(points, key=lambda point: point[1])
    ax.annotate(pretty_percent(decline_y, 5), xy=(decline_x, decline_y), xytext=(9, 5),
                textcoords="offset points", color=RUST, ha="left", va="bottom", fontsize=8.5)

    ax.set_xlabel("Starting-tour reduction of K versus M (%)", color=INK)
    ax.set_ylabel("Final-tour reduction of K versus M (%)", color=INK)
    ax.xaxis.set_major_locator(MultipleLocator(.005))
    ax.yaxis.set_major_locator(MultipleLocator(.01))
    for axis in (ax.xaxis, ax.yaxis):
        axis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.3f}".replace("-", "−")))
    ax.grid(color="#D6DFE2", linewidth=.52)
    style_axes(ax)
    fig.legend(loc="lower center", bbox_to_anchor=(.51, .035), ncol=2, frameon=False,
               fontsize=8.6, columnspacing=1.6)
    save(fig, output, "Figure_S1_start_vs_final")


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("output", type=Path, help="new directory for Figure 1 and Figure S1")
    cli.add_argument("--data-dir", type=Path, default=DATA,
                     help="directory containing the two public CSVs")
    args = cli.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9.5,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })
    map_effects(args.data_dir, args.output)
    start_final(args.data_dir, args.output)


if __name__ == "__main__":
    main()
