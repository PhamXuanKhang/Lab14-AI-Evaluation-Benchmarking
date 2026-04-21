import json
import asyncio
import os
import sys
from typing import List, Dict
# Thêm workspace root vào sys.path để import module rag
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from openai import OpenAI
from rag.rag_system import load_and_chunk


# Thiết lập OpenAI
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
CHAT_MODEL = os.environ.get("CHAT_MODEL", "gpt-3.5-turbo")
client = OpenAI(api_key=OPENAI_API_KEY)

async def generate_qa_from_text(text: str, num_pairs: int = 5) -> List[Dict]:
    """
    Sử dụng OpenAI API để tạo các cặp (Question, Expected Answer, Context) từ đoạn văn bản cho trước.
    Đảm bảo có ít nhất 1 câu hỏi 'lừa' hoặc cực khó.
    """
    print(f"Generating {num_pairs} QA pairs from text...")
    prompt = f"""
Bạn là chuyên gia tạo bộ dữ liệu kiểm thử cho AI. Hãy tạo {num_pairs} cặp câu hỏi-đáp (QA) từ đoạn văn sau, mỗi cặp gồm:
- question: Câu hỏi dựa trên nội dung, đa dạng mức độ (dễ, trung bình, khó, lừa).
- expected_answer: Đáp án đúng, ngắn gọn, chính xác.
- context: Trích đoạn liên quan (có thể là toàn bộ hoặc một phần text).
- metadata: Ghi rõ 'difficulty' (easy/medium/hard/adversarial) và 'type' (fact-check, reasoning, adversarial...)
Yêu cầu: Ít nhất 1 câu hỏi phải là loại 'adversarial' hoặc rất khó.
Trả về kết quả dưới dạng một list JSON Python hợp lệ.
Đoạn văn:
"""
    prompt += text.strip()

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "Bạn là chuyên gia tạo bộ dữ liệu kiểm thử cho AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1200
    )
    import json
    content = response.choices[0].message.content
    # Loại bỏ code block markdown nếu có
    if content.strip().startswith("```"):
        content = content.strip().split('\n', 1)[-1]
        if content.endswith('```'):
            content = content[:-3]
    try:
        qa_pairs = json.loads(content)
        assert isinstance(qa_pairs, list)
    except Exception as e:
        print("Lỗi khi parse kết quả từ LLM:", e)
        print("Nội dung trả về:", content)
        qa_pairs = []
    return qa_pairs

async def main():
    # Đọc file tài liệu gốc
    with open("docs/truyen.md", "r", encoding="utf-8") as f:
        raw_text = f.read()
    
    # Chunking
    chunks = load_and_chunk("docs/truyen.md", chunk_size=300, overlap=50)
    print(f"Tổng số chunk: {len(chunks)}")

    golden_set = []
    for idx, chunk in enumerate(chunks):
        print(f"\n---\nChunk {idx} (length {len(chunk)}): {chunk[:60]}...")
        qa_pairs = await generate_qa_from_text(chunk, num_pairs=2)  # sinh 2 QA cho mỗi chunk
        print(f"Chunk {idx}: Sinh được {len(qa_pairs)} QA pairs")
        if not qa_pairs:
            print(f"LỖI: Không sinh được QA cho chunk {idx}. Dừng script để kiểm tra.")
            break
        for qa in qa_pairs:
            qa["ground_truth_id"] = idx
            qa["chunk_text"] = chunk[:200]  # lưu trích đoạn chunk (nếu muốn)
            golden_set.append(qa)

    with open("data/golden_set.jsonl", "w", encoding="utf-8") as f:
        for pair in golden_set:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")
    print(f"Done! Saved {len(golden_set)} QA pairs to data/golden_set.jsonl")

if __name__ == "__main__":
    asyncio.run(main())
