import os

import pytest

from simple_agent.config import Settings


@pytest.mark.integration
def test_required_databricks_configuration_is_present() -> None:
    if os.getenv("RUN_DATABRICKS_INTEGRATION") != "1":
        pytest.skip("Set RUN_DATABRICKS_INTEGRATION=1 in a configured CI environment.")

    settings = Settings(agent_backend="databricks")
    assert settings.databricks_model_endpoint
    assert settings.uc_function_full_name.count(".") == 2
    assert settings.mlflow_experiment_name
