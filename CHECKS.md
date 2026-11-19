# Checks performed on the public files

The following checks ran on the public staging directory before packaging. All 14 Stirling member hashes agreed with the registered member hashes. The three Word files have no recorded author name, tracked insertions or deletions, or comment ranges. The English paper, Chinese manuscript and supplementary PDF contain 10, 10 and 5 pages respectively. The embedded PDF attachments in the English and Chinese manuscripts are equation XML.

`python -B -X utf8 check_tables.py` completed using only files in this package. It verified nine R4 map-level comparisons, including the four testable primary bootstrap intervals and sign-flip p-values and the registered five-comparison Holm family. It reconstructed the V22 counts and mean reductions from 20 equally weighted maps. It also verified the 9/5/6 endpoint counts for Figure S1.

| Batch and comparison | Shorter / equal / longer | Mean reduction |
|---|---:|---:|
| V22 K/M | 44 / 41 / 15 | +0.002930011% |
| V22 K/C | 36 / 38 / 26 | +0.003476334% |
| V22 M/C | 27 / 37 / 36 | +0.000545698% |
| R4 K/M | 9 / 21 / 6 | −0.000405037% |
| R4 K/C | 13 / 16 / 7 | +0.003327072% |
| R4 M/C | 11 / 17 / 8 | +0.003732069% |

The independent `verify_tour.py` was smoke-tested with one retained V22 coordinate file (RUE-1000-01) and its authorized original C tour for seed 541. It validated 1,000 distinct cities and obtained the registered circuit length of 23,345,321. This test used private access to the saved tour. The historical 464-route result was recorded separately with the original verifier. The public package does not contain those city orders. No solver ran during packaging.

The current public figure script was run offline using the two included CSV tables. Figure 1 (2,130 × 1,740 pixels) and S1 (2,010 × 1,470 pixels) matched the corresponding published PNG images pixel for pixel. Both PDFs matched the archived vector figures when rendered at 144 dpi. The S1 table retains all 20 observations at 19 distinct plotted positions, ordered as in the manuscript so overlapping markers are drawn in the same order. A separate test with the locally authorized seed-level package also passed the historical statistical replay and generated its original map plot.
