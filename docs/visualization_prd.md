### 失智助理 視覺化模組升級 PRD 與開發計畫（v1.1）

狀態: 審核版（準備進入實作）
負責: 產品/設計/後端/前端（LIFF）
參考來源索引: 失智照護資源彙整（Google Drive）`https://drive.google.com/drive/folders/14OwApuA1t2RPhxkdJdF1Il5RGAJEvf20?usp=sharing`

### 1) 目標與範圍
- 以 Frame25 在 3 秒內提供高品質「What」摘要（無動畫）。
- 以 Frame36「4 頁 Carousel」提供「Why & How」與模組導覽（預設 XAI 頁）。
- 以 LIFF 承載完整詳情、引用、工具（行事曆/提醒/收藏等後續擴充）。
- 導入 Confidence、ReasoningPath、來源引用、追問機制（minimal interruption）。
- M2 採三段（早/中/晚）先行，保留未來擴充空間。

不在本期範圍：完整任務工具落地、第三方醫療系統串接。

### 2) 已決策略與合規
- LIFF 連結政策：
  - 正式：`line://app/{LIFF_ID}`（LINE 客戶端深鏈，原生開啟 LIFF）
  - 占位：`https://your-domain.tld/liff?pending=true`（需 HTTPS 與可信網域）
  - Flex 使用 `URIAction` 綁定，兩種 URI 均合法
- LINE 規範對齊（精要）
  - Flex altText 必填，≤ 400 字
  - 單則 Flex JSON ≤ 50 KB；Carousel ≤ 10 張 bubble（本案用 4 張）
  - Postback `data` ≤ 300 bytes，鍵值精簡（例：`view=frame36&page=1`）
  - 回覆時限：即時回覆建議 ≤ 1 秒（必要時先回輕量訊息，後續補送）
  - LIFF 深鏈 `line://app/{LIFF_ID}`；若外開網址需 HTTPS

### 3) IA 與流程（無動畫）
- Frame25（What｜即時主回應）
  - 風險徽章（低/中/高）
  - Confidence（animated=false，showLabel=true）
  - AI 小幫手「節錄 2–3 行」＋「看原文」展開（不跳 LIFF）
  - 警訊卡片 2–3 張（依偵測主症狀）
  - 行動列：
    - 深入分析 → Frame36 Carousel 預設頁（XAI）
    - 看原文 → 回傳完整原文（超長時提供 LIFF 連結）
    - 開啟 LIFF（占位）
- Frame36（Why & How｜4 頁 Carousel，預設頁為 1/4 XAI 報告）
  - 1/4 XAI 報告：Confidence、ReasoningPath（收起）、來源 2–3 筆、主 CTA 開啟 LIFF
  - 2/4 M2 病程（固定三段）：時間軸＋當前定位＋下一步建議；次 CTA「補充 ADL/IADL」
  - 3/4 M3 BPSD：Top 1–2 類別嚴重度＋即用技巧（環境/溝通/安全）；次 CTA「補充誘因/時段」
  - 4/4 M4 照護：優先級任務（緊急/建議/可選）＋分類（醫療/日常/社交）＋進度提示；次 CTA「設定提醒」
  - 頁底提供「頁碼指示＋快捷切換鍵（postback 模擬 tabs）」
- LIFF（完整內容）
  - 完整 ReasoningPath 展開、完整引用清單、工具功能（後續）

### 4) 動作映射（Frame25）
- 深入分析 → PostbackAction `data=\"view=frame36&page=1\"`
- 看原文 → PostbackAction `data=\"view=original&ref={full_text_id}\"`
- 開啟 LIFF → URIAction `uri=\"line://app/{LIFF_ID}\"`（占位可用 `https://…/liff?pending=true`）

### 5) 資料契約（後端）
- 共通欄位
  - user_id, ts, user_text
  - confidence: number(0–100)，來源優先序：模型回傳 > 規則推算 > 預設（70）
  - sources_summary: Array<{source_id, title, type(local|external), citation, snippet}>
- ReasoningPath（Frame36/頁1）
  - steps: [{ id, label(輸入|分析|比對|結果), summary, evidence_refs:[source_id] }]
  - currentStep: number（預設末節）
  - showDetails: boolean（預設 false）
- M2（三段）
  - stage: enum(early|middle|late)
  - evidence: [{symptom, severity(1–5), freq}]
  - next_actions: string[]
- M3
  - categories: [{name, score(0–100), tips:{env, comm, safety}}]
- M4
  - tasks: [{title, priority(urgent|recommended|optional), category(medical|daily|social), progress(0–100)}]

### 6) 來源管理與版本凍結（新）
- 需求：Google Drive 來源需版本控管與可追溯。
- 檔案：`docs/source_mapping.json`（由 PM/研究維護）
- 範例（可擴充 checksum/title/url）：
```json
{
  "sources": {
    "A_local": {
      "id": "taipei_guide_v2.1",
      "drive_id": "xxx",
      "last_update": "2024-12-01",
      "title": "113年臺北市失智照護資源手冊",
      "checksum": "sha256:..."
    },
    "B_local": {
      "id": "dementia_handbook_v1.3",
      "drive_id": "yyy",
      "last_update": "2024-11-10",
      "title": "失智症診療手冊"
    }
  }
}
```
- 來源優先序（Frame36 顯示 2–3 筆，完整移 LIFF）：
  - A 本地權威/指南（Drive）：113年臺北市失智照護資源手冊、失智症診療手冊、衛教資源手冊
  - B 專業照護/教育（Drive）：iSupport（繁中）、照顧者使用手冊、宣導手冊（分期）
  - C 主題專篇（期刊/專文）
  - 不足由小幫手補充，但需標註為 supplemental 並顯示信任等級

### 7) 追問（Orchestrator）與防疲勞策略（新）
- 最小打擾：不在 Frame25 主卡插入追問；以獨立短訊息/浮動提示呈現
- 每輪 ≤ 2 題；動態優先序：安全風險 > 決策關鍵 > 補充
- 總追問輪數上限：每使用者 24 小時內 ≤ 3 輪
- 冷卻期：每輪間隔 ≥ 8 小時；24 小時內最多 3 輪（伺服端強制）
- 智慧跳過：若最近 3 輪完成率 < 40%，自動降頻並改以保守預設
- 可跳過與目的說明：敏感題附「為何需要」與「跳過」選項
- 狀態保存：per user_id 維護 missing_fields、已回答/有效期、完成率

### 8) MVP 優先序（重排）
- P0: Frame25 核心 + 基礎 Confidence（規則/預設回退）
- P1: Frame36 Page1（XAI 報告：Confidence + ReasoningPath + 來源簡表）
- P2: 降級策略 + 錯誤處理（>3 秒回退、離線模式）
- P3: M2 三段模型（時間軸＋定位）
- P4: 追問 orchestrator（上限/冷卻/跳過）
- P5: M3/M4 ＋ LIFF 完整版（工具/引用完整清單）

### 9) 測試策略（新增）
- A/B：有/無 ReasoningPath 對「信任感」的影響（自填量表/CSI）
- 壓力：>3 秒降級實測（網路/模型延遲注入），確保 Frame25 仍 ≤ 3 秒回應
- 可用性：4 頁 Carousel 的學習曲線（首次成功切換率、錯誤點擊率）

### 10) 監控與目標（新增）
- Frame25→Frame36 轉換率：> 30%
- ReasoningPath 展開率：< 10%
- 追問完成率：> 60%
- LIFF 平均停留：> 2 分鐘
- 錯誤率：Flex payload 超限、postback 超長、LIFF 開啟失敗率 < 1%

### 11) 降級與錯誤處理
- Confidence：模型回傳 > 規則推算 > 預設 70%；T+2s 顯示「計算中」，T+3s 採回退值
- ReasoningPath：若來源不足，顯示摘要＋補充來源提示；長文移 LIFF
- 服務不可用：先回「輕量安全摘要」＋後送詳情（或提供 LIFF 入口）

### 12) 與現有專案契合度
- `services/line-bot/main.py`：
  - 保留同步 handler（相容 LINE SDK v3）
  - 使用 PostbackAction `data` 參數路由至 Frame36 各頁（`view=frame36&page=n`）
  - 保持 `data` 精簡以符合 300 bytes 限制
- 視覺化結構：
  - Frame25 主卡（What）＋ Frame36 4 頁 Carousel（Why & How）
  - M2 固定三段先行，不破壞契約；後續擴充至 5 段僅增枚舉與模板
- 來源：
  - 新增 `docs/source_mapping.json` 作為權威來源凍結表；伺服端以 `source_id` 連結引用

### 13) 交付物與驗收
- 文檔：本 PRD（`docs/visualization_prd.md`）與 `docs/source_mapping.json` 草案
- P0 成果：
  - Frame25 Flex（無動畫）按設計呈現；
  - Confidence 顯示與優先序；
  - 行動列可用（深入分析/看原文/開啟 LIFF 占位）
- P1 成果：Frame36 Page1（XAI）可切換；來源 2–3 筆顯示；ReasoningPath 收起
- 指標：P0 上線後一週內達成 Frame25→Frame36 轉換率 ≥ 30%

### 14) 後續工作（提要）
- 建立來源校驗工具（比對 Drive 檔名/版本/雜湊）
- 追問 orchestrator 狀態儲存（Redis/DB，依現有基礎選擇）
- LIFF 真實頁面（line://app/{LIFF_ID}）與占位網址落地

—— 本文件供 Cursor 追蹤，實作時請嚴格遵守 LINE 規範與本 PRD 資料契約 ——
