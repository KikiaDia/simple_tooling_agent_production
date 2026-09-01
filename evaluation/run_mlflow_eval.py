"""Optional Databricks/MLflow 3 evaluation example.

This script is intentionally separate from the deterministic quality gate.
Run it in an environment where MLflow GenAI evaluation and Databricks credentials are configured.
"""

import asyncio
import os

import pandas as pd

from simple_agent.backends import build_backend
from simple_agent.config import Settings
from simple_agent.service import AgentService


def main() -> None:
    import mlflow
    from mlflow.genai.scorers import Correctness, Safety

    settings = Settings(agent_backend="databricks")
    service = AgentService(build_backend(settings), settings.request_timeout_seconds)
    mlflow.set_experiment(settings.mlflow_experiment_name)

    data = pd.DataFrame(
        [
            {
                "inputs": {"message": "Is $150/night a good deal in SF?"},
                "expectations": {"expected_response": "The price is in the Mid-Range tier."},
            }
        ]
    )

    def predict_fn(message: str) -> str:
        return asyncio.run(service.ask(message)).answer

    result = mlflow.genai.evaluate(
        data=data,
        predict_fn=predict_fn,
        scorers=[Correctness(), Safety()],
    )
    print(result)


if __name__ == "__main__":
    if os.getenv("AGENT_BACKEND") != "databricks":
        raise SystemExit("Set AGENT_BACKEND=databricks before running MLflow evaluation.")
    main()
