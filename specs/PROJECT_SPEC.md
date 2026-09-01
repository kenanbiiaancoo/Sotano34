# PROJECT_SPEC.md

> **Status:** Authoritative project specification  
> **Project:** Legal Intake AI — Ático34 interview demo  
> **Last updated:** 2026-08-31  
> **Audience:** Codex and the developer implementing the repository

---

## 0. Source-of-truth rule

`specs/PROJECT_SPEC.md` is the **authoritative source of truth** for the project.

Codex MUST NOT change the architecture, scope, external services, domain contracts, security/privacy decisions, workflow states, or Definition of Done unless this specification is updated first.

`docs/atico34_knowledge.md` is the authoritative knowledge snapshot for Ático34 services and products.

`docs/ROADMAP.md` is an execution plan derived from this specification. If `docs/ROADMAP.md` conflicts with this file, **this file wins**.

`specs/personal_specs.md` defines the developer's collaboration preferences for manual guidance versus Codex automation. It does not override this project's architecture or product requirements.

`README.md` is intentionally out of scope until the implementation is finished.

---

# 1. Business objective

Build a small, polished technical demo aimed at the second interview with **Ático34**, a legaltech company specialized in protection of data, compliance and artificial intelligence.

The demo addresses a concrete pain point described during the first interview:

> A potential client may call while a telephone agent is already busy. The company can lose the lead because the client cannot be attended immediately.

The demo proposes a written intake channel that can receive the case asynchronously, structure it, request human follow-up when information is insufficient, and produce a **preliminary diagnosis plus an explicit recommendation of Ático34 services/products**.

This is not intended to replace lawyers, consultants or sales staff. It is a **lead intake and triage system** that reduces the amount of unstructured information a human must process before contacting the potential client.

---

# 2. Alignment with the role

The implementation must deliberately demonstrate the capabilities requested in the job description and discussed during the interview:

- Solid backend foundations using Python.
- Real API design.
- Real webhook handling.
- Service-oriented architecture.
- Practical AI integration in a real workflow.
- Integration with an external messaging platform.
- Structured and validated model outputs.
- Privacy-aware processing.
- Auditable workflow execution.
- Error handling, retries and idempotency.
- Docker-based reproducible deployment.
- A local-first demo that does not depend on the secondary server.

The demo should look like a small production-minded service, not like a notebook or a single prompt call.

---

# 3. High-level use case

Example inbound message:

> “Hola, soy Marta de Clínica Ejemplo. Somos 12 empleados y tratamos datos de pacientes. Tenemos web con formulario de citas y nunca hemos hecho una revisión completa de protección de datos. Podéis contactarme por WhatsApp.”

Expected outcome:

1. The message reaches the backend through a Twilio WhatsApp webhook or the local demo form.
2. The backend validates and normalizes the event.
3. Duplicate external events are rejected idempotently.
4. Direct contact identifiers and unnecessary sensitive identifiers are minimized before OpenAI receives the case.
5. **OpenAI Intake** converts the free text into a typed `IntakeAnalysis`.
6. Deterministic rules decide whether the information is sufficient.
7. If insufficient, the workflow stops in `NEEDS_INFO` and exposes concrete follow-up questions.
8. If sufficient, **OpenAI Diagnosis** receives the sanitized structured case and the controlled Ático34 knowledge snapshot.
9. The diagnosis model returns a typed preliminary diagnosis, possible solution, and explicit recommended Ático34 services/products.
10. The result and all relevant workflow events are persisted and rendered in the dashboard.
11. A human remains responsible for final legal/commercial assessment.

---

# 4. Architecture

```text
                  ┌──────────────────────┐
                  │ WhatsApp / Twilio    │
                  └──────────┬───────────┘
                             │ HTTPS webhook
                             ▼
                  ┌──────────────────────┐
                  │ FastAPI Webhook API  │
                  └──────────┬───────────┘
                             │
                  validate + normalize
                  signature + idempotency
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Privacy Service      │
                  │ data minimization    │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ OpenAI Intake        │
                  │ Structured Output    │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Deterministic Gate   │
                  └───────┬───────┬──────┘
                          │       │
                 insufficient    sufficient
                          │       │
                          ▼       ▼
                  ┌──────────┐  ┌──────────────────────┐
                  │NEEDS_INFO│  │ OpenAI Diagnosis     │
                  └──────────┘  │ + controlled KB      │
                                │ Structured Output    │
                                └──────────┬───────────┘
                                           │
                                           ▼
                                ┌──────────────────────┐
                                │ SQLite + Audit Trail │
                                └──────────┬───────────┘
                                           │
                                           ▼
                                ┌──────────────────────┐
                                │ Demo Dashboard       │
                                └──────────────────────┘
```

Architecture style: **modular monolith with service-oriented boundaries**.

Do not split the demo into networked microservices. The service abstractions must make external providers replaceable without adding unnecessary operational complexity.

---

# 5. Mandatory technology stack

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| API framework | FastAPI |
| Contracts / validation | Pydantic v2 |
| AI provider | OpenAI API |
| OpenAI interface | Official OpenAI Python SDK + Responses API |
| AI output | Structured Outputs mapped to Pydantic models |
| Messaging | Twilio WhatsApp test environment / Sandbox |
| Persistence | SQLite |
| ORM | SQLAlchemy 2 |
| Tests | pytest |
| Frontend | Minimal HTML/CSS/vanilla JS |
| Packaging | Docker + Docker Compose |
| Local public endpoint | Cloudflare Tunnel |
| Secondary deployment | Frankserver via Docker Compose |

### OpenAI model configuration

Models MUST be configurable through environment variables and MUST NOT be hardcoded throughout the codebase.

Recommended initial values:

```ini
OPENAI_INTAKE_MODEL=gpt-5.6-terra
OPENAI_DIAGNOSIS_MODEL=gpt-5.6-sol
```

If either model is unavailable to the account, use a currently available OpenAI model supporting the required structured-output contract without changing domain interfaces.

No fine-tuning is required for this demo.

---

# 6. Explicit non-scope

Do NOT add these features unless this specification is updated:

- Google Calendar.
- Speech-to-text or voice ingestion.
- Phone-call automation.
- RAG/vector database.
- Embeddings.
- Fine-tuning.
- Autonomous agents.
- React/Next.js.
- Redis.
- Celery.
- Kafka.
- RabbitMQ.
- Kubernetes.
- Authentication/roles/admin panel.
- Production WhatsApp Business onboarding.
- CRM integration.
- Automated final legal advice.
- Automatic legal conclusions presented as certain.
- Automatic contracting or pricing.
- A full conversational chatbot.

The input channel for the demo is **written text only**.

---

# 7. Repository structure

Target structure:

```text
legal-intake-ai/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── health.py
│   │   ├── demo.py
│   │   ├── runs.py
│   │   └── twilio.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   │
│   ├── domain/
│   │   ├── models.py
│   │   └── enums.py
│   │
│   ├── services/
│   │   ├── privacy.py
│   │   ├── intake/
│   │   │   ├── base.py
│   │   │   ├── openai.py
│   │   │   └── mock.py
│   │   ├── diagnosis/
│   │   │   ├── base.py
│   │   │   ├── openai.py
│   │   │   └── mock.py
│   │   ├── knowledge.py
│   │   └── audit.py
│   │
│   ├── repositories/
│   │   └── sqlite.py
│   │
│   ├── workflows/
│   │   └── intake.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── app.js
│       └── app.css
│
├── tests/
├── data/                    # gitignored
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── specs/
│   ├── PROJECT_SPEC.md
│   └── personal_specs.md
├── docs/
│   ├── ROADMAP.md
│   ├── Checkpoint 1.md
│   └── atico34_knowledge.md
└── README.md                # created only at the end
```

A slightly different folder decomposition is acceptable only if all required service boundaries remain explicit.

---

# 8. Configuration

Use Pydantic Settings or equivalent centralized configuration.

`.env.example`:

```ini
APP_ENV=development
DEMO_MODE=true

PUBLIC_BASE_URL=
DATABASE_URL=sqlite:///data/legal_intake.db
APP_SECRET=

OPENAI_API_KEY=
OPENAI_INTAKE_MODEL=gpt-5.6-terra
OPENAI_DIAGNOSIS_MODEL=gpt-5.6-sol

TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=

ATICO34_KNOWLEDGE_PATH=docs/atico34_knowledge.md
TIMEZONE=Europe/Madrid
```

Rules:

- No scattered `os.getenv()` calls.
- No secrets in source code.
- `.env`, `data/`, local databases and other secrets MUST be gitignored.
- The knowledge file itself is version-controlled because it is intentionally a frozen public-source snapshot.

---

# 9. Domain contracts

## 9.1 InboundMessage

All external channels are normalized before entering the workflow.

Required logical fields:

```text
external_id
channel
sender_reference
contact_method
contact_value
text
received_at
```

`contact_method` should support at least:

```text
whatsapp
phone
email
other
unknown
```

For Twilio WhatsApp:

- `external_id` = `MessageSid`
- `channel` = `whatsapp`
- `contact_method` = `whatsapp`
- `contact_value` = sender WhatsApp address/number
- `text` = `Body`

The rest of the application MUST NOT depend on Twilio-specific field names.

---

## 9.2 Lead identity and contact

The system must preserve enough local information so a human can recover the lead.

Required output/display information:

```text
contact_name
company_name
contact_method
contact_value
```

Rules:

- `contact_value` is operational contact data and is stored locally.
- `contact_value` MUST NOT be sent to OpenAI.
- A pseudonymous `sender_hash` MUST be derived using HMAC-SHA256 and `APP_SECRET`.
- Contact name and company name may be extracted from the written message if supplied.
- The system performs **data minimization**, not a claim of full anonymization.

---

## 9.3 IntakeAnalysis

The first OpenAI step transforms free text into structured business facts.

Required logical fields:

```text
contact_name: str | None
company_name: str | None

case_category:
    data_protection
    dpo
    privacy_web_lssi
    risk_audit_eipd
    security_incident
    rights_claim_aepd
    compliance
    whistleblowing_channel
    time_tracking
    ai_compliance
    digital_rights
    training
    other

organization_type: str | None
sector: str | None
employee_count: int | None

current_situation: str
detected_needs: list[str]
relevant_facts: list[str]

urgency:
    low
    normal
    high

missing_information: list[str]
next_questions: list[str]

requires_human_review: bool
human_review_reason: str | None
```

The model may identify missing information, but **the workflow gate itself remains deterministic**.

---

## 9.4 Deterministic completeness gate

A dedicated domain function/service must decide whether diagnosis may proceed.

It must not delegate the final proceed/stop decision entirely to the language model.

Minimum behavior:

```text
insufficient required context
    -> NEEDS_INFO

high-risk / ambiguous / unsupported case
    -> HUMAN_REVIEW

sufficient supported case
    -> DIAGNOSIS_REQUESTED
```

The exact required facts may differ by category.

Examples:

- General RGPD adaptation:
  - organization/activity or sector
  - some description of personal-data processing
  - concrete problem or objective

- Whistleblowing channel:
  - organization type
  - employee count if known
  - whether a channel already exists / what problem is being solved

- AI compliance:
  - intended/current AI use
  - role of organization if known
  - affected business process/data if known

- Security incident:
  - enough context to classify as incident-related
  - always strongly favor human review

If insufficient, return `NEEDS_INFO` and expose `next_questions`.

---

## 9.5 PreliminaryDiagnosis

The second OpenAI step MUST return a structured object.

Required logical fields:

```text
case_summary: str
case_category: str

preliminary_diagnosis: str
possible_solution: str

recommended_atico34_services: list[
    {
        service_id: str,
        service_name: str,
        rationale: str
    }
]

missing_information: list[str]

urgency:
    low
    normal
    high

confidence:
    low
    medium
    high

requires_human_review: bool
human_review_reason: str | None

next_questions: list[str]
```

The result MUST include both:

1. a preliminary diagnosis, and
2. explicit recommendations of relevant Ático34 services/products when supported by `docs/atico34_knowledge.md`.

Recommended `service_id` values MUST come from the knowledge file. The diagnosis model MUST NOT invent Ático34 products or services.

---

# 10. Legal and diagnostic boundary

This demo provides **triage and preliminary diagnosis**, not definitive legal advice.

Allowed formulations:

- “El caso presenta indicios de que podría ser necesario revisar…”
- “Una posible actuación sería…”
- “Por la información facilitada, podría encajar el servicio…”
- “Conviene que un profesional confirme…”

Disallowed behavior:

- Declaring legal compliance/non-compliance with certainty on incomplete facts.
- Presenting the model as a lawyer.
- Issuing final legal advice.
- Making guarantees.
- Inventing legal obligations.
- Inventing Ático34 services.
- Quoting prices unless explicitly present in an approved current source and specifically requested.
- Hiding uncertainty.

High-risk or ambiguous cases MUST set `requires_human_review=true`.

---

# 11. Controlled Ático34 knowledge

`docs/atico34_knowledge.md` is the only approved Ático34-specific knowledge source for the diagnosis step in this demo.

The diagnosis service must:

1. Load the file from `ATICO34_KNOWLEDGE_PATH`.
2. Treat it as controlled reference material.
3. Instruct the model not to rely on remembered company-specific facts when they conflict with or are absent from the file.
4. Only recommend service IDs that exist in the file.
5. Prefer `NEEDS_INFO`/human review over inventing unsupported company claims.

No vector database or RAG is required because the controlled knowledge snapshot is intentionally small.

---

# 12. Privacy Service

The service exists before any OpenAI call.

Initial minimization rules:

- phone numbers -> `[PHONE]`
- email addresses -> `[EMAIL]`
- DNI/NIE-like identifiers -> `[ID]`
- IBAN-like identifiers -> `[IBAN]`

Do not send these provider/channel metadata fields to OpenAI:

- Twilio Account SID
- Twilio Message SID except where replaced with local workflow context
- raw `From`
- raw `To`
- WhatsApp address/phone
- Twilio signature
- HTTP headers
- unrelated webhook metadata

The sanitized message may retain business facts that are relevant to triage, including a stated person/company name when necessary for lead identification.

The README and presentation MUST describe this as **minimization/pseudonymization**, not complete anonymization.

---

# 13. OpenAI integration

Use the official OpenAI Python SDK and the **Responses API**.

Use **Structured Outputs** mapped to Pydantic-compatible schemas for both model stages.

Do not use:

```python
json.loads(arbitrary_model_text)
```

as the primary contract mechanism.

Two independent provider interfaces are required:

```python
class IntakeService(Protocol):
    def analyze(...) -> IntakeAnalysis:
        ...

class DiagnosisService(Protocol):
    def diagnose(...) -> PreliminaryDiagnosis:
        ...
```

Implementations:

```text
MockIntakeService
OpenAIIntakeService

MockDiagnosisService
OpenAIDiagnosisService
```

### Intake model responsibility

Only:

- understand unstructured written input,
- extract relevant facts,
- classify the case,
- identify likely missing information,
- generate candidate follow-up questions.

It does not issue the final workflow decision.

### Diagnosis model responsibility

Only after the deterministic gate approves:

- consume sanitized structured case facts,
- consume the approved Ático34 knowledge snapshot,
- produce preliminary diagnosis,
- propose a possible solution,
- map the case to explicit approved Ático34 services/products,
- expose uncertainty and need for human review.

No model is allowed to execute external side effects.

---

# 14. Mock mode

Mock mode is mandatory.

```ini
DEMO_MODE=true
```

Behavior:

```text
local form
  -> same normalized InboundMessage
  -> PrivacyService
  -> MockIntakeService
  -> deterministic gate
  -> MockDiagnosisService (when applicable)
  -> SQLite
  -> dashboard
```

The same workflow code must be used in live and mock modes.

Acceptance criterion:

> With no Internet connection, no Twilio credentials and no OpenAI API key, the full presentation must still be demonstrable locally.

Mock mode must include at least:

1. a complete case -> `COMPLETED`,
2. an incomplete case -> `NEEDS_INFO`,
3. optionally a human-review case -> `HUMAN_REVIEW`.

---

# 15. Twilio WhatsApp webhook

Endpoint:

```http
POST /webhooks/twilio/whatsapp
```

Expected Twilio inbound fields include:

```text
MessageSid
From
To
Body
```

The route is responsible only for:

1. receiving the request,
2. validating the Twilio signature,
3. normalizing the payload,
4. enforcing idempotency,
5. persisting the accepted work,
6. triggering/backgrounding the workflow,
7. returning promptly.

It must not contain domain diagnosis logic.

---

# 16. Twilio webhook security

Validate `X-Twilio-Signature` using the official Twilio SDK `RequestValidator`.

Do not implement Twilio's signature algorithm manually.

The application may sit behind a reverse proxy/tunnel, therefore signature verification must use the **exact public URL** expected by Twilio.

Use:

```ini
PUBLIC_BASE_URL=https://...
```

and reconstruct the signed URL from the configured public base URL plus the exact request path/query where required.

Invalid signature:

```text
HTTP 403
```

---

# 17. Persistence and idempotency

Minimum tables:

```text
messages
--------
id
external_id UNIQUE
channel
sender_hash
contact_method
contact_value
sanitized_text
received_at

workflow_runs
-------------
id
message_id
status
intake_json
diagnosis_json
error_code
created_at
updated_at

audit_events
------------
id
workflow_id
event_type
metadata_json
created_at
```

If preserving raw text locally, it must be a deliberate configuration choice and must not be logged. Prefer the smallest amount of stored raw content required for the demo.

`external_id UNIQUE` is mandatory.

If the same Twilio `MessageSid` arrives twice:

- do not call OpenAI again,
- do not create a second workflow,
- return a successful/idempotent response.

---

# 18. Workflow states

Minimum states/events:

```text
RECEIVED
VALIDATED
MINIMIZED

INTAKE_REQUESTED
INTAKE_PARSED

NEEDS_INFO

DIAGNOSIS_REQUESTED
DIAGNOSIS_PARSED

HUMAN_REVIEW
COMPLETED
FAILED
```

Representative audit events:

```text
webhook.received
webhook.signature.validated
message.normalized
privacy.minimized
intake.request.started
intake.response.validated
gate.needs_info
gate.approved
diagnosis.request.started
diagnosis.response.validated
workflow.human_review
workflow.completed
workflow.failed
```

Every event MUST carry a `workflow_id`.

Do not log raw PII or OpenAI API secrets.

---

# 19. Background processing

The inbound webhook should respond promptly and should not intentionally block on two external model calls.

For this demo use a simple in-process/background worker pattern backed by persisted workflow state.

Do not add Celery/Redis/RabbitMQ/Kafka.

Production evolution may replace the local background mechanism with a dedicated queue without changing domain service interfaces.

---

# 20. Retries and error handling

Create clear error categories, for example:

```text
ValidationError
ExternalServiceError
WorkflowError
```

For OpenAI calls, use bounded retries with exponential backoff for transient failures.

Typical retry candidates:

```text
429
5xx
timeout
connection error
```

Do not blindly retry:

```text
400
401
403
schema/validation errors
```

Suggested demo retry cadence:

```text
attempt 1
1s
attempt 2
2s
attempt 3
4s
FAILED
```

All terminal failures must be visible in the audit trail/dashboard without exposing secrets.

---

# 21. API surface

Minimum endpoints:

```text
GET  /
GET  /health

POST /api/demo/messages
GET  /api/runs/{id}
GET  /api/runs/latest

POST /webhooks/twilio/whatsapp
```

FastAPI-generated interfaces must remain available:

```text
/docs
/openapi.json
```

---

# 22. Local demo dashboard

The UI is intentionally minimal.

Target layout:

```text
┌─────────────────────────────────────────────────────────────┐
│                     Legal Intake AI                        │
├─────────────────┬──────────────────┬────────────────────────┤
│ INPUT           │ INTAKE           │ PRELIMINARY DIAGNOSIS  │
│                 │                  │                        │
│ Contact/company │ Category         │ Diagnosis              │
│ Contact method  │ Key facts        │ Possible solution      │
│ Message         │ Missing info     │ Ático34 recommendations│
│ Timestamp       │ Urgency          │ Human review / status  │
└─────────────────┴──────────────────┴────────────────────────┘

Timeline
──────────────────────────────────────────────────────────────
16:31:02 webhook.received
16:31:02 privacy.minimized
16:31:03 intake.response.validated
16:31:03 gate.approved
16:31:04 diagnosis.response.validated
16:31:04 workflow.completed
```

For `NEEDS_INFO`, the third column should clearly show:

- status,
- missing information,
- next questions.

Use vanilla JS polling against:

```text
GET /api/runs/{workflow_id}
```

Polling every roughly 500–1000 ms is sufficient.

Do not add WebSockets.

---

# 23. Tests

Minimum mandatory tests:

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
```

Strongly preferred:

```text
test_invalid_twilio_signature_returns_403
```

The test suite must run without real OpenAI or Twilio calls.

---

# 24. Docker

The project must start locally with:

```bash
docker compose up --build
```

Expected local URLs:

```text
http://localhost:8000
http://localhost:8000/docs
```

The container must expose a working `/health`.

The SQLite data directory must be persisted through a local volume/bind mount as appropriate.

---

# 25. Cloudflare Tunnel

Only configure the tunnel after the local and mock workflows are stable.

Target:

```text
HP laptop
│
├── Docker app :8000
│
└── Cloudflare Tunnel
        ↓
public HTTPS URL
        ↓
Twilio WhatsApp webhook
```

The tunnel is a temporary demo exposure mechanism, not the source of truth for the application.

`PUBLIC_BASE_URL` must match the externally visible Twilio webhook base URL for signature validation.

---

# 26. Frankserver

Frankserver is the **secondary deployment**, never a dependency of the interview demo.

Target process:

```text
clone same repository
configure environment
docker compose up -d --build
```

No code changes should be necessary between HP and Frankserver.

Interview principle:

> The HP/local instance is the primary presentation environment so the demo is resilient to connectivity or home-server issues. Frankserver demonstrates portability and secondary deployment only.

---

# 27. Observability

Use structured application logs and the SQLite audit trail.

Every workflow-related log should include:

```text
workflow_id
event
timestamp
status where useful
```

Never log:

- API keys,
- Twilio auth token,
- raw contact values unnecessarily,
- raw identity documents,
- webhook signatures.

The dashboard is a business/demo view; terminal logs are not the primary presentation interface.

---

# 28. Priority order

## P0 — mandatory

- FastAPI.
- Modular service architecture.
- Pydantic contracts.
- SQLite/audit trail.
- Privacy minimization.
- Full mock workflow.
- OpenAI intake.
- Deterministic completeness gate.
- `docs/atico34_knowledge.md` loading.
- OpenAI diagnosis.
- Explicit Ático34 service recommendations.
- Dashboard.
- Docker.
- Core tests.

## P1 — high value

- Real Twilio WhatsApp inbound webhook.
- Twilio signature validation.
- Idempotency.
- Background execution.
- Retry/error handling.
- Cloudflare Tunnel.

## P2 — only after P0/P1 are stable

- Frankserver secondary deployment.
- Polishing the UI.
- Additional test scenarios.
- Optional Twilio acknowledgement message if time remains.

---

# 29. Definition of Done

## A. Offline / resilient demo

With Internet unavailable:

```text
docker compose up
    ↓
localhost
    ↓
submit demo case
    ↓
PrivacyService
    ↓
Mock Intake
    ↓
deterministic gate
    ↓
Mock Diagnosis
    ↓
dashboard result
```

A complete case reaches `COMPLETED`.

An incomplete case reaches `NEEDS_INFO`.

---

## B. Online OpenAI demo

With OpenAI available:

```text
local demo form
    ↓
FastAPI
    ↓
privacy minimization
    ↓
OpenAI Intake structured output
    ↓
deterministic gate
    ↓
OpenAI Diagnosis + docs/atico34_knowledge.md
    ↓
preliminary diagnosis
    ↓
explicit approved Ático34 recommendations
```

No arbitrary free-text JSON parsing.

---

## C. Online Twilio demo

```text
WhatsApp
    ↓
Twilio
    ↓
HTTPS webhook
    ↓
signature validated
    ↓
idempotency
    ↓
same workflow
    ↓
dashboard
```

---

## D. Development quality

```bash
pytest
```

passes without external API dependencies.

```bash
docker compose up --build
```

starts the application from a clean checkout after environment setup.

---

## E. Interview resilience

If Twilio, OpenAI, Cloudflare Tunnel, Frankserver or the Internet becomes unavailable during the interview, the local mock demo remains usable.

---

# 30. Technical narrative to preserve

The implementation should support this explanation:

> “No es un chatbot genérico. Es un workflow event-driven para no perder leads cuando el canal telefónico está ocupado. Una entrada escrita llega por webhook, se valida, se normaliza y se minimizan datos antes de llamar al proveedor de IA. Un primer modelo transforma lenguaje natural en un contrato tipado. Reglas deterministas deciden si hay información suficiente. Solo entonces un segundo modelo, limitado por una base de conocimiento versionada de Ático34, genera un diagnóstico preliminar y recomienda únicamente servicios reales de la compañía. El resultado es auditable, idempotente, tiene human-in-the-loop y dispone de providers mock para no acoplar la demo a servicios externos.”

---

# 31. Codex operating rules

Codex MUST:

1. Read `specs/PROJECT_SPEC.md` before implementing a roadmap item.
2. Read `docs/atico34_knowledge.md` before implementing diagnosis.
3. Work checkpoint by checkpoint.
4. Keep tests green before moving forward.
5. Prefer the smallest implementation that satisfies the specification.
6. Keep provider-specific logic behind adapters/services.
7. Keep domain logic out of route handlers.
8. Never commit secrets.
9. Never silently expand scope.
10. Update `docs/ROADMAP.md` with completion state, tests run, and blockers after each checkpoint.
11. Ask before changing a decision marked mandatory.
12. Create `README.md` only after the implementation reaches Definition of Done.

---

# 32. External technical references

These references guide implementation details; they do not override this specification.

- OpenAI API documentation — Responses API / migration guidance:  
  https://developers.openai.com/api/docs/guides/migrate-to-responses
- OpenAI API documentation — Structured Outputs:  
  https://developers.openai.com/api/docs/guides/structured-outputs
- OpenAI model catalog:  
  https://platform.openai.com/docs/models
- Twilio WhatsApp API overview:  
  https://www.twilio.com/docs/whatsapp/api
- Twilio secure webhooks:  
  https://www.twilio.com/docs/usage/webhooks/webhooks-security
- Twilio WhatsApp test environment:  
  https://www.twilio.com/docs/whatsapp/sandbox
