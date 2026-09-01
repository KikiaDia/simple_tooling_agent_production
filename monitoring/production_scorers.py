"""Example MLflow production scorer definitions.

Register/start these from a Databricks notebook after validating them offline.
Production monitoring is intentionally not auto-configured by CI here because
sampling, permissions and thresholds are environment/governance decisions.
"""


def define_scorers():
    from mlflow.genai.scorers import Safety

    return [Safety()]
