# 資料契約及追溯

來源與統計期間見 `data/snapshot.json` 的 sources、source_status、brands。[Dashboard 原始試算表](https://docs.google.com/spreadsheets/d/16XYjr0e7MwAyCdJ-pXb-IxzUtU7hw0BCmAcNd0v1CPE/edit)、[活動企劃](https://docs.google.com/spreadsheets/d/17yuhWGnN0ht9ILnse5QgQET5uKDEFIwn9rhhrUdCfC8/edit?gid=1285415161)、[雙11規劃](https://docs.google.com/spreadsheets/d/1Nv19o9KGHYnobEwuj1XgJf8k7RPqUz2XCefw__9yk48/edit)。Meta 與 Shopify 入口見報告各章資料依據。

## 期間、市場
DS 2026/10/30–11/22；ASH、CA、2XU 2026/11/2–11/22。活動前等天數；去年採同日曆日期，未取得2025活動規劃。2XU Taiwan Meta 帳戶 846153180987660，排除香港。Meta country TW；Shopify billing_country Taiwan、sessions session_country Taiwan。兩種地區維度不同，不強行合併成同一使用者漏斗。

## 快照 schema（沿用 V2 陣列順序，避免無依據轉換）
- `brands.<key>.periods.<now|prev|yoy>.m`：[花費、曝光、連結點擊、LPV、加購事件、結帳事件、網站歸因購買、網站歸因購買價值]
- `s`：[訂單、gross_sales、discounts（負）、sales_reversals（負）、net_sales、新客訂單、新客淨營收、舊客訂單、舊客淨營收]
- `g`：null 代表未取得資料列，非確認零花費。非空陣列第一項為花費、第二項歸因價值；其餘依 Google 原始快照保留。跨媒體歸因金額不相加。
- `daily`：date、net、orders、meta、google；Callaway 原12個缺列日已直接用 Shopify TIMESERIES 查證為0；11/6負值保留。
- `sessions`：[網站sessions、加購sessions、結帳sessions、完成購買sessions]；購買Sessions不等於實際訂單。
- `ads[].v`、`audience[].v`：[花費、曝光、連結點擊、歸因購買、歸因購買價值]；同名群組不等於 Creative ID，19組代表文案有實際來源ID。
- `shopify_totals`：[net_sales、orders、new_customers、returning_customers、net_items_sold]，去重顧客與 Dashboard 新舊客訂單不同；ASH只有本期直接營收對帳。
- `types`、`products`、`vendors`：[分類或名稱、淨營收、淨售出件數]，成交商品列表不代表可購買SKU全集。

## 公式與可重現查詢
- ROI = Shopify net_sales / (Meta amount_spent + Google 已記錄花費)。2025 Google花費為使用者2026/11/25提供之期間總額（TWD），未獨立對帳；其轉換、曝光、點擊指標為null，不比較。ASH、CA本期及活動前Google無資料列，暫依已記錄值；非確認未投放。
- Meta ROAS = offsite_conversion_fb_pixel_purchase_values / amount_spent；CPM = amount_spent / impressions × 1000；CTR = link_click / impressions；CPC = amount_spent / link_click；CPA = amount_spent / offsite_conversion_fb_pixel_purchase。
- Shopify CVR = sessions_that_completed_checkout / sessions；加購率、結帳率同分母。同比 = current / prior - 1；零分母留空。
- 折扣率 = -discounts/gross_sales；退貨金額率 = -sales_reversals/(gross_sales+discounts)；非同批訂單退貨率。淨客單 = net_sales/orders；非 Shopify 原生 AOV。費用/新客訂單並非因果 CAC。
- ShopifyQL 銷售：`FROM sales SHOW net_sales, gross_sales, discounts, sales_reversals, orders, new_customers, returning_customers, net_items_sold WHERE billing_country = 'Taiwan' SINCE <起日> UNTIL <迄日>`
- ShopifyQL 漏斗：`FROM sessions SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout, conversion_rate WHERE session_country = 'Taiwan' SINCE <起日> UNTIL <迄日>`
- ShopifyQL 商品：`FROM sales SHOW net_sales, net_items_sold WHERE billing_country = 'Taiwan' GROUP BY product_title SINCE <起日> UNTIL <迄日> ORDER BY net_sales DESC LIMIT 30`；ASH group by product_vendor；DS、2XU另取 product_type。
- Meta 帳戶：ad_account level, country breakdown=TW, date range inclusive；廣告 level，impressions>0，group by name；age/gender為帳戶層級。
- Dashboard sheets：DESCENTE, ASH GOLF, Callaway, 2XU TW；gads_by brand_contry, metaads_by_brand_contry。廣告原始表自2026/1/1。

## 缺口
2025 Google獨立來源驗證及逐日數據、完整素材影像、全部文案、版位與受眾重疊、歷史可購買SKU、季別標籤及跨店客戶識別尚未完整。沒有毛利、庫存或重大事件補充。SKU豐富度是 Callaway 優先驗證假設，不是已證明原因。
