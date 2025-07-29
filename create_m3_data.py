#!/usr/bin/env python3
"""
創建 M3 BPSD 行為心理症狀資料
建立失智症行為心理症狀的知識片段
"""

import json
import os

print("🔧 建立 M3 BPSD 行為心理症狀模組...")

# 確保目錄存在
os.makedirs('data/chunks', exist_ok=True)

# M3 BPSD 行為心理症狀知識片段
m3_chunks = [
    {
        "chunk_id": "M3-01",
        "module_id": "M3",
        "chunk_type": "delusion_symptoms",
        "title": "妄想症狀",
        "content": "失智症患者可能出現妄想症狀，如被偷妄想、被害妄想、嫉妒妄想等。常見表現包括懷疑有人偷東西、認為配偶不忠、認為有人要害自己。這些症狀會增加照護困難，需要耐心處理和適當的醫療介入。",
        "keywords": ["妄想", "被偷妄想", "被害妄想", "嫉妒妄想", "懷疑", "不忠"],
        "confidence_score": 0.94,
        "source": "BPSD 評估量表"
    },
    {
        "chunk_id": "M3-02",
        "module_id": "M3",
        "chunk_type": "hallucination_symptoms",
        "title": "幻覺症狀",
        "content": "患者可能出現視覺、聽覺或其他感官幻覺。常見包括看到已故親人、聽到有人說話、感覺有蟲在身上爬等。幻覺可能導致患者恐懼、激動或困惑，需要安全環境和適當的藥物治療。",
        "keywords": ["幻覺", "視覺幻覺", "聽覺幻覺", "已故親人", "恐懼", "激動"],
        "confidence_score": 0.92,
        "source": "BPSD 評估量表"
    },
    {
        "chunk_id": "M3-03",
        "module_id": "M3",
        "chunk_type": "agitation_aggression",
        "title": "激動攻擊行為",
        "content": "包括言語攻擊、身體攻擊、激動不安等行為。患者可能大聲叫罵、推人、打人、破壞物品。這些行為通常由環境刺激、身體不適或溝通困難引起，需要找出原因並適當處理。",
        "keywords": ["激動", "攻擊", "言語攻擊", "身體攻擊", "叫罵", "推人", "破壞"],
        "confidence_score": 0.90,
        "source": "BPSD 評估量表"
    },
    {
        "chunk_id": "M3-04",
        "module_id": "M3",
        "chunk_type": "depression_anxiety",
        "title": "憂鬱與焦慮",
        "content": "患者可能出現憂鬱症狀如情緒低落、興趣喪失、食慾改變、睡眠障礙。焦慮症狀包括過度擔心、緊張不安、坐立難安。這些症狀會影響生活品質，需要心理支持和藥物治療。",
        "keywords": ["憂鬱", "焦慮", "情緒低落", "興趣喪失", "食慾改變", "睡眠障礙", "擔心"],
        "confidence_score": 0.93,
        "source": "BPSD 評估量表"
    },
    {
        "chunk_id": "M3-05",
        "module_id": "M3",
        "chunk_type": "wandering_repetitive",
        "title": "遊走與重複行為",
        "content": "患者可能出現無目的遊走、重複動作或言語。遊走可能導致走失風險，需要安全措施如定位器、安全手環。重複行為包括重複問問題、重複整理物品等，需要耐心和理解。",
        "keywords": ["遊走", "重複行為", "走失", "重複問問題", "重複整理", "定位器"],
        "confidence_score": 0.89,
        "source": "BPSD 評估量表"
    },
    {
        "chunk_id": "M3-06",
        "module_id": "M3",
        "chunk_type": "sleep_disorder",
        "title": "睡眠障礙",
        "content": "包括失眠、日夜顛倒、夜間遊走等問題。患者可能晚上不睡覺、到處走動、大聲說話。這些問題會影響患者和照護者的休息，需要建立規律作息和適當的環境調整。",
        "keywords": ["睡眠障礙", "失眠", "日夜顛倒", "夜間遊走", "不睡覺", "規律作息"],
        "confidence_score": 0.91,
        "source": "BPSD 評估量表"
    },
    {
        "chunk_id": "M3-07",
        "module_id": "M3",
        "chunk_type": "eating_behavior",
        "title": "飲食行為改變",
        "content": "包括食慾改變、吞嚥困難、飲食偏好改變等。患者可能忘記吃飯、拒絕進食、或過度進食。吞嚥困難可能導致嗆咳、肺炎等併發症，需要適當的飲食調整和醫療評估。",
        "keywords": ["飲食行為", "食慾改變", "吞嚥困難", "忘記吃飯", "拒絕進食", "嗆咳"],
        "confidence_score": 0.88,
        "source": "BPSD 評估量表"
    },
    {
        "chunk_id": "M3-08",
        "module_id": "M3",
        "chunk_type": "apathy_indifference",
        "title": "冷漠與缺乏動機",
        "content": "患者可能表現出對日常活動缺乏興趣、情感淡漠、缺乏動機。這種症狀會影響生活品質和照護效果，需要鼓勵參與活動、提供適當的刺激和情感支持。",
        "keywords": ["冷漠", "缺乏動機", "缺乏興趣", "情感淡漠", "參與活動", "情感支持"],
        "confidence_score": 0.87,
        "source": "BPSD 評估量表"
    },
    {
        "chunk_id": "M3-09",
        "module_id": "M3",
        "chunk_type": "disinhibition",
        "title": "脫抑制行為",
        "content": "包括不適當的言語、行為或情感表達。患者可能說出不當的話、在公共場合脫衣服、過度親密等。這些行為會造成社交困擾，需要適當的引導和環境控制。",
        "keywords": ["脫抑制", "不當言語", "不當行為", "過度親密", "社交困擾", "環境控制"],
        "confidence_score": 0.86,
        "source": "BPSD 評估量表"
    },
    {
        "chunk_id": "M3-10",
        "module_id": "M3",
        "chunk_type": "treatment_guidance",
        "title": "BPSD 治療指引",
        "content": "BPSD 的治療需要多面向介入，包括非藥物治療如環境調整、行為治療、認知刺激等。藥物治療需要謹慎使用，避免過度用藥。照護者教育和支持也是重要環節。",
        "keywords": ["治療指引", "非藥物治療", "環境調整", "行為治療", "藥物治療", "照護者教育"],
        "confidence_score": 0.95,
        "source": "BPSD 治療指引"
    }
]

# 儲存為 JSON 檔案
output_file = 'm3_bpsd_data.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(m3_chunks, f, ensure_ascii=False, indent=2)

print(f"✅ M3 BPSD 資料已建立：{output_file}")
print(f"📊 共建立 {len(m3_chunks)} 個知識片段")

# 同時建立 JSONL 格式（用於 RAG 系統）
output_jsonl = 'data/chunks/m3_bpsd_chunks.jsonl'
with open(output_jsonl, 'w', encoding='utf-8') as f:
    for chunk in m3_chunks:
        f.write(json.dumps(chunk, ensure_ascii=False) + '\n')

print(f"✅ M3 JSONL 格式已建立：{output_jsonl}")

print("\n📋 M3 模組功能：")
print("   🧠 BPSD 行為心理症狀分析")
print("   🔍 妄想/幻覺症狀檢測")
print("   ⚡ 激動攻擊行為評估")
print("   😢 憂鬱焦慮症狀分析")
print("   🚶 遊走重複行為檢測")
print("   😴 睡眠障礙評估")
print("   🍽️  飲食行為改變分析")
print("   💊 治療指引建議")
