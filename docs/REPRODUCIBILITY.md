# Full reproducibility strategy

A release is not "the Git commit". It is the complete set of coordinates required to
identify and restore the behavior that was approved.

## Coordinates

- code: Git SHA + tag
- artifact: immutable digest
- runtime: Python version + dependency lock hash
- prompt: MLflow Prompt Registry name + resolved immutable version
- model: endpoint/type + inference parameters
- tools: Unity Catalog function coordinate
- evaluation data: MLflow Evaluation Dataset in Unity Catalog + dataset/version lineage
- evaluation: MLflow evaluation run + report hash
- environment: dev/staging/prod + DAB configuration hash
- observability: MLflow experiment / traces

## Mutable aliases vs immutable versions

Application configuration may point to `dev`, `staging`, or `production` prompt aliases.
At release time, resolve the alias and persist the actual numeric prompt version in the
release manifest. Rollback can then either:
1. move the environment alias back to the previous approved prompt version; or
2. redeploy a previous complete release manifest/artifact.

Never claim a release is reproducible if only mutable aliases are stored.

## Build once, promote the same artifact

The desired flow is:
build -> digest -> test/evaluate -> staging -> prod.

Do not rebuild source separately for production after staging approval.

## Evaluation data

The checked-in JSON is only a bootstrap fixture. Production evaluation data should live
as an MLflow Evaluation Dataset backed by Unity Catalog for governance, lineage and
versioning. The release records the dataset identity/version/digest used for approval.
