#!/usr/bin/env python3
"""
創建 M4 照護任務導航資料
建立失智症照護任務導航和緊急指南的知識片段
"""

import json
import os

print("🔧 建立 M4 照護任務導航模組...")

# 確保目錄存在
os.makedirs('data/chunks', exist_ok=True)

# M4 照護任務導航知識片段
m4_chunks = [
    {
        "chunk_id": "M4-01",
        "module_id": "M4",
        "chunk_type": "care_task_navigation",
        "title": "早期階段照護任務",
        "content": "早期階段重點任務：1.認知功能維持 - 進行益智遊戲、閱讀、社交活動；2.安全環境建立 - 移除危險物品、加裝安全設備；3.醫療追蹤管理 - 定期回診、藥物管理、健康監測。常見挑戰：患者可能對診斷感到否認或沮喪。",
        "keywords": ["早期", "認知維持", "安全環境", "醫療追蹤", "否認", "沮喪"],
        "confidence_score": 0.95,
        "source": "照護任務指引"
    },
    {
        "chunk_id": "M4-02",
        "module_id": "M4",
        "chunk_type": "care_task_navigation",
        "title": "中期階段照護任務",
        "content": "中期階段重點任務：1.日常生活協助 - 協助洗澡、穿衣、進食等基本需求；2.行為症狀管理 - 處理遊走、激動等問題行為；3.家庭支援協調 - 安排日照服務、居家照護資源。常見挑戰：照護負擔增加，需要更多外部支援。",
        "keywords": ["中期", "日常生活協助", "行為管理", "家庭支援", "照護負擔", "外部支援"],
        "confidence_score": 0.93,
        "source": "照護任務指引"
    },
    {
        "chunk_id": "M4-03",
        "module_id": "M4",
        "chunk_type": "care_task_navigation",
        "title": "晚期階段照護任務",
        "content": "晚期階段重點任務：1.舒適照護提供 - 疼痛管理、舒適體位、皮膚照護；2.營養水分維持 - 協助進食、預防嗆咳、營養評估；3.家屬情緒支持 - 提供心理支持、預立醫療決定討論。常見挑戰：面對生命末期照護的身心壓力。",
        "keywords": ["晚期", "舒適照護", "營養維持", "家屬支持", "生命末期", "身心壓力"],
        "confidence_score": 0.91,
        "source": "照護任務指引"
    },
    {
        "chunk_id": "M4-04",
        "module_id": "M4",
        "chunk_type": "emergency_guidance",
        "title": "緊急情況處理指南",
        "content": "緊急情況包括：走失、跌倒、吞嚥困難、發燒、意識不清等。立即行動：1.評估安全狀況；2.撥打緊急電話；3.準備就醫資料；4.通知家屬。預防措施：環境安全檢查、定期健康評估、緊急聯絡卡。",
        "keywords": ["緊急", "走失", "跌倒", "吞嚥困難", "發燒", "意識不清", "安全評估"],
        "confidence_score": 0.98,
        "source": "緊急處理指引"
    },
    {
        "chunk_id": "M4-05",
        "module_id": "M4",
        "chunk_type": "resource_navigation",
        "title": "照護資源導航",
        "content": "長照 2.0 服務：居家服務、日間照顧、家庭托顧、喘息服務。醫療資源：失智症門診、神經內科、精神科、復健科。社會資源：失智症協會、家屬支持團體、照護者課程。申請流程：評估→核定→服務提供。",
        "keywords": ["長照2.0", "居家服務", "日間照顧", "醫療資源", "社會資源", "申請流程"],
        "confidence_score": 0.94,
        "source": "資源導航指引"
    },
    {
        "chunk_id": "M4-06",
        "module_id": "M4",
        "chunk_type": "legal_rights",
        "title": "法律權益保障",
        "content": "重要法律文件：監護宣告、輔助宣告、預立醫療決定、安寧緩和醫療意願書。財產管理：信託、保險、遺產規劃。照護者權益：勞動保障、經濟補助、心理支持。建議諮詢：律師、會計師、社工師。",
        "keywords": ["法律文件", "監護宣告", "預立醫療", "財產管理", "照護者權益", "專業諮詢"],
        "confidence_score": 0.92,
        "source": "法律權益指引"
    }
]

# 儲存為 JSON 檔案
output_file = 'm4_care_navigation_data.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(m4_chunks, f, ensure_ascii=False, indent=2)

print(f"✅ M4 照護任務導航資料已建立：{output_file}")
print(f"📊 共建立 {len(m4_chunks)} 個知識片段")

# 同時建立 JSONL 格式（用於 RAG 系統）
output_jsonl = 'data/chunks/m4_care_navigation_chunks.jsonl'
with open(output_jsonl, 'w', encoding='utf-8') as f:
    for chunk in m4_chunks:
        f.write(json.dumps(chunk, ensure_ascii=False) + '\n')

print(f"✅ M4 JSONL 格式已建立：{output_jsonl}")

print("\n📋 M4 模組功能：")
print("   🎯 照護任務導航")
print("   🚨 緊急情況處理")
print("   📚 資源導航服務")
print("   ⚖️  法律權益保障")
print("   💡 階段性任務指引")
print("   🆘 緊急指南與聯絡") 