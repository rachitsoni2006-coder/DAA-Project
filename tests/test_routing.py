import copy
import itertools
import math
import unittest
from routing import compare, closure, length, branch_and_bound, validate, ScenarioError
from scenarios import sample, generate

class RoutingTests(unittest.TestCase):
    def test_exact_against_exhaustive(self):
        for seed in range(25):
            s=generate(6,seed);stops,d,_,bad=closure(s)
            self.assertFalse(bad)
            optimum=min(length([0]+list(p)+[0],d) for p in itertools.permutations(range(1,len(d))))
            r=compare(s,5)
            self.assertTrue(r['results'][-1]['optimal'])
            self.assertAlmostEqual(r['results'][-1]['distance'],optimum)
            self.assertLessEqual(r['results'][1]['distance'],r['results'][0]['distance']+1e-8)
    def test_walk_matches_distance_and_open_roads(self):
        s=sample();s['roads'][0]['blocked']=True
        report=compare(s)
        edges={frozenset((e['u'],e['v'])):e['distance'] for e in s['roads'] if not e.get('blocked')}
        for r in report['results']:
            self.assertEqual(r['route'][0],s['depot']);self.assertEqual(r['route'][-1],s['depot'])
            self.assertEqual(set(r['route'][1:-1]),set(s['deliveries']))
            distance=sum(edges[frozenset((a,b))] for a,b in zip(r['road_walk'],r['road_walk'][1:]))
            self.assertAlmostEqual(distance,r['distance'])
    def test_disconnection(self):
        s=sample()
        for e in s['roads']:
            if 'Hospital' in (e['u'],e['v']):e['blocked']=True
        r=compare(s);self.assertFalse(r['feasible']);self.assertIn('Hospital',r['unreachable']);self.assertEqual(r['results'],[])
    def test_no_deliveries(self):
        s=sample();s['deliveries']=[]
        for r in compare(s)['results']:self.assertEqual(r['distance'],0)
    def test_one_delivery(self):
        s=sample();s['deliveries']=['Hospital']
        for r in compare(s)['results']:self.assertEqual(r['distance'],10)
    def test_timeout_and_bound(self):
        _,d,_,_=closure(generate(6,12))
        optimum=min(length([0]+list(p)+[0],d) for p in itertools.permutations(range(1,len(d))))
        route,complete,_,_,lower=branch_and_bound(d,0)
        self.assertFalse(complete);self.assertLessEqual(lower,optimum+1e-8);self.assertGreaterEqual(length(route,d),optimum-1e-8)
    def test_bad_input(self):
        for change in ('negative','duplicate','unknown','nan','boolean'):
            s=copy.deepcopy(sample())
            if change=='negative':s['roads'][0]['distance']=-1
            if change=='duplicate':s['roads'].append(s['roads'][0].copy())
            if change=='unknown':s['deliveries']=['Unknown']
            if change=='nan':s['roads'][0]['distance']=math.nan
            if change=='boolean':s['roads'][0]['distance']=True
            with self.assertRaises(ScenarioError):validate(s)
    def test_deterministic_generation(self):self.assertEqual(generate(6,3,.2),generate(6,3,.2))

if __name__=='__main__':unittest.main()
