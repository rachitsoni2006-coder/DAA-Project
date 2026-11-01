# Measured research results

Run: 2026-10-27T17:12:30.241811+00:00; Python 3.14.5; macOS-27.0.1-arm64-arm-64bit-Mach-O.

45 synthetic scenarios; 43 feasible and 2 disconnected. Three repetitions after warm-up. Same base graph and nested blocked-road order within each seed/count. B&B cap: 0.2 seconds.

| Method | Median solver ms | Mean worst-repetition gap % | Certified B&B runs |
|---|---:|---:|---:|
| nn | 0.0032 | 7.437 | N/A |
| 2opt | 0.0091 | 0.312 | N/A |
| bnb | 0.7475 | 0.000 | 129/129 |

## Feasibility by disruption

| Requested blocked fraction | Feasible / 15 |
|---|---:|
| 0% | 15 / 15 |
| 15% | 15 / 15 |
| 30% | 13 / 15 |

Disconnection is reported separately, never converted to a zero-distance success. Gaps are measured against a certified optimum only. Requested blockage fractions are rounded to a road count; actual fractions vary. Median times exclude Dijkstra preprocessing, which is recorded separately. B&B timing includes construction of its heuristic incumbent. No real disaster data or operational safety validation is claimed. These aggregates do not establish universal algorithm rankings.
