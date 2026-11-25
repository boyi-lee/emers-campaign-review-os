import json,math,unittest
from pathlib import Path
D=json.loads((Path(__file__).resolve().parents[1]/'data/snapshot.json').read_text())
def corr(x,y):
 a=sum(x)/len(x);b=sum(y)/len(y)
 return sum((i-a)*(j-b) for i,j in zip(x,y))/math.sqrt(sum((i-a)**2 for i in x)*sum((j-b)**2 for j in y))
class MarketTest(unittest.TestCase):
 def test_pairs(self):
  rows=D['market']['rows'];self.assertEqual(len(rows),15);self.assertEqual(sum(r['return_pct']>0 for r in rows),5)
  brands=D['brands'];daily={k:{r['date']:r['net'] for r in b['daily']} for k,b in brands.items()}
  x=[r['return_pct'] for r in rows]
  for k,target in [('DS',.363),('ASH',.412),('CA',-.166),('2XU',.628)]:
   self.assertAlmostEqual(corr(x,[daily[k][r['date']] for r in rows]),target,places=3)
  y=[sum(a[r['date']] for a in daily.values()) for r in rows]
  self.assertAlmostEqual(corr(x,y),.609,places=3)
  self.assertAlmostEqual(sum(v for v,r in zip(y,rows) if r['return_pct']>0)/5,472828.64,places=2)
if __name__=='__main__':unittest.main()
