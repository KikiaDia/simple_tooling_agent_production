#!/usr/bin/env bash
set -euo pipefail

: "${ROLLBACK_GIT_SHA:?Set ROLLBACK_GIT_SHA to a known-good commit}"
: "${BUNDLE_TARGET:=prod}"

echo "Rollback policy:"
echo "  known-good git SHA: ${ROLLBACK_GIT_SHA}"
echo "  target: ${BUNDLE_TARGET}"
echo
echo "This script intentionally does NOT mutate Git history automatically."
echo "Checkout/build the immutable release associated with the SHA, then deploy it:"
echo
echo "  git checkout ${ROLLBACK_GIT_SHA}"
echo "  databricks bundle validate -t ${BUNDLE_TARGET}"
echo "  databricks bundle deploy -t ${BUNDLE_TARGET}"
echo
echo "After deployment, run the smoke test and verify SLO/MLflow traces."
