from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: Literal["local", "dev", "staging", "prod"] = "local"
    agent_backend: Literal["fake", "databricks"] = "fake"

    # Runtime coordinates: no prompt/model choice is hard-coded in agent logic.
    prompt_name: str = "main.genai.sf_pricing_agent"
    prompt_ref: str = "dev"  # alias (dev/staging/production) or explicit integer version
    model_endpoint: str = "databricks-llama-4-maverick"
    model_type: str = "chat"
    model_temperature: float = Field(default=0.0, ge=0, le=2)
    model_max_tokens: int = Field(default=800, gt=0)

    uc_function_full_name: str = "main.genai.classify_price_tier_uc"
    mlflow_experiment_name: str = "/Shared/simple-tool-agent"
    eval_dataset_name: str = "main.genai.simple_tool_agent_eval"
    eval_dataset_digest: str | None = None

    release_id: str = "local"
    git_sha: str = "local"
    artifact_digest: str | None = None
    dependency_lock_digest: str | None = None

    request_timeout_seconds: float = Field(default=30.0, gt=0)
    max_request_chars: int = Field(default=10_000, gt=0)

    min_tool_correctness: float = Field(default=0.95, ge=0, le=1)
    min_answer_correctness: float = Field(default=0.90, ge=0, le=1)
    max_p95_latency_ms: float = Field(default=8_000.0, gt=0)


@lru_cache
def get_settings() -> Settings:
    return Settings()
