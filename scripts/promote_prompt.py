import argparse
import mlflow


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--from-alias", required=True)
    p.add_argument("--to-alias", required=True)
    args = p.parse_args()

    source = mlflow.genai.load_prompt(f"prompts:/{args.name}@{args.from_alias}")
    try:
        current = mlflow.genai.load_prompt(f"prompts:/{args.name}@{args.to_alias}")
        mlflow.genai.set_prompt_alias(
            name=args.name, alias=f"{args.to_alias}-previous", version=current.version
        )
    except Exception:
        pass

    mlflow.genai.set_prompt_alias(
        name=args.name, alias=args.to_alias, version=source.version
    )
    print(f"{args.to_alias} -> prompt v{source.version}")


if __name__ == "__main__":
    main()
