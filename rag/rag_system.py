# rag_system.py
import re
import os
from dotenv import load_dotenv
import numpy as np
from openai import OpenAI


# ──────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
EMBED_MODEL = os.environ["EMBED_MODEL"]
CHAT_MODEL = os.environ["CHAT_MODEL"]

client = OpenAI(api_key=OPENAI_API_KEY)

# ──────────────────────────────────────────
# STEP 1: CHUNKING
# ──────────────────────────────────────────
def load_and_chunk(filepath, chunk_size=300, overlap=50):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    text = re.sub(r"#{1,6}\s+", "", text)
    text = re.sub(r"\*\*|__|\*|_|`", "", text)
    text = re.sub(r"\n{2,}", "\n", text).strip()

    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap

    print(f"✅ Chunked thành {len(chunks)} đoạn")
    return chunks

# ──────────────────────────────────────────
# STEP 2: EMBEDDING
# ──────────────────────────────────────────
def get_embeddings(texts: list[str]) -> np.ndarray:
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=texts
    )
    vectors = [item.embedding for item in response.data]
    print(f"✅ Đã embedding {len(vectors)} chunks (dim={len(vectors[0])})")
    return np.array(vectors, dtype=np.float32)

# ──────────────────────────────────────────
# STEP 3: RETRIEVAL
# ──────────────────────────────────────────
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = a / np.linalg.norm(a, axis=1, keepdims=True)
    b = b / np.linalg.norm(b, axis=1, keepdims=True)
    return a @ b.T

def retrieve(query: str, chunks: list[str], chunk_embeddings: np.ndarray, top_k=3):
    query_emb = get_embeddings([query])
    scores    = cosine_similarity(query_emb, chunk_embeddings)[0]
    top_idx   = np.argsort(scores)[::-1][:top_k]
    return [chunks[i] for i in top_idx], scores[top_idx]

# ──────────────────────────────────────────
# STEP 4: GENERATION bằng OpenAI
# ──────────────────────────────────────────
def ask(question: str, chunks: list[str], chunk_embeddings: np.ndarray):
    relevant, scores = retrieve(question, chunks, chunk_embeddings, top_k=3)

    print(f"\n📎 Top chunks (scores: {scores.round(3)}):")
    for i, c in enumerate(relevant):
        print(f"  [{i+1}] {c[:80]}...")

    context = "\n\n---\n\n".join(relevant)

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Bạn là trợ lý trả lời câu hỏi dựa trên tài liệu được cung cấp. Chỉ dùng thông tin trong ngữ cảnh. Nếu không có thông tin liên quan, hãy nói 'Tài liệu không đề cập đến vấn đề này.'"
            },
            {
                "role": "user",
                "content": f"Ngữ cảnh:\n{context}\n\nCâu hỏi: {question}"
            }
        ],
        temperature=0.2,  # thấp để câu trả lời bám sát tài liệu
    )
    return response.choices[0].message.content

# ──────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────
if __name__ == "__main__":
    chunks = load_and_chunk("docs/truyen.md")
    chunk_embeddings = get_embeddings(chunks)

    # Lưu lại để không cần embed lại lần sau
    np.save("embeddings.npy", chunk_embeddings)

    print("\n🤖 RAG sẵn sàng! Gõ 'exit' để thoát.\n")

    while True:
        question = input("Câu hỏi: ").strip()
        if question.lower() in ("exit", "quit"):
            break
        if not question:
            continue
        answer = ask(question, chunks, chunk_embeddings)
        print(f"\n💬 Trả lời:\n{answer}\n")