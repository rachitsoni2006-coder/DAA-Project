# First run and demo

1. In VS Code choose File → Open Folder and select this DAA project folder.
2. Choose Terminal → New Terminal.
3. Run `python3 main.py` (Windows: `python main.py`).
4. Enter `1` to view the sample, then `3` to compare routes.
5. Enter `2`, then `1` to block Depot–Hospital; enter `3` to compare again.
6. To show algorithm differences: enter `7`, then `data/comparison_demo.json`, then `3`.
7. To show unreachable delivery handling: enter `7`, then `data/disconnected_demo.json`, then `3`.
8. Enter `0` to finish.

Menu inputs are entered one per line. Option 7 loads a file; it does not run a solver. Option 3 actually calculates routes. The file open in the editor does not need to be routing.py; main.py is the program entry point.

Research output is in docs/RESULTS.md and data/benchmark_results.csv. The paper is docs/PAPER_DRAFT.md. Explain the supplied run honestly: synthetic data, one vehicle, known road closures, no capacity/priority constraints.
