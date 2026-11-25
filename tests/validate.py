import json,math,unittest,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=json.loads((R/'data/snapshot.json').read_text());B=D['brands']
class ReportTests(unittest.TestCase):
 def test_brand_scope(self):
  self.assertEqual(set(B),{'DS','ASH','CA','2XU'});self.assertEqual(B['2XU']['id'],'846153180987660');self.assertEqual(B['DS']['start'],'2026-10-30');self.assertTrue(all(b['end']=='2026-11-22' for b in B.values()))
 def test_reconciliation(self):
  for k,b in B.items():
   with self.subTest(brand=k):
    p=b['periods']['now'];self.assertAlmostEqual(sum(x['net'] or 0 for x in b['daily']),p['s'][4],places=2);self.assertEqual(sum(x['meta'] for x in b['daily']),p['m'][0]);self.assertAlmostEqual(sum(x['google'] or 0 for x in b['daily']),(p['g'] or [0])[0],places=2);self.assertEqual(sum(x['v'][0] for x in b['ads']),p['m'][0]);self.assertEqual(sum(x['orders'] or 0 for x in b['daily']),p['s'][0])
 def test_date_coverage(self):
  for b in B.values():
   dates=[datetime.date.fromisoformat(x['date']) for x in b['daily']];self.assertEqual(len(dates),b['days']);self.assertEqual(dates,[dates[0]+datetime.timedelta(days=i) for i in range(b['days'])]);self.assertEqual(str(dates[0]),b['start']);self.assertEqual(str(dates[-1]),b['end']);self.assertEqual([i for _,s,e in b['phases'] for i in range(s,e+1)],list(range(b['days'])))
  self.assertEqual(B['DS']['daily'][B['DS']['phases'][-1][1]]['date'],'2026-11-18')
 def test_no_imputed_google(self):
  self.assertEqual([B[k]['periods']['yoy']['g'][0] for k in ('DS','ASH','CA','2XU')],[90357.31,91037.55,33394.28,37748.16]);self.assertTrue(all(b['periods']['yoy']['g'][1:]==[None]*4 for b in B.values()));self.assertIsNone(B['ASH']['periods']['now']['g']);self.assertIsNone(B['CA']['periods']['now']['g'])
 def test_funnel_and_shopify(self):
  for k,b in B.items():
   for p,a in b['sessions'].items():
    self.assertEqual(len(a),4);self.assertTrue(all(x>=0 for x in a));self.assertTrue(all(a[i]>=a[i+1] for i in range(3)))
   if 'shopify_totals' in b:
    for p,x in b['shopify_totals'].items():self.assertAlmostEqual(x[0],b['periods'][p]['s'][4],places=2);self.assertEqual(x[1],b['periods'][p]['s'][0])
  self.assertEqual(sum(x['net']==0 and x['orders']==0 for x in B['CA']['daily']),12)
 def test_totals(self):
  net=sum(b['periods']['now']['s'][4] for b in B.values());sp=sum(b['periods']['now']['m'][0]+(b['periods']['now']['g'] or [0])[0] for b in B.values());self.assertAlmostEqual(net,9008206.59,2);self.assertAlmostEqual(sp,1389629.89,2);self.assertAlmostEqual(net/sp,6.48245,4)
 def test_yoy_totals(self):
  net=sum(b['periods']['yoy']['s'][4] for b in B.values());sp=sum(b['periods']['yoy']['m'][0]+b['periods']['yoy']['g'][0] for b in B.values());self.assertAlmostEqual(sp,1276848.30,2);self.assertAlmostEqual(net/sp,6.69640697,6);self.assertAlmostEqual(sum(b['periods']['yoy']['g'][0] for b in B.values()),252537.30,2)
 def test_content_contract(self):
  js='\n'.join(x.read_text() for x in (R/'src/sections').glob('*.js'));self.assertNotIn('11月營收目標進度',js);self.assertNotIn('不建議在未釐清缺列',js);self.assertNotIn('不在 ROI 3.00 時直接加碼',js);self.assertIn('id="metaMode"',js);self.assertIn('id="funnelYear"',js);self.assertIn('歷史可購買SKU',js)
if __name__=='__main__':unittest.main(verbosity=2)
