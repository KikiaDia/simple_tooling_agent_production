import os
import mlflow

PROMPT_NAME = os.environ["PROMPT_NAME"]
TEMPLATE_FILE = os.getenv("PROMPT_TEMPLATE_FILE", "prompts/sf_pricing_agent.txt")

template = open(TEMPLATE_FILE, encoding="utf-8").read()
prompt = mlflow.genai.register_prompt(
    name=PROMPT_NAME,
    template=template,
    commit_message=os.getenv("PROMPT_COMMIT_MESSAGE", "Register prompt from CI"),
    tags={"git_sha": os.getenv("CI_COMMIT_SHA", "local"), "use_case": "sf_pricing_agent"},
)
mlflow.genai.set_prompt_model_config(
    name=PROMPT_NAME,
    version=prompt.version,
    model_config={
        "model_name": os.environ["MODEL_ENDPOINT"],
        "model_type": os.getenv("MODEL_TYPE", "chat"),
        "temperature": float(os.getenv("MODEL_TEMPERATURE", "0")),
        "max_tokens": int(os.getenv("MODEL_MAX_TOKENS", "800")),
    },
)
print(f"{PROMPT_NAME} version={prompt.version}")
