from typing import List, Dict
import statistics

class RetrievalEvaluator:
    """
    Evaluator for retrieval quality metrics.
    Calculates Hit Rate and MRR (Mean Reciprocal Rank).
    """

    def __init__(self, top_k: int = 3):
        self.top_k = top_k

    def calculate_hit_rate(self, expected_ids: List[str], retrieved_ids: List[str], top_k: int = None) -> float:
        """
        Tính toán xem ít nhất 1 trong expected_ids có nằm trong top_k của retrieved_ids không.

        Args:
            expected_ids: List of ground truth document IDs
            retrieved_ids: List of retrieved document IDs (ordered by relevance)
            top_k: Number of top results to consider

        Returns:
            1.0 if at least one expected doc is in top_k, else 0.0
        """
        if not expected_ids:
            return 0.0  # No expected docs means we can't evaluate

        k = top_k or self.top_k
        top_retrieved = retrieved_ids[:k]
        hit = any(doc_id in top_retrieved for doc_id in expected_ids)
        return 1.0 if hit else 0.0

    def calculate_mrr(self, expected_ids: List[str], retrieved_ids: List[str]) -> float:
        """
        Tính Mean Reciprocal Rank.
        Tìm vị trí đầu tiên của một expected_id trong retrieved_ids.
        MRR = 1 / position (vị trí 1-indexed). Nếu không thấy thì là 0.

        Args:
            expected_ids: List of ground truth document IDs
            retrieved_ids: List of retrieved document IDs (ordered by relevance)

        Returns:
            1/position of first match, or 0.0 if no match
        """
        if not expected_ids:
            return 0.0

        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in expected_ids:
                return 1.0 / (i + 1)
        return 0.0

    def calculate_precision_at_k(self, expected_ids: List[str], retrieved_ids: List[str], k: int = None) -> float:
        """
        Calculate Precision@K: proportion of relevant docs in top-k.

        Args:
            expected_ids: List of ground truth document IDs
            retrieved_ids: List of retrieved document IDs
            k: Number of top results to consider

        Returns:
            Precision score between 0.0 and 1.0
        """
        if not expected_ids or not retrieved_ids:
            return 0.0

        k = k or self.top_k
        top_k_retrieved = retrieved_ids[:k]
        relevant_in_top_k = sum(1 for doc_id in top_k_retrieved if doc_id in expected_ids)
        return relevant_in_top_k / k

    def calculate_recall_at_k(self, expected_ids: List[str], retrieved_ids: List[str], k: int = None) -> float:
        """
        Calculate Recall@K: proportion of relevant docs that are retrieved in top-k.

        Args:
            expected_ids: List of ground truth document IDs
            retrieved_ids: List of retrieved document IDs
            k: Number of top results to consider

        Returns:
            Recall score between 0.0 and 1.0
        """
        if not expected_ids:
            return 0.0

        k = k or self.top_k
        top_k_retrieved = retrieved_ids[:k]
        relevant_retrieved = sum(1 for doc_id in expected_ids if doc_id in top_k_retrieved)
        return relevant_retrieved / len(expected_ids)

    async def evaluate_single(self, test_case: Dict, agent_response: Dict) -> Dict:
        """
        Evaluate a single test case.

        Args:
            test_case: Dict with 'expected_retrieval_ids'
            agent_response: Dict with 'retrieved_ids'

        Returns:
            Dict with hit_rate, mrr, precision, recall
        """
        expected_ids = test_case.get("expected_retrieval_ids", [])
        retrieved_ids = agent_response.get("retrieved_ids", [])

        return {
            "hit_rate": self.calculate_hit_rate(expected_ids, retrieved_ids),
            "mrr": self.calculate_mrr(expected_ids, retrieved_ids),
            "precision_at_k": self.calculate_precision_at_k(expected_ids, retrieved_ids),
            "recall_at_k": self.calculate_recall_at_k(expected_ids, retrieved_ids),
            "expected_ids": expected_ids,
            "retrieved_ids": retrieved_ids[:self.top_k]
        }

    async def evaluate_batch(self, dataset: List[Dict], agent_responses: List[Dict] = None) -> Dict:
        """
        Chạy eval cho toàn bộ bộ dữ liệu.
        Dataset cần có trường 'expected_retrieval_ids' và 'retrieved_ids' (từ agent response).

        Args:
            dataset: List of test cases with expected_retrieval_ids
            agent_responses: Optional list of agent responses with retrieved_ids

        Returns:
            Dict with average metrics and detailed results
        """
        hit_rates = []
        mrrs = []
        precisions = []
        recalls = []
        detailed_results = []

        for i, case in enumerate(dataset):
            expected_ids = case.get("expected_retrieval_ids", [])

            # Get retrieved_ids from agent_responses if provided, else from case
            if agent_responses and i < len(agent_responses):
                retrieved_ids = agent_responses[i].get("retrieved_ids", [])
            else:
                retrieved_ids = case.get("retrieved_ids", [])

            hit_rate = self.calculate_hit_rate(expected_ids, retrieved_ids)
            mrr = self.calculate_mrr(expected_ids, retrieved_ids)
            precision = self.calculate_precision_at_k(expected_ids, retrieved_ids)
            recall = self.calculate_recall_at_k(expected_ids, retrieved_ids)

            hit_rates.append(hit_rate)
            mrrs.append(mrr)
            precisions.append(precision)
            recalls.append(recall)

            detailed_results.append({
                "case_index": i,
                "question": case.get("question", "")[:50],
                "hit_rate": hit_rate,
                "mrr": mrr,
                "precision": precision,
                "recall": recall,
                "expected": expected_ids,
                "retrieved": retrieved_ids[:5]
            })

        # Calculate statistics
        n = len(hit_rates)
        avg_hit_rate = sum(hit_rates) / n if n > 0 else 0
        avg_mrr = sum(mrrs) / n if n > 0 else 0
        avg_precision = sum(precisions) / n if n > 0 else 0
        avg_recall = sum(recalls) / n if n > 0 else 0

        # Calculate additional stats
        hit_rate_std = statistics.stdev(hit_rates) if n > 1 else 0
        mrr_std = statistics.stdev(mrrs) if n > 1 else 0

        return {
            "avg_hit_rate": round(avg_hit_rate, 4),
            "avg_mrr": round(avg_mrr, 4),
            "avg_precision": round(avg_precision, 4),
            "avg_recall": round(avg_recall, 4),
            "hit_rate_std": round(hit_rate_std, 4),
            "mrr_std": round(mrr_std, 4),
            "total_cases": n,
            "perfect_retrieval_count": sum(1 for hr in hit_rates if hr == 1.0),
            "zero_retrieval_count": sum(1 for hr in hit_rates if hr == 0.0),
            "top_k": self.top_k,
            "detailed_results": detailed_results
        }

    def get_failure_analysis(self, eval_results: Dict) -> Dict:
        """
        Analyze retrieval failures for debugging.

        Args:
            eval_results: Results from evaluate_batch

        Returns:
            Dict with failure analysis
        """
        detailed = eval_results.get("detailed_results", [])
        failures = [r for r in detailed if r["hit_rate"] == 0.0]
        partial = [r for r in detailed if 0 < r["hit_rate"] < 1.0]

        return {
            "total_failures": len(failures),
            "total_partial": len(partial),
            "failure_rate": len(failures) / len(detailed) if detailed else 0,
            "failed_questions": [f["question"] for f in failures[:10]],
            "recommendations": self._generate_recommendations(failures, eval_results)
        }

    def _generate_recommendations(self, failures: List[Dict], eval_results: Dict) -> List[str]:
        """Generate improvement recommendations based on failures."""
        recommendations = []

        avg_mrr = eval_results.get("avg_mrr", 0)
        avg_hit_rate = eval_results.get("avg_hit_rate", 0)

        if avg_hit_rate < 0.7:
            recommendations.append("Hit Rate thấp (<70%): Cần cải thiện chunking strategy hoặc embedding model")

        if avg_mrr < 0.5:
            recommendations.append("MRR thấp (<0.5): Documents đúng không được rank cao. Cân nhắc thêm Reranking step")

        if len(failures) > eval_results.get("total_cases", 1) * 0.3:
            recommendations.append("Tỷ lệ failure cao (>30%): Review lại indexing pipeline và document coverage")

        if not recommendations:
            recommendations.append("Retrieval performance tốt. Tiếp tục monitor và fine-tune thresholds")

        return recommendations

# For testing
if __name__ == "__main__":
    import asyncio

    async def test():
        evaluator = RetrievalEvaluator(top_k=3)

        # Test cases
        test_data = [
            {
                "question": "RAG là gì?",
                "expected_retrieval_ids": ["doc_rag_01"],
                "retrieved_ids": ["doc_rag_01", "doc_vector_01", "doc_eval_01"]
            },
            {
                "question": "Vector database",
                "expected_retrieval_ids": ["doc_vector_01"],
                "retrieved_ids": ["doc_chunking_01", "doc_rag_01", "doc_vector_01"]
            },
            {
                "question": "Unknown topic",
                "expected_retrieval_ids": ["doc_unknown"],
                "retrieved_ids": ["doc_rag_01", "doc_vector_01"]
            }
        ]

        results = await evaluator.evaluate_batch(test_data)
        print("Evaluation Results:")
        print(f"  Avg Hit Rate: {results['avg_hit_rate']}")
        print(f"  Avg MRR: {results['avg_mrr']}")
        print(f"  Perfect Retrievals: {results['perfect_retrieval_count']}/{results['total_cases']}")

        failure_analysis = evaluator.get_failure_analysis(results)
        print("\nFailure Analysis:")
        print(f"  Total Failures: {failure_analysis['total_failures']}")
        print(f"  Recommendations: {failure_analysis['recommendations']}")

    asyncio.run(test())
