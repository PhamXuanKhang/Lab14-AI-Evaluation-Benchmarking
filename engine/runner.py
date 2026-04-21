import asyncio
import time
from typing import List, Dict, Any
from tqdm.asyncio import tqdm_asyncio

class BenchmarkRunner:
    """
    Async Benchmark Runner for AI Evaluation.
    Runs tests in parallel batches to optimize throughput while respecting rate limits.
    """

    def __init__(self, agent, evaluator, judge, retrieval_evaluator=None):
        """
        Args:
            agent: The AI agent to benchmark
            evaluator: RAGAS or custom evaluator for response quality
            judge: LLM Judge for multi-model consensus scoring
            retrieval_evaluator: Optional retrieval metrics evaluator
        """
        self.agent = agent
        self.evaluator = evaluator
        self.judge = judge
        self.retrieval_evaluator = retrieval_evaluator

        # Performance tracking
        self.total_tokens = 0
        self.total_latency = 0
        self.test_count = 0

    async def run_single_test(self, test_case: Dict, test_index: int = 0) -> Dict:
        """
        Run a single test case through the full evaluation pipeline.

        Args:
            test_case: Dict containing question, expected_answer, context, etc.
            test_index: Index for tracking

        Returns:
            Dict with complete test results
        """
        start_time = time.perf_counter()

        try:
            # 1. Call Agent
            response = await self.agent.query(test_case["question"])
            agent_latency = time.perf_counter() - start_time

            # 2. Run RAGAS/Custom metrics
            ragas_start = time.perf_counter()
            ragas_scores = await self.evaluator.score(test_case, response)
            ragas_latency = time.perf_counter() - ragas_start

            # 3. Run Retrieval Evaluation (if available)
            retrieval_metrics = {}
            if self.retrieval_evaluator:
                expected_ids = test_case.get("expected_retrieval_ids", [])
                retrieved_ids = response.get("retrieved_ids", [])
                retrieval_metrics = {
                    "hit_rate": self.retrieval_evaluator.calculate_hit_rate(expected_ids, retrieved_ids),
                    "mrr": self.retrieval_evaluator.calculate_mrr(expected_ids, retrieved_ids)
                }
                ragas_scores["retrieval"] = retrieval_metrics

            # 4. Run Multi-Judge
            judge_start = time.perf_counter()
            judge_result = await self.judge.evaluate_multi_judge(
                test_case["question"],
                response["answer"],
                test_case["expected_answer"]
            )
            judge_latency = time.perf_counter() - judge_start

            # Calculate total latency
            total_latency = time.perf_counter() - start_time

            # Track tokens
            agent_tokens = response.get("metadata", {}).get("tokens_used", 0)
            judge_tokens = judge_result.get("tokens_used", 0)
            total_tokens = agent_tokens + judge_tokens

            # Update totals
            self.total_tokens += total_tokens
            self.total_latency += total_latency
            self.test_count += 1

            # Determine pass/fail
            final_score = judge_result["final_score"]
            status = "pass" if final_score >= 3.0 else "fail"

            return {
                "test_index": test_index,
                "test_case": test_case["question"],
                "expected_answer": test_case["expected_answer"][:200],
                "agent_response": response["answer"],
                "retrieved_ids": response.get("retrieved_ids", []),
                "expected_retrieval_ids": test_case.get("expected_retrieval_ids", []),
                "latency": {
                    "total": round(total_latency, 3),
                    "agent": round(agent_latency, 3),
                    "ragas": round(ragas_latency, 3),
                    "judge": round(judge_latency, 3)
                },
                "ragas": ragas_scores,
                "judge": judge_result,
                "tokens": {
                    "agent": agent_tokens,
                    "judge": judge_tokens,
                    "total": total_tokens
                },
                "status": status,
                "metadata": test_case.get("metadata", {})
            }

        except Exception as e:
            total_latency = time.perf_counter() - start_time
            return {
                "test_index": test_index,
                "test_case": test_case["question"],
                "error": str(e),
                "latency": {"total": round(total_latency, 3)},
                "status": "error",
                "judge": {"final_score": 0, "agreement_rate": 0},
                "ragas": {"faithfulness": 0, "relevancy": 0, "retrieval": {"hit_rate": 0, "mrr": 0}}
            }

    async def run_all(
        self,
        dataset: List[Dict],
        batch_size: int = 5,
        show_progress: bool = True
    ) -> List[Dict]:
        """
        Chạy song song bằng asyncio.gather với giới hạn batch_size để không bị Rate Limit.

        Args:
            dataset: List of test cases
            batch_size: Number of concurrent tests per batch
            show_progress: Whether to show progress bar

        Returns:
            List of test results
        """
        results = []
        total_batches = (len(dataset) + batch_size - 1) // batch_size

        print(f"\nRunning {len(dataset)} tests in {total_batches} batches (batch_size={batch_size})")

        for i in range(0, len(dataset), batch_size):
            batch = dataset[i:i + batch_size]
            batch_num = i // batch_size + 1

            if show_progress:
                print(f"  Batch {batch_num}/{total_batches}...", end=" ")

            batch_start = time.perf_counter()

            # Create tasks with indices
            tasks = [
                self.run_single_test(case, idx)
                for idx, case in enumerate(batch, start=i)
            ]

            # Run batch in parallel
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)

            batch_time = time.perf_counter() - batch_start

            if show_progress:
                passed = sum(1 for r in batch_results if r.get("status") == "pass")
                print(f"Done ({passed}/{len(batch)} passed, {batch_time:.2f}s)")

            # Small delay between batches to avoid rate limits
            if i + batch_size < len(dataset):
                await asyncio.sleep(0.5)

        return results

    def get_summary_stats(self, results: List[Dict]) -> Dict:
        """
        Calculate summary statistics from benchmark results.

        Args:
            results: List of test results from run_all

        Returns:
            Dict with summary statistics
        """
        total = len(results)
        if total == 0:
            return {"error": "No results to summarize"}

        # Count statuses
        passed = sum(1 for r in results if r.get("status") == "pass")
        failed = sum(1 for r in results if r.get("status") == "fail")
        errors = sum(1 for r in results if r.get("status") == "error")

        # Calculate averages
        valid_results = [r for r in results if r.get("status") != "error"]

        avg_score = sum(r["judge"]["final_score"] for r in valid_results) / len(valid_results) if valid_results else 0
        avg_agreement = sum(r["judge"]["agreement_rate"] for r in valid_results) / len(valid_results) if valid_results else 0

        # Retrieval metrics
        retrieval_results = [r for r in valid_results if "retrieval" in r.get("ragas", {})]
        avg_hit_rate = sum(r["ragas"]["retrieval"]["hit_rate"] for r in retrieval_results) / len(retrieval_results) if retrieval_results else 0
        avg_mrr = sum(r["ragas"]["retrieval"]["mrr"] for r in retrieval_results) / len(retrieval_results) if retrieval_results else 0

        # RAGAS metrics
        avg_faithfulness = sum(r["ragas"].get("faithfulness", 0) for r in valid_results) / len(valid_results) if valid_results else 0
        avg_relevancy = sum(r["ragas"].get("relevancy", 0) for r in valid_results) / len(valid_results) if valid_results else 0

        # Latency stats
        latencies = [r["latency"]["total"] for r in valid_results if "latency" in r]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        max_latency = max(latencies) if latencies else 0
        min_latency = min(latencies) if latencies else 0

        # Token stats
        total_tokens = sum(r.get("tokens", {}).get("total", 0) for r in valid_results)

        # Cost estimation (based on GPT-4o-mini pricing: $0.15/1M input, $0.6/1M output)
        estimated_cost = (total_tokens / 1_000_000) * 0.4  # Rough average

        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "pass_rate": round(passed / total * 100, 1),
            "avg_score": round(avg_score, 2),
            "avg_agreement_rate": round(avg_agreement, 2),
            "retrieval": {
                "avg_hit_rate": round(avg_hit_rate, 4),
                "avg_mrr": round(avg_mrr, 4)
            },
            "ragas": {
                "avg_faithfulness": round(avg_faithfulness, 4),
                "avg_relevancy": round(avg_relevancy, 4)
            },
            "latency": {
                "avg_ms": round(avg_latency * 1000, 1),
                "max_ms": round(max_latency * 1000, 1),
                "min_ms": round(min_latency * 1000, 1),
                "total_s": round(sum(latencies), 2)
            },
            "tokens": {
                "total": total_tokens,
                "avg_per_test": round(total_tokens / total, 1) if total > 0 else 0
            },
            "cost": {
                "estimated_usd": round(estimated_cost, 4),
                "per_test_usd": round(estimated_cost / total, 6) if total > 0 else 0
            }
        }

    def get_failure_details(self, results: List[Dict]) -> List[Dict]:
        """
        Extract details of failed tests for analysis.

        Args:
            results: List of test results

        Returns:
            List of failed test details
        """
        failures = []
        for r in results:
            if r.get("status") in ["fail", "error"]:
                failures.append({
                    "index": r.get("test_index"),
                    "question": r.get("test_case", "")[:100],
                    "score": r.get("judge", {}).get("final_score", 0),
                    "status": r.get("status"),
                    "error": r.get("error"),
                    "metadata": r.get("metadata", {}),
                    "retrieval_hit": r.get("ragas", {}).get("retrieval", {}).get("hit_rate", 0)
                })
        return failures


# For testing
if __name__ == "__main__":
    from agent.main_agent import MainAgent
    from engine.llm_judge import LLMJudge
    from engine.retrieval_eval import RetrievalEvaluator

    class MockEvaluator:
        async def score(self, case, response):
            return {"faithfulness": 0.8, "relevancy": 0.75}

    async def test():
        agent = MainAgent()
        evaluator = MockEvaluator()
        judge = LLMJudge()
        retrieval_eval = RetrievalEvaluator()

        runner = BenchmarkRunner(agent, evaluator, judge, retrieval_eval)

        test_data = [
            {
                "question": "RAG là gì?",
                "expected_answer": "RAG là Retrieval-Augmented Generation.",
                "expected_retrieval_ids": ["doc_rag_01"]
            }
        ]

        results = await runner.run_all(test_data, batch_size=1)
        summary = runner.get_summary_stats(results)

        print("\nSummary:")
        print(f"  Pass Rate: {summary['pass_rate']}%")
        print(f"  Avg Score: {summary['avg_score']}")

    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test())
