"""Plot all 36 valid R4 K/M seed pairs at their original embedding-map identities."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from verify_seed_export import differences, read


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("destination",type=Path)
    args=parser.parse_args()
    args.destination.mkdir(parents=True,exist_ok=True)
    rows=differences(read("R4_method_results_180.csv",180),"K_three_pair_GPX2","M_best_parent")
    assert len(rows)==36
    names=sorted({r[0] for r in rows},key=lambda n:("10000" in n,n))
    seeds=sorted({r[1] for r in rows})
    colors={seeds[0]:"#17617F",seeds[1]:"#4C3B87",seeds[2]:"#BA5324"}
    markers={seeds[0]:"o",seeds[1]:"s",seeds[2]:"^"}
    fig,ax=plt.subplots(figsize=(7.5,5.05),layout="constrained")
    for i,name in enumerate(names):
        if i%2==0:
            ax.axhspan(i-.5,i+.5,color="#F1F4F6",zorder=0)
        batch=[r for r in rows if r[0]==name]
        for _,seed,_,effect in batch:
            shift=(seeds.index(seed)-1)*.19
            ax.scatter(float(effect)*10_000,i+shift,s=33,marker=markers[seed],
                       color=colors[seed],edgecolor="white",linewidth=.5,zorder=3)
        ax.plot([min(float(r[3])*10_000 for r in batch),max(float(r[3])*10_000 for r in batch)],
                [i,i],color="#9AA9B3",alpha=.8,linewidth=1)
    ax.axvline(0,color="#415765",linewidth=1)
    ax.axhline(5.5,color="#D5DEE5")
    ax.set_yticks(range(len(names)),[n.removeprefix("V242-") for n in names])
    ax.invert_yaxis()
    ax.set_xlabel("K/M relative reduction (ppm; positive favors K)")
    ax.set_title("Historical R4 seed pairs",loc="left")
    ax.legend(handles=[Line2D([0],[0],color=colors[s],marker=markers[s],linestyle="none",label=f"Seed {s}") for s in seeds],
              loc="upper left",ncol=3,frameon=False,bbox_to_anchor=(0,1.15))
    ax.grid(axis="x",color="#D9E1E7",linewidth=.75)
    for side in ("top","right"):
        ax.spines[side].set_visible(False)
    for ext in ("pdf","png"):
        fig.savefig(args.destination/f"R4_KM_individual_historical_seeds.{ext}",dpi=420,
                    metadata={"Creator":"plot_historical_seed_pairs.py"})
    plt.close(fig)

if __name__=="__main__":
    main()
