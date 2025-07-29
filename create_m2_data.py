#!/usr/bin/env python3
"""
創建 M2 病程階段資料
建立失智症病程階段的知識片段
"""

import json
import os

print("🔧 建立 M2 病程階段模組...")

# 確保目錄存在
os.makedirs('data/chunks', exist_ok=True)

# M2 病程階段知識片段
m2_chunks = [
    {
        "chunk_id": "M2-01",
        "module_id": "M2",
        "chunk_type": "stage_description",
        "title": "輕度失智症階段特徵",
        "content": "患者在熟悉環境中仍可獨立生活，但在複雜任務上需要協助。認知能力有輕微記憶缺損，主要影響近期記憶。日常生活基本活動多數可自理，但複雜活動如理財、購物需要監督。照護重點：建立規律作息、安全環境、認知刺激活動。",
        "keywords": ["輕度", "獨立生活", "複雜任務", "監督", "規律作息", "提醒", "協助"],
        "confidence_score": 0.92,
        "source": "CDR量表與照護指引"
    },
    {
        "chunk_id": "M2-02",
        "module_id": "M2",
        "chunk_type": "stage_description",
        "title": "中度失智症階段特徵",
        "content": "明顯認知功能衰退，日常生活需要相當程度協助。記憶力顯著下降，時空混亂常見。基本活動需要提醒或協助，複雜活動無法獨立完成。可能出現遊走、重複行為、睡眠障礙、情緒不穩。需要協助穿衣、容易迷路。",
        "keywords": ["中度", "認知衰退", "協助", "穿衣", "迷路", "睡眠障礙", "遊走", "重複行為"],
        "confidence_score": 0.90,
        "source": "CDR量表與照護指引"
    },
    {
        "chunk_id": "M2-03",
        "module_id": "M2",
        "chunk_type": "stage_description",
        "title": "重度失智症階段特徵",
        "content": "嚴重認知功能喪失，完全依賴他人照顧。無法辨認家人，語言能力嚴重受損，可能無法說話或理解語言。基本生活功能如進食、如廁、穿衣都需要完全協助。可能出現吞嚥困難、大小便失禁。",
        "keywords": ["重度", "完全依賴", "無法辨認", "語言受損", "吞嚥困難", "失禁", "餵食"],
        "confidence_score": 0.88,
        "source": "CDR量表與照護指引"
    },
    {
        "chunk_id": "M2-04",
        "module_id": "M2",
        "chunk_type": "care_guidance",
        "title": "輕度階段照護指引",
        "content": "建立規律作息，保持認知刺激活動，確保居家安全。協助建立提醒系統，如藥盒、日曆。鼓勵參與社交活動，保持身體活動。定期就醫追蹤，監測病情變化。",
        "keywords": ["規律作息", "認知刺激", "居家安全", "提醒系統", "社交活動", "定期追蹤"],
        "confidence_score": 0.95,
        "source": "照護指引"
    },
    {
        "chunk_id": "M2-05",
        "module_id": "M2",
        "chunk_type": "care_guidance",
        "title": "中度階段照護指引",
        "content": "提供全天候照顧，防止走失。建立安全環境，移除危險物品。協助日常生活活動，建立固定作息。處理行為問題，如遊走、重複行為。考慮使用輔具，如定位器、安全手環。",
        "keywords": ["全天候照顧", "防止走失", "安全環境", "固定作息", "行為問題", "輔具"],
        "confidence_score": 0.93,
        "source": "照護指引"
    },
    {
        "chunk_id": "M2-06",
        "module_id": "M2",
        "chunk_type": "care_guidance",
        "title": "重度階段照護指引",
        "content": "提供完全照護，包括餵食、如廁、清潔。預防併發症，如褥瘡、感染。維持舒適，緩解不適症狀。支持家屬，提供心理支持。考慮安寧照護選項。",
        "keywords": ["完全照護", "預防併發症", "維持舒適", "支持家屬", "安寧照護"],
        "confidence_score": 0.91,
        "source": "照護指引"
    }
]

# 儲存為 JSON 檔案
output_file = 'm2_stage_data.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(m2_chunks, f, ensure_ascii=False, indent=2)

print(f"✅ M2 病程階段資料已建立：{output_file}")
print(f"📊 共建立 {len(m2_chunks)} 個知識片段")

# 同時建立 JSONL 格式（用於 RAG 系統）
output_jsonl = 'data/chunks/m2_stage_chunks.jsonl'
with open(output_jsonl, 'w', encoding='utf-8') as f:
    for chunk in m2_chunks:
        f.write(json.dumps(chunk, ensure_ascii=False) + '\n')

print(f"✅ M2 JSONL 格式已建立：{output_jsonl}")

print("\n📋 M2 模組功能：")
print("   🏥 病程階段分析")
print("   📊 輕度/中度/重度評估")
print("   💡 階段性照護指引")
print("   🔍 症狀嚴重程度評估")
