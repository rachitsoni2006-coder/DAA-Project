"""Emergency supply route planner. Run python3 main.py in VS Code."""
import json
from pathlib import Path
from routing import compare, validate
from scenarios import sample, generate
ROOT=Path(__file__).resolve().parent
LABELS={'nn':'Nearest neighbour','2opt':'NN + 2-opt','bnb':'Branch and bound'}

def number(prompt,low,high):
    while True:
        try:
            n=int(input(prompt))
            if low<=n<=high:return n
        except ValueError:pass
        print(f'Enter an integer from {low} to {high}.')

def show(s):
    print(f"\n{s.get('name','Custom scenario')}\nDepot: {s['depot']}\nRequired deliveries: {', '.join(s['deliveries']) or '(none)'}")
    for i,e in enumerate(s['roads'],1):
        print(f"{i:>3}. {e['u']:<15} <-> {e['v']:<15} {e['distance']:>8.2f} km  {'BLOCKED' if e.get('blocked') else 'open'}")

def run(s):
    report=compare(s)
    if not report['feasible']:
        print('\nNO COMPLETE DELIVERY ROUTE. Unreachable: '+', '.join(report['unreachable']))
        print('No route is fabricated; reopen roads or change the scenario.')
    else:
        print(f"\nShortest-path preprocessing: {report['preprocessing_ms']:.3f} ms")
        print(f"{'Algorithm':<22}{'Distance km':>13}{'Time ms':>12}{'Gap %':>10}  Status")
        for r in report['results']:
            gap='unknown' if r['gap_percent'] is None else f"{r['gap_percent']:.2f}"
            status='Optimal (tolerance 1e-9)' if r['optimal'] else 'Time limit / feasible' if r['method']=='bnb' else 'Heuristic'
            print(f"{LABELS[r['method']]:<22}{r['distance']:>13.2f}{r['runtime_ms']:>12.3f}{gap:>10}  {status}")
            print('  Planned stop order: '+' -> '.join(r['route']))
            print('  Actual road walk:   '+' -> '.join(r['road_walk']))
            if r['method']=='bnb':print(f"  Nodes visited: {r['nodes']}; branches pruned: {r['pruned']}; lower bound: {r['lower_bound']:.2f} km")
        print('Intermediate nodes may repeat; passing a delivery node may serve it early. Routes return to the depot.')
        print('B&B limit: 2 seconds. Gaps use a proven optimum only. Times exclude shortest-path preprocessing.')
    (ROOT/'data'/'last_result.json').write_text(json.dumps(report,indent=2))
    return report

def main():
    scenario=sample()
    print('\nRELIEF ROUTE - EMERGENCY SUPPLY DELIVERY PLANNER\nSynthetic simulation | one vehicle | VS Code terminal')
    while True:
        print('\n1 Show network       2 Block/reopen road     3 Compare algorithms\n4 Load sample        5 Generate network      6 Save scenario\n7 Load JSON scenario 8 Export network SVG    9 Run research experiment\n0 Exit')
        choice=input('Choose: ').strip()
        try:
            if choice=='0':return
            if choice=='1':show(scenario)
            elif choice=='2':
                show(scenario)
                if not scenario['roads']:print('No roads.');continue
                i=number('Road number to toggle: ',1,len(scenario['roads']))-1
                e=scenario['roads'][i];e['blocked']=not e.get('blocked',False)
                print('Road is now '+('blocked.' if e['blocked'] else 'open.'))
            elif choice=='3':run(scenario)
            elif choice=='4':scenario=sample();print('Sample loaded.')
            elif choice=='5':
                n=number('Delivery locations (2–12): ',2,12);seed=number('Random seed (0–999999): ',0,999999);b=number('Road blockage percentage (0–70): ',0,70)
                scenario=generate(n,seed,b/100);print('Network generated. Choose 1 to inspect or 3 to compare.')
            elif choice=='6':
                (ROOT/'data'/'saved_scenario.json').write_text(json.dumps(scenario,indent=2));print('Saved: data/saved_scenario.json')
            elif choice=='7':
                name=input('JSON path (Enter for data/saved_scenario.json): ').strip()
                path=Path(name).expanduser() if name else ROOT/'data'/'saved_scenario.json'
                if not path.is_absolute():path=ROOT/path
                if path.stat().st_size>200000:raise ValueError('File too large.')
                loaded=json.loads(path.read_text());validate(loaded);scenario=loaded;print('Scenario loaded.')
            elif choice=='8':
                from visualization import export_svg
                path=ROOT/'data'/'network.svg';export_svg(scenario,path);print(f'Saved {path}. Open this file in VS Code or an image viewer.')
            elif choice=='9':
                from benchmark import main as benchmark
                benchmark()
            else:print('Choose 0–9.')
        except (ValueError,OSError,KeyError,TypeError) as exc:print(f'Cannot complete action: {exc}')

if __name__=='__main__':
    try:main()
    except (EOFError,KeyboardInterrupt):print('\nStopped.')
