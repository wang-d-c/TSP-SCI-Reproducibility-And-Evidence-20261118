# Replaying the archived TSP analyses and tours

The two Python helpers and the two CSV manifests in this folder contain no instance coordinates, tour permutations, frozen solver code or solver binaries. They check input identities before using locally supplied material. They require no network access. Give reviewers the stable source links and obtain any required project permission before sending the underlying research files.

## A. Statistics and the archived map plot

Use the published review snapshot or an authorized private copy with the same hashes. On the source snapshot, `03_图表与支撑数据/复算资料_权利待作者确认` is the package root. Version tested: Python 3.13.9, NumPy 2.3.5, Matplotlib 3.10.6. The tested snapshot is [f6a76acf on GitHub](https://github.com/wang-d-c/TSP-SCI-Manuscript-Revision-20261118/tree/f6a76acf541a9467e23601e159c6162a5e44a817). Git clients on Windows can use `git -c core.autocrlf=false clone` to preserve repository bytes. An existing output path is rejected. In these commands, replace paths in quotes with the actual local folders.

```powershell
python -B -X utf8 replay_authorized_inputs.py stats "C:\review-copy\03_图表与支撑数据\复算资料_权利待作者确认" "C:\review-results\new-statistics"
```

The command stages the verified minimum inputs into your own new private output directory. The original scripts regenerate V22 and R4 statistics and the historical style of Figure 1. It creates numerical JSON, vector PDF and PNG files. Styling of the revised Figure 1 and Supplementary Figure S1 was developed later. Their separate data and plotting sources appear in the scientific revision. Both editions use the same historical outcomes. The test reproduced the prior statistics JSON and generated both plot formats. Keep outputs containing third-party or project material within the permissions applicable to the inputs.

## B. Saved tours and the three source archives

Obtain the authorized tour package from the actual project rights holder. Its root contains `scripts/verify_tsp_routes.py`, `LOCAL_REVIEW_DO_NOT_SHARE/route_manifest.csv`, all 464 tour files, and the 18 project-generated maps laid out as in the manifest. The public research repository contains statistics, hashes and a verifier; it omits the saved tours and project-generated coordinate files. With those authorized local files, an explicitly partial check covers 254 tours:

```powershell
python -B -X utf8 replay_authorized_inputs.py routes "C:\authorized\02_复现资料" "C:\review-results\new-partial" --partial
```

For the other 210 tours, obtain **RUE.zip**, **NETGEN.zip** and **MORPH.zip** from the [University of Stirling dataset](https://datastorre.stir.ac.uk/handle/11667/127). Cite McMenemy, Veerapen, Adair and Ochoa (2019), *Rigorous Performance Analysis of State-of-the-art TSP Heuristic Solvers*, University of Stirling. The dataset record specifies CC BY 4.0 for the rights it covers. The dataset README describes the three synthetic families. These 14 maps do not use the separate TSPLIB.zip. Each source URL, exact case-sensitive archive member, archive and member SHA256, batch, ID, dimension and tour count appears in `stirling_14.csv`. Store the three ZIPs in one private source directory.

```powershell
python -B -X utf8 prepare_stirling.py "C:\downloads\Stirling" --stage "C:\review-results\new-maps"
python -B -X utf8 replay_authorized_inputs.py routes "C:\authorized\02_复现资料" "C:\review-results\new-full" --external-maps "C:\review-results\new-maps"
```

Omit `--stage` to verify the archive versions without copying any maps. With staging enabled, file names become the registered map IDs under V22/ and R4/. Coordinates and all bytes remain exactly as deposited. The Windows integration check used the previously acquired frozen source ZIPs. It matched all 14 members. The registered verifier then read these maps, the 18 local maps and the 464 saved tours, checked SHA256 and city coverage, closed each ring and recounted its EUC_2D length. All 464 passed. The result JSON matched the prior full receipt byte for byte. A missing map is reported as missing. Any disagreement between hashes or lengths must be resolved before claiming a successful check.

The repository record and README were accessible during the audit. The three direct ZIP requests did not complete within our bounded live network check. We do not claim a fresh download of today's bytes. If a source archive changes even though a member name looks familiar, the helper deliberately stops; obtain the identified version or resolve the change with the depositors. See [dataset README](https://datastorre.stir.ac.uk/bitstream/11667/127/8/README.txt) and [CC BY 4.0 terms](https://creativecommons.org/licenses/by/4.0/).

## C. Solving again

These commands run no TSP solver. A new timed solve needs the exact project-specific C/M/K programs and configurations, all legitimate upstream and local dependencies, the shared-prefix charging rules and the frozen Windows runtime protections. The new local engineering attempt reached native P5 during parent generation, then the original resource guard stopped the run. Neither continuation produced an endpoint. No external or full C/M/K solver reproduction is claimed. Timed stochastic search on different CPUs or under different load may produce different endpoints even with identical seeds.
