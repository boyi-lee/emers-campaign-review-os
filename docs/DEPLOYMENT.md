# 私有部署交接

目前交付是本機網頁及可重建原始碼；沒有雲端網址、沒有正式登入測試，也沒有修改現行 Dashboard。先前 AppDeploy 回覆 FREE_DEPLOYMENT_WINDOW_EXPIRED；不為繞過限制公開商業數據。

可採公司現有 Cloudflare：新建獨立 Pages/Worker 專案，在部署含數據檔之前確認 Cloudflare Access 的預設拒絕政策、公司指定人員或群組登入，並阻擋所有可直接取得原始資料的路徑、preview deployment 及替代網域。禁止在未受保護的 URL、公開 GitHub repo、public assets CDN 放置 snapshot。若不能保證所有路由及 preview 受保護，應改用後端角色授權 API 並將資料置於非公開儲存。noindex 不是存取控制。

部署驗收：授權使用者可看各章、篩選、匯出；未登入或未授權者無法下載 HTML/JSON/任何含公司資料的路徑；檢查 preview 網域、CDN快取及分享權限。正式部署需要相應公司 Cloudflare 權限。
