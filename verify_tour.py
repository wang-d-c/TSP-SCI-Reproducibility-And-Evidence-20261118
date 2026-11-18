"""Count one explicit TSPLIB TOUR using EUC_2D and integer coordinates."""
import argparse
from math import isqrt
from pathlib import Path


def sections(path, section):
    lines = [line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    pivot = lines.index(section)
    head = {}
    for line in lines[:pivot]:
        key, separator, value = line.partition(":")
        if separator:
            key = key.strip().upper()
            if key in {"TYPE", "DIMENSION", "EDGE_WEIGHT_TYPE"}:
                if key in head:
                    raise ValueError(f"duplicate {key}")
                head[key] = value.strip().upper()
    body = lines[pivot + 1:]
    if body and body[-1] == "EOF":
        body.pop()
    return head, body


def verify(instance, tour):
    h, coordinates = sections(instance, "NODE_COORD_SECTION")
    th, sequence = sections(tour, "TOUR_SECTION")
    n = int(h["DIMENSION"])
    if h.get("TYPE") != "TSP" or h.get("EDGE_WEIGHT_TYPE") != "EUC_2D" or n < 3:
        raise ValueError("expected an explicit EUC_2D TSP of at least three cities")
    if th.get("TYPE") != "TOUR" or int(th["DIMENSION"]) != n:
        raise ValueError("incompatible TOUR header")
    points = {}
    for line in coordinates:
        city, x, y = map(int, line.split())
        if city in points or not 1 <= city <= n:
            raise ValueError(f"invalid or duplicate city {city}")
        points[city] = (x, y)
    order = [int(k) for line in sequence for k in line.split()]
    if not order or order.pop() != -1:
        raise ValueError("missing -1 terminator")
    if len(order) != n or len(points) != n or set(order) != points.keys():
        raise ValueError("incomplete tour or coordinate set")
    total = 0
    previous = points[order[-1]]
    for city in order:
        x, y = points[city]
        square = (x-previous[0])**2 + (y-previous[1])**2
        # For integer squared distance, nint(sqrt(square)) = (isqrt(4*square)+1)//2.
        total += (isqrt(4*square)+1)//2
        previous = (x, y)
    return n, total


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("instance", type=Path)
    p.add_argument("tour", type=Path)
    p.add_argument("--expect", type=int)
    a = p.parse_args()
    dimension, length = verify(a.instance, a.tour)
    if a.expect is not None and length != a.expect:
        raise SystemExit(f"length mismatch: found {length}, expected {a.expect}")
    print(f"Valid closed tour: {dimension} cities; EUC_2D length {length}.")
