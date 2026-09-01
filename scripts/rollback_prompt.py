import argparse
import mlflow


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--environment", default="production")
    args = p.parse_args()
    previous = mlflow.genai.load_prompt(
        f"prompts:/{args.name}@{args.environment}-previous"
    )
    mlflow.genai.set_prompt_alias(
        name=args.name, alias=args.environment, version=previous.version
    )
    print(f"Rolled back {args.environment} to prompt v{previous.version}")


if __name__ == "__main__":
    main()
