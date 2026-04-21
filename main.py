import asyncio
import json
import os
import sys
import time

from engine.runner import BenchmarkRunner
from engine.llm_judge import LLMJudge
from engine.retrieval_eval import RetrievalEvaluator
from agent.main_agent import MainAgent, MainAgentV2


# ---------------------------------------------------------------------------
# ExpertEvaluator – replaces the stub from the original template.
# Wraps RetrievalEvaluator to provide RAGAS-style faithfulness/relevancy
# scores alongside real Hit Rate & MRR.
# ---------------------------------------------------------------------------
class ExpertEvaluator:
    def __init__(self):
        self._retrieval = RetrievalEvaluator(top_k=3)

    async def score(self, case: dict, resp: dict) -> dict:
        expected_ids = case.get("expected_retrieval_ids", [])
        retrieved_ids = resp.get("retrieved_ids", [])

        # Retrieval metrics
        hit_rate = self._retrieval.calculate_hit_rate(expected_ids, retrieved_ids)
        mrr = self._retrieval.calculate_mrr(expected_ids, retrieved_ids)

        # Lightweight faithfulness: word overlap between answer and retrieved contexts
        answer_words = set(resp.get("answer", "").lower().split())
        context_text = " ".join(resp.get("contexts", [])).lower()
        context_words = set(context_text.split())
        if answer_words:
            faithfulness = min(1.0, len(answer_words & context_words) / len(answer_words) * 1.5)
        else:
            faithfulness = 0.0

        # Lightweight relevancy: overlap between answer and question
        q_words = set(case.get("question", "").lower().split())
        if q_words:
            relevancy = min(1.0, len(answer_words & q_words) / len(q_words) * 2.0)
        else:
            relevancy = 0.5

        return {
            "faithfulness": round(faithfulness, 4),
            "relevancy": round(relevancy, 4),
            "retrieval": {"hit_rate": hit_rate, "mrr": mrr},
        }


# ---------------------------------------------------------------------------
# MultiModelJudge – replaces the stub from the original template.
# Wraps LLMJudge with 2 OpenAI models for consensus scoring.
# ---------------------------------------------------------------------------
class MultiModelJudge:
    def __init__(self):
        self._judge = LLMJudge(models=["gpt-4o", "gpt-4o-mini"])

    async def evaluate_multi_judge(self, question: str, answer: str, ground_truth: str) -> dict:
        return await self._judge.evaluate_multi_judge(question, answer, ground_truth)


# ---------------------------------------------------------------------------
# Benchmark runner – signature matches original template
# ---------------------------------------------------------------------------
async def run_benchmark_with_results(agent_version: str):
    print(f"\n{'='*60}")
    print(f"BENCHMARK: {agent_version}")
    print(f"{'='*60}")

    if not os.path.exists("data/golden_set.jsonl"):
        print("❌ Thiếu data/golden_set.jsonl. Hãy chạy 'python data/synthetic_gen.py' trước.")
        return None, None

    with open("data/golden_set.jsonl", "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f if line.strip()]

    if not dataset:
        print("❌ File data/golden_set.jsonl rỗng. Hãy tạo ít nhất 1 test case.")
        return None, None

    print(f"\n[1/4] Loaded {len(dataset)} test cases")

    # Pick agent based on version string
    print("\n[2/4] Initializing components...")
    agent = MainAgentV2() if "V2" in agent_version or "v2" in agent_version else MainAgent()

    runner = BenchmarkRunner(agent, ExpertEvaluator(), MultiModelJudge())

    print("\n[3/4] Running benchmark...")
    start = time.perf_counter()
    results = await runner.run_all(dataset, batch_size=5, show_progress=True)
    elapsed = time.perf_counter() - start

    print("\n[4/4] Generating summary...")
    stats = runner.get_summary_stats(results)
    total = len(results)

    summary = {
        "metadata": {
            "version": agent_version,
            "total": total,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "execution_time_seconds": round(elapsed, 2),
        },
        "metrics": {
            "avg_score": stats["avg_score"],
            "hit_rate": stats["retrieval"]["avg_hit_rate"],
            "mrr": stats["retrieval"]["avg_mrr"],
            "agreement_rate": stats["avg_agreement_rate"],
            "pass_rate": stats["pass_rate"],
            "faithfulness": stats["ragas"]["avg_faithfulness"],
            "relevancy": stats["ragas"]["avg_relevancy"],
        },
        "performance": {
            "total_time_seconds": round(elapsed, 2),
            "avg_latency_ms": stats["latency"]["avg_ms"],
            "total_tokens": stats["tokens"]["total"],
            "estimated_cost_usd": stats["cost"]["estimated_usd"],
        },
        "breakdown": {
            "passed": stats["passed"],
            "failed": stats["failed"],
            "errors": stats["errors"],
        },
    }
    return results, summary


async def run_benchmark(version: str):
    _, summary = await run_benchmark_with_results(version)
    return summary


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
async def main():
    # Run V1 (template-based agent)
    v1_results, v1_summary = await run_benchmark_with_results("Agent_V1_Base")

    # Run V2 (LLM-powered agent)
    v2_results, v2_summary = await run_benchmark_with_results("Agent_V2_Optimized")

    if not v1_summary or not v2_summary or not v1_results or not v2_results:
        print("❌ Không thể chạy Benchmark. Kiểm tra lại data/golden_set.jsonl.")
        return

    # --- Regression Analysis ---
    print("\n📊 --- KẾT QUẢ SO SÁNH (REGRESSION) ---")
    delta = v2_summary["metrics"]["avg_score"] - v1_summary["metrics"]["avg_score"]
    delta_hit = v2_summary["metrics"]["hit_rate"] - v1_summary["metrics"]["hit_rate"]

    print(f"{'Metric':<25} {'V1':>10} {'V2':>10} {'Delta':>10}")
    print("-" * 55)
    print(f"{'Avg Score':<25} {v1_summary['metrics']['avg_score']:>10.2f} {v2_summary['metrics']['avg_score']:>10.2f} {delta:>+10.2f}")
    print(f"{'Hit Rate':<25} {v1_summary['metrics']['hit_rate']:>10.2%} {v2_summary['metrics']['hit_rate']:>10.2%} {delta_hit:>+10.2%}")
    print(f"{'Pass Rate':<25} {v1_summary['metrics']['pass_rate']:>9.1f}% {v2_summary['metrics']['pass_rate']:>9.1f}%")
    print(f"{'Agreement Rate':<25} {v1_summary['metrics']['agreement_rate']:>10.2f} {v2_summary['metrics']['agreement_rate']:>10.2f}")

    # --- Release Gate ---
    v1_cost = v1_summary["performance"]["estimated_cost_usd"]
    v2_cost = v2_summary["performance"]["estimated_cost_usd"]
    cost_ratio = (v2_cost - v1_cost) / v1_cost if v1_cost > 0 else 0

    quality_pass = delta >= 0.0
    retrieval_pass = delta_hit >= -0.05
    cost_pass = cost_ratio <= 0.30

    v2_summary["regression"] = {
        "v1_score": v1_summary["metrics"]["avg_score"],
        "v2_score": v2_summary["metrics"]["avg_score"],
        "delta": round(delta, 4),
        "decision": "APPROVE" if (quality_pass and retrieval_pass and cost_pass) else "BLOCK",
        "gates": {
            "quality_pass": quality_pass,
            "retrieval_pass": retrieval_pass,
            "cost_pass": cost_pass,
        },
    }

    print(f"\n{'='*55}")
    print("RELEASE GATE:")
    print(f"  [{'✅' if quality_pass else '❌'}] Quality delta >= 0   (actual: {delta:+.2f})")
    print(f"  [{'✅' if retrieval_pass else '❌'}] Hit Rate delta >= -5% (actual: {delta_hit:+.2%})")
    print(f"  [{'✅' if cost_pass else '❌'}] Cost increase <= 30%  (actual: {cost_ratio:+.1%})")

    decision = v2_summary["regression"]["decision"]
    print(f"\n{'✅' if decision == 'APPROVE' else '❌'} QUYẾT ĐỊNH: {decision}")
    print("=" * 55)

    # --- Save reports ---
    os.makedirs("reports", exist_ok=True)
    with open("reports/summary.json", "w", encoding="utf-8") as f:
        json.dump(v2_summary, f, ensure_ascii=False, indent=2)
    with open("reports/benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(v2_results, f, ensure_ascii=False, indent=2)
    with open("reports/v1_results.json", "w", encoding="utf-8") as f:
        json.dump({"summary": v1_summary, "results": v1_results}, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Saved: reports/summary.json")
    print(f"✅ Saved: reports/benchmark_results.json")
    print(f"✅ Saved: reports/v1_results.json")
    print("\nNext: python check_lab.py")


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
