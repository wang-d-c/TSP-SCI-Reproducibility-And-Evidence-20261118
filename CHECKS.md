# Checks performed on the public files

The release file manifest records exact bytes. `.gitattributes` disables Git line-ending conversion for all archived files. The checkers use hashes of the original bytes rather than normalizing files on disk.

An offline test on Windows 11 (Git 2.54.0 and Python 3.13.9) ran the complete manifest and statistics checks after both a fresh Git clone with `core.autocrlf=true` and ZIP extraction. All 14 Stirling maps matched their original member hashes. When a copy of one map was deliberately converted from LF to CRLF, both checkers failed with a line-ending diagnosis and left the bytes in place. These are Windows test results. The verification commands use Python's standard library.

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

The public figure script renders Figure 1 and Supplementary Figure S1 from the included CSV tables. Figure 1 shows the map-level outcomes and seed-pair counts. S1 preserves 20 observations at 19 distinct coordinate pairs and includes the equality line. A separate check with the locally authorized seed-level package passed the historical statistical replay and generated its original map plot.

The historical seed extract independently reproduces the valid-pair counts and equal-map means. All 18 regenerated project maps match the registered byte hashes. The preannounced new slots remain unexecuted.
