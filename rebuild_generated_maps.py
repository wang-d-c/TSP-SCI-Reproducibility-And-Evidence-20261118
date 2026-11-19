"""Reconstruct the geometry and registered input bytes of the 18 project-generated maps."""
import argparse
import csv
import hashlib
from pathlib import Path

MANIFEST=Path(__file__).with_name("generated_map_manifest.csv")


def number(domain, seed, city, axis, dup, modulus):
    limit=(2**64//modulus)*modulus
    for retry in range(100):
        tag=f"{domain}|{seed}|{city}|{axis}|{dup}|{retry}".encode("ascii")
        draw=int.from_bytes(hashlib.sha256(tag).digest()[:8],"big")
        if draw<limit:
            return draw%modulus
    raise RuntimeError("coordinate rejection limit exceeded")


def coordinates(domain, seed, family):
    used=set()
    for city in range(10_000):
        if family=="uniform":
            x0,y0,nx,ny=0,0,10000,10000
        elif family=="clustered":
            k=city%32
            x0,y0,nx,ny=300+1250*(k%8),950+2500*(k//8),601,601
        elif family=="mixed":
            bands=((1000,450,8001,451),(1000,9000,8001,501),(450,1000,451,8001),
                   (9000,1000,501,8001),(1500,1500,7001,7001))
            x0,y0,nx,ny=bands[city%4 if city<8000 else 4]
        else:
            raise ValueError(family)
        for dup in range(10_000):
            point=(x0+number(domain,seed,city,"x",dup,nx),y0+number(domain,seed,city,"y",dup,ny))
            if point not in used:
                used.add(point)
                yield point
                break
        else:
            raise RuntimeError("coordinate duplicate limit exceeded")


def map_bytes(row):
    name,seed,family=row["map_id"],int(row["generation_seed"]),row["geometry"]
    if row["batch"]=="V22":
        domain="V20"
        header=f"NAME : {name}\nCOMMENT : V20 preregistered {family} seed {seed}\nTYPE : TSP\nDIMENSION : 10000\nEDGE_WEIGHT_TYPE : EUC_2D\n"
    else:
        domain="V19"
        header=f"NAME: {name}\nTYPE: TSP\nCOMMENT: V24.2 proposed confirmation; generator V19; seed {seed}\nDIMENSION: 10000\nEDGE_WEIGHT_TYPE: EUC_2D\n"
    body="".join(f"{i} {x} {y}\n" for i,(x,y) in enumerate(coordinates(domain,seed,family),1))
    return (header+"NODE_COORD_SECTION\n"+body+"EOF\n").encode("ascii")


def main():
    p=argparse.ArgumentParser()
    p.add_argument("destination",type=Path,help="New output directory")
    a=p.parse_args()
    with MANIFEST.open(encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=18:
        raise ValueError("expected 18 frozen project-generated maps")
    products=[]
    for row in rows:
        data=map_bytes(row)
        if hashlib.sha256(data).hexdigest()!=row["sha256"]:
            raise ValueError(f"byte-level provenance check failed for {row['map_id']}")
        products.append((row["map_id"],data))
    a.destination.mkdir(parents=True,exist_ok=False)
    for name,data in products:
        (a.destination/f"{name}.tsp").write_bytes(data)
    print("All 18 generated inputs match their original SHA-256 checksums.")

if __name__=="__main__":
    main()
