# Verification record

- Eight routing unittest methods pass.
- Twenty-five generated six-delivery graphs compared against exhaustive permutation optima.
- Open-road walk distances, complete stop coverage and 2-opt non-worsening checked.
- Disconnected, empty-delivery, single-delivery, invalid-weight, duplicate-road and forced-timeout cases checked.
- Terminal integration run: load comparison JSON → compare → load disconnected JSON → compare → exit. Verified distances and infeasibility output. Transcript saved in DEMO_TRANSCRIPT.txt.
- Manual scripted terminal exercise: inspect roads, compare sample, toggle road, compare again, save/reset/load and SVG export.
- Forty-five benchmark scenarios completed; 43 feasible, two disconnected; all 129 timed B&B searches on feasible scenarios certified optimality.
- Source compilation checked.
- Diagram is a schematic network export, not a geographic map; no browser/server required.
- Publisher bibliographic metadata checked for the two paper references.

Scope: this is software/model verification on synthetic inputs, not operational emergency validation. Performance conclusions apply only to the saved experimental settings.
