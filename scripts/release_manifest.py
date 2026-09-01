import hashlib
import json
import os
import platform
from pathlib import Path


def sha256_file(path: str) -> str | None:
    p = Path(path)
    if not p.exists():
        return None
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    manifest = {
        "release": {
            "release_id": os.getenv("RELEASE_ID", os.getenv("CI_COMMIT_TAG", "local")),
            "git_sha": os.getenv("CI_COMMIT_SHA", "local"),
            "git_tag": os.getenv("CI_COMMIT_TAG"),
            "pipeline_id": os.getenv("CI_PIPELINE_ID"),
            "artifact_digest": os.getenv("ARTIFACT_DIGEST"),
        },
        "runtime": {
            "python": platform.python_version(),
            "dependency_lock": os.getenv("DEPENDENCY_LOCK_FILE", "requirements.lock"),
            "dependency_lock_sha256": sha256_file(
                os.getenv("DEPENDENCY_LOCK_FILE", "requirements.lock")
            ),
        },
        "environment": {
            "bundle_target": os.getenv("BUNDLE_TARGET"),
            "environment": os.getenv("ENVIRONMENT"),
        },
        "genai": {
            "prompt_name": os.getenv("PROMPT_NAME"),
            "prompt_ref": os.getenv("PROMPT_REF"),
            "prompt_resolved_version": os.getenv("PROMPT_RESOLVED_VERSION"),
            "model_endpoint": os.getenv("MODEL_ENDPOINT"),
            "model_type": os.getenv("MODEL_TYPE"),
            "model_temperature": os.getenv("MODEL_TEMPERATURE"),
            "model_max_tokens": os.getenv("MODEL_MAX_TOKENS"),
            "uc_function": os.getenv("UC_FUNCTION_FULL_NAME"),
        },
        "evaluation": {
            "dataset_name": os.getenv("EVAL_DATASET_NAME"),
            "dataset_digest": os.getenv("EVAL_DATASET_DIGEST"),
            "source_sha256": sha256_file("evaluation/golden_dataset.json"),
            "evaluation_run_id": os.getenv("EVALUATION_RUN_ID"),
            "report_sha256": sha256_file("evaluation/results/offline_eval.json"),
        },
        "observability": {
            "mlflow_experiment": os.getenv("MLFLOW_EXPERIMENT_NAME"),
        },
        "deployment": {
            "databricks_yml_sha256": sha256_file("databricks.yml"),
        },
    }
    Path("release-manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
