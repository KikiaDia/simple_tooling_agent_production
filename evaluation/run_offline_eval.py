import asyncio
import json
import statistics
import sys
import time
from pathlib import Path

from simple_agent.backends import build_backend
from simple_agent.config import get_settings
from simple_agent.service import AgentService

from scorers import score_example


async def main() -> int:
    settings = get_settings()
    service = AgentService(build_backend(settings), settings.request_timeout_seconds)

    dataset_path = Path(__file__).with_name("golden_dataset.json")
    cases = json.loads(dataset_path.read_text())

    tool_scores: list[float] = []
    answer_scores: list[float] = []
    latencies: list[float] = []
    rows = []

    for case in cases:
        started = time.perf_counter()
        result = await service.ask(case["input"])
        latency_ms = (time.perf_counter() - started) * 1000

        score = score_example(
            answer=result.answer,
            tool_calls=result.tool_calls,
            expected_tiers=case["expected_tiers"],
            expected_tool_calls=case["expected_tool_calls"],
        )

        tool_scores.append(float(score.tool_correct))
        answer_scores.append(float(score.answer_correct))
        latencies.append(latency_ms)
        rows.append(
            {
                "id": case["id"],
                "tool_correct": score.tool_correct,
                "answer_correct": score.answer_correct,
                "latency_ms": round(latency_ms, 2),
                "answer": result.answer,
            }
        )

    tool_correctness = statistics.fmean(tool_scores)
    answer_correctness = statistics.fmean(answer_scores)
    ordered = sorted(latencies)
    p95_idx = max(0, min(len(ordered) - 1, int(round(0.95 * (len(ordered) - 1)))))
    p95_latency_ms = ordered[p95_idx]

    report = {
        "tool_correctness": tool_correctness,
        "answer_correctness": answer_correctness,
        "p95_latency_ms": p95_latency_ms,
        "cases": rows,
    }

    results_dir = Path(__file__).with_name("results")
    results_dir.mkdir(exist_ok=True)
    output = results_dir / "offline_eval.json"
    output.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))

    failed = []
    if tool_correctness < settings.min_tool_correctness:
        failed.append(
            f"tool_correctness={tool_correctness:.3f} < {settings.min_tool_correctness:.3f}"
        )
    if answer_correctness < settings.min_answer_correctness:
        failed.append(
            f"answer_correctness={answer_correctness:.3f} < {settings.min_answer_correctness:.3f}"
        )
    if p95_latency_ms > settings.max_p95_latency_ms:
        failed.append(
            f"p95_latency_ms={p95_latency_ms:.1f} > {settings.max_p95_latency_ms:.1f}"
        )

    if failed:
        print("\nQUALITY GATE FAILED:")
        for reason in failed:
            print(f" - {reason}")
        return 1

    print("\nQUALITY GATE PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
