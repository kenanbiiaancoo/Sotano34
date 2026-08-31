# ROADMAP.md

> **Derived from:** `PROJECT_SPEC.md`  
> **Knowledge source:** `atico34_knowledge.md`  
> **Rule:** If this file conflicts with `PROJECT_SPEC.md`, the specification wins.  
> **Execution style:** One checkpoint at a time; tests green before continuing.

---

# 0. Codex workflow

For every checkpoint:

1. Read the relevant section of `PROJECT_SPEC.md`.
2. Implement only the current checkpoint.
3. Run the checkpoint tests.
4. Run the existing full test suite.
5. Start the app when relevant and verify behavior manually.
6. Mark the checkpoint status below.
7. Record commands/tests executed and any blocker.
8. Do not silently expand scope.

Status values:

```text
[ ] not started
[~] in progress
[x] complete
[!] blocked
```

---

# Phase 1 — Local foundation

## Checkpoint 1 — Scaffold, configuration and `/health`

**Status:** [ ]

### Build

- Create the FastAPI application.
- Add centralized Pydantic settings.
- Add `.env.example`.
- Add `.gitignore`.
- Add requirements/dependencies.
- Add `GET /health`.
- Add Dockerfile.
- Add `compose.yaml`.
- Expose port `8000`.
- Ensure `/docs` and `/openapi.json` work.

### Acceptance

```bash
docker compose up --build
```

starts successfully.

```text
GET /health -> 200
```

### Tests

- `test_healthcheck`

### Stop condition

Do not continue until the container starts cleanly.

---

## Checkpoint 2 — Domain models and provider interfaces

**Status:** [ ]

### Build

Create typed models/enums for:

- `InboundMessage`
- workflow states
- case categories
- urgency
- contact method
- `IntakeAnalysis`
- `PreliminaryDiagnosis`
- Ático34 recommendation object

Create provider protocols/interfaces:

- `IntakeService`
- `DiagnosisService`

### Acceptance

- Domain code has no Twilio/OpenAI imports.
- Contracts validate sample complete/incomplete cases.
- Diagnosis recommendations use `service_id`.

### Tests

- basic contract validation tests
- `test_intake_output_validation`
- `test_diagnosis_output_validation`

---

## Checkpoint 3 — SQLite repository and audit trail

**Status:** [ ]

### Build

Create SQLAlchemy persistence for:

```text
messages
workflow_runs
audit_events
```

Requirements:

- `external_id` unique.
- UUID workflow ID.
- serialized intake/diagnosis output.
- timestamps.
- audit-event append function.

### Acceptance

A workflow/message can be created, loaded and updated.

Duplicate `external_id` does not create a second workflow.

### Tests

- repository CRUD
- duplicate external ID behavior

---

## Checkpoint 4 — PrivacyService

**Status:** [ ]

### Build

Implement minimization:

- phone -> `[PHONE]`
- email -> `[EMAIL]`
- DNI/NIE-like -> `[ID]`
- IBAN-like -> `[IBAN]`

Implement sender pseudonym:

```text
HMAC-SHA256(APP_SECRET, contact_value)
```

Ensure raw contact value is not included in model payload builders.

### Acceptance

Input containing phone/email/IBAN does not expose those values in sanitized text/model payload.

### Tests

- `test_privacy_redacts_phone_and_email`
- add IBAN/ID coverage if cheap

---

# Phase 2 — Full offline workflow first

## Checkpoint 5 — Mock intake and mock diagnosis providers

**Status:** [ ]

### Build

Create:

```text
MockIntakeService
MockDiagnosisService
```

Mock data must cover:

1. complete case,
2. incomplete case,
3. optional human-review case.

Mocks must return the same Pydantic contracts as live providers.

### Acceptance

No external API credentials required.

---

## Checkpoint 6 — Deterministic completeness gate

**Status:** [ ]

### Build

Create a pure/domain-oriented gate.

Behavior:

```text
insufficient -> NEEDS_INFO
unsupported/high-risk -> HUMAN_REVIEW
sufficient -> diagnosis allowed
```

Use category-aware minimum information from `PROJECT_SPEC.md`.

### Acceptance

The gate can be unit tested without FastAPI, DB or OpenAI.

### Tests

- complete RGPD case -> diagnosis allowed
- vague case -> `NEEDS_INFO`
- security incident -> human-review behavior

---

## Checkpoint 7 — Workflow orchestrator

**Status:** [ ]

### Build

Implement the single orchestration path:

```text
InboundMessage
  -> persistence/idempotency
  -> privacy
  -> intake provider
  -> deterministic gate
  -> diagnosis provider when approved
  -> persistence
  -> audit
```

Required states/events from `PROJECT_SPEC.md`.

### Acceptance

The following are the minimum expected persisted state transitions, not
abbreviated examples.

Complete mock case:

```text
RECEIVED
VALIDATED
MINIMIZED
INTAKE_REQUESTED
INTAKE_PARSED
DIAGNOSIS_REQUESTED
DIAGNOSIS_PARSED
COMPLETED
```

Incomplete mock case:

```text
RECEIVED
VALIDATED
MINIMIZED
INTAKE_REQUESTED
INTAKE_PARSED
NEEDS_INFO
```

Human-review case:

```text
RECEIVED
VALIDATED
MINIMIZED
INTAKE_REQUESTED
INTAKE_PARSED
HUMAN_REVIEW
```

Any terminal workflow failure must end in:

```text
FAILED
```

The corresponding audit events defined in `PROJECT_SPEC.md` must be appended,
and every event must carry its `workflow_id`.

Diagnosis must not run after a rejected gate.

### Tests

- `test_mock_complete_workflow_completes`
- `test_incomplete_case_stops_at_needs_info`
- `test_diagnosis_not_called_when_gate_rejects`

---

## Checkpoint 8 — Local demo API

**Status:** [ ]

### Build

Implement:

```http
POST /api/demo/messages
GET  /api/runs/{id}
GET  /api/runs/latest
```

Demo payload should support:

```text
text
contact_name optional
company_name optional
contact_method
contact_value
```

All demo inputs must enter the same normalized workflow used by Twilio.

### Acceptance

A local HTTP request can create a workflow and query the result.

---

## Checkpoint 9 — Dashboard

**Status:** [ ]

### Build

Single-page UI with:

### Input

- contact/person
- company
- contact method
- message
- timestamp

### Intake

- category
- detected facts
- missing information
- urgency

### Result

For completed case:

- preliminary diagnosis
- possible solution
- explicit Ático34 recommendations
- confidence
- human-review status

For incomplete case:

- `NEEDS_INFO`
- missing information
- next questions

### Timeline

Render audit events.

Use polling every ~500–1000 ms.

### Acceptance

The entire mock demo can be presented without opening a terminal except to start Docker.

---

# Phase 3 — Controlled Ático34 knowledge

## Checkpoint 10 — Knowledge loader and service catalog validation

**Status:** [ ]

### Build

Load:

```text
ATICO34_KNOWLEDGE_PATH=atico34_knowledge.md
```

Create a small parser/registry sufficient to validate approved service IDs.

Approved IDs must come from the knowledge file.

At minimum the system must reject or flag a diagnosis that recommends an unknown service ID.

### Acceptance

The diagnosis layer cannot persist an invented Ático34 service.

### Tests

- `test_recommended_services_exist_in_knowledge_catalog`

### Important

Do not introduce embeddings/vector DB/RAG.

---

# Phase 4 — OpenAI integration

## Checkpoint 11 — OpenAI Intake provider

**Status:** [ ]

### Build

Use:

- official OpenAI Python SDK,
- Responses API,
- Structured Outputs,
- `OPENAI_INTAKE_MODEL`.

Model responsibility:

- extract structured facts,
- classify,
- identify missing info,
- propose follow-up questions.

The workflow gate remains deterministic.

### Acceptance

A real sample message returns a valid `IntakeAnalysis`.

No raw `contact_value` is sent.

No `json.loads()` of arbitrary prose as the contract mechanism.

### Tests

- provider mocked at HTTP/SDK boundary
- structured-response validation
- no real API dependency in test suite

---

## Checkpoint 12 — OpenAI Diagnosis provider

**Status:** [ ]

### Build

Use:

- official OpenAI Python SDK,
- Responses API,
- Structured Outputs,
- `OPENAI_DIAGNOSIS_MODEL`.

Input:

```text
sanitized structured case
+
atico34_knowledge.md
+
strict diagnosis instructions
```

Output:

```text
PreliminaryDiagnosis
```

Rules:

- no final legal advice,
- only approved service IDs,
- explicit diagnosis + possible solution,
- explicit service recommendations,
- confidence,
- human review when appropriate.

### Acceptance

For a sufficiently detailed sample case, the provider returns valid structured output and only approved services.

### Manual scenario

Use the clinic example from `PROJECT_SPEC.md`.

---

## Checkpoint 13 — Live OpenAI end-to-end via local form

**Status:** [ ]

### Build/verify

Switch providers through configuration without changing workflow code.

Target:

```text
local form
 -> PrivacyService
 -> OpenAI Intake
 -> deterministic gate
 -> OpenAI Diagnosis
 -> dashboard
```

### Acceptance

At least:

- one complete case succeeds,
- one incomplete case stops in `NEEDS_INFO`.

### Regression

```bash
pytest
```

must still run without external API calls.

---

# Phase 5 — Twilio webhook

## Checkpoint 14 — Twilio adapter and normalized inbound message

**Status:** [ ]

### Build

Implement:

```http
POST /webhooks/twilio/whatsapp
```

Normalize:

```text
MessageSid -> external_id
From       -> contact_value
Body       -> text
channel    -> whatsapp
method     -> whatsapp
```

Keep Twilio-specific fields out of domain services.

### Acceptance

A locally simulated Twilio form POST produces the same workflow as `/api/demo/messages`.

---

## Checkpoint 15 — Twilio signature validation

**Status:** [ ]

### Build

Use official Twilio SDK `RequestValidator`.

Validate:

```text
X-Twilio-Signature
```

Use exact externally visible URL based on:

```text
PUBLIC_BASE_URL
```

Invalid signature:

```text
403
```

### Tests

- `test_invalid_twilio_signature_returns_403`
- valid signed fixture/request if practical

### Acceptance

Do not implement signature algorithm manually.

---

## Checkpoint 16 — Idempotency through real webhook path

**Status:** [ ]

### Build/verify

Send the same `MessageSid` twice.

Expected:

- first request creates workflow,
- second request does not call OpenAI,
- second request does not create another workflow,
- endpoint responds safely.

### Tests

- `test_duplicate_external_message_is_idempotent`

---

# Phase 6 — Robust execution

## Checkpoint 17 — Background processing

**Status:** [ ]

### Build

Webhook path should persist work and return promptly.

Use the simple background mechanism defined by `PROJECT_SPEC.md`.

Do not add external queue infrastructure.

### Acceptance

The request is not deliberately held open for both model calls.

The dashboard can poll until terminal state.

---

## Checkpoint 18 — Retries and typed errors

**Status:** [ ]

### Build

Add:

```text
ValidationError
ExternalServiceError
WorkflowError
```

OpenAI retry policy:

```text
429 / 5xx / timeout / connection
 -> bounded exponential backoff

400 / 401 / 403 / schema error
 -> no blind retry
```

Suggested:

```text
1s -> 2s -> 4s -> FAILED
```

### Acceptance

A simulated transient provider failure can recover.

A permanent failure ends in `FAILED` with audit event and no secret leakage.

---

# Phase 7 — Public demo path

## Checkpoint 19 — Cloudflare Tunnel

**Status:** [ ]

### Preconditions

All P0 local functionality works.

### Build/configure

Expose local port 8000 over HTTPS.

Set:

```text
PUBLIC_BASE_URL=<current public base URL>
```

Configure Twilio inbound WhatsApp webhook to:

```text
<public base>/webhooks/twilio/whatsapp
```

### Acceptance

Real WhatsApp message reaches the HP-hosted application.

Signature validation succeeds behind the tunnel.

Dashboard shows the workflow.

---

# Phase 8 — Secondary deployment

## Checkpoint 20 — Frankserver

**Status:** [ ]

### Preconditions

HP/local demo is already interview-ready.

### Deploy

Use the same repository and Docker Compose.

No code fork.

### Acceptance

```bash
docker compose up -d --build
```

runs on Frankserver after environment configuration.

The interview demo must remain fully usable if Frankserver is offline.

---

# Phase 9 — Final verification

## Checkpoint 21 — Required test suite

**Status:** [ ]

Required tests green:

```text
test_healthcheck
test_privacy_redacts_phone_and_email
test_duplicate_external_message_is_idempotent
test_mock_complete_workflow_completes
test_incomplete_case_stops_at_needs_info
test_intake_output_validation
test_diagnosis_output_validation
test_diagnosis_not_called_when_gate_rejects
test_recommended_services_exist_in_knowledge_catalog
test_invalid_twilio_signature_returns_403
```

Run:

```bash
pytest
```

Record result below.

**Result:** _pending_

---

## Checkpoint 22 — Clean-start rehearsal

**Status:** [ ]

Simulate interview startup.

### Offline rehearsal

```text
docker compose up
 -> localhost:8000
 -> complete mock case
 -> COMPLETED
 -> incomplete mock case
 -> NEEDS_INFO
```

### Online rehearsal

```text
OpenAI live
 -> valid intake
 -> valid diagnosis
 -> approved recommendations
```

### Twilio rehearsal

```text
WhatsApp
 -> Twilio
 -> tunnel
 -> signature
 -> workflow
 -> dashboard
```

### Failure rehearsal

Verify presentation survives:

- OpenAI unavailable,
- Twilio unavailable,
- Internet unavailable,
- Frankserver unavailable.

Fallback:

```text
DEMO_MODE=true
```

---

# Phase 10 — README only after completion

## Checkpoint 23 — Final README

**Status:** [ ]

Create only after Definition of Done.

Recommended sections:

```text
# Legal Intake AI
## Problem
## Architecture
## Workflow
## Privacy decisions
## Local development
## Configuration
## Tests
## Deployment
## Production considerations
```

The README must describe what was actually implemented, not planned features that were never completed.

---

# P0 / P1 / P2 summary

## P0 — must finish

```text
FastAPI
Pydantic contracts
SQLite + audit
PrivacyService
mock workflow
deterministic gate
dashboard
OpenAI Intake
knowledge loader
OpenAI Diagnosis
explicit Ático34 recommendations
Docker
core tests
```

## P1 — strongly preferred

```text
Twilio real webhook
signature validation
idempotency
background execution
retries/errors
Cloudflare Tunnel
```

## P2 — only after stability

```text
Frankserver
UI polish
extra scenarios/tests
optional Twilio acknowledgement
```

---

# Do not build

```text
Google Calendar
STT/voice
RAG/vector DB
fine-tuning
autonomous agents
React/Next.js
Redis
Celery
RabbitMQ
Kafka
Kubernetes
CRM
authentication/admin panel
```

---

# Implementation log

Codex should append short factual entries here after checkpoints.

Format:

```text
## YYYY-MM-DD HH:MM — Checkpoint N
Status: complete / blocked
Implemented:
- ...

Tests:
- `pytest ...` -> ...

Notes/blockers:
- ...
```

Do not use this log to change the specification.
