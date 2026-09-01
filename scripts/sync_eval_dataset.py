import json
import os
from pathlib import Path

import mlflow

name = os.environ["EVAL_DATASET_NAME"]
source = Path(os.getenv("EVAL_DATASET_SOURCE", "evaluation/golden_dataset.json"))
rows = json.loads(source.read_text())

dataset = mlflow.genai.datasets.get_dataset(name)
records = [
    {
        "inputs": {"message": row["input"]},
        "expectations": {
            "expected_tiers": row["expected_tiers"],
            "expected_tool_calls": row["expected_tool_calls"],
        },
        "tags": {"case_id": row["id"], "git_sha": os.getenv("CI_COMMIT_SHA", "local")},
    }
    for row in rows
]
dataset.merge_records(records)
print(f"Synced {len(records)} records into {name}")
