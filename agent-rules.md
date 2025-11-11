🧭 Agent Mission Template (Code-Producing Version)
Mission Overview

You are an autonomous AI development agent responsible for implementing one component of a modular, multi-agent document processing system.
The platform allows configurable pipelines for document ingestion, processing, validation, and staging — enabling different use cases such as invoice validation and FOIA request triage.

Each pipeline can be executed from a CLI, and consists of modular components implemented using:

FastAPI, LangGraph, PostgreSQL, Milvus, nv-ingest, and supporting Python libraries.

You will implement one of the 15 steps described in the Reference Architecture Document.

Mission Context

You will receive:

The Reference Architecture Document (global design).

Your assigned Step ID and Title (e.g., Step 05 – LangGraph Pipeline Builder).

Dependency Summaries from previous steps.

Use this information to build a working implementation of your assigned component.
The output should include code files, docstrings, and a short Markdown summary.

Do not attempt to reimplement other steps or re-explain system-wide logic already covered by the reference architecture.
---

## 1. Multi-Agent System Overview

You will use **multiple AI agents**, each with a clear specialization:

1. **Architect Agent** – keeps the big picture consistent, refines requirements.
2. **Backend Service Agent** – builds FastAPI layers and request/response contracts.
3. **Orchestration Agent** – builds and maintains the LangGraph pipeline execution logic.
4. **Data & Storage Agent** – owns Postgres schemas, migrations, and Milvus integration.
5. **Ingestion Agent** – integrates nv-ingest and normalizes ingestion output format.
6. **Processing Agent** – implements text processing modes and LLM interaction patterns.
7. **Validation Agent** – implements rule-based and semantic validations.
8. **Staging Agent** – implements writing to staging tables and vector stores.
9. **CLI Agent** – implements the CLI interface to the backend / runtime.
10. **Observability Agent** – implements structured logging, metrics, and run traces.
11. **Use-Case Agent** – configures and validates domain-specific pipelines (Invoice, FOIA).
12. **QA Agent** – performs integration checks and scenario-based validation.
13. **Packaging Agent** – handles Docker, environment setup, and deploy docs.

Not every step needs all of them; each step has **one primary agent** and possibly **supporting agents**.

---

## 2. Core Rules for All Agents

To avoid context and coordination chaos, all agents must follow these rules:

1. **One Step = One Mission**
   Each agent run focuses on *exactly one* of the 15 steps from the plan. No agent should try to complete multiple steps in a single mission.

2. **Inputs and Outputs Are Textual Artifacts**
   Each step must produce a short, human-readable artifact describing:

   * What was implemented.
   * Public interfaces (names, responsibilities, and expected inputs/outputs).
   * Any assumptions or constraints.

3. **No Source Code in Shared Context**

   * Agents can generate and modify code in the repository, but **do not paste code into shared discussion**.
   * Only describe behavior, contracts, and file/module responsibilities.

4. **Localize Context**

   * An agent working on a step must only load:

     * The original reference architecture.
     * The previous steps’ **summary artifacts**, not all underlying details.
   * Each artifact should be capped in length (e.g., a few paragraphs), so later agents can load many of them without context overflow.

5. **Explicit Interfaces, Not Hidden Coupling**

   * Every integration between components must be described through:

     * A named interface or service.
     * A clearly described input and output structure (in natural language).

6. **Traceability**

   * Each artifact must reference:

     * The step number (1–15).
     * The responsible agent.
     * Any downstream steps that depend on it.

---

## 3. Per-Step Assignment and Expectations

Below is how agents should interpret each step from your development plan.

### Step 1 – System Environment and Dependency Bootstrap

**Primary Agent:** Architect Agent
**Supporting:** Packaging Agent

**Responsibilities:**

* Decide final tech stack boundaries (Python version, container base image, core libraries, process topology).
* Define how services are deployed together via containers (e.g., backend service, Postgres, Milvus) in conceptual terms.
* Produce an artifact describing:

  * Environment variables required.
  * Services that must be running.
  * How agents should conceptually think about “environment ready” (e.g., “database reachable”, “vector store reachable”).

---

### Step 2 – Database Schema Definition

**Primary Agent:** Data & Storage Agent

**Responsibilities:**

* Define logical schemas, tables, and relationships for:

  * pipelines
  * pipeline_runs
  * staged_data
  * documents
* Define minimal reference data for known use cases (invoice, FOIA).
* Output:

  * A natural-language description of each table:

    * Purpose
    * Key fields
    * Relationships (e.g., pipeline_runs belongs to pipelines).
  * Constraints that future components must respect (e.g., run_id must exist before writing staged_data).

---

### Step 3 – FastAPI Core Application Layer

**Primary Agent:** Backend Service Agent
**Supporting:** Architect Agent

**Responsibilities:**

* Define the FastAPI application entrypoint conceptually:

  * General routing pattern (e.g., `/pipelines`, `/runs`, `/health`).
  * How configuration is loaded and injected (no code, just flow description).
* Describe:

  * How database sessions are managed.
  * How global error handling and response formatting work.
* Produce:

  * An artifact explaining module boundaries within the backend (e.g., “api layer”, “services layer”, “core config layer”).

---

### Step 4 – Pipeline Management API

**Primary Agent:** Backend Service Agent
**Supporting:** Data & Storage Agent

**Responsibilities:**

* Define the behavior of endpoints for:

  * Create pipeline
  * Update pipeline
  * Get pipeline
  * List pipelines
  * Delete pipeline
* For each endpoint, specify in words:

  * Request fields and response fields.
  * Validation rules (e.g., graph JSON must contain nodes and edges).
* Ensure these map cleanly onto the schemas defined in Step 2.

---

### Step 5 – LangGraph Pipeline Builder

**Primary Agent:** Orchestration Agent
**Supporting:** Architect Agent

**Responsibilities:**

* Define how a stored pipeline graph (nodes + edges as JSON) is converted into an executable graph.
* Define a conceptual registry:

  * Node types → execution behaviors (IngestionNode, ProcessingNode, ValidationNode, StagingNode).
* Document:

  * How nodes receive input and produce output (e.g., a shared context object).
  * Requirements for acyclic graph and connectedness.
* Output:

  * A clear description of the pipeline build process:

    * “Load pipeline definition” → “Validate topology” → “Attach node behaviors” → “Expose graph for execution”.

---

### Step 6 – Ingestion Engine Integration (nv-ingest)

**Primary Agent:** Ingestion Agent

**Responsibilities:**

* Describe the ingestion flow:

  * Input: document reference (file path, upload id, or raw bytes).
  * Internal: nv-ingest handles parsing/OCR/chunking.
  * Output: standardized “chunks” and metadata (in natural language format, not code).
* Define:

  * Error states and how they bubble upwards.
  * Logging expectations (e.g., record number of chunks, pages, file type).

---

### Step 7 – Processing Engine Implementation

**Primary Agent:** Processing Agent

**Responsibilities:**

* Define processing modes (for now, just conceptually):

  * Extraction (structured fields from text).
  * Summarization.
  * Classification.
* Describe:

  * What each mode expects as input (e.g., a list of chunks).
  * What each mode returns (e.g., structured key/value pairs, summaries, labels).
  * How LLM prompts are conceptually constructed from configuration (no actual prompt text required).
* Ensure output fits what the Validation and Staging engines will need later.

---

### Step 8 – Validation Engine Implementation

**Primary Agent:** Validation Agent
**Supporting:** Data & Storage Agent, Processing Agent

**Responsibilities:**

* Define validation behaviors:

  * Rule-based (e.g., numeric thresholds, required fields).
  * Semantic (e.g., “compare invoice content to contract embeddings”).
* For invoice use case:

  * Explain how invoice data and contract data are conceptually aligned and compared.
* For FOIA use case:

  * Explain what “valid request” means in structural terms.
* Define the **validation output schema** in words:

  * Status (pass/fail/needs_review).
  * List of issues or anomalies with descriptions and severity.

---

### Step 9 – Staging Engine Implementation

**Primary Agent:** Staging Agent
**Supporting:** Data & Storage Agent, Milvus (via Data Agent)

**Responsibilities:**

* Define how processed and validated outputs are written to:

  * Postgres staging tables.
  * Milvus collections (with embeddings).
* Describe:

  * Required metadata (e.g., pipeline_id, run_id, document_id).
  * How errors in staging should be handled and logged.
* Ensure the staging result is:

  * Queryable later.
  * Linked back to the originating pipeline run.

---

### Step 10 – Pipeline Execution Engine

**Primary Agent:** Orchestration Agent
**Supporting:** Backend Service Agent

**Responsibilities:**

* Define the lifecycle of a pipeline run:

  * Created (queued), started (running), completed, failed.
* Describe:

  * How LangGraph is invoked with initial input (document reference, request text, etc.).
  * How data flows between nodes (shared context object).
  * How node-level errors lead to run-level errors.
* Provide:

  * A natural-language sequence diagram for a typical run:
    “Fetch pipeline → Build graph → Start run record → Execute nodes in order → Update status → Write logs”.

---

### Step 11 – CLI Orchestrator Layer

**Primary Agent:** CLI Agent
**Supporting:** Backend Service Agent

**Responsibilities:**

* Define CLI commands and their interaction with FastAPI:

  * Create pipeline (possibly from templates).
  * List pipelines.
  * Run pipeline.
  * Check run status.
* For each command, specify:

  * Required arguments and options.
  * Output format to the user (text vs structured JSON).
* Describe how the CLI handles:

  * Non-successful statuses.
  * User feedback (e.g., short summaries of what happened).

---

### Step 12 – Logging and Observability Layer

**Primary Agent:** Observability Agent

**Responsibilities:**

* Define a consistent logging schema:

  * Levels (info, warning, error).
  * Required fields (timestamp, component, pipeline_id, run_id, node_type).
* Describe:

  * Where logs are written (stdout, files, or external service).
  * How they are correlated to pipeline runs.
* Define basic metrics:

  * Number of runs.
  * Average duration.
  * Failure rate.
  * Average number of anomalies per invoice / FOIA request.

---

### Step 13 – Reference Use Cases Implementation

**Primary Agent:** Use-Case Agent
**Supporting:** Orchestration, Validation, Processing, Staging Agents

**Responsibilities:**

* Configure two concrete pipeline definitions using the existing architecture:

  1. **Invoice Validation Pipeline**
  2. **FOIA Request Pipeline**
* For each pipeline:

  * Describe its nodes, node types, and high-level configuration.
  * Describe expected inputs and outputs.
  * Describe typical anomalies or validation outcomes.
* These definitions become **templates** that the CLI can reference when creating new pipelines.

---

### Step 14 – End-to-End Execution Validation

**Primary Agent:** QA Agent

**Responsibilities:**

* Define test scenarios for:

  * Successful runs with clean documents/requests.
  * Runs with deliberate anomalies (e.g., invoice amount mismatch, incomplete FOIA).
* Describe:

  * Expected run statuses and validation outcomes.
  * What should be visible via CLI inspection and logs.
* Produce:

  * A checklist of success criteria for the entire system.

---

### Step 15 – Packaging and Deployment

**Primary Agent:** Packaging Agent
**Supporting:** Architect Agent

**Responsibilities:**

* Define:

  * How containers are built and run together.
  * What environment configuration is needed in production vs local.
* Describe:

  * A minimal startup procedure (e.g., “Run this compose file, then use CLI to register example pipelines, then run them”).
* Produce:

  * A concise deployment guide in plain language.

---

## 4. Coordination & Context Management Strategy

To keep context small and coherent:

1. **One Artifact per Step**

   * After each step is completed, the responsible agent writes a short “Step Summary Document”.
   * All future agents read only these summaries plus the original architecture, not raw code.

2. **Index by Step and Component**

   * Each artifact is labeled like:
     `Step-08_Validation-Engine_Summary`
   * Agents only load the subsets relevant to their dependencies.

3. **Avoid Re-describing the Whole System**

   * Agents should reference components by name and step ID, not re-explain architectures already documented.
   * Example: “This feature relies on the pipeline schema defined in Step 2.”

4. **Strict Interface Discipline**

   * For each cross-component relationship, use stable conceptual contracts:

     * Example: “Validation Engine consumes `Processing Output Object` and produces `Validation Report Object`.”
   * Don’t redefine what those objects mean in each step; reference where they were first defined.

---


