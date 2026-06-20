# Enterprise AI Decision Intelligence Copilot

## Build Manual: Zero to Working Platform

**Purpose:** This document is the execution guide for building the platform step by step.  
**Use this with:** the engineering handbook. The handbook explains concepts; this manual tells you what to build next.

---

# 1. How To Use This Manual

Follow the phases in order. Do not start the next phase until the
current phase is passing its checks.

The build path is:

1.  Set up your machine and local services.

2.  Create the repository skeleton and health check.

3.  Build authentication, tenants, and RBAC.

4.  Build dataset upload, validation, and versioning.

5.  Build analytics tables and a dashboard.

6.  Build the first data science model.

7.  Add ML engineering, tracking, serving, and monitoring.

8.  Add document ingestion and RAG.

9.  Add agent routing and human approval.

10. Add prompt management, evals, and benchmarking.

11. Add observability, security hardening, and deployment.

Build the Retail domain first. Reuse the same pattern for Healthcare,
BFSI, and Marketing after the Retail path works end to end.

# What "Done" Means

The project is not done when the backend runs. It is done when:

-   a user can log in

-   a tenant can upload a CSV

-   the upload is validated and versioned

-   the dashboard shows trusted metrics

-   at least one model can train and serve predictions

-   documents can be searched with citations

-   the copilot can route between SQL, ML, and RAG

-   the system is monitored, tested, and deployed

If a phase does not produce a visible artifact, it is not complete.

# Repository Target

Use this structure as the implementation target:

    enterprise-ai-copilot/
      backend/
        app/
          main.py
          core/
          db/
          models/
          schemas/
          api/
          services/
          auth/
          tenants/
          datasets/
          analytics/
          data_science/
          ml/
          rag/
          agents/
          llm/
          evals/
          observability/
          security/
          workflows/
          scripts/
        tests/
        alembic/
        pyproject.toml
      frontend/
        src/
      dbt/
        models/
      infra/
        docker/
        k8s/
        helm/
        terraform/
      data/
        sample_datasets/
        sample_documents/
      docs/
      docker-compose.yml
      README.md

Build the backend first. Build the frontend against stable APIs. Do not
let the UI drive the backend schema.

# Phase Map

  Phase   Outcome                               Exit Criteria
  ------- ------------------------------------- -----------------------------------------------
  0       Local machine and services ready      Docker, Python, Node, PostgreSQL, Redis work
  1       Repo skeleton and health endpoint     FastAPI boots and returns `/health`
  2       Identity, tenancy, RBAC               Users can log in and protected routes work
  3       CSV ingestion and validation          Dataset upload, versioning, report generation
  4       Analytics layer                       dbt marts and KPI dashboard render
  5       Data science baseline                 RFM, churn, forecasting, or A/B reports exist
  6       ML engineering                        Train, track, serve, monitor, retrain
  7       GenAI and RAG                         Doc Q&A with citations works
  8       Agentic AI                            Tool routing and approvals work
  9       LLMOps and benchmarking               Prompts, evals, and regression tests exist
  10      Security, observability, deployment   Logs, metrics, alerts, and cloud deploy work

# Phase 0: Local Setup

## Goal {#goal .unnumbered}

Prepare your machine so the platform can run locally.

## What You Need {#what-you-need .unnumbered}

-   Python 3.11 or newer

-   Node.js 20 or newer

-   Docker Desktop or Docker Engine

-   Git

-   VS Code or PyCharm

## Environment Variables {#environment-variables .unnumbered}

Create an `.env` file early. Start with these values:

-   `DATABASE_URL`

-   `REDIS_URL`

-   `JWT_SECRET`

-   `APP_ENV`

-   `OPENAI_API_KEY` or `AZURE_OPENAI_API_KEY`

-   `AZURE_OPENAI_ENDPOINT`

## Bootstrap Commands {#bootstrap-commands .unnumbered}

Run these from the repository root:

    git clone <repo-url> enterprise-ai-copilot
    cd enterprise-ai-copilot
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -e backend
    cd frontend
    npm install
    cd ..
    docker compose up -d postgres redis
    cd backend
    alembic upgrade head
    python scripts/load_sample_data.py
    uvicorn app.main:app --reload

In another terminal:

    cd frontend
    npm run dev

## Pass Check {#pass-check .unnumbered}

-   `GET /health` returns `{"status":"ok"}`

-   PostgreSQL accepts connections

-   Redis accepts connections

-   the frontend loads without errors

## Common Failure Points {#common-failure-points .unnumbered}

-   dependencies installed outside the virtual environment

-   database not started before migrations

-   backend started before `.env` exists

-   frontend started without installing packages

# Phase 1: Backend Skeleton

## Goal {#goal-1 .unnumbered}

Create the smallest working backend that can prove the app boots.

## Create These Files First {#create-these-files-first .unnumbered}

-   `backend/app/main.py`

-   `backend/app/core/config.py`

-   `backend/app/db/session.py`

-   `backend/app/db/base.py`

-   `backend/app/api/v1/health.py`

## Implementation Steps {#implementation-steps .unnumbered}

1.  Create the FastAPI app.

2.  Add a `/health` endpoint.

3.  Add a request ID middleware.

4.  Load settings from environment variables.

5.  Set up SQLAlchemy engine and session factory.

6.  Add an API router versioned as `v1`.

## Minimal Example {#minimal-example .unnumbered}

    # backend/app/main.py
    from fastapi import FastAPI

    app = FastAPI(title="Enterprise AI Decision Intelligence Copilot")

    @app.get("/health")
    def health():
        return {"status": "ok"}

## Pass Check {#pass-check-1 .unnumbered}

-   backend starts with no stack trace

-   `/health` returns 200

-   OpenAPI docs are visible at `/docs`

# Phase 2: Identity, Tenancy, and RBAC

## Goal {#goal-2 .unnumbered}

Make the app safe for multi-tenant enterprise use.

## Create These Tables First {#create-these-tables-first .unnumbered}

1.  `organizations`

2.  `users`

3.  `roles`

4.  `permissions`

5.  `user_roles`

6.  `role_permissions`

7.  `audit_logs`

## Create These Files {#create-these-files .unnumbered}

-   `backend/app/models/organization.py`

-   `backend/app/models/user.py`

-   `backend/app/models/role.py`

-   `backend/app/models/permission.py`

-   `backend/app/auth/jwt.py`

-   `backend/app/auth/dependencies.py`

-   `backend/app/security/permissions.py`

## Implementation Steps {#implementation-steps-1 .unnumbered}

1.  Create the organization model.

2.  Create the user model.

3.  Add password hashing.

4.  Add JWT login and refresh flow.

5.  Add role and permission checks.

6.  Add tenant scoping to every query.

7.  Add audit logging for sensitive actions.

8.  Add PostgreSQL row-level security later, after the application-level
    checks work.

## Pass Check {#pass-check-2 .unnumbered}

-   a user can log in

-   a protected endpoint rejects anonymous requests

-   tenant A cannot see tenant B data

-   audit logs record sensitive operations

# Phase 3: Dataset Upload, Validation, and Versioning

## Goal {#goal-3 .unnumbered}

Let a tenant upload CSV files and receive a dataset version plus a
quality report.

## Create These Files {#create-these-files-1 .unnumbered}

-   `backend/app/datasets/api.py`

-   `backend/app/datasets/service.py`

-   `backend/app/datasets/storage.py`

-   `backend/app/datasets/schema_inference.py`

-   `backend/app/datasets/validation.py`

-   `backend/app/datasets/models.py`

## Create These Tables {#create-these-tables .unnumbered}

1.  `datasets`

2.  `dataset_versions`

3.  `dataset_files`

4.  `validation_reports`

5.  `validation_issues`

## Implementation Steps {#implementation-steps-2 .unnumbered}

1.  Add a CSV upload endpoint.

2.  Store the raw file in local storage first.

3.  Save dataset metadata.

4.  Infer column names and types.

5.  Validate required columns, nulls, ranges, and allowed values.

6.  Generate a validation report.

7.  Version each upload so the original file is never overwritten.

8.  Add a download or preview endpoint for the uploaded file.

## Pass Check {#pass-check-3 .unnumbered}

-   a file upload creates a dataset record

-   the system assigns a version number

-   validation issues appear in the report

-   failed validation does not overwrite raw data

# Phase 4: Analytics and Dashboard

## Goal {#goal-4 .unnumbered}

Turn clean data into trusted business metrics.

## Create These Files {#create-these-files-2 .unnumbered}

-   `backend/app/analytics/models.py`

-   `backend/app/analytics/metrics.py`

-   `backend/app/analytics/service.py`

-   `backend/app/analytics/api.py`

-   `frontend/src/features/dashboard/*`

-   `dbt/models/staging/*`

-   `dbt/models/marts/*`

## Create These Tables {#create-these-tables-1 .unnumbered}

1.  `fact_orders`

2.  `dim_customers`

3.  `dim_products`

4.  `dim_campaigns`

5.  `metric_definitions`

## Implementation Steps {#implementation-steps-3 .unnumbered}

1.  Build dbt staging models.

2.  Build one retail mart.

3.  Define a metric catalog.

4.  Add a KPI API.

5.  Render cards and simple charts in React.

6.  Add cohort or funnel analysis later, after the base dashboard works.

## Pass Check {#pass-check-4 .unnumbered}

-   dashboard shows revenue or order metrics

-   dbt tests pass

-   metrics are computed from the warehouse, not from raw CSVs

# Phase 5: Data Science Baseline

## Goal {#goal-5 .unnumbered}

Build one simple but real business model. Use Retail churn first.

## Create These Files {#create-these-files-3 .unnumbered}

-   `backend/app/data_science/churn/features.py`

-   `backend/app/data_science/churn/train.py`

-   `backend/app/data_science/churn/evaluate.py`

-   `backend/app/data_science/churn/api.py`

-   `backend/app/data_science/experiments/*.py`

## Implementation Steps {#implementation-steps-4 .unnumbered}

1.  Define churn clearly.

2.  Create observation and performance windows.

3.  Build features only from historical data.

4.  Start with logistic regression or XGBoost.

5.  Evaluate with AUC, precision, recall, and lift.

6.  Store the experiment in MLflow.

7.  Show feature importance or SHAP output.

8.  Add RFM or segmentation after churn works.

## Pass Check {#pass-check-5 .unnumbered}

-   a reproducible training job exists

-   metrics are logged

-   the model outputs a risk score

-   the model can be explained

# Phase 6: ML Engineering

## Goal {#goal-6 .unnumbered}

Move the model from notebook code into a production pattern.

## Create These Files {#create-these-files-4 .unnumbered}

-   `backend/app/ml/pipelines/*`

-   `backend/app/ml/feature_store/*`

-   `backend/app/ml/model_registry.py`

-   `backend/app/ml/serving.py`

-   `backend/app/ml/batch_inference.py`

-   `backend/app/ml/retraining.py`

-   `backend/app/ml/monitoring.py`

## Implementation Steps {#implementation-steps-5 .unnumbered}

1.  Add a feature pipeline.

2.  Save features in a reusable table or feature store pattern.

3.  Track runs in MLflow.

4.  Add a prediction API for single requests.

5.  Add a batch scoring job.

6.  Add drift detection with Evidently or similar reports.

7.  Add a retraining trigger.

8.  Add promotion and rollback logic.

## Pass Check {#pass-check-6 .unnumbered}

-   model training is repeatable

-   prediction service returns stable schema

-   drift report can be generated

-   retraining can be triggered manually

# Phase 7: GenAI and RAG

## Goal {#goal-7 .unnumbered}

Answer questions from documents with citations.

## Create These Files {#create-these-files-5 .unnumbered}

-   `backend/app/rag/parser.py`

-   `backend/app/rag/chunker.py`

-   `backend/app/rag/embeddings.py`

-   `backend/app/rag/vector_store.py`

-   `backend/app/rag/retriever.py`

-   `backend/app/rag/api.py`

## Create These Tables {#create-these-tables-2 .unnumbered}

1.  `documents`

2.  `document_chunks`

3.  `embeddings`

4.  `rag_queries`

5.  `rag_answers`

## Implementation Steps {#implementation-steps-6 .unnumbered}

1.  Parse PDFs and DOCX files.

2.  Clean extracted text.

3.  Chunk the text.

4.  Create embeddings.

5.  Store vectors in pgvector.

6.  Retrieve top-k chunks.

7.  Rerank if needed.

8.  Generate answer text.

9.  Attach citations.

## Pass Check {#pass-check-7 .unnumbered}

-   a question returns an answer

-   the answer contains citations

-   the cited chunks come from approved documents

# Phase 8: Agentic AI

## Goal {#goal-8 .unnumbered}

Let the copilot choose tools instead of forcing the user to choose
endpoints.

## Create These Files {#create-these-files-6 .unnumbered}

-   `backend/app/agents/router.py`

-   `backend/app/agents/tools/sql_tool.py`

-   `backend/app/agents/tools/rag_tool.py`

-   `backend/app/agents/tools/ml_tool.py`

-   `backend/app/agents/tools/chart_tool.py`

-   `backend/app/agents/memory.py`

-   `backend/app/agents/api.py`

## Implementation Steps {#implementation-steps-7 .unnumbered}

1.  Define a limited tool registry.

2.  Add routing rules for SQL, RAG, and ML.

3.  Keep the workflow stateful.

4.  Add a human approval step for risky actions.

5.  Store traces and outcomes.

6.  Add fallback behavior when the router is uncertain.

## Pass Check {#pass-check-8 .unnumbered}

-   a query can be routed to SQL, RAG, or ML

-   tool selection is logged

-   approval is required before risky actions

# Phase 9: LLMOps and Benchmarking

## Goal {#goal-9 .unnumbered}

Make prompts, RAG, and agents measurable.

## Create These Files {#create-these-files-7 .unnumbered}

-   `backend/app/evals/benchmark_set.py`

-   `backend/app/evals/prompt_registry.py`

-   `backend/app/evals/rag_eval.py`

-   `backend/app/evals/agent_eval.py`

-   `backend/app/evals/llm_eval.py`

-   `backend/app/evals/feedback.py`

## Implementation Steps {#implementation-steps-8 .unnumbered}

1.  Freeze a golden dataset.

2.  Define success metrics for ML, RAG, LLM, and agents.

3.  Version prompts like code.

4.  Add prompt regression tests.

5.  Add RAG evaluation metrics such as citation accuracy and recall.

6.  Add human feedback capture.

7.  Block releases when critical metrics regress.

## Pass Check {#pass-check-9 .unnumbered}

-   eval results are reproducible

-   prompt changes are versioned

-   regression failures stop release

# Phase 10: Security, Observability, and Deployment

## Goal {#goal-10 .unnumbered}

Make the platform safe, visible, and deployable.

## Security Work {#security-work .unnumbered}

-   JWT authentication

-   RBAC

-   PostgreSQL row-level security

-   secrets in a secret manager

-   PII masking

-   audit logs

## Observability Work {#observability-work .unnumbered}

-   structured JSON logs

-   request IDs

-   OpenTelemetry traces

-   Prometheus metrics

-   Grafana dashboards

-   LLM cost tracking

-   model drift dashboards

## Deployment Work {#deployment-work .unnumbered}

-   Docker images for backend and frontend

-   Docker Compose for local integration

-   GitHub Actions for CI

-   Azure deployment for production

-   rollback and release notes

## Pass Check {#pass-check-10 .unnumbered}

-   logs show request IDs

-   metrics show latency and errors

-   alerts fire on failure conditions

-   the app deploys to Azure successfully

# Practical Build Order

If you want the shortest route to a demo, build in this order:

1.  health endpoint

2.  auth and tenancy

3.  dataset upload and validation

4.  retail dashboard

5.  churn model

6.  document upload and RAG

7.  agent routing

8.  evals and guardrails

9.  monitoring and deployment

This is the order that gets you from nothing to something visible
fastest.

# Final Acceptance Checklist

You can say the project is complete when all of these are true:

-   a new user can run the app locally

-   a new tenant can sign in

-   a CSV can be uploaded and validated

-   a dashboard can be generated from the data

-   a baseline model can train and score

-   a document can be parsed and queried

-   the copilot can route to SQL, ML, and RAG

-   prompts and evals are versioned

-   logs, metrics, and traces exist

-   the system can be deployed and rolled back

# Troubleshooting Rules

When something fails:

1.  check the logs first

2.  check the environment variables second

3.  check the database migrations third

4.  check the API contract fourth

5.  check the sample data fifth

Do not debug ML or GenAI before the app foundation works.

# Next Step After This Manual

Use this file as the build order. Use the handbook for theory. Work one
phase at a time, commit each phase separately, and do not move on until
the checks pass.
