"""Seeded paired disruption experiment; all output stays in this project."""
import csv
import json
import platform
import statistics
from datetime import datetime,timezone
from pathlib import Path
from routing import compare
from scenarios import generate
ROOT=Path(__file__).resolve().parent

def main():
    rows=[];instances=[]
    for n in (5,7,9):
        for seed in range(5):
            for disruption in (0,.15,.30):
                s=generate(n,3130+seed+100*n,disruption);instances.append(s)
                compare(s,.2) # warm-up
                reports=[compare(s,.2) for _ in range(3)]
                if not reports[0]['feasible']:
                    rows.append({'n':n,'seed':seed,'blockage':disruption,'method':'none','feasible':False,'distance':None,'median_ms':None,'gap_percent':None,'completed_runs':0,'median_nodes':None,'preprocess_ms':statistics.median(r['preprocessing_ms'] for r in reports)})
                    continue
                # Identical instance across repetitions. Only use certified optimum if obtained.
                optima=[r['results'][-1]['distance'] for r in reports if r['results'][-1]['optimal']]
                optimum=optima[0] if optima else None
                if optima:assert all(abs(x-optimum)<1e-7 for x in optima)
                for i,method in enumerate(('nn','2opt','bnb')):
                    group=[r['results'][i] for r in reports]
                    distance=max(r['distance'] for r in group)
                    rows.append({'n':n,'seed':seed,'blockage':disruption,'method':method,'feasible':True,'distance':distance,'median_ms':statistics.median(r['runtime_ms'] for r in group),'gap_percent':100*(distance-optimum)/optimum if optimum else None,'completed_runs':sum(r['optimal'] for r in group) if method=='bnb' else 3,'median_nodes':statistics.median(r['nodes'] for r in group),'preprocess_ms':statistics.median(r['preprocessing_ms'] for r in reports)})
    out=ROOT/'data'
    with (out/'benchmark_results.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
    (out/'benchmark_instances.json').write_text(json.dumps(instances,indent=2))
    meta={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'platform':platform.platform(),'processor':platform.processor(),'instances':45,'repetitions':3,'bnb_limit_seconds':.2,'seed_rule':'3130 + seed_index + 100 * delivery_count','counts':[5,7,9],'blockages':[0,.15,.3]}
    (out/'experiment_metadata.json').write_text(json.dumps(meta,indent=2))
    feasible=sum(r['feasible'] for r in rows if r['method']=='nn');disconnected=sum(not r['feasible'] for r in rows)
    lines=['# Measured research results','',f"Run: {meta['timestamp_utc']}; Python {meta['python']}; {meta['platform']}.",'',f'45 synthetic scenarios; {feasible} feasible and {disconnected} disconnected. Three repetitions after warm-up. Same base graph and nested blocked-road order within each seed/count. B&B cap: 0.2 seconds.','', '| Method | Median solver ms | Mean worst-repetition gap % | Certified B&B runs |','|---|---:|---:|---:|']
    for method in ('nn','2opt','bnb'):
        group=[r for r in rows if r['method']==method];gaps=[r['gap_percent'] for r in group if r['gap_percent'] is not None]
        lines.append(f"| {method} | {statistics.median(r['median_ms'] for r in group):.4f} | {statistics.mean(gaps):.3f} | {str(sum(r['completed_runs'] for r in group))+'/'+str(3*len(group)) if method=='bnb' else 'N/A'} |")
    lines+=['','## Feasibility by disruption','', '| Requested blocked fraction | Feasible / 15 |','|---|---:|']
    for b in (0,.15,.3):lines.append(f"| {b:.0%} | {sum(r['method']=='nn' and r['blockage']==b for r in rows)} / 15 |")
    lines+=['','Disconnection is reported separately, never converted to a zero-distance success. Gaps are measured against a certified optimum only. Requested blockage fractions are rounded to a road count; actual fractions vary. Median times exclude Dijkstra preprocessing, which is recorded separately. B&B timing includes construction of its heuristic incumbent. No real disaster data or operational safety validation is claimed. These aggregates do not establish universal algorithm rankings.']
    (ROOT/'docs'/'RESULTS.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))
if __name__=='__main__':main()
