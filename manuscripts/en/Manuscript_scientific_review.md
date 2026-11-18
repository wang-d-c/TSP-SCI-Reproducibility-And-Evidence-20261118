# When a Better Recombined Tour Does Not Yield a Better Final Tour: A Fixed-Budget Empirical Study of LKH-Based Search


## Abstract

Under a fixed budget, a better intermediate solution may be offset by the cost of obtaining it or by a different subsequent search trajectory. We examine this trade-off for the symmetric Euclidean traveling salesperson problem using three frozen project configurations: continuous LKH-derived search C, continuation from the best of three parents M, and K, which adds three pairwise GPX2 recombinations of the same parents before continuation. The parents are physically shared by M and K but their full generation cost is charged to both; K additionally pays the recombination, selection and validation costs. In the local Windows R4 batch, twelve preselected maps and three seeds yielded 36 map–seed groups with valid C, M and K tours. K versus M was shorter, tied and longer in 9, 21 and 6 pairs; the map-equal mean reduction was −0.000405% with an exploratory map-level 95% interval of [−0.002241%, 0.001096%]. K versus C was 13/16/7, with a mean reduction of 0.003327%; its prespecified family-wise Holm-adjusted p-value was 0.125. On six public maps, both M and K attained the published optimum in all 18 paired runs. Two author LKH configurations produced budget non-deliveries, and a comparable unified edge-assembly-crossover baseline remains incomplete. The separately reported 20-map CPU2 batch had a positive K/M mean. A conditional old-pool diagnostic shows that shorter starts sometimes end worse, without isolating the cause. The study measures the net effect of additional recombination in a same-parent, separately charged comparison and examines whether intermediate gains persist in delivered tours. The evidence is limited to the recorded instances, configurations and budgets.

**Keywords:** traveling salesperson problem; Lin–Kernighan–Helsgaun; partition crossover; fixed-budget optimization; reproducibility; non-delivery

## 1. Introduction

When a heuristic must deliver a complete tour by a fixed deadline, time devoted to creating and combining initial tours is time not available for later search. The Lin–Kernighan–Helsgaun (LKH) heuristic [1] and generalized partition crossover (GPX2) [2,3] are established approaches. They can be composed in many ways, but an improvement of the intermediate tour does not itself establish an improvement of the final delivered tour. GPX2 already supports recombination among LKH results, and earlier studies have considered both crossover inside LKH and feedback of improved solutions to search [2–4].

We compare three project-defined configurations rather than propose a new crossover. C starts independently from the instance, M selects the shortest of three parent tours and continues search, and K performs three additional pairwise GPX2 operations on that same pool before continuation. Necessary generation, selection, recombination, verification and delivery are charged to the appropriate method. We ask whether the additional three-pair preparation improves final tour quality relative to M under the same total budget. Secondary questions concern comparison with continuous C, registered author LKH configurations, and the relationship between starting and final quality.

This study contributes a same-parent comparison in which both M and K are charged for producing their shared parents, alongside separate reporting of route quality and delivery. It measures the net effect of K’s three additional recombinations and describes when a shorter selected starting tour did not retain its advantage at the deadline. The earlier V22 batch and the conditional old-pool diagnostic provide separately reported context. These observations apply to the recorded configurations and do not by themselves identify the cause of a reversal.

## 2. Related work

Helsgaun's LKH implements an effective Lin–Kernighan heuristic [1]. GPX2 identifies recombining components and was evaluated with multi-trial LKH [2,3]. GPX and GPX2 research already covers multi-run recombination, selection and, in related settings, return of offspring to local search [2–4]. Consequently, multiple parents, pairwise recombination, selection of a shorter start and LKH continuation are not new ideas here. GPX2's piecewise local-optimality discussion also depends on its stated assumptions and does not prove how the time-limited parents in the present experiments behave [3].

POPMUSIC has been used to construct LKH candidate edges using tour information [5]. Friedrich et al. [6] and Weise et al. [7] study fixed-budget bet-and-run strategies, including allocation of decision time and prediction; choosing among short initial searches is therefore not a new general strategy. Zhang and Looks [8] use backbone information from tours to guide LK search and perturbation. Our M is a concrete comparison configuration, not an invented bet-and-run framework. Recent candidate-list and partition-crossover studies [9,10] further limit any general novelty claim. McMenemy et al. [11] already compared LKH variants and EAX across a large set of structurally varied instances and investigated instance characteristics; their setting and budgets differ from ours. The present study differs operationally by recording the exact shared parent pool, charging its cost to both arms, and testing the *net* effect of three additional external GPX2 calls on delivered tours. Different implementations, benchmarks and deadlines prevent direct numerical comparisons with the cited studies.

## 3. Problem and comparison methods

For coordinates \((x_i,y_i)\), EUC_2D edge cost is \(d(i,j)=\lfloor\sqrt{(x_i-x_j)^2+(y_i-y_j)^2}+0.5\rfloor\). A feasible solution is a closed permutation of all cities, with length \(L(T)\) equal to the sum of its edges. Independent checks validate coverage, uniqueness, closure and length; they do not prove global optimality.

P5 denotes the project's frozen LKH-derived configuration; it is not represented as an unmodified author LKH release. The comparison methods are:

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

ChatGPT and Codex were used to assist research-design discussions, code development, data analysis and manuscript preparation. Human authors retain responsibility for the scientific results, references and final manuscript.

### 4.1 Batches and execution

The earlier V22 batch was run on CPU2 using native Windows with an AMD EPYC 7T83 processor. It includes 20 fixed maps, five search seeds per map, and 100 C/M/K groups, for 300 valid method results. Its dataset comprises eight public research instances at 1,000–2,000 cities and twelve generated 10,000-city instances. CPU2 and later local results are not combined in a common test.

The local R4 batch uses twelve preselected maps, three search seeds (541, 761 and 981), and native Windows on a machine reporting an Intel Core Ultra 9 275HX and approximately 47.38 GiB system-visible physical memory. Six maps have 10,000 cities, with two each in the U, C and R generated families; six are 1,500/2,000-city RUE, NETGEN and MORPH public research instances [11]. Input origins, generators, hashes and permissions are recorded in the project manifest; being publicly accessible does not by itself confer unrestricted redistribution rights. Two map–seed groups had earlier exposure and are retained in the main analysis, with separately reported exposure sensitivity. The benchmark is a finite selection, not a random sample of all TSP instances.

Each local method runs serially with the registered CPU0 affinity and one search task at a time. Affinity does not establish exclusive access to a physical core, and monitoring and operating-system activity remain possible. The native builds and source snapshots are versioned; the project P5, signed-coordinate-compatible binaries, author LKH 3.0.14 configurations with required numerical compatibility changes, and GA-EAX Windows adaptation must not be relabeled as byte-identical author releases. The registered author configurations comprise a GPX2/non-population setting and a population setting; these are particular configurations, not a test of every reasonable LKH parameterization. Compiler, executable and per-task hashes are retained with the execution record.

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

The K/M exact sign-flip raw p-value is 0.65625 and the five-comparison Holm-adjusted value is 1. K/C has raw p=0.03125 and adjusted p=0.125. The unadjusted exploratory interval for K/C and the adjusted test answer different questions; the former should not be reported as an adjusted significant result. M/C is computed directly from its own pairs and is not obtained by subtracting separate mean percentages.

K/M map means are positive on two maps, zero on six and negative on four. The median map mean is zero; leaving one map out gives a mean range of −0.000887% to 0.000337%. The largest individual improvement is 0.008249%; the largest regression is −0.028575% (139 length units on R10000-01/541). Prespecified exposed-case sensitivity gives a K/M mean of approximately −0.000378%; it does not replace the complete main analysis. In a post hoc description by size, all 18 paired seeds on the six 1,500/2,000-city maps tie. On the six 10,000-city maps K/M has 9 shorter, 3 tied and 6 longer outcomes, and the equal-map mean reduction is −0.000810%. A post hoc match to external reference values [13] found that both methods reached the published optimum in every one of those 18 small-map pairs (Supplementary Table S4). Once M attained that length, a shorter K endpoint was impossible on that run. These six maps contribute zero to the 12-map mean. Size is confounded with map origin and structure in this selected set, so the contrast does not isolate a size effect or establish equivalence.

![](Figure_1_R4_K_vs_M.png)

**Figure 1.** R4 K/M relative reduction for each map, averaged over its three paired seeds; the dashed line shows the equal-map mean. C10000-02 has a very small negative value; Table 1a shows rounded map means and the source CSV retains full precision.

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

Across the five methods all 180 slots reached a terminal state; the existing independent audit matched 164 valid route records and lengths. The LKH-GPX2 and LKH-POP route-quality comparisons use only valid pairs: 29 seeds over 10 maps and 27 seeds over 10 maps, respectively. K/LKH-GPX2 has 17 shorter, 10 tied and 2 longer pairs, with map-equal mean reduction 0.024225% [0.006563%, 0.051640%]; K/LKH-POP has 13/14/0 and 0.031630% [0.007688%, 0.063988%]. Their five-hypothesis Holm-adjusted p-values are 0.078125 and 0.125, respectively. Missing maps and non-delivery limit interpretation; these values are not evidence of superiority to all LKH variants.

M/LKH-GPX2 is 17/10/2 with mean 0.024780%, and C/LKH-GPX2 is 16/8/5 with 0.020421%. M/LKH-POP is 13/14/0 with 0.031213%, and C/LKH-POP is 13/12/2 with 0.025930%. These are secondary valid-pair comparisons, not adjusted primary superiority claims.

The original R4 EAX arm, based on the author's edge-assembly crossover approach [12], has 19 attempted slots and 17 deferred slots. Eighteen valid results cover the six 10,000-city U/C/R synthetic maps and all three registered seeds; in these available matched pairs M/EAX is 18/0/0 shorter/tied/longer, C/EAX is 16/0/2, and K/EAX is 17/0/1. This coverage was truncated by the task failure and does not represent a complete or independent 12-map EAX comparison. The adapted EAX program and cold-restart wrapper are not byte-identical to the unmodified author release. A separate EAX supplement also has 18 valid, one failure and 17 unstarted slots; the different execution versions/time blocks cannot be selectively pooled to create a complete uniform baseline. EAX execution failure or deferral is not a route-quality victory. No comprehensive claim against EAX is made.

### 5.4 Starting tours and continuation

M and K parent hashes match in all 36 R4 groups. In 16 groups the selected starting cycles are identical up to rotation and reversal, and their final lengths tie. In the remaining 20 groups K starts shorter; it finishes shorter in 9, tied in 5 and longer in 6. On four of the small-map runs, K started at the published optimum while M reached it during continuation. Of the 16 strictly better K starts on the 10,000-city maps, 9 led to shorter endpoints, 1 to a tie and 6 to longer endpoints. No matched external optimum was established for these six large maps. Thus a shorter start did not guarantee the shorter final tour in these observed configurations. The per-group start and final differences are shown in Supplementary Figure S1; their association is descriptive and does not isolate a causal mechanism. It is not possible from this observation alone to attribute the six reversals uniquely to extra recombination time, route structure, initialization state, randomness or other search dynamics.

The three external GPX2 operations took a mean recorded wall time of 0.328780 seconds. The recorded mean remaining continuation budgets were 31.152158 seconds for M and 30.880452 seconds for K. Their difference also reflects preparation and validation, and must not all be attributed to GPX2 itself. The mean charged shared prefix for M was about 53.09 seconds; it includes necessary preparation and is not pure solver CPU time. Supplementary Table S3 reports only separately recorded costs; selection and validation are not assigned a component cost when separate measurements are unavailable. The exploratory cost distributions are reported alongside the means in Supplementary Table S3.

In a separate conditional diagnostic, 12 already-exposed development parent pools from six maps supplied two starting tours; three continuation seeds per pool yielded 72 valid 30-second tasks. Among 36 matched pairs, continuation from the second start ended shorter/tied/longer in 12/20/4. In all 18 pairs with the same undirected starting cycle, final cycles matched. Four worse endpoints occurred despite a shorter second start. The historical pools were supplied without charging their production and A was run before B within each pair; this is not a complete-budget performance ranking or a causal intervention isolating structure. The recorded inner and outer deadline fields have different scopes; the existing audit uses its registered outer stop and delivery evidence and retains the inner fields rather than recoding them.

## 6. Discussion

The earlier positive mean in V22 and the slightly negative local R4 K/M mean show that the added recombination benefit is not established as stable across these two nonidentical batches. Neither comparison isolates hardware from dataset, time accounting and other differences, so the reversal of batch means should not be assigned to hardware alone. K/M has more shorter than longer seed pairs in R4 but a negative map-equal mean because the few regressions have larger magnitudes; the leave-one-map range includes both signs. Selecting only favorable maps or reporting seed-level wins as independent map-level evidence would obscure that result.

Distinguishing an intermediate gain from a delivered final gain helps evaluate heuristic pipelines under a complete budget. However, prior bet-and-run and GPX literature has already recognized selection and future trajectory issues [3,6,7]. The present contribution is an explicit, auditable comparison in this setting and a quantified observation of reversals, not a new theory or a general proof of why reversals occur. Different starts can consume pseudorandom numbers differently even with equal seed labels. In particular, best-parent M is a strong control for the incremental effect of K's three external operations.

The author LKH results illustrate why route quality and delivery must be reported separately. Initialization is part of a real time budget, but a budget failure does not show that a method would fail under a longer or otherwise appropriate budget. The planned six-map, 30-second U prototype assessment remains incomplete: ten individual results are valid, while an additional task failed a Job-monitor evidence check and the rest were not run. It is not a validated method or a basis for performance claims; the monitor failure is not an algorithm-quality loss. EAX remains an important gap for broader external competitiveness, not an opportunity to turn incomplete comparisons into wins.

## 7. Limitations and future work

The selected benchmark has only 12 local maps, some previously exposed cases, three seeds per map and two principal scale ranges; inference to all Euclidean or non-Euclidean TSPs is not justified. The valid-pair external comparisons exclude maps without author-LKH deliveries. CPU affinity does not ensure processor isolation, and unrecorded temperature or exact internal discovery times must not be imputed. R4's two LKH configurations and the incomplete EAX supplement do not cover all strong baselines. Independent route validation verifies feasibility and objective value, not the internal correctness of every search operation or global optimality.

A separate preregistered eight-map confirmation was started but remains incomplete at the time of this draft. Of the 64 planned slots, only C, M and K for one seed on the first map have been recorded as valid; the corresponding author-LKH wrapper failed its output-path check before the native solver started, and the remaining 60 slots have not started. This first case has therefore been exposed. These partial records are not a completed independent confirmation and are not included in any aggregate or performance claim here; a wrapper error is not an author-LKH route-quality result.

If the contribution claim is expanded beyond this bounded empirical question, a future study should preregister a genuinely independent benchmark and complete a uniform, reproducible strong-baseline comparison, including a functioning same-budget EAX execution. It should freeze versions, handle failure prospectively and not select a better-looking historical attempt. Any future U mechanism would require separately validated same-cost controls and unseen instances; no such performance claim is made here.

## 8. Conclusion

On the local 12-map batch, the observed mean final quality of K did not improve over same-parent M, while K/C had a small positive point estimate without a family-wise significant K/C test. The earlier CPU2 batch showed a different positive K/M mean under a different experimental setting. These findings support a narrow lesson: intermediate recombination improvements and final-budget improvements must be measured separately, including preparation cost and non-delivery. They do not establish general superiority, equivalence, or a novel LKH/GPX algorithm. Complete external-baseline evidence and a broader independent instance set remain necessary for stronger claims.

## Reproducibility and declarations

Statistical replay uses the saved paired records, map-level aggregation and figure scripts. A separate checker read 464 historical tours against their coordinate files: 300 from V22 and 164 from R4. It verified city coverage, closure and EUC_2D length. In the local review bundle, 18 project-generated maps suffice for 254 tours. Verifying the other 210 requires the exact 14 third-party coordinate files as well as the corresponding saved tours. A separate check extracted those 14 inputs from locally retained copies of the source archives by member and SHA-256. Combined with the locally held tours and project maps, they yielded 464 matching route lengths. The third-party inputs are available from the University of Stirling data record [11], which states CC BY 4.0.

Solver replay also requires the frozen executables, parameters, wrapper dependencies and Windows timing and resource controls. In an isolated local engineering check on a previously exposed instance, P5 started generating parents. The registered system paging guard stopped the shared stage before either continuation began. This check yielded no M or K endpoint and contributes no performance result. The public author-review repository (https://github.com/wang-d-c/TSP-SCI-Manuscript-Revision-20261118) contains drafts and selected derived tables and scripts. A complete executable distribution, all route and map inputs, and a persistent DOI are not provided there. Authors and rights holders still need to establish which project-generated material and third-party software derivatives may be released. An independent tour length can be verified even when a time-limited search cannot be rerun from the public materials.

## References

1. Helsgaun, K. (2000). An effective implementation of the Lin–Kernighan traveling salesman heuristic. *European Journal of Operational Research*, 126(1), 106–130. https://doi.org/10.1016/S0377-2217(99)00284-2
2. Tinós, R., Helsgaun, K., & Whitley, D. (2018). Efficient recombination in the Lin–Kernighan–Helsgaun traveling salesman heuristic. *Parallel Problem Solving from Nature*, LNCS 11101, 95–107. https://doi.org/10.1007/978-3-319-99253-2_8
3. Tinós, R., Whitley, D., & Ochoa, G. (2020; online 2019). A new generalized partition crossover for the traveling salesman problem: Tunneling between local optima. *Evolutionary Computation*, 28(2), 255–288. https://doi.org/10.1162/evco_a_00254
4. Hains, D., Whitley, D., & Howe, A. (2012). Improving Lin–Kernighan–Helsgaun with crossover on clustered instances of the TSP. *PPSN XII*, 388–397. https://doi.org/10.1007/978-3-642-32964-7_39
5. Taillard, É. D., & Helsgaun, K. (2019). POPMUSIC for the travelling salesman problem. *European Journal of Operational Research*, 272(2), 420–429. https://doi.org/10.1016/j.ejor.2018.06.039
6. Friedrich, T., Kötzing, T., & Wagner, M. (2017). A generic bet-and-run strategy for speeding up stochastic local search. *AAAI Conference on Artificial Intelligence*, 31, 801–807. https://doi.org/10.1609/aaai.v31i1.10645
7. Weise, T., Wu, Z., & Wagner, M. (2019). An improved generic bet-and-run strategy with performance prediction for stochastic local search. *AAAI Conference on Artificial Intelligence*, 33, 2395–2402. https://doi.org/10.1609/aaai.v33i01.33012395
8. Zhang, W., & Looks, M. (2005). A novel local search algorithm for the traveling salesman problem that exploits backbones. *IJCAI*, 343–349. https://ijcai.org/proceedings/2005/182
9. Heins, J., Schäpermeier, L., Kerschke, P., & Whitley, D. (2024). Dancing to the state of the art? How candidate lists influence LKH for solving the traveling salesperson problem. *PPSN*, 100–115. https://doi.org/10.1007/978-3-031-70055-2_7
10. de Carvalho, O. Q., & Whitley, D. (2025). Dramatically faster partition crossover for the traveling salesman problem. *GECCO*. https://doi.org/10.1145/3712256.3726465
11. McMenemy, P., Veerapen, N., Adair, J., & Ochoa, G. (2019). Rigorous performance analysis of state-of-the-art TSP heuristic solvers. *EvoCOP*, 99–114. https://doi.org/10.1007/978-3-030-16711-0_7. Associated dataset record: https://datastorre.stir.ac.uk/handle/11667/127 (research use and third-party redistribution rights require final verification).
12. Nagata, Y., & Kobayashi, S. (2013). A powerful genetic algorithm using edge assembly crossover for the traveling salesman problem. *INFORMS Journal on Computing*. https://doi.org/10.1287/ijoc.1120.0506
13. Kerschke, P., Kotthoff, L., Bossek, J., Hoos, H. H., & Trautmann, H. (2018). Leveraging TSP solver complementarity through machine learning. *Evolutionary Computation*, 26(4), 597–620. https://doi.org/10.1162/evco_a_00215
