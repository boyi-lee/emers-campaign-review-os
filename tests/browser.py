from pathlib import Path
from playwright.sync_api import sync_playwright
import tempfile
root=Path(__file__).resolve().parents[1]
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for label,width,height in [('desktop',1440,950),('mobile',390,844)]:
  context=browser.new_context(viewport={'width':width,'height':height},accept_downloads=True)
  page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content((root/'dist/index.html').read_text(),wait_until='load');page.wait_for_selector('#s0.active')
  assert '9,008,207' in page.locator('#s0').inner_text()
  assert '1,389,630' in page.locator('#s0').inner_text();assert '6.70' in page.locator('#s0').inner_text();assert '15.96%' not in page.locator('#s0').inner_text()
  assert '11月營收目標進度' not in page.locator('body').inner_text()
  for i in range(10):
   page.locator(f'#nav [data-i="{i}"]').click();assert page.locator(f'#s{i}').is_visible(),f'{label}, chapter {i}'
  page.locator('#nav [data-i="9"]').click();assert '補充資訊' in page.locator('#s9').inner_text();page.select_option('#marketBrand','2XU');assert '138,595.30' in page.locator('#marketDetail').inner_text();assert page.locator('#marketTrend .chart-mark').count()==30
  # Verify real plotted marks and chart controls, not just section existence.
  for i in range(8):
   page.locator(f'#nav [data-i="{i}"]').click(); assert page.locator(f'#s{i} .chart-mark, #s{i} .rankfill').count()>0
  page.locator('#nav [data-i="1"]').click();assert page.locator('#s1 circle.bubble').count()==4
  bubble=page.locator('#s1 circle.bubble').first;bubble.focus();page.keyboard.press('Enter');assert '花費 NT$' in page.locator('#budgetDetail').inner_text()
  page.locator('#nav [data-i="4"]').click();page.select_option('#minsp','0');assert page.locator('#adBubble circle.bubble').count()==73
  bubble=page.locator('#adBubble circle.bubble').first;bubble.focus();page.keyboard.press('Enter');assert '花費 NT$' in page.locator('#creativeDetail').inner_text()
  page.get_by_role('button',name='歸因購買次數',exact=True).click();assert '歸因購買次數' in page.locator('#adBubble svg').text_content()
  page.locator('#nav [data-i="3"]').click();assert page.locator('#period').is_disabled()
  page.get_by_role('button',name='YoY 變化',exact=True).click();assert '+62.9%' in page.locator('#metaCompare').inner_text();assert page.locator('#metaChart rect.chart-mark').count()==4
  page.get_by_role('button',name='ROAS',exact=True).click();assert '47.2%' in page.locator('#metaChart svg').text_content()
  page.locator('#s3 .segmented button[data-value="yoy"]').last.click();assert '99,947' in page.locator('#funnelVisual svg').text_content();assert page.locator('#funnelVisual path.chart-mark').count()==4
  page.locator('#s3 .segmented button[data-value="now"]').last.click();assert '120,497' in page.locator('#funnelVisual svg').text_content()

  page.select_option('#metaMode','delta');assert '+62.9%' in page.locator('#metaCompare').inner_text();assert '+435.9%' in page.locator('#metaCompare').inner_text()
  page.select_option('#funnelBrand','CA');page.select_option('#funnelYear','yoy');assert '20,284' in page.locator('#funnelVisual').inner_text();assert '-90.9%' in page.locator('#funnelVisual').inner_text();assert page.locator('#funnelYear option').count()==2
  page.select_option('#funnelYear','now');assert '16,186' in page.locator('#funnelVisual').inner_text()
  page.select_option('#brand','2XU');assert '43,390' in page.locator('#funnelVisual').inner_text()
  page.locator('#nav [data-i="2"]').click();assert page.locator('#period').is_enabled();assert page.locator('#trendChart').count()==0;assert '各階段 ROI 比較' in page.locator('#s2').inner_text()
  page.fill('#from','2026-11-17');page.fill('#to','2026-11-22');assert '6天' in page.locator('#trendTable').inner_text()
  page.locator('#nav [data-i="4"]').click();page.fill('#search','倒數');assert '倒數' in page.locator('#adTable').inner_text();page.select_option('#sort','roas');page.fill('#search','xyz-absent');assert '0 組' in page.locator('#adTable').inner_text()
  page.locator('#nav [data-i="5"]').click();page.select_option('#sex','female');assert '女性' in page.locator('#audTable').inner_text();assert '男性' not in page.locator('#audTable').inner_text()
  page.locator('#nav [data-i="8"]').click();assert '對帳驗收' not in page.locator('#s8').inner_text();page.get_by_text('展開 Shopify / Dashboard 銷售原始對照',exact=True).click();assert '0.00' in page.locator('#s8').inner_text();page.select_option('#brand','ALL');assert page.locator('#s8').is_visible();
  with page.expect_download() as info:page.locator('#raw').click()
  assert info.value.suggested_filename.endswith('.json')
  with page.expect_download() as info:page.locator('#export').click()
  assert info.value.suggested_filename.endswith('.csv')
  page.locator('#nav [data-i="0"]').click();page.screenshot(path=str(root/'tests'/f'{label}.png'),full_page=True)
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),f'{label} page overflow'
  page.locator('#nav [data-i="3"]').click();page.select_option('#metaMode','delta');page.screenshot(path=str(root/'tests'/f'{label}-diagnostics.png'),full_page=True)
  context.close();print(label,'all 9 chapters, brand filter, YoY, funnel, date, creative, age/sex and downloads passed')
 browser.close()
assert not errors,errors
print('No browser exceptions')
