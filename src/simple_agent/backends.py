import asyncio
import re
from dataclasses import dataclass
from typing import Protocol

from simple_agent.config import Settings
from simple_agent.prompt_registry import load_runtime_prompt
from simple_agent.tools import classify_price_tier_json


@dataclass(frozen=True)
class AgentResult:
    answer: str
    tool_calls: int
    prompt_version: int | None = None
    model_name: str | None = None


class AgentBackend(Protocol):
    async def invoke(self, message: str) -> AgentResult: ...


_PRICE_RE = re.compile(r"\$?\s*(\d+(?:\.\d+)?)")


class FakeAgentBackend:
    async def invoke(self, message: str) -> AgentResult:
        await asyncio.sleep(0)
        prices = [float(x) for x in _PRICE_RE.findall(message)]
        if not prices:
            return AgentResult(
                answer="Please provide a nightly price so I can classify the market tier.",
                tool_calls=0,
            )
        import json
        rows = [json.loads(classify_price_tier_json(price)) for price in prices]
        if len(rows) == 1:
            row = rows[0]
            answer = (
                f"${row['price']:.0f}/night is {row['tier']} "
                f"({row['percentile_band']}). {row['interpretation']}"
            )
        else:
            answer = "; ".join(
                f"${row['price']:.0f}: {row['tier']} ({row['percentile_band']})" for row in rows
            )
        return AgentResult(answer=answer, tool_calls=len(rows))


class DatabricksAgentBackend:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def invoke(self, message: str) -> AgentResult:
        try:
            import mlflow
            from agents import Agent, Runner, set_default_openai_api, set_default_openai_client
            from agents.tracing import set_trace_processors
            from databricks_openai import AsyncDatabricksOpenAI
            from databricks_openai.agents import McpServer
        except ImportError as exc:
            raise RuntimeError(
                'Databricks dependencies missing. Install: pip install -e ".[databricks]"'
            ) from exc

        resolved_prompt = load_runtime_prompt(self.settings)
        mlflow.set_experiment(self.settings.mlflow_experiment_name)
        mlflow.openai.autolog()

        set_default_openai_client(AsyncDatabricksOpenAI())
        set_default_openai_api("chat_completions")
        set_trace_processors([])

        catalog, schema, function_name = self.settings.uc_function_full_name.split(".", 2)
        mcp_server = McpServer.from_uc_function(
            catalog=catalog,
            schema=schema,
            function_name=function_name,
            timeout=self.settings.request_timeout_seconds,
        )

        # Model and instructions are resolved at runtime from versioned registry/config.
        agent = Agent(
            name="SF Pricing Analyst",
            instructions=resolved_prompt.template,
            model=str(resolved_prompt.model_config["model_name"]),
            mcp_servers=[mcp_server],
        )

        async with mcp_server:
            result = await Runner.run(agent, message)

        tool_calls = sum(
            1 for item in getattr(result, "new_items", [])
            if "tool" in type(item).__name__.lower()
        )
        return AgentResult(
            answer=str(result.final_output),
            tool_calls=tool_calls,
            prompt_version=resolved_prompt.version,
            model_name=str(resolved_prompt.model_config["model_name"]),
        )


def build_backend(settings: Settings) -> AgentBackend:
    return DatabricksAgentBackend(settings) if settings.agent_backend == "databricks" else FakeAgentBackend()
