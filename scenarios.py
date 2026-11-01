import random

def sample():
    nodes=['Depot','Hospital','Shelter','School','Clinic','Warehouse','Junction']
    edges=[('Depot','Hospital',5),('Depot','Junction',3),('Junction','School',4),('Hospital','Shelter',4),('Shelter','School',3),('School','Clinic',5),('Clinic','Warehouse',4),('Warehouse','Depot',7),('Junction','Clinic',6),('Hospital','Warehouse',8),('Shelter','Clinic',7)]
    return {'name':'Illustrative emergency network (synthetic)','nodes':nodes,'depot':'Depot','deliveries':nodes[1:6],'roads':[{'u':u,'v':v,'distance':w,'blocked':False} for u,v,w in edges]}

def generate(n,seed,blockage=0):
    rng=random.Random(seed);nodes=['Depot']+[f'L{i}' for i in range(1,n+1)]
    coords={x:(rng.uniform(0,100),rng.uniform(0,100)) for x in nodes}
    roads=[]
    # Ring guarantees the pre-disruption network is connected; sparse chords add options.
    for i,u in enumerate(nodes):
        for j in range(i+1,len(nodes)):
            v=nodes[j]
            if j==i+1 or (i==0 and j==len(nodes)-1) or rng.random()<.3:
                a,b=coords[u],coords[v]
                w=round(((a[0]-b[0])**2+(a[1]-b[1])**2)**.5,2)
                roads.append({'u':u,'v':v,'distance':max(.01,w),'blocked':False})
    indices=list(range(len(roads)));rng.shuffle(indices)
    for i in indices[:round(blockage*len(roads))]:roads[i]['blocked']=True
    return {'name':f'Synthetic n={n}, seed={seed}, blockage={blockage:.0%}','nodes':nodes,'depot':'Depot','deliveries':nodes[1:],'roads':roads,'coordinates':coords}
