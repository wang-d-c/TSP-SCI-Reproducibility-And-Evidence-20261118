# Reproduce results from public tables or authorized source files

## 1. Public results and figures

Open a shell at the top level of the extracted public package or repository. The [map-level data](../data/) and [published plotting coordinates](../data/Figure_S1_plot_coordinates.csv) are sufficient for both commands. They work offline.

```sh
python -B -X utf8 check_tables.py
python -B -X utf8 rebuild_figures.py reproduced-figures
```

The statistics checker uses the Python standard library. The figure script requires Matplotlib (tested with 3.10.6). Give it a new output directory. It writes two PNGs and two vector PDFs. Figure 1 uses the 12 map-level K/M means at their stored precision. S1 displays 20 pairs with shorter K starts. One plotted coordinate represents two observations. See the [reported checks](../CHECKS.md).

## 2. Seed-level statistics with authorized local inputs

Ask the authors for the hash-matching V22 and R4 analysis package, including the registered statistics and plotting scripts and the tables listed under `stats` in [replay_inputs.csv](replay_inputs.csv). Provision depends on applicable rights. Its root must contain `data/` and `scripts/`. Once a copy is available, the following command verifies the input hashes, stages the required files in a new directory outside the input, and runs the historical seed-level analysis. It produces V22 and R4 statistical results and the earlier design of the map plot. The original analysis was tested with Python 3.13.9, NumPy 2.3.5 and Matplotlib 3.10.6. Replace example paths with your local paths.

```powershell
python -B -X utf8 replay/replay_authorized_inputs.py stats "C:\authorized\02_复现资料" "C:\reanalysis\new-statistics"
```

The two hash columns in the input manifest record recognized file encodings of the preserved analysis inputs. The manifest identifies files independently of any online source. Individual seed-level method records, tour files and the solver toolchain have separate access conditions.

## 3. Saved tour verification

With one legally obtained city order and the corresponding integer-coordinate EUC_2D instance, use the public [standalone verifier](../verify_tour.py) from the repository root:

```sh
python -B verify_tour.py path/to/instance.tsp path/to/route.tour --expect LENGTH
```

For the registered 464-tour check, request the authorized package containing the 464 city orders, 18 project-generated instances, the two files listed under `routes` in the input manifest and the registered layout. A subset of 254 tours has the required coordinates in that package. This repository includes the other 14 maps under [instances/](../instances/) with their exact original bytes. Use that directory for the remaining 210 tours:

```powershell
python -B -X utf8 replay/replay_authorized_inputs.py routes "C:\authorized\02_复现资料" "C:\reanalysis\new-full" --external-maps "instances"
```

For a deliberately partial check, replace the `--external-maps` option and its argument with `--partial`. The registered verifier checks hashes, coverage, closure and EUC_2D length. Historically all 300 V22 and 164 R4 saved valid tours passed. These instructions describe how an authorized recipient can repeat the check.

The included RUE, NETGEN and MORPH instances are attributed in [the instance licence notice](../instances/ATTRIBUTION.md). To check them against independently acquired original archives, obtain RUE.zip, NETGEN.zip and MORPH.zip from the [University of Stirling dataset](https://datastorre.stir.ac.uk/handle/11667/127) and run `python -B -X utf8 replay/prepare_stirling.py "C:\downloads\Stirling"`. The [instance manifest](stirling_14.csv) identifies the archive URLs, member names and exact checksums.

## 4. New timed searches

An end-to-end C/M/K search requires the frozen project programs and parameters, upstream and local rights, shared-prefix charging, and the Windows resource controls. The latest independent test started P5 during parent generation and stopped at the registered resource guard. It delivered no M or K continuation endpoint. The public replay commands perform statistics, plotting and tour verification only.
