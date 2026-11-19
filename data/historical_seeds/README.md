# Historical seed-level data and table mapping

This numerical extract provides the recorded 300 V22 rows and 180 R4 rows. The files are unchanged from the previous public release. V22 used C, M and K on 20 maps with five seeds each. R4 used five methods on 12 maps with three seeds each. They are different batches with separate environments and clocks. Use the map as the independent unit and match runs by map and seed within each batch.

| Field | Meaning |
|---|---|
| `batch` | `V22` or `R4` |
| `map_id` | Frozen experiment instance. Public attribution and exact member hashes are in `../../replay/stirling_14.csv`. The other 18 IDs are in `../../generated_map_manifest.csv`. |
| `seed` | Registered paired formal search seed as an integer. The same seed label identifies the paired slot. |
| `method` | V22 uses `C`, `M`, `K`. R4 uses `C_project`, `M_best_parent`, `K_three_pair_GPX2`, `LKH_GPX2`, `LKH_POP`. See the paper and Supplementary Methods for settings and versions. |
| `status` | `valid` means a deadline-qualified recorded result. `budget_no_delivery` means ordinary expiry without a qualifying result. `monitor_invalid` is a separate recorded monitoring interruption. V22 is 300 valid. R4 is 164 valid, 15 budget no-delivery and 1 monitor-invalid. |
| `length` | Integer closed-tour EUC_2D length when `status=valid`. A blank means an unavailable score and never counts as a distance or as a pairwise loss. |
| `final_delivery_s` | Counted wall seconds to recorded delivery when supplied by that batch. Blank denotes an inapplicable or unrecorded measurement. |
| `search_stop_observed_s` | Counted wall seconds to recorded stop observation, when available. V22 rows use their original elapsed field. |
| `cleanup_observed_s` | Counted wall seconds to recorded cleanup, when available. |
| `elapsed_s` | Historical recorded method wall time for V22. The R4 export supplies separate observations instead. |
| `shared_prefix_paid_s` | Counted wall seconds of recorded shared-parent overhead when applicable. Each M and K arm pays the full shared prefix. |

## Trace from individual records to tables and figures

| Output | Input and command |
|---|---|
| V22 manuscript results and map table | `V22_method_results_300.csv` joins valid methods by map and seed. `../V22_20_maps_CN.csv` gives map-level signs and effects. `python -B -X utf8 replay_historical_inference.py` checks every map and computes the original intervals and tests against `V22_frozen_inference_reference.json`. |
| R4 main and secondary comparisons and Figure 1 | `R4_method_results_180.csv` joins valid methods by map and seed. `../R4_map_comparisons.csv` provides map data and `../R4_summary.csv` provides paper summary data. `python -B -X utf8 replay_historical_inference.py` checks the run-to-map mapping and the registered main inference. `python -B -X utf8 rebuild_figures.py new-figure-folder` redraws Figure 1. |
| R4 seed-pair display | `python -B -X utf8 plot_historical_seed_pairs.py new-seed-figure-folder` plots all 36 valid K/M pairs from `R4_method_results_180.csv`. |
| Supplementary Figure S1 | `../Figure_S1_plot_coordinates.csv` gives the reported start-to-finish coordinates and their multiplicity. `python -B -X utf8 rebuild_figures.py new-figure-folder` redraws S1. `python -B -X utf8 check_tables.py` checks its 20 observations. |

Run commands at the package root. The inference replay requires NumPy 2.3.5 for V22. Plots use Matplotlib 3.10.6. Both were tested with Python 3.13.9. Scores, pair signs and equal-map effects can also be checked with the standard library using `python -B -X utf8 verify_seed_export.py`.

V22 uses 20,000 stratified NumPy PCG64 draws with seed 20261112 and linear percentile quantiles. It resamples whole map means within the frozen public, uniform, clustered and mixed strata. V22's exact rational two-sided sign flip and Holm adjustment use the two primary comparisons. R4 retains its separately registered map resampling with Python's `random.Random(20261116)`, 20,000 draws, and the five-slot primary Holm family. The untested EAX comparison has no estimate and occupies its recorded adjustment slot. Engineering outcomes, routes, and solver source or binaries remain outside this numerical extract.
