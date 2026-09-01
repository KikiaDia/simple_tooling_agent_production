from dataclasses import dataclass


@dataclass(frozen=True)
class EvalScore:
    tool_correct: bool
    answer_correct: bool


def score_example(
    *,
    answer: str,
    tool_calls: int,
    expected_tiers: list[str],
    expected_tool_calls: int,
) -> EvalScore:
    return EvalScore(
        tool_correct=tool_calls == expected_tool_calls,
        answer_correct=all(tier in answer for tier in expected_tiers),
    )
