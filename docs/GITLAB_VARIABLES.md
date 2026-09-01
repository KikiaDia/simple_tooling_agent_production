# GitLab CI/CD variables

Configure through protected/masked variables or workload identity, not in Git.

Typical variables:
- Databricks host / identity parameters required by your auth method
- RUN_DATABRICKS_INTEGRATION=1 for integration pipelines
- STAGING_APP_URL for smoke tests
- DATABRICKS_MODEL_ENDPOINT
- UC_FUNCTION_FULL_NAME
- MLFLOW_EXPERIMENT_NAME

Production environment and production credentials should be protected.
