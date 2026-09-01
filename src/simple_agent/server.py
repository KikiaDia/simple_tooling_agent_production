import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from simple_agent.backends import build_backend
from simple_agent.config import get_settings
from simple_agent.contracts import HealthResponse, InvocationRequest, InvocationResponse
from simple_agent.observability import log_event
from simple_agent.service import AgentService

settings = get_settings()
service = AgentService(
    backend=build_backend(settings),
    timeout_seconds=settings.request_timeout_seconds,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    log_event("app_started", environment=settings.environment, backend=settings.agent_backend)
    yield
    log_event("app_stopped")


app = FastAPI(
    title="Simple Tool-Calling Agent",
    version="0.1.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        log_event("request_failed", request_id=request_id, path=request.url.path)
        raise
    latency_ms = (time.perf_counter() - started) * 1000
    response.headers["x-request-id"] = request_id
    log_event(
        "request_completed",
        request_id=request_id,
        path=request.url.path,
        status=response.status_code,
        latency_ms=round(latency_ms, 2),
    )
    return response


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", environment=settings.environment, release_id=settings.release_id)


@app.get("/ready", response_model=HealthResponse)
def ready() -> HealthResponse:
    return HealthResponse(status="ready", environment=settings.environment, release_id=settings.release_id)


@app.post("/invocations", response_model=InvocationResponse)
async def invocations(payload: InvocationRequest, request: Request) -> InvocationResponse:
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    started = time.perf_counter()

    if len(payload.message) > settings.max_request_chars:
        raise HTTPException(status_code=413, detail="request too large")

    try:
        result = await service.ask(payload.message)
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail="agent timeout") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    latency_ms = (time.perf_counter() - started) * 1000
    return InvocationResponse(
        answer=result.answer,
        request_id=request_id,
        backend=settings.agent_backend,
        tool_calls=result.tool_calls,
        latency_ms=latency_ms,
        release_id=settings.release_id,
        prompt_version=result.prompt_version,
        model_name=result.model_name,
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    log_event("unhandled_exception", error=type(exc).__name__, message=str(exc))
    return JSONResponse(status_code=500, content={"detail": "internal server error"})
