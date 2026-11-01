"""Undirected road routing and metric travelling-salesperson solvers."""
import heapq
import math
from time import perf_counter

class ScenarioError(ValueError): pass

def validate(s):
    if not isinstance(s,dict): raise ScenarioError('Scenario must be an object.')
    nodes=s.get('nodes',[])
    if not isinstance(nodes,list) or not 1<=len(nodes)<=100 or any(not isinstance(x,str) or not x.strip() or len(x)>60 for x in nodes) or len(set(nodes))!=len(nodes):
        raise ScenarioError('Use 1–100 unique nonempty node names (up to 60 characters).')
    if s.get('depot') not in nodes: raise ScenarioError('Depot must be a road-network node.')
    deliveries=s.get('deliveries',[])
    if not isinstance(deliveries,list) or len(deliveries)>12 or any(x not in nodes or x==s['depot'] for x in deliveries) or len(set(deliveries))!=len(deliveries):
        raise ScenarioError('Use at most 12 unique delivery nodes, excluding the depot.')
    roads=s.get('roads',[])
    if not isinstance(roads,list) or len(roads)>4950: raise ScenarioError('Invalid roads list.')
    seen=set()
    for edge in roads:
        if not isinstance(edge,dict): raise ScenarioError('Each road must be an object.')
        u,v=edge.get('u'),edge.get('v');w=edge.get('distance')
        if u not in nodes or v not in nodes or u==v: raise ScenarioError('Road endpoints must be distinct known nodes.')
        if type(w) not in (int,float) or not math.isfinite(w) or not 0<w<=100000: raise ScenarioError('Road distances must be positive finite values up to 100000 km.')
        if type(edge.get('blocked',False)) is not bool: raise ScenarioError('Road blocked status must be boolean.')
        key=frozenset((u,v))
        if key in seen: raise ScenarioError('Duplicate undirected road.')
        seen.add(key)
    return s

def graph(s):
    validate(s)
    g={x:[] for x in s['nodes']}
    for e in s['roads']:
        if not e.get('blocked',False):
            g[e['u']].append((e['v'],e['distance']));g[e['v']].append((e['u'],e['distance']))
    return g

def dijkstra(g, source):
    dist={x:math.inf for x in g};previous={};dist[source]=0;queue=[(0,source)]
    while queue:
        cost,u=heapq.heappop(queue)
        if cost!=dist[u]:continue
        for v,w in g[u]:
            candidate=cost+w
            if candidate<dist[v]:
                dist[v]=candidate;previous[v]=u;heapq.heappush(queue,(candidate,v))
    return dist,previous

def closure(s):
    g=graph(s);stops=[s['depot']]+s['deliveries'];matrix=[];paths={}
    unreachable=[]
    for i,u in enumerate(stops):
        dist,prev=dijkstra(g,u)
        matrix.append([dist[v] for v in stops])
        if i==0:unreachable=[v for v in stops[1:] if math.isinf(dist[v])]
        for j,v in enumerate(stops):
            if math.isinf(dist[v]):continue
            path=[v]
            while path[-1]!=u:path.append(prev[path[-1]])
            paths[i,j]=list(reversed(path))
    return stops,matrix,paths,unreachable

def length(route,d):return sum(d[a][b] for a,b in zip(route,route[1:]))

def nearest_neighbour(d):
    route=[0];remaining=set(range(1,len(d)))
    while remaining:
        nxt=min(remaining,key=lambda j:(d[route[-1]][j],j));route.append(nxt);remaining.remove(nxt)
    return route+[0],0

def two_opt(d, initial=None):
    route=list(initial or nearest_neighbour(d)[0]);moves=0
    while True:
        best_delta=0;pair=None
        for i in range(1,len(route)-2):
            for j in range(i+1,len(route)-1):
                a,b,c,e=route[i-1],route[i],route[j],route[j+1]
                delta=d[a][c]+d[b][e]-d[a][b]-d[c][e]
                if delta<best_delta-1e-9:best_delta=delta;pair=(i,j)
        if pair is None:return route,moves
        i,j=pair;route[i:j+1]=reversed(route[i:j+1]);moves+=1

def branch_and_bound(d,time_limit=2):
    initial,_=two_opt(d);best=initial;best_cost=length(best,d)
    n=len(d);start=perf_counter();nodes=0;pruned=0
    def mst(vertices):
        if len(vertices)<2:return 0
        pending=set(vertices);first=min(pending);pending.remove(first)
        costs={v:d[first][v] for v in pending};total=0
        while pending:
            v=min(pending,key=lambda x:(costs[x],x));total+=costs[v];pending.remove(v)
            for x in pending:costs[x]=min(costs[x],d[v][x])
        return total
    def bound(route,remaining,cost):
        if not remaining:return cost+d[route[-1]][0]
        return cost+mst(remaining)+min(d[route[-1]][j] for j in remaining)+min(d[0][j] for j in remaining)
    # Maintain bounds of unexplored nodes to certify a gap on timeout.
    root_remaining=tuple(range(1,n));root_bound=bound([0],root_remaining,0)
    stack=[([0],root_remaining,0,root_bound)]
    while stack:
        if perf_counter()-start>=time_limit:
            lower=min([best_cost]+[x[3] for x in stack])
            return best,False,nodes,pruned,lower
        route,remaining,cost,lb=stack.pop();nodes+=1
        if lb>=best_cost-1e-9:pruned+=1;continue
        if not remaining:
            total=cost+d[route[-1]][0]
            if total<best_cost:best=route+[0];best_cost=total
            continue
        ordered=sorted(remaining,key=lambda x:(d[route[-1]][x],x),reverse=True)
        for nxt in ordered:
            rest=tuple(x for x in remaining if x!=nxt);r=route+[nxt];c=cost+d[route[-1]][nxt]
            lower=bound(r,rest,c)
            if lower<best_cost-1e-9:stack.append((r,rest,c,lower))
            else:pruned+=1
    return best,True,nodes,pruned,best_cost

def compare(s,time_limit=2):
    start=perf_counter();stops,d,paths,unreachable=closure(s);pre_ms=(perf_counter()-start)*1000
    if unreachable:return {'feasible':False,'unreachable':unreachable,'results':[],'preprocessing_ms':pre_ms}
    results=[]
    for method in ('nn','2opt','bnb'):
        start=perf_counter();complete=False;nodes=pruned=moves=0;lower=None
        if method=='nn':route,_=nearest_neighbour(d)
        elif method=='2opt':route,moves=two_opt(d)
        else:route,complete,nodes,pruned,lower=branch_and_bound(d,time_limit)
        elapsed=(perf_counter()-start)*1000
        walk=[]
        for a,b in zip(route,route[1:]):
            segment=paths[a,b]
            walk.extend(segment if not walk else segment[1:])
        distance=length(route,d)
        results.append({'method':method,'route':[stops[i] for i in route],'road_walk':walk,'distance':distance,'runtime_ms':elapsed,'optimal':complete,'nodes':nodes,'pruned':pruned,'improvements':moves,'lower_bound':lower})
    optimum=results[-1]['distance'] if results[-1]['optimal'] else None
    for r in results:
        r['gap_percent']=100*(r['distance']-optimum)/optimum if optimum else 0 if optimum==0 else None
    return {'feasible':True,'unreachable':[],'results':results,'preprocessing_ms':pre_ms}
