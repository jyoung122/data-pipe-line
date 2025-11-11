# Document Pipeline Minimal POC

This repository provides a minimal proof of concept for the document processing pipeline platform described in the mission template.

## Features

- FastAPI backend with CRUD for pipelines, runs, and document registration.
- SQLAlchemy models for pipeline, document, staging, invoice, FOIA, and validation entities.
- Synchronous pipeline orchestrator that ingests text, performs mock processing/validation, and stages results.
- Milvus client stub that records embeddings in-memory when no vector store is configured.
- Typer-based CLI that consumes the HTTP API.
- Example pipeline definition (`examples/sample_pipeline.json`).

## Quickstart

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the API:

   ```bash
   uvicorn app.main:app --reload
   ```

3. Register the sample pipeline via CLI:

   ```bash
   python -m app.cli.main pipelines-create --from-file examples/sample_pipeline.json
   ```

4. Trigger the pipeline against inline text:

   ```bash
   python -m app.cli.main pipelines-run <pipeline_id> --text "Sample invoice text"
   ```

5. Inspect run status:

   ```bash
   python -m app.cli.main runs-status <run_id>
   ```

The SQLite database file (`app.db`) is created automatically at startup.

## Configuration

Environment variables can be provided through an `.env` file:

- `DATABASE_URL` / `SYNC_DATABASE_URL` – override the default SQLite database.
- `MILVUS_URI` – supply a Milvus connection string to enable embedding storage.
- `ENABLE_BACKGROUND_WORKERS` – reserved flag for future async execution.

## Testing

Compile-time validation can be performed with:

```bash
python -m compileall app
```

Additional runtime tests can be added under a `tests/` directory.
