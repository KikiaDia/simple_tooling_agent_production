# Release and rollback

A production release must be traceable to:
- Git SHA / tag
- CI pipeline
- deployment target
- model endpoint
- UC function
- MLflow experiment
- evaluation report
- immutable artefact/image digest where applicable

## Promotion
main -> tests/eval -> staging -> smoke -> tag -> manual protected prod deploy.

## Rollback
Do not "fix prod by hand".
Select a known-good release, redeploy the exact artefact/configuration, smoke-test it,
then monitor quality, errors and latency.

A single probabilistic quality signal should normally trigger investigation rather than
blind automatic rollback.
