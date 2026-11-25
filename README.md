# EMERS 2026 雙11廣告投放覆盤 V3.4.0

內部限定 / 台灣 / TWD / 2026-11-22 截止 / 2026-11-25 固定資料快照。

## 使用方式
- `dist/index.html` 是離線自足的互動報告，瀏覽器開啟即可；不需安裝依賴、不需連線取得報告資料。
- `python build.py` 由資料、樣式、章節與模板重新生成 `dist/`。
- `python tests/validate.py` 驗證期間、品牌、金額、訂單、素材花費、漏斗、資料缺值與內容限制。
- `node --check dist/report.js` 檢查 JavaScript 語法。
- `python tests/browser.py` 需已安裝 Python Playwright 與 Chromium（目前測試使用 `/usr/bin/chromium`），驗證桌面／手機互動。測試以 Chromium set_content 載入實際建置 HTML，因執行環境政策限制 file:// 導航；不等同雲端上線測試。

## 架構
```
data/snapshot.json           固定資料快照，更新時先對帳
styles/tokens.css            企業視覺、字體、顏色 token
styles/report.css            共用元件、RWD、列印
src/template.html            報告外殼
src/sections/00-core.js       指標、表格、共用圖表元素、來源連結
src/sections/01..09-*.js      各章內容及互動
src/sections/10-runtime.js   導覽、事件、匯出
build.py                     組裝成離線 HTML
 tests/validate.py            資料與內容檢查
 tests/browser.py             互動驗收
 docs/                       資料契約、CIS、部署、變更紀錄
```

## 疊代原則
1. 先修改資料或來源紀錄；保留前一版快照。資料不可得使用 null，不以 0 代替。
2. 更新公式在 `00-core.js`；章節分析在對應章節修改。部分經營敘述是固定快照的人工審閱結論，不會因更新 JSON 自動改寫，必須同步複核。
3. UI 僅調整 tokens 和共用樣式，不逐頁設定品牌色。
4. 建置後完成數據測試、瀏覽器測試與分析結論人工查核。不可將資料結構一致視為源系統內容全部正確。
5. 報告包含公司商業資料。未設妥伺服器端身份驗證前不可公開部署；本機 HTML 無登入保護。雲端部署是獨立驗收項目。

第10章市場補充資料位於 `data/snapshot.json` 的 `market`、`src/sections/09-market.js`。執行 `python tests/market.py` 驗證交易日配對與相關係數。
