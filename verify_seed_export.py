"""Recompute the paired historical estimates from the released numerical rows."""
import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parent
TABLE=ROOT/"data/historical_seeds"


def read(name,n):
    with (TABLE/name).open(encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==len({(r["map_id"],r["seed"],r["method"]) for r in rows})==n
    assert all((bool(r["length"]) and int(r["length"])>0) == (r["status"]=="valid") for r in rows)
    return rows


def differences(rows,left,right):
    keyed=defaultdict(dict)
    for r in rows:
        if r["status"]=="valid":
            keyed[r["map_id"],int(r["seed"])][r["method"]]=int(r["length"])
    return [(name,seed,values[right]-values[left],Decimal(100)*
             Decimal(values[right]-values[left])/Decimal(values[right]))
            for (name,seed),values in sorted(keyed.items()) if {left,right}<=set(values)]


def summarize(rows,left,right):
    effects=differences(rows,left,right)
    maps=defaultdict(list)
    for name,_,_,effect in effects:
        maps[name].append(effect)
    map_mean=sum(sum(g)/len(g) for g in maps.values())/len(maps)
    order=[sum(compare(delta) for _,_,delta,_ in effects) for compare in
           (lambda d:d>0,lambda d:d==0,lambda d:d<0)]
    return {"pairs":len(effects),"maps":len(maps),"shorter_tied_longer":order,
            "map_equal_mean_percent":map_mean}


def main():
    v22=read("V22_method_results_300.csv",300)
    r4=read("R4_method_results_180.csv",180)
    assert sum(r["status"]=="valid" for r in r4)==164
    checks=(
        (r4,"K_three_pair_GPX2","M_best_parent", [9,21,6], "-0.0004050368851267785"),
        (r4,"K_three_pair_GPX2","C_project", [13,16,7], "0.0033270718611023626"),
        (r4,"K_three_pair_GPX2","LKH_GPX2", [17,10,2], "0.024225386"),
        (r4,"K_three_pair_GPX2","LKH_POP", [13,14,0], "0.031630365"),
        (v22,"K","M", [44,41,15], "0.002930011"),
        (v22,"K","C", [36,38,26], "0.003476334"),
    )
    for batch,x,y,wlt,mean in checks:
        s=summarize(batch,x,y)
        assert s["shorter_tied_longer"]==wlt and abs(s["map_equal_mean_percent"]-Decimal(mean))<Decimal("0.000000001")
        print(f"{batch[0]['batch']} {x}/{y}: {s['maps']} maps, {s['pairs']} valid pairs, "
              f"{'/'.join(map(str,wlt))}, mean {s['map_equal_mean_percent']:.9f}%")

if __name__=="__main__":
    main()
