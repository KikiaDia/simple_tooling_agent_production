from dataclasses import dataclass

from simple_agent.config import Settings


@dataclass(frozen=True)
class ResolvedPrompt:
    name: str
    version: int
    template: str
    model_config: dict[str, object]


def prompt_uri(name: str, ref: str) -> str:
    # Explicit versions are immutable coordinates; aliases are movable environment pointers.
    return f"prompts:/{name}/{ref}" if ref.isdigit() else f"prompts:/{name}@{ref}"


def load_runtime_prompt(settings: Settings) -> ResolvedPrompt:
    try:
        import mlflow
    except ImportError as exc:
        raise RuntimeError('Install MLflow with: pip install -e ".[databricks]"') from exc

    prompt = mlflow.genai.load_prompt(prompt_uri(settings.prompt_name, settings.prompt_ref))
    registry_config = dict(getattr(prompt, "model_config", None) or {})

    # Registry model config wins; env settings are a controlled fallback.
    model_config: dict[str, object] = {
        "model_name": registry_config.get("model_name", settings.model_endpoint),
        "model_type": registry_config.get("model_type", settings.model_type),
        "temperature": registry_config.get("temperature", settings.model_temperature),
        "max_tokens": registry_config.get("max_tokens", settings.model_max_tokens),
    }
    return ResolvedPrompt(
        name=str(prompt.name),
        version=int(prompt.version),
        template=str(prompt.template),
        model_config=model_config,
    )
