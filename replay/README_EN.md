# Reproduce results from public tables or authorized city orders

## Public numerical replay and figures

Start at the root of the extracted ZIP or a fresh Git checkout. The file manifest covers exact bytes, including line endings. The [run-level numerical tables and dictionary](../data/historical_seeds/) contain 300 V22 and 180 R4 records. The [map-level effects and plotting coordinates](../data/) identify the numerical inputs for the main results, Figure 1 and Supplementary Figure S1.

```sh
python -B -X utf8 verify_package.py
python -B -X utf8 check_tables.py
python -B -X utf8 verify_seed_export.py
python -B -X utf8 replay_historical_inference.py
python -B -X utf8 rebuild_figures.py reproduced-figures
python -B -X utf8 plot_historical_seed_pairs.py individual-pair-figures
```

Python 3.13.9 was used for the registered inference replay. It uses NumPy 2.3.5 for the V22 PCG64 stream at seed `20261112` and the 20,000 stratified resamples, preserving the map-level sign-flip tests and original two-comparison Holm family. R4 uses its registered map-level procedure and five-comparison family. Figures were rebuilt with Matplotlib 3.10.6. Pass new output directories to the figure commands. [Result mapping and variable definitions](../data/historical_seeds/README.md).

## Coordinate files

Fourteen exact Stirling maps are included. The [member manifest](stirling_14.csv) gives the original archive URLs, member names and hashes. Retain their [source attribution and licence notices](../instances/ATTRIBUTION.md). To match independently obtained source archives, place `RUE.zip`, `NETGEN.zip` and `MORPH.zip` from the [original deposit](https://datastorre.stir.ac.uk/handle/11667/127) in a local folder and run `python -B -X utf8 replay/prepare_stirling.py <download-directory>`.

Run `python -B -X utf8 rebuild_generated_maps.py generated-local` for the other 18 historical maps. The generator checks each SHA256 against the [frozen manifest](../generated_map_manifest.csv).

## Tour verification with authorized city orders

Obtain the saved city order from the authors or another rights holder before making an independent check. This release provides lengths and map hashes. It omits individual city orders. With the matching input and a saved TSPLIB TOUR file, run the following.

```sh
python -B -X utf8 verify_tour.py path/to/instance.tsp path/to/tour.tour --expect LENGTH
```

The verifier checks a complete city permutation and its closed integer EUC_2D circuit. The authors' local review materials permit all 300 V22 and 164 R4 valid saved routes to be checked when the routes are accessible. The public commands alone compute no city order and verify no proof of global optimality.

If the authors provide the original archived access-controlled replay layout, the earlier raw-input helper is available. It checks the files listed in [replay_inputs.csv](replay_inputs.csv) and copies work inputs to a new scratch area before replay. The 14 supplementary coordinate files can be drawn from this release. The historical `stats` mode checks the earlier analysis package; the public inference command above works from the released numerical CSVs.

```powershell
python -B -X utf8 replay/replay_authorized_inputs.py routes "C:\authorized\02_复现资料" "C:\reanalysis\new-full" --external-maps "instances"
```

## Timed solving and engineering scope

Full timed reruns need the exact solver builds and parameters, authorization, Windows runtime, parent-pool accounting, and memory, paging and stop controls. The [toolchain guide](TOOLCHAIN.md) records the access and build boundary. A 2026-11-18 replay attempt stopped at the resource guard. Both shared-pool orders passed on a separate 101-city case on 2026-11-19. POPMUSIC and four candidate-edge cases passed checks of the implementation and route delivery. The largest EAX engineering case was excluded because complete proof of stopping before the deadline was unavailable. The 1,600 later proposed formal runs remain unstarted. [Engineering status and evidence](../实验与稿件交付状态.md).
