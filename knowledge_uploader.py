# knowledge_uploader.py - 批量上传知识文件到 Pinecone
from pinecone import Pinecone
import json
import csv
import hashlib
import random
import time
from pathlib import Path
from typing import List, Dict

# 初始化 Pinecone
pc = Pinecone(api_key="pcsk_4WvWXx_G5bRUFdFNzLzRHNM9rkvFMvC18TMRTaeYXVCxmWSPQLmKr4xAs4UaZg5NvVb69m")
index = pc.Index("dementia-care-knowledge")

def create_embedding(text, dimension=1024):
    """创建文本嵌入向量"""
    text_hash = hashlib.md5(text.encode()).hexdigest()
    vector = []
    for i in range(dimension):
        seed = int(text_hash[i % len(text_hash)], 16) + i
        random.seed(seed)
        vector.append(random.uniform(-1, 1))

    magnitude = sum(x*x for x in vector) ** 0.5
    return [x/magnitude for x in vector] if magnitude > 0 else [1.0/dimension] * dimension

class KnowledgeUploader:
    """知识文件上传器"""

    def __init__(self):
        self.supported_formats = ['.json', '.csv', '.txt', '.md']
        self.batch_size = 10  # 每批上传数量

    def process_json_file(self, file_path: str) -> List[Dict]:
        """处理 JSON 文件"""
        print(f"📄 Processing JSON file: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            chunks = []

            # 处理不同的 JSON 结构
            if isinstance(data, list):
                # 如果是数组格式
                for i, item in enumerate(data):
                    chunk = self._extract_chunk_from_dict(item, f"json-{i:03d}")
                    if chunk:
                        chunks.append(chunk)
            elif isinstance(data, dict):
                if 'chunks' in data:
                    # 如果有 chunks 字段
                    for i, item in enumerate(data['chunks']):
                        chunk = self._extract_chunk_from_dict(item, f"json-{i:03d}")
                        if chunk:
                            chunks.append(chunk)
                else:
                    # 如果是单个对象
                    chunk = self._extract_chunk_from_dict(data, "json-001")
                    if chunk:
                        chunks.append(chunk)

            print(f"✅ Extracted {len(chunks)} chunks from JSON")
            return chunks

        except Exception as e:
            print(f"❌ Error processing JSON file: {str(e)}")
            return []

    def process_csv_file(self, file_path: str) -> List[Dict]:
        """处理 CSV 文件"""
        print(f"📄 Processing CSV file: {file_path}")

        try:
            chunks = []

            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for i, row in enumerate(reader):
                    chunk = {
                        'id': f"csv-{i:03d}",
                        'title': row.get('title', row.get('標題', f"CSV Row {i+1}")),
                        'content': row.get('content', row.get('內容', '')),
                        'type': row.get('type', row.get('類型', 'general')),
                        'source': file_path,
                        'metadata': {k: v for k, v in row.items() if k not in ['title', 'content', 'type']}
                    }

                    # 确保有内容
                    if chunk['content'].strip():
                        chunks.append(chunk)

            print(f"✅ Extracted {len(chunks)} chunks from CSV")
            return chunks

        except Exception as e:
            print(f"❌ Error processing CSV file: {str(e)}")
            return []

    def process_text_file(self, file_path: str) -> List[Dict]:
        """处理纯文本/Markdown 文件"""
        print(f"📄 Processing text file: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 按段落分割
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

            chunks = []
            for i, paragraph in enumerate(paragraphs):
                # 提取标题（如果是 markdown 格式）
                if paragraph.startswith('#'):
                    lines = paragraph.split('\n')
                    title = lines[0].strip('#').strip()
                    content = '\n'.join(lines[1:]).strip()
                else:
                    title = f"Section {i+1}"
                    content = paragraph

                if len(content) > 50:  # 过滤太短的内容
                    chunk = {
                        'id': f"txt-{i:03d}",
                        'title': title,
                        'content': content,
                        'type': 'text_section',
                        'source': file_path
                    }
                    chunks.append(chunk)

            print(f"✅ Extracted {len(chunks)} chunks from text file")
            return chunks

        except Exception as e:
            print(f"❌ Error processing text file: {str(e)}")
            return []

    def _extract_chunk_from_dict(self, item: Dict, default_id: str) -> Dict:
        """从字典中提取 chunk 数据"""
        # 尝试不同的字段名组合
        title_fields = ['title', '標題', 'name', '名稱', 'heading']
        content_fields = ['content', '內容', 'text', '文字', 'description', '描述']
        type_fields = ['type', '類型', 'category', '分類', 'chunk_type']

        title = None
        content = None
        chunk_type = 'general'

        # 查找标题
        for field in title_fields:
            if field in item and item[field]:
                title = str(item[field])
                break

        # 查找内容
        for field in content_fields:
            if field in item and item[field]:
                content = str(item[field])
                break

        # 查找类型
        for field in type_fields:
            if field in item and item[field]:
                chunk_type = str(item[field])
                break

        if not title or not content:
            return None

        return {
            'id': item.get('id', item.get('chunk_id', default_id)),
            'title': title,
            'content': content,
            'type': chunk_type,
            'metadata': {k: v for k, v in item.items() 
                        if k not in ['id', 'chunk_id', 'title', 'content', 'type']}
        }

    def upload_chunks_to_pinecone(self, chunks: List[Dict]):
        """批量上传 chunks 到 Pinecone"""
        print(f"🚀 Uploading {len(chunks)} chunks to Pinecone...")

        total_uploaded = 0

        # 分批上传
        for i in range(0, len(chunks), self.batch_size):
            batch = chunks[i:i + self.batch_size]
            vectors_to_upload = []

            for chunk in batch:
                try:
                    # 创建嵌入向量
                    text_content = f"{chunk['title']} {chunk['content']}"
                    embedding = create_embedding(text_content)

                    # 准备向量数据
                    vector_data = {
                        'id': chunk['id'],
                        'values': embedding,
                        'metadata': {
                            'title': chunk['title'][:200],  # 限制长度
                            'content': chunk['content'][:500],
                            'type': chunk['type'],
                            'source': chunk.get('source', 'uploaded'),
                            **chunk.get('metadata', {})
                        }
                    }

                    vectors_to_upload.append(vector_data)

                except Exception as e:
                    print(f"⚠️ Skipping chunk {chunk.get('id', 'unknown')}: {str(e)}")
                    continue

            # 上传这一批
            if vectors_to_upload:
                try:
                    upsert_response = index.upsert(vectors=vectors_to_upload)
                    uploaded_count = upsert_response.upserted_count
                    total_uploaded += uploaded_count
                    print(f"✅ Batch {i//self.batch_size + 1}: Uploaded {uploaded_count} vectors")

                    # 稍微等待一下
                    time.sleep(1)

                except Exception as e:
                    print(f"❌ Failed to upload batch {i//self.batch_size + 1}: {str(e)}")

        print(f"🎉 Total uploaded: {total_uploaded} vectors")
        return total_uploaded

    def upload_file(self, file_path: str):
        """上传单个文件"""
        file_path = Path(file_path)

        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return False

        if file_path.suffix.lower() not in self.supported_formats:
            print(f"❌ Unsupported file format: {file_path.suffix}")
            print(f"Supported formats: {', '.join(self.supported_formats)}")
            return False

        # 根据文件类型处理
        chunks = []
        if file_path.suffix.lower() == '.json':
            chunks = self.process_json_file(str(file_path))
        elif file_path.suffix.lower() == '.csv':
            chunks = self.process_csv_file(str(file_path))
        elif file_path.suffix.lower() in ['.txt', '.md']:
            chunks = self.process_text_file(str(file_path))

        if chunks:
            uploaded_count = self.upload_chunks_to_pinecone(chunks)
            print(f"✅ Successfully processed {file_path.name}: {uploaded_count} chunks uploaded")
            return True
        else:
            print(f"❌ No valid chunks extracted from {file_path.name}")
            return False

    def upload_directory(self, directory_path: str):
        """上传整个目录的文件"""
        directory = Path(directory_path)

        if not directory.exists():
            print(f"❌ Directory not found: {directory}")
            return

        # 查找支持的文件
        files = []
        for ext in self.supported_formats:
            files.extend(directory.glob(f"*{ext}"))
            files.extend(directory.glob(f"**/*{ext}"))  # 递归查找

        if not files:
            print(f"❌ No supported files found in {directory}")
            return

        print(f"📁 Found {len(files)} files to process")

        successful = 0
        for file_path in files:
            print(f"\n{'='*50}")
            if self.upload_file(str(file_path)):
                successful += 1

        print(f"\n🎉 Processing complete: {successful}/{len(files)} files uploaded successfully")

def create_sample_files():
    """创建示例文件供测试"""
    print("📝 Creating sample files...")

    # 创建 JSON 示例
    json_data = {
        "chunks": [
            {
                "chunk_id": "sample-001",
                "title": "失智症日常照護",
                "content": "失智症患者的日常照護需要耐心和技巧，包括協助洗澡、用餐、服藥等基本生活需求。",
                "chunk_type": "care_guide",
                "keywords": ["日常照護", "生活協助", "基本需求"]
            },
            {
                "chunk_id": "sample-002", 
                "title": "環境安全設計",
                "content": "為失智症患者設計安全的居住環境很重要，包括移除障礙物、增加照明、安裝扶手等。",
                "chunk_type": "safety_guide",
                "keywords": ["環境安全", "居住設計", "障礙物"]
            }
        ]
    }

    with open('sample_knowledge.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    # 创建 CSV 示例
    csv_data = [
        ["title", "content", "type"],
        ["藥物管理", "失智症患者容易忘記服藥，建議使用藥盒分裝和鬧鐘提醒。", "medication"],
        ["營養照護", "確保患者攝取均衡營養，注意水分補充和吞嚥安全。", "nutrition"],
        ["運動療法", "適度運動有助於維持認知功能和身體健康。", "exercise"]
    ]

    with open('sample_knowledge.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)

    # 创建 Markdown 示例
    markdown_content = """# 失智症照護指南

## 認知訓練

認知訓練可以幫助延緩認知功能退化，包括記憶遊戲、拼圖、閱讀等活動。

## 社交互動

維持社交互動對失智症患者很重要，可以參加社區活動或定期與家人朋友聚會。

## 睡眠管理

良好的睡眠品質有助於認知功能，建議建立規律的作息時間。
"""

    with open('sample_knowledge.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print("✅ Sample files created:")
    print("  - sample_knowledge.json")
    print("  - sample_knowledge.csv") 
    print("  - sample_knowledge.md")

def main():
    """主函数"""
    print("🚀 Pinecone Knowledge Uploader")
    print("=" * 50)

    uploader = KnowledgeUploader()

    while True:
        print("\n📋 Options:")
        print("1. Upload single file")
        print("2. Upload directory")
        print("3. Create sample files")
        print("4. Check Pinecone status")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == '1':
            file_path = input("Enter file path: ").strip()
            uploader.upload_file(file_path)

        elif choice == '2':
            dir_path = input("Enter directory path: ").strip()
            uploader.upload_directory(dir_path)

        elif choice == '3':
            create_sample_files()

        elif choice == '4':
            try:
                stats = index.describe_index_stats()
                print(f"📊 Pinecone Status:")
                print(f"  Total vectors: {stats.total_vector_count}")
                print(f"  Dimension: {stats.dimension}")
                print(f"  Index fullness: {stats.index_fullness}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")

        elif choice == '5':
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    main()

# 快速上传命令示例:
# uploader = KnowledgeUploader()
# uploader.upload_file("your_file.json")
# uploader.upload_directory("./knowledge_files/")

# 支持的文件格式示例:

# JSON 格式:
"""
{
  "chunks": [
    {
      "chunk_id": "001",
      "title": "标题",
      "content": "内容",
      "chunk_type": "类型",
      "keywords": ["关键词1", "关键词2"]
    }
  ]
}
"""

# CSV 格式:
"""
title,content,type
失智症症状,记忆力减退是主要症状,symptom
照护技巧,保持耐心很重要,care_tip
"""

# Markdown/Text 格式:
"""
# 主标题

## 子标题1
内容段落1

## 子标题2  
内容段落2
"""