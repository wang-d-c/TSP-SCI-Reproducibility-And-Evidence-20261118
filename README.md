# Fixed-budget TSP recombination and continuation

**Corresponding-author review · v1.6 minor scientific revision · 2026-11-19 · Not submitted.** Authorship and approval remain pending. [English paper](manuscripts/en/Manuscript_scientific_review.pdf) · [Supplementary methods](manuscripts/en/Supplementary_Methods.pdf) · [中文审阅稿](manuscripts/zh/中文科学修订_作者审阅.pdf).

This empirical study asks whether three GPX2 recombinations improve the final delivered tour when M and K start with the same three parents, each pays the full shared parent-pool cost, and both have the same total time budget. In R4, K was shorter, tied or longer than M in 9, 21 and 6 pairs. Its equally map-weighted mean reduction was −0.000405%, with a map-level 95% interval of [−0.002241%, +0.001096%]. In the 20 pairs with a shorter K start, the endpoint was shorter in nine, tied in five and longer in six. V22 and R4 differ in platform and protocol and are analyzed separately.

| Task | Included material |
|---|---|
| Audit the study and figures | [Experiment report](实验报告_公开版.md), [figures](figures/) and [data](data/) |
| Recompute historical results | [300 V22 and 180 R4 numerical outcomes and dictionary](data/historical_seeds/), [replay guide](replay/README_EN.md) and [checks](CHECKS.md) |
| Obtain the exact map bytes | [14 original Stirling maps and licence](instances/ATTRIBUTION.md) and [18 exact project-map reconstructions](generated_map_manifest.csv) |
| Check a saved tour | [Independent verifier](verify_tour.py); complete city orders require authorized access |
| Review timed execution requirements | [Toolchain and access guide](replay/TOOLCHAIN.md) and [engineering status](实验与稿件交付状态.md) |

## Reproduce the numerical results

Extract this revision into a new directory or clone a fresh matching commit. `.gitattributes` preserves the archived bytes on Git checkout. Run from the package root.

```sh
python -B -X utf8 verify_package.py
python -B -X utf8 check_tables.py
python -B -X utf8 verify_seed_export.py
python -B -X utf8 rebuild_figures.py reproduced-figures
python -B -X utf8 rebuild_generated_maps.py generated-local
```

The [replay guide](replay/README_EN.md) also gives the original V22 inference convention and the tour-verification commands. The two principal figures use frozen historical CSVs. All 464 saved valid historical tours were independently verified on the project machine. The results, checksums and coordinates here do not include the city orders. New timed searches require the registered solver versions and Windows environment and the applicable rights.

## Minor scientific revision

The current English abstract has 233 whitespace-delimited words. The English and Chinese Markdown, Word and PDF files include the related-work clarification, R4 Holm-adjusted interpretation and EAX stop-evidence wording. [Revision record](manuscripts/修订对照.md).

## New engineering evidence

POPMUSIC passed one entry-point, valid-tour and deadline check. The four candidate-edge cells verified that the intervention changed the candidate graph while preserving the assigned actual first tour. The 101-city K→M and M→K runs both passed shared-pool charging and route checks. At 19,402 cities, EAX produced an independently checked candidate of length 61,779. The stop request was at 85.806 s and the subsequent exit observation at 86.064 s. Complete stop proof by 86 s was unavailable. That engineering run is unscored. **The 1,600 proposed formal slots remain at 0 started and 0 completed.** [Engineering summary](engineering/engineering_qualification_status.json) · [Frozen proposed schedules](planned_confirmation/).

## Rights and manuscript status

The original Stirling inputs carry source attribution and the deposit's CC BY 4.0 notice. The 18 other historical inputs can be reconstructed from the public project script. Results, manuscripts and project code have separate provenance. Frozen executables, third-party source and patches with unresolved redistribution rights, full city orders, internal logs and the complete author archive require separate authorization and remain outside this release.

## 中文导读

先看[中文审阅稿](manuscripts/zh/中文科学修订_作者审阅.pdf)、[英文正文](manuscripts/en/Manuscript_scientific_review.pdf)与[补充方法](manuscripts/en/Supplementary_Methods.pdf)，再按[复现指南](replay/README_EN.md)复核公开的 480 条历史数值。14 张地图可直接使用，18 张项目地图可精确重建。数字复算、保存路线验环和从零求解各有不同输入。新增工程验收没有产生正式性能结论。[公开实验报告](实验报告_公开版.md)
