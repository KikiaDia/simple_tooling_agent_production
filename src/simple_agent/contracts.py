from pydantic import BaseModel, Field


class InvocationRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10_000)
    session_id: str | None = None


class InvocationResponse(BaseModel):
    answer: str
    request_id: str
    backend: str
    tool_calls: int = 0
    latency_ms: float
    release_id: str
    prompt_version: int | None = None
    model_name: str | None = None


class HealthResponse(BaseModel):
    status: str
    environment: str
    release_id: str
