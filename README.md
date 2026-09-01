# Simple Tool-Calling Agent — Production / CI-CD / Databricks

Projet pédagogique complet pour comprendre l'industrialisation d'un agent GenAI :
qualité Python, tests unitaires/intégration/fonctionnels, évaluation GenAI, GitLab CI/CD,
Databricks Declarative Automation Bundles, staging, smoke tests, MLflow tracing,
monitoring et rollback.

## Architecture

```text
Git push
  -> GitLab CI
     -> Ruff / format / typing
     -> unit tests
     -> functional tests
     -> integration tests
     -> GenAI evaluation gate
     -> databricks bundle validate
     -> deploy staging
     -> smoke test
     -> approval
     -> deploy prod

Production
  -> MLflow traces
  -> production scorers / SLI / SLO
  -> alert
  -> investigation
  -> rollback to known-good release
```

## Démarrage local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
uvicorn simple_agent.server:app --reload
```

Par défaut, `AGENT_BACKEND=fake`, donc l'API fonctionne sans Databricks et sans LLM.
Pour utiliser le backend Databricks/OpenAI Agents SDK :

```bash
export AGENT_BACKEND=databricks
export DATABRICKS_MODEL_ENDPOINT=databricks-llama-4-maverick
export UC_FUNCTION_FULL_NAME=main.genai.classify_price_tier_uc
export MLFLOW_EXPERIMENT_NAME=/Shared/simple-tool-agent
```

L'authentification Databricks doit être fournie par le mécanisme d'identité de l'environnement
(service principal / workload identity / configuration approuvée), jamais hardcodée.

## Tests

```bash
pytest tests/unit -q
pytest tests/functional -q
pytest tests/integration -q -m integration
pytest --cov=simple_agent --cov-report=term-missing
```

## Evaluation GenAI

Le script `evaluation/run_offline_eval.py` exécute le golden dataset et applique des quality gates.
En backend `fake`, il permet de tester toute la mécanique CI sans coût LLM.

```bash
python evaluation/run_offline_eval.py
```

## Databricks Bundle

```bash
databricks bundle validate -t staging
databricks bundle deploy -t staging
```

Puis configure `STAGING_APP_URL` et lance :

```bash
python scripts/smoke_test.py
```

## Important

Ce repository est un squelette réaliste d'apprentissage. Les noms de ressources,
permissions, endpoints, chemins MLflow, identité CI et seuils métier doivent être adaptés
au workspace et à l'organisation avant usage réel en production.


## Reproductibilité complète

La version déployée est définie par un `release-manifest.json`, pas uniquement par Git.
Le manifest capture : Git SHA/tag, artefact digest, Python + lock hash, environnement,
prompt MLflow + version résolue, modèle/type/paramètres, UC function, dataset d'évaluation,
evaluation run/report et hash du DAB.

Le prompt n'est pas hardcodé dans l'agent. L'application charge le MLflow Prompt Registry
avec `PROMPT_NAME` + `PROMPT_REF`. Les environnements utilisent des aliases `dev`,
`staging`, `production`, mais chaque release enregistre la version numérique résolue.

Voir `docs/REPRODUCIBILITY.md`.
"# simple_tooling_agent_production" 
