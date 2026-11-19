# When a Better Recombined Tour Does Not Yield a Better Final Tour: A Fixed-Budget Empirical Study of LKH-Based Search

## Abstract

Under a fixed budget, a better intermediate solution may be offset by the cost of obtaining it or by a different subsequent search trajectory. We examine this trade-off for the symmetric Euclidean traveling salesperson problem using three frozen project configurations: continuous LKH-derived search C, continuation from the best of three parents M, and K, which adds three pairwise GPX2 recombinations of the same parents before continuation. The parents are physically shared by M and K but their full generation cost is charged to both; K additionally pays the recombination, selection and validation costs. In the local Windows R4 batch, twelve preselected maps and three seeds yielded 36 map–seed groups with valid C, M and K tours. K versus M was shorter, tied and longer in 9, 21 and 6 pairs; the map-equal mean reduction was −0.000405% with an exploratory map-level 95% interval of [−0.002241%, 0.001096%]. K versus C was 13/16/7, with a mean reduction of 0.003327%. The observed map ties limited the resolution of the registered family-wise tests. On six public maps, both M and K attained the published optimum in all 18 paired runs. Two author LKH configurations produced budget non-deliveries, and a comparable unified edge-assembly-crossover baseline remains incomplete. The separately reported 20-map CPU2 batch had a positive K/M mean. A conditional old-pool diagnostic shows that shorter starts sometimes end worse, without isolating the cause. The study measures the net effect of additional recombination in a same-parent, separately charged comparison and examines whether intermediate gains persist in delivered tours. The evidence is limited to the recorded instances, configurations and budgets.

**Keywords:** traveling salesperson problem; Lin–Kernighan–Helsgaun; partition crossover; fixed-budget optimization; reproducibility; non-delivery

## 1. Introduction

When a heuristic must deliver a complete tour by a fixed deadline, time devoted to creating and combining initial tours is time not available for later search. The Lin–Kernighan–Helsgaun (LKH) heuristic [1] and generalized partition crossover (GPX2) [2,3] are established approaches. They can be composed in many ways, but an improvement of the intermediate tour does not itself establish an improvement of the final delivered tour. GPX2 already supports recombination among LKH results, and earlier studies have considered both crossover inside LKH and feedback of improved solutions to search [2–4].

We compare three project-defined configurations rather than propose a new crossover. C starts independently from the instance, M selects the shortest of three parent tours and continues search, and K performs three additional pairwise GPX2 operations on that same pool before continuation. Necessary generation, selection, recombination, verification and delivery are charged to the appropriate method. We ask whether the additional three-pair preparation improves final tour quality relative to M under the same total budget. Secondary questions concern comparison with continuous C, registered author LKH configurations, and the relationship between starting and final quality.

This study contributes a same-parent comparison in which both M and K are charged for producing their shared parents, alongside separate reporting of route quality and delivery. It measures the net effect of K’s three additional recombinations and describes when a shorter selected starting tour did not retain its advantage at the deadline. The earlier V22 batch and the conditional old-pool diagnostic provide separately reported context. These observations apply to the recorded configurations and do not by themselves identify the cause of a reversal.

## 2. Related work

Helsgaun’s LKH implements the Lin–Kernighan heuristic [1]. LKH-2 extended k-opt submoves [14], and the LKH-3 report describes the later solver lineage [15]. GPX2 identifies recombining components and was evaluated within LKH and across separate runs [2,3]. Hains et al. [4] studied crossover on clustered TSP instances. These studies motivate an incremental comparison under a fixed delivery budget.

POPMUSIC has been used to construct LKH candidate edges using tour information [5]. Friedrich et al. [6] and Weise et al. [7] study fixed-budget bet-and-run strategies, including allocation of decision time and prediction; choosing among short initial searches is therefore not a new general strategy. Zhang and Looks [8] use backbone information from tours to guide LK search and perturbation. Our M is a concrete comparison configuration, not an invented bet-and-run framework. Recent candidate-list and partition-crossover studies [9,10] further limit any general novelty claim. McMenemy et al. [11] already compared LKH variants and EAX across a large set of structurally varied instances and investigated instance characteristics; their setting and budgets differ from ours. The present study differs operationally by recording the exact shared parent pool, charging its cost to both arms, and testing the *net* effect of three additional external GPX2 calls on delivered tours. Different implementations, benchmarks and deadlines prevent direct numerical comparisons with the cited studies.

## 3. Problem and comparison methods

For coordinates \((x_i,y_i)\), EUC_2D edge cost is \(d(i,j)=\lfloor\sqrt{(x_i-x_j)^2+(y_i-y_j)^2}+0.5\rfloor\). A feasible solution is a closed permutation of all cities, with length \(L(T)\) equal to the sum of its edges. Independent checks validate coverage, uniqueness, closure and length; they do not prove global optimality.

P5 is the project’s frozen Windows LKH-derived configuration. Its registered settings use POPMUSIC candidate generation, no subgradient ascent, five candidates per node and internal GPX2. Each M/K continuation starts a fresh P5-resume process. The selected tour is supplied through INITIAL_TOUR_FILE and candidate generation runs in that process. Supplementary Table S1 documents the settings and implementation scope.

* **C — continuous:** start from the coordinates and run the frozen strong P5 configuration, including its registered internal GPX2 use.
* **M — best parent:** generate three complete parent tours, select the shortest verified parent, and continue P5 from that tour. M does not make K's three *additional external* GPX2 calls; its underlying search retains its configured internal recombination.
* **K — three-pair recombination:** use the identical actual three-parent pool (P1, P2, P3), apply external GPX2 to the three pairs (P1, P2), (P1, P3) and (P2, P3), verify the resulting candidates, select the shortest legitimate parent or offspring, and continue with the same P5 continuation rules.

For the frozen configuration, the three parent seeds are \(s,s+1000,s+2000\), and M/K continuation uses \(s+3000\). A parent stage is capped at a nominal 17 seconds. Candidate selection retains a prior candidate on ties. The first actual working cycle of continuation is checked against the selected input. The method labels are local labels rather than standard names. The configuration, executable hashes and source-bound parameter records are listed in Supplementary Tables S1 and S2.

```text
Input: instance I, group seed s, frozen programs and parameters.
C: search from I; retain an eligible certified complete tour.
Generate and verify parent tours P1, P2 and P3 sequentially.
Record the necessary full common-prefix cost.
M: select the best parent; continue P5; charge the prefix and M's own work.
K: GPX2(P1,P2), GPX2(P1,P3), GPX2(P2,P3); verify candidates;
   select the best parent or valid offspring; continue P5;
   charge the prefix and all K-specific preparation and continuation work.
For each method: record and certify the eligible final complete tour and
its deadline, or retain the actual non-delivery or error status.
```

M and K physically reuse the same recorded parent pool, not three separately resampled parents. The full measured prefix is nevertheless invoiced to each method; K additionally pays its own GPX2, candidate selection and validation. Physical queuing and admission waiting are recorded separately, and M is not made to wait for K's recombination. The two continuation lengths may differ because the total budget, rather than the post-prefix search duration, is the controlled resource.

## 4. Experimental design and validity

### 4.1 Batches and execution

The earlier V22 batch was run on CPU2 using native Windows with an AMD EPYC 7T83 processor. It includes 20 fixed maps, five search seeds per map, and 100 C/M/K groups, for 300 valid method results. Its dataset comprises eight public research instances at 1,000–2,000 cities and twelve generated 10,000-city instances. CPU2 and later local results are not combined in a common test.

R4 used native Windows on a laptop with an Intel Core Ultra 9 275HX and about 47.38 GiB of system-visible memory. Each of 12 preselected instances used seeds 541, 761 and 981. The six generated 10,000-city instances comprise two uniform (U), two clustered (C) and two mixed (R) instances. In instance names, C identifies the clustered family. Supplementary Table S1 describes the generators. The six 1,500–2,000-city RUE, NETGEN and MORPH instances come from the Stirling collection [11]. The inputs use the TSPLIB EUC_2D convention [16]. Two previously exposed map–seed groups remain in the main analysis and are handled separately in the exposure sensitivity.

R4 ran serially with one search task at a time and the registered CPU0 affinity. M preceded K within each shared pool. Affinity specifies placement. Per-arm temperature, effective frequency and trial counts were unavailable for quantifying any order or thermal effect. The project P5, the LKH 3.0.14 Ascent64 builds and the Windows GA-EAX adaptation have separate version records.

The local R4 accounting protocol uses a 90-second total ceiling, search stopping/closing by 86 seconds, certified delivery strictly before 88 seconds, and final cleanup within 90 seconds. Necessary startup, input, initialization, parent production, recombination, continuation, validation and delivery are charged. Recorded discovery, observation, certification, stop and cleanup times are distinct. Admission waiting before a task and physical queueing are reported separately and do not give an in-progress task free continuation time. The earlier V22 protocol and its recorded timestamps are interpreted separately rather than overwritten to match R4.

### 4.2 Quality, failure and statistical analysis

For method X against reference Y, a paired percentage reduction is
\[
r_{X,Y}=100\frac{L(Y)-L(X)}{L(Y)}.
\]
Positive values favor X. Same-map, same-seed pairs are averaged within each map; the available map means are then equally weighted. Seeds are repeated observations within a map, not independent maps. Each map's valid-pair count and failed outcomes are retained. Non-delivery or engineering failure receives neither a zero distance nor an arbitrarily large one, and is not a route-quality win for the other method.

The R4 analysis uses 20,000 map-level bootstrap resamples with the registered random seed and percentile rule, keeping all within-map comparisons together. Intervals are exploratory for this fixed finite map set. Prespecified primary comparisons are K/M, K/C and K against the three registered external configurations. Two-sided exact map-level sign-flip tests and Holm correction are applied to this five-comparison family; the sign-flip inference requires sign symmetry or exchangeability of map-level paired differences under the null, and the non-random fixed maps, fixed M/K order and prior case exposure limit its interpretation; the untested EAX comparison is not treated as significant or silently removed from the family. Other comparisons are descriptive/secondary. Leave-one-map and exposure analyses are sensitivities, not grounds for selecting favorable instances. Failure to reject a difference does not prove equivalence.

## 5. Results

### 5.1 Earlier CPU2 batch

V22 produced 300 valid C/M/K results with no recorded formal failures or retries. K/C was shorter/tied/longer in 36/38/26 of the 100 seed groups and had a map-equal mean reduction of 0.0034763%; K/M was 44/41/15 with 0.0029300%; M/C was 27/37/36 with 0.0005457%. The earlier V23 audit used 20,000 map-level bootstrap resamples stratified by map family and reported 95% intervals of [0.0012516%, 0.0058313%] and [0.0016491%, 0.0041841%] for K/C and K/M, respectively. In 64 groups K's recombination start was strictly shorter than the best parent; final K/M outcomes in those groups were 44 shorter, five tied and 15 longer. These are CPU2 results under that batch's protocol, not observations that can be paired or pooled with local R4.

### 5.2 Local R4 C/M/K results

All C, M and K slots yielded valid routes on 12 maps and three seeds. Table 1 reports the map-weighted results. K was shorter more often than it was longer relative to M, but the longer outcomes had a larger average magnitude. The K/M interval crosses zero and the observed data do not demonstrate equivalence.

**Table 1. R4 complete paired route comparisons.**

| Comparison | Valid seed pairs / maps | X shorter / tied / longer | Map-equal mean reduction (%) | Exploratory 95% interval (%) |
|---|---:|---:|---:|---:|
| K/M | 36 / 12 | 9 / 21 / 6 | −0.000405 | [−0.002241, 0.001096] |
| K/C | 36 / 12 | 13 / 16 / 7 | 0.003327 | [0.000745, 0.006461] |
| M/C | 36 / 12 | 11 / 17 / 8 | 0.003732 | [−0.000018, 0.008460] |

The registered five-comparison Holm family is retained. The four estimable contrasts have six or seven nonzero map effects. Their minimum attainable two-sided sign-flip p-values are 0.03125 and 0.015625, respectively, above the first Holm threshold of 0.01. With this observed tie structure the family could not reject at 0.05. The registered p-values document the analysis. The maps, effect estimates and intervals carry the substantive interpretation. M/C is calculated directly from its own pairs.

K/M has two positive, six zero and four negative means under the registered seed-relative metric. Its median map effect is zero. The largest individual improvement was 0.00825% and the largest regression was 0.02858% (139 length units on R10000-01/541). Leaving one map out yields means from −0.000887% to +0.000337%. The registered exposure sensitivity remains slightly negative. Both methods attained the published optimum in all 18 pairs on six 1,500–2,000-city instances [13]. On six 10,000-city maps, K/M was 9 shorter, 3 tied and 6 longer with mean reduction −0.000810%. This exploratory contrast confounds size with origin and structure. On C10000-02 the three absolute K/M differences sum to zero, but seed-specific denominators give the registered map mean a tiny negative sign. The supplementary sensitivity first computes each method’s mean within each map.

![](Figure_1_R4_K_vs_M.png)

Figure 1. Mean R4 K/M reduction by map. Circles mark exact ties, the triangle a tiny negative effect, and the dashed line the equally weighted mean.

**Table 1a. R4 map-level means of paired seed reductions (%).** Each entry averages the three seeds on that map. The small negative value on C10000-02 is not rounded to a tie for sign counting.

| Map | K/M | K/C | M/C |
|---|---:|---:|---:|
| V242-C10000-01 | 0.00490172 | −0.00000006 | −0.0049020 |
| V242-C10000-02 | −0.00000002 | 0.0040537 | 0.0040536 |
| V242-MORPH-1500 | 0 | 0 | 0 |
| V242-MORPH-2000 | 0 | 0 | 0 |
| V242-NETGEN-1500 | 0 | 0 | 0 |
| V242-NETGEN-2000 | 0 | 0 | 0 |
| V242-R10000-01 | −0.00856565 | 0.0155472 | 0.0241129 |
| V242-R10000-02 | −0.00184786 | 0.0058167 | 0.0076644 |
| V242-RUE-1500 | 0 | 0 | 0 |
| V242-RUE-2000 | 0 | 0.0014116 | 0.0014116 |
| V242-U10000-01 | −0.00102209 | 0.0122589 | 0.0132811 |
| V242-U10000-02 | 0.00167346 | 0.0008368 | −0.0008367 |

### 5.3 Author configurations and delivery

**Table 2. R4 terminal status.**

| Method | Valid | Budget non-delivery | Resource-monitor interruption |
|---|---:|---:|---:|
| C | 36 | 0 | 0 |
| M | 36 | 0 | 0 |
| K | 36 | 0 | 0 |
| Author LKH-GPX2 | 29 | 7 | 0 |
| Author LKH-POP | 27 | 8 | 1 |

All 180 R4 slots for these five methods reached a terminal state, with 164 valid routes. Both author-LKH configurations delivered in zero of six runs on the two 10,000-city clustered maps. The twelve logs report completed ascent and 72.97–74.58 CPU s of preprocessing. These CPU times describe the burden of initial work. They do not locate the wall-clock cutoffs. This comparison uses the registered ALPHA/subgradient configurations and provides no controlled comparison with an author LKH POPMUSIC/no-subgradient configuration.

**Table 2a. Secondary comparisons among pairs with valid deliveries.**

| Comparison | Valid pairs / maps | Shorter / tied / longer | Mean reduction (%) |
| --- | --- | --- | --- |
| M / LKH-GPX2 | 29 / 10 | 17 / 10 / 2 | 0.024780 |
| M / LKH-POP | 27 / 10 | 13 / 14 / 0 | 0.031213 |
| C / LKH-GPX2 | 29 / 10 | 16 / 8 / 5 | 0.020421 |
| C / LKH-POP | 27 / 10 | 13 / 12 / 2 | 0.025930 |

The table reports the four secondary valid-pair comparisons. Map means use participating maps with equal weights.

The original R4 EAX arm, based on the author's edge-assembly crossover approach [12], has 19 attempted slots and 17 deferred slots. Eighteen valid results cover the six 10,000-city U/C/R synthetic maps and all three registered seeds; in these available matched pairs M/EAX is 18/0/0 shorter/tied/longer, C/EAX is 16/0/2, and K/EAX is 17/0/1. This coverage was truncated by the task failure and does not represent a complete or independent 12-map EAX comparison. The adapted EAX program and cold-restart wrapper are not byte-identical to the unmodified author release. A separate EAX supplement also has 18 valid, one failure and 17 unstarted slots; the different execution versions/time blocks cannot be selectively pooled to create a complete uniform baseline. EAX execution failure or deferral is not a route-quality victory. No comprehensive claim against EAX is made.

### 5.4 Starting tours and continuation

M and K parent hashes match in all 36 R4 groups. In 16 groups the selected starting cycles are identical up to rotation and reversal, and their final lengths tie. In the remaining 20 groups K starts shorter; it finishes shorter in 9, tied in 5 and longer in 6. On four of the small-map runs, K started at the published optimum while M reached it during continuation. Of the 16 strictly better K starts on the 10,000-city maps, 9 led to shorter endpoints, 1 to a tie and 6 to longer endpoints. No matched external optimum was established for these six large maps. Thus a shorter start did not guarantee the shorter final tour in these observed configurations. The per-group start and final differences are shown in Supplementary Figure S1; their association is descriptive and does not isolate a causal mechanism. It is not possible from this observation alone to attribute the six reversals uniquely to extra recombination time, route structure, initialization state, randomness or other search dynamics.

The three external GPX2 calls took 0.33 s on average. Available continuation allowances averaged 31.15 s for M and 30.88 s for K. On the larger maps the paired allowance difference (M minus K) ranged from −0.288 to +0.450 s. The allowance is computed after charged branch preparation. A longer measured M startup explains the most negative difference (Supplementary Table S3).

A separate 30-second diagnostic used 12 already-exposed development pools from six maps and three continuation seeds per pool (72 valid tasks). Start A was the shortest parent and start B was the tour selected by the historical K procedure. B finished shorter/tied/longer in 12/20/4 of 36 pairs. The 18 same-cycle pairs tied. Among the 18 pairs starting from different cycles, B started shorter and finished shorter/tied/longer in 12/2/4. A ran before B and the already-generated pools were supplied without charge. These repeat seeds characterize sensitivity in the development pools. R4 used different pools and one continuation seed per pool.

## 6. Discussion

The earlier positive mean in V22 and the slightly negative local R4 K/M mean show that the added recombination benefit is not established as stable across these two nonidentical batches. Neither comparison isolates hardware from dataset, time accounting and other differences, so the reversal of batch means should not be assigned to hardware alone. K/M has more shorter than longer seed pairs in R4 but a negative map-equal mean because the few regressions have larger magnitudes; the leave-one-map range includes both signs. Selecting only favorable maps or reporting seed-level wins as independent map-level evidence would obscure that result.

Distinguishing an intermediate gain from a delivered final gain helps evaluate heuristic pipelines under a complete budget. However, prior bet-and-run and GPX literature has already recognized selection and future trajectory issues [3,6,7]. The present contribution is an explicit, auditable comparison in this setting and a quantified observation of reversals, not a new theory or a general proof of why reversals occur. Different starts can consume pseudorandom numbers differently even with equal seed labels. In particular, best-parent M is a strong control for the incremental effect of K's three external operations.

The two author-LKH settings illustrate why delivered quality and delivery probability are separate outcomes. A budget failure applies to the tested setup and deadline. A configuration-matched author LKH baseline with POPMUSIC and no subgradient would be needed to isolate this aspect of the external comparison. The EAX records cover separate versions and remain an incomplete external comparison.

## 7. Limitations and future work

The selected benchmark has only 12 local maps, some previously exposed cases, three seeds per map and two principal scale ranges; inference to all Euclidean or non-Euclidean TSPs is not justified. The valid-pair external comparisons exclude maps without author-LKH deliveries. CPU affinity does not ensure processor isolation, and unrecorded temperature or exact internal discovery times must not be imputed. R4's two LKH configurations and the incomplete EAX supplement do not cover all strong baselines. Independent route validation verifies feasibility and objective value, not the internal correctness of every search operation or global optimality.

The scope of the performance analysis is the completed batches and the explicitly labeled conditional diagnostic. The supplementary execution record documents the incomplete independent confirmation and other development checks, with their exclusions.

A follow-up that separates mechanism from end-to-end effect would combine same-total-budget runs with matched continuation windows or trial counts and repeated continuation seeds per shared pool. Randomizing paired execution order and logging search trajectories would help attribute variation. The current comparison estimates the incremental outcome of the combined procedure.

## 8. Conclusion

In R4, extra recombination improved the selected starting tour in 20 pairs and produced nine shorter, five tied and six longer endings within those pairs. Across the full 12-map batch, K’s mean final quality was slightly worse than M’s and the interval crossed zero. In V22 the K/M mean was positive under a different setting. Together these results motivate measuring delivered tours and preparation time directly when evaluating an extra heuristic stage.

## Reproducibility and declarations

Statistical replay uses the saved paired records, map-level aggregation and figure scripts. A separate checker read 464 historical tours against their coordinate files: 300 from V22 and 164 from R4. It verified city coverage, closure and EUC_2D length. In the local review bundle, 18 project-generated maps suffice for 254 tours. Verifying the other 210 requires the exact 14 third-party coordinate files as well as the corresponding saved tours. A separate check extracted those 14 inputs from locally retained copies of the source archives by member and SHA-256. Combined with the locally held tours and project maps, they yielded 464 matching route lengths. The third-party inputs are available from the University of Stirling data record [11], which states CC BY 4.0.

The [review repository](https://github.com/wang-d-c/TSP-SCI-Reproducibility-And-Evidence-20261118) provides the 14 attributed public instances and the packaged map-level checking and plotting tools. Full seed-level replay requires the authorized inputs listed in the replay instructions. Access to the saved tour orders, generated coordinates and frozen solver chain is handled separately. Re-running the search also requires the recorded executable versions, Windows environment and budget controls. The supplementary execution record describes the observed limit of local solver replay.

## AI assistance

ChatGPT and Codex assisted research design, code development, analysis and manuscript preparation. The authors are responsible for the results, references and final text.

## References

1. Helsgaun, K. (2000). An effective implementation of the Lin–Kernighan traveling salesman heuristic. *European Journal of Operational Research*, 126(1), 106–130. https://doi.org/10.1016/S0377-2217(99)00284-2
2. Tinós, R., Helsgaun, K., & Whitley, D. (2018). Efficient recombination in the Lin–Kernighan–Helsgaun traveling salesman heuristic. *Parallel Problem Solving from Nature*, LNCS 11101, 95–107. https://doi.org/10.1007/978-3-319-99253-2_8
3. Tinós, R., Whitley, D., & Ochoa, G. (2020; online 2019). A new generalized partition crossover for the traveling salesman problem: Tunneling between local optima. *Evolutionary Computation*, 28(2), 255–288. https://doi.org/10.1162/evco_a_00254
4. Hains, D., Whitley, D., & Howe, A. (2012). Improving Lin–Kernighan–Helsgaun with crossover on clustered instances of the TSP. *PPSN XII*, 388–397. https://doi.org/10.1007/978-3-642-32964-7_39
5. Taillard, É. D., & Helsgaun, K. (2019). POPMUSIC for the travelling salesman problem. *European Journal of Operational Research*, 272(2), 420–429. https://doi.org/10.1016/j.ejor.2018.06.039
6. Friedrich, T., Kötzing, T., & Wagner, M. (2017). A generic bet-and-run strategy for speeding up stochastic local search. *AAAI Conference on Artificial Intelligence*, 31, 801–807. https://doi.org/10.1609/aaai.v31i1.10645
7. Weise, T., Wu, Z., & Wagner, M. (2019). An improved generic bet-and-run strategy with performance prediction for stochastic local search. *AAAI Conference on Artificial Intelligence*, 33, 2395–2402. https://doi.org/10.1609/aaai.v33i01.33012395
8. Zhang, W., & Looks, M. (2005). A novel local search algorithm for the traveling salesman problem that exploits backbones. *IJCAI*, 343–349. https://ijcai.org/proceedings/2005/182
9. Heins, J., Schäpermeier, L., Kerschke, P., & Whitley, D. (2024). Dancing to the state of the art? How candidate lists influence LKH for solving the traveling salesperson problem. *PPSN XVIII*, LNCS 15148, 100–115. https://doi.org/10.1007/978-3-031-70055-2_7
10. de Carvalho, O. Q., & Whitley, D. (2025). Dramatically faster partition crossover for the traveling salesman problem. *GECCO ’25*, 818–826. https://doi.org/10.1145/3712256.3726465
11. McMenemy, P., Veerapen, N., Adair, J., & Ochoa, G. (2019). Rigorous performance analysis of state-of-the-art TSP heuristic solvers. *EvoCOP*, LNCS 11452, 99–114. https://doi.org/10.1007/978-3-030-16711-0_7. Associated dataset record: https://datastorre.stir.ac.uk/handle/11667/127 (CC BY 4.0 for the 14 included instance files).
12. Nagata, Y., & Kobayashi, S. (2013). A powerful genetic algorithm using edge assembly crossover for the traveling salesman problem. *INFORMS Journal on Computing*, 25(2), 346–363. https://doi.org/10.1287/ijoc.1120.0506
13. Kerschke, P., Kotthoff, L., Bossek, J., Hoos, H. H., & Trautmann, H. (2018). Leveraging TSP solver complementarity through machine learning. *Evolutionary Computation*, 26(4), 597–620. https://doi.org/10.1162/evco_a_00215
14. Helsgaun, K. (2009). General k-opt submoves for the Lin–Kernighan TSP heuristic. Mathematical Programming Computation, 1, 119–163. https://doi.org/10.1007/s12532-009-0004-6
15. Helsgaun, K. (2017). An extension of the Lin–Kernighan–Helsgaun TSP solver for constrained traveling salesman and vehicle routing problems. [Roskilde University technical report](https://forskning.ruc.dk/da/publications/an-extension-of-the-lin-kernighan-helsgaun-tsp-solver-for-constra/).
16. Reinelt, G. (1991). TSPLIB—A traveling salesman problem library. ORSA Journal on Computing, 3(4), 376–384. https://doi.org/10.1287/ijoc.3.4.376
