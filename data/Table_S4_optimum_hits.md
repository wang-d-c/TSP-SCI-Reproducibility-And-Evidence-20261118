## Supplementary Table S4. Attainment of published optima on the six public R4 instances

| Map | Published optimum | C | M | K | LKH-GPX2 | LKH-POP |
|---|---|---|---|---|---|---|
| RUE-1500 | 28369732 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| RUE-2000 | 32633059 | 1/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| NETGEN-1500 | 9149713 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| NETGEN-2000 | 9852725 | 3/3 | 3/3 | 3/3 | 0/3 | 1/3 |
| MORPH-1500 | 18533583 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 |
| MORPH-2000 | 21099918 | 3/3 | 3/3 | 3/3 | 0/3 | 1/3 |
| All six | — | 16/18 | 18/18 | 18/18 | 10/18 | 14/18 |

Entries give the number of independently recounted delivered tours equal in length to the published optimum, divided by the number of runs. Each of the five methods delivered on all 18 runs here. All six source instances matched the benchmark files byte for byte, including the EUC_2D specification. The reference values were computed with Concorde and published by Kerschke et al. The present study compared lengths against those values without rerunning an exact solver or auditing a proof certificate.

On the eight public V22 instances, C, M and K attained the published optimum in 37/40, 36/40 and 39/40 runs, respectively. The per-instance values for both batches are in `Table_S4_source_all_public_maps.csv`. V22 is reported separately because it used a different implementation and execution environment. The 18 project-generated maps across the two batches have no externally verified reference here.

Reference: Kerschke P, Kotthoff L, Bossek J, Hoos HH, Trautmann H. Leveraging TSP Solver Complementarity through Machine Learning. Evolutionary Computation 26(4), 597–620 (2018). [Article](https://doi.org/10.1162/evco_a_00215) · [Authors’ data record and Concorde targets](https://tspalgsel.github.io/#data) · [Stirling study instances](https://datastorre.stir.ac.uk/handle/11667/127).
