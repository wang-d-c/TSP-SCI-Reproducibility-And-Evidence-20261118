# Fixed-budget TSP recombination and continuation

**Author-review materials** · [English manuscript](manuscripts/en/Manuscript_scientific_review.pdf) · [Supplementary methods](manuscripts/en/Supplementary_Methods.pdf) · [中文审阅稿](manuscripts/zh/中文科学修订_作者审阅.pdf). The Markdown and Word files are in the same folders as their PDFs. Formal author approval and journal submission are pending.

The study asks whether spending part of a fixed time budget on three GPX2 recombinations yields shorter delivered tours than continuing from the best of the same three parents. Under the R4 protocol, K finished shorter/tied/longer than M in 9/21/6 pairs across 12 maps. Its equally map-weighted mean reduction was −0.000405%, with a map-level 95% interval of [−0.002241%, +0.001096%]. In 20 comparisons K started from a shorter tour, but its final tour was shorter in nine, tied in five and longer in six. Different environments were used for the historical V22 and R4 batches. Their observations are reported separately.

| Contents | Where to find them |
|---|---|
| English manuscript, supplement, Word and PDF versions | [English files](manuscripts/en/) |
| Chinese author-review manuscript and figures | [中文文件](manuscripts/zh/) |
| Main map-level comparisons, delivery evidence in the paper, summary intervals and published-optimum comparisons | [Tables and figure data](data/) |
| Vector publication figures | [PDF figures](figures/) |
| Fourteen original Stirling instances, matched by SHA256 to individual deposit members | [Coordinates, provenance and licences](instances/ATTRIBUTION.md) |
| Source archives, original member names and exact checksums | [Instance manifest](replay/stirling_14.csv) |
| Exact-byte manifest, verification and replay instructions | [FILE_SHA256.csv](FILE_SHA256.csv) · [Replay instructions](replay/README_EN.md) |

## Recalculate results

Extract this revision's ZIP into a new directory or make a fresh checkout of the matching Git tree. A Git tree that includes `.gitattributes` preserves the registered file bytes even with Windows `core.autocrlf=true`. From the package root, verify the file manifest and check the map-level results with Python 3.9 or later. Rebuild both manuscript figures with Matplotlib in a new output directory. The commands use the included files and work offline.

```sh
python -B -X utf8 verify_package.py
python -B -X utf8 check_tables.py
python -B -X utf8 rebuild_figures.py reproduced-figures
```

`verify_package.py` checks the size and SHA256 of each listed file. `check_tables.py` recomputes V22 and R4 paired counts and equal-map means, checks the registered R4 primary intervals and tests, verifies the S1 outcome counts, and checks all 14 map hashes against the Stirling identifiers. If a check reports changed line endings, re-extract the ZIP or make a fresh checkout of this revision before analyzing the data. `rebuild_figures.py` renders PDF and PNG versions of Figure 1 and Supplementary Figure S1. For seed-level reanalysis, request the authorized input package from the authors and follow the [offline instructions](replay/README_EN.md). Compare the local inputs against the [file hashes](replay/replay_inputs.csv).

To check a tour you lawfully hold, run `python -B verify_tour.py instance.tsp route.tour --expect LENGTH`. This standalone verifier accepts integer-coordinate EUC_2D instances and TSPLIB TOUR files, checks city coverage and closes the ring. The source package previously verified all 300 V22 and 164 R4 saved valid tours on the authors’ Windows system. Repeating all 464 tour checks requires authorized access to the city orders and 18 project-generated maps in addition to the 14 publicly attributed maps in this archive. New timed C/M/K searches require the frozen project executables, upstream permissions, project configuration and Windows resource controls. See the [replay instructions](replay/README_EN.md) for the current scope of those checks.

The 90-second formal comparisons and the 30-second continuation diagnostic use different accounting. The [experiment report](实验报告_公开版.md) records the incomplete EAX trials and eight-map attempt alongside the completed work, with budget non-delivery, resource interruptions, wrapper failures and unstarted work classified separately.

## Rights and version notes

Use the [individual-source attribution](instances/ATTRIBUTION.md) for the 14 Stirling maps. Frozen solver sources and binaries, the 464 individual tours, 18 project-generated maps and detailed internal audit material require separate access or rights confirmation. The manuscripts and project-derived files retain their respective rights.

## 中文导读

建议老师先看[中文审阅稿](manuscripts/zh/中文科学修订_作者审阅.pdf)，再对照[英文正文](manuscripts/en/Manuscript_scientific_review.pdf)和[补充方法与表格](manuscripts/en/Supplementary_Methods.pdf)。这些文件供科学审阅，正式署名与投稿期刊待确认。

交付包附有 V22 的 20 图和 R4 的 12 图地图级数据、14 张可署名分享的原始地图，以及复算入口。先运行 `python -B -X utf8 verify_package.py` 核对清单，再运行 `python -B -X utf8 check_tables.py` 复核地图级结果。用 `python -B -X utf8 rebuild_figures.py reproduced-figures` 重绘图 1 和补充图 S1。逐种子复算、验证全部历史路线和重跑定时求解各有不同输入，所需材料和授权范围见[复现说明](replay/README_EN.md)。

[中文公开实验报告](实验报告_公开版.md)
