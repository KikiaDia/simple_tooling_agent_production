# Test strategy

## Unit
Fast, deterministic, no network:
- price-tier business rules
- tool serialization
- backend orchestration

## Functional
Application contract through FastAPI:
- `/health`
- `/invocations`
- validation and response schema

## Integration
Requires configured Databricks resources:
- credentials/identity
- model endpoint
- UC/MCP function availability
- MLflow experiment

## GenAI evaluation
Golden dataset + scorers:
- expected tool selection / count
- expected semantic facts
- latency threshold
- later: MLflow judges, safety, task-specific scorers

The CI pipeline promotes only if all mandatory gates pass.
