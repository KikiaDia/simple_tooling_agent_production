"""Register the deterministic tool as a Unity Catalog Python function.

Run from a Databricks environment or another environment configured for the
Unity Catalog AI Python client used by your organization.
"""

import os

from simple_agent.tools import classify_price_tier_uc


def main() -> None:
    from unitycatalog.ai.core.databricks import DatabricksFunctionClient

    full_name = os.environ["UC_FUNCTION_FULL_NAME"]
    catalog, schema, _ = full_name.split(".", 2)

    client = DatabricksFunctionClient()
    info = client.create_python_function(
        func=classify_price_tier_uc,
        catalog=catalog,
        schema=schema,
        replace=True,
    )
    print(f"Registered: {info.full_name}")


if __name__ == "__main__":
    main()
