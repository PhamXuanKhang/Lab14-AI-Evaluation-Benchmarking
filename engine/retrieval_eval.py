import numpy as np
from typing import List, Dict
from rag.rag_system import get_embeddings, cosine_similarity

class RetrievalEvaluator:
    def __init__(self):
        pass

    def retrieve_top_k(self, query: str, chunks: List[str], chunk_embeddings: np.ndarray, k: int = 3):
        """
        Truy hồi top-k chunk index cho 1 câu hỏi dựa trên cosine similarity.
        """
        query_emb = get_embeddings([query])
        scores = cosine_similarity(query_emb, chunk_embeddings)[0]
        top_idx = np.argsort(scores)[::-1][:k]
        return top_idx, scores[top_idx]

    def calculate_hit_rate(self, ground_truth_id: int, retrieved_ids: List[int], top_k: int = 3) -> float:
        """
        Tính toán xem ground_truth_id có nằm trong top_k của retrieved_ids không.
        """
        top_retrieved = retrieved_ids[:top_k]
        hit = ground_truth_id in top_retrieved
        return 1.0 if hit else 0.0

    def calculate_mrr(self, ground_truth_id: int, retrieved_ids: List[int]) -> float:
        """
        Tính Mean Reciprocal Rank cho ground_truth_id trong retrieved_ids.
        """
        for i, idx in enumerate(retrieved_ids):
            if idx == ground_truth_id:
                return 1.0 / (i + 1)
        return 0.0

    def evaluate_retrieval(self, golden_set: List[Dict], chunks: List[str], chunk_embeddings: np.ndarray, k: int = 3) -> Dict:
        """
        Đánh giá toàn bộ bộ test: tính hit rate và mrr trung bình.
        """
        hits = []
        mrrs = []
        for qa in golden_set:
            top_idx, _ = self.retrieve_top_k(qa["question"], chunks, chunk_embeddings, k)
            top_idx = list(top_idx)
            hit = self.calculate_hit_rate(qa["ground_truth_id"], top_idx, k)
            mrr = self.calculate_mrr(qa["ground_truth_id"], top_idx)
            hits.append(hit)
            mrrs.append(mrr)
        hit_rate = np.mean(hits)
        mean_mrr = np.mean(mrrs)
        return {"hit_rate": hit_rate, "mrr": mean_mrr}
