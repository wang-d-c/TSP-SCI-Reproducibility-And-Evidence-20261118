# Fixed-budget TSP recombination and continuation

**Start with the [English paper](manuscripts/en/Manuscript_scientific_review.pdf), [supplementary methods](manuscripts/en/Supplementary_Methods.pdf) or [中文审阅稿](manuscripts/zh/中文科学修订_作者审阅.pdf).** This archive accompanies an author-review manuscript. The English paper and supplement are from revision 09. The most recent Chinese manuscript is revision 07 and predates the published-optima supplement. Both manuscripts are included as original Word, PDF and Markdown files. Author approval and journal submission are pending.

The study asks whether spending part of a fixed time budget on three GPX2 recombinations yields shorter delivered tours than continuing from the best of the same three parents. Under the R4 protocol, K finished shorter/tied/longer than M in 9/21/6 pairs across 12 maps. Its equally map-weighted mean reduction was −0.000405%, with a map-level 95% interval of [−0.002241%, +0.001096%]. In 20 comparisons K started from a shorter tour, but its final tour was shorter in nine, tied in five and longer in six. Different environments were used for the historical V22 and R4 batches. Their observations are reported separately.

| Contents | Where to find them |
|---|---|
| English manuscript, supplement, Word and PDF versions | [English files](manuscripts/en/) |
| Chinese author-review manuscript and original figure | [中文文件](manuscripts/zh/) |
| Main map-level comparisons, delivery evidence in the paper, summary intervals and published-optimum comparisons | [Tables and figure data](data/) |
| Vector publication figures | [PDF figures](figures/) |
| Fourteen original Stirling instances, matched by SHA256 to individual deposit members | [Coordinates, provenance and licences](instances/ATTRIBUTION.md) |
| Source archives, original member names and exact checksums | [Instance manifest](replay/stirling_14.csv) |
| Further verification using authorized inputs and archived analysis versions | [Replay instructions](replay/README_EN.md) |

## Recalculate results

From this folder, run `python -B -X utf8 check_tables.py` with Python 3.9 or later. It reads the included map summaries to reproduce signed sample counts and equal-map mean reductions for V22 and R4, checks the plotted S1 outcome counts and verifies all 14 instance hashes. This check starts at map summaries. For the original seed-level analysis, archived uncertainty procedure and previous plot, follow the pinned snapshot and input checks in the replay instructions. The archived results and restricted individual run files have separate access conditions.

To check a tour you lawfully hold, run `python -B verify_tour.py instance.tsp route.tour --expect LENGTH`. This standalone verifier accepts integer-coordinate EUC_2D instances and TSPLIB TOUR files, checks city coverage and closes the ring. The source package previously verified all 300 V22 and 164 R4 saved valid tours on the authors’ Windows system. This public archive includes 14 map files; replicating all 464 tour checks requires authorized access to the city orders and the other 18 project-generated maps. Running timed C/M/K searches separately requires the frozen project executables, upstream permissions, project configuration and Windows resource controls. The latest isolated shared-parent smoke test stopped at its resource guard before either continuation delivered a tour. No full solver rerun is claimed.

The 90-second formal comparisons and the 30-second continuation diagnostic use different accounting. Budget non-delivery, resource interruptions, wrapper failures and unstarted work are separately identified in the manuscripts. EAX comparisons across wrapper versions must be kept separate. The later eight-map attempt produced three valid results, one execution error and 60 unstarted slots; it does not contribute to the main ranking.

## Rights and version notes

Use the individual-source attribution for the 14 Stirling maps. This archive grants no blanket open-source licence for the manuscript, project-derived materials or third-party software. Frozen solver sources and binaries, the 464 individual tours, 18 project-generated maps, detailed internal audit material and private correspondence are outside this public package. The original Chinese manuscript contains references to the authors' accompanying evidence index and an earlier EAX comparison sheet. Those private cross-references describe provenance; their targets are retained in the local author archive. The two original manuscript stages preserve the data-access statements in force when each was written; this repository adds the fourteen individually attributed maps listed above.

## 中文导读

建议老师先看[中文稿](manuscripts/zh/中文科学修订_作者审阅.pdf)，再对照[最新英文正文](manuscripts/en/Manuscript_scientific_review.pdf)和[补充方法与表格](manuscripts/en/Supplementary_Methods.pdf)。这些文件供科学审阅，正式作者、署名与投稿期刊待确认。中文稿是第07版；第09版英文正文与补充材料增加了可核验的公开最优值对照。

仓库附有20图和12图的地图级数据、图表、统计复核入口以及14张可署名分享的原始地图。运行 `python -B -X utf8 check_tables.py` 可以重算各图等权的均值、胜平负并检查地图哈希。逐图输入相同、预算相同的两种方法才构成直接配对。取得合法的完整路线后，可以单独验环和计长。464条历史有效路线此前已在本机全部核验。完整城市顺序、18张项目生成地图及冻结求解链仍有另外的获取条件。运行程序和全成本计时能否复现，与已保存路线的长度能否复核，是两个不同的问题。

[中文公开实验报告与 09 版增补](实验报告_公开版.md)
