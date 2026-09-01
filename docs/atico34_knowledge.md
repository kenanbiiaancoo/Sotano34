# atico34_knowledge.md

> **Purpose:** Controlled Ático34 knowledge snapshot for the `Legal Intake AI` diagnosis service  
> **Snapshot date:** 2026-08-31  
> **Source policy:** Official Ático34 / Grupo Atico34 website only  
> **Use:** Preliminary lead triage and service recommendation, never definitive legal advice

---

# 1. Model-use rules

This file is a **controlled reference snapshot**.

When using it in the diagnosis model:

1. Recommend only services/products that appear in this file.
2. Use the `service_id` identifiers defined below.
3. Do not invent product names, legal guarantees, prices or obligations.
4. Do not treat generic blog content as proof that every described capability is a contracted product.
5. If a case cannot be mapped safely, request more information or set `requires_human_review=true`.
6. Describe recommendations as a **possible fit** for the case.
7. Final legal/commercial assessment belongs to Ático34 professionals.
8. This file is frozen for the demo. Public webpages may change after the snapshot date.

---

# 2. Company profile

## COMPANY_PROFILE

- **Name:** Grupo Atico34 / Atico34.
- **Positioning:** Legaltech specialized in **Protección de Datos, Compliance e Inteligencia Artificial**.
- **Core proposition:** Personalized legal/technical support for regulatory compliance and management of organizational data.
- **Current homepage positioning:** protection of data and control horario are highlighted as prominent solution areas.
- **Operating model:** personalized service backed by lawyers/experts, from initial diagnosis through implementation, training/advice and ongoing follow-up.
- **Scale statements on current official homepage:** approximately 15 years of experience, more than 11,000 clients and presence in more than 26 provincial capitals.
- **Client profiles referenced by official pages:** autónomos, pymes, companies of different sizes/sectors, public bodies/administrations and other organizations.
- **Málaga presence:** official Málaga page lists a local office and local protection-data service.

### Practical implication for this demo

The diagnosis system should favor a **needs-based mapping**:

```text
client facts
    ↓
preliminary need
    ↓
relevant Ático34 service area
    ↓
human professional review
```

The model must not behave like an autonomous lawyer or a price configurator.

Sources: `S01`, `S02`, `S03`.

---

# 3. Service catalog

The following IDs are the only approved IDs for `recommended_atico34_services`.

---

## SERVICE: `rgpd_lopdgdd_consulting`

**Display name:** Consultoría / adaptación RGPD y LOPDGDD

### What official sources support

Ático34 offers personalized protection-data consulting and adaptation services for organizations, including assessment of the client's situation and actions required to meet applicable data-protection obligations.

Official pages list work such as:

- Registro de actividades de tratamiento.
- Responsable/encargado contracts and review of third-party access.
- Consent management.
- Legal privacy documentation.
- Website privacy/cookies texts.
- Confidentiality commitments.
- Videovigilance-related compliance.
- Policies and procedures.
- Ongoing monitoring/update.
- Legal support/consultation.

### Good routing signals

Recommend as a possible fit when a lead says things such as:

- “Nunca hemos adaptado la empresa al RGPD/LOPDGDD.”
- “No sabemos qué documentación necesitamos.”
- “Tratamos datos de clientes/empleados/proveedores y queremos revisar cumplimiento.”
- “Queremos una revisión integral.”
- “Necesitamos actualizar contratos, cláusulas, políticas o consentimientos.”

### Important boundary

Do not claim from a short intake that the client is compliant/non-compliant. Phrase as a possible need for review/adaptation.

Sources: `S02`, `S04`.

---

## SERVICE: `atico34_lopd_software`

**Display name:** Atico34 LOPD — software/plataforma de gestión de protección de datos

### What official sources support

Ático34 describes **Atico34 LOPD** as its software/platform for managing protection-data obligations.

Officially described capabilities include:

- management of providers with access to data,
- cloud-accessible information,
- signature/document functionality,
- employee-related data-access management,
- legal documents for websites/ecommerce,
- privacy/cookie-related management,
- access to legal documentation,
- risk/compliance visibility,
- support connected to the service.

Official pages also state that clients can receive access to the online platform.

### Good routing signals

Possible fit where the lead needs:

- centralized ongoing management,
- document generation/availability,
- management of suppliers/employees and access to data,
- privacy documentation for website/ecommerce,
- a recurring operational tool rather than a one-off document.

### Important boundary

Do not invent modules beyond those supported by the official page.

Sources: `S05`, `S06`.

---

## SERVICE: `dpo_service`

**Display name:** Delegado de Protección de Datos (DPO/DPD)

### What official sources support

Ático34 offers DPO services. Its official material describes the DPO as the independent/confidential role that supervises and monitors compliance with data-protection rules and points to the legal circumstances in which appointment is mandatory.

### Good routing signals

Possible fit when the lead:

- explicitly asks for a DPO/DPD,
- says an authority/client has requested one,
- performs activities that may require evaluation of DPO obligation,
- wants an external DPO function.

### Human-review rule

A short lead intake normally should not make a definitive statement that a DPO is legally mandatory. Recommend **DPO obligation assessment / DPO service** and human review when facts are incomplete.

Sources: `S07`, `S02`.

---

## SERVICE: `risk_audit_eipd`

**Display name:** Auditoría, análisis de riesgos y evaluación de impacto (EIPD/DPIA)

### What official sources support

Ático34 lists:

- audits,
- risk analysis,
- evaluation of technical and organizational measures,
- impact assessments,
- recommendations/corrective measures,
- monitoring.

Its audit area presents Data Protection services including adaptation, DPO, risk analysis, impact assessment and training.

### Good routing signals

Potential fit where:

- the organization wants an audit/review of current measures,
- processing may involve elevated privacy risk,
- new technology/processes are being introduced,
- large/sensitive datasets are involved,
- the lead specifically asks about EIPD/DPIA or risk assessment.

### Human-review rule

Do not decide solely from a brief message that an EIPD is legally mandatory.

Sources: `S02`, `S08`, `S04`.

---

## SERVICE: `web_privacy_lssi`

**Display name:** Privacidad web / LSSI / textos legales / cookies

### What official sources support

Ático34 provides assistance around website/ecommerce legal and privacy requirements, including:

- legal/privacy/cookie texts,
- form adaptation/consent,
- LSSI-related audit/advice,
- ecommerce-related legal support,
- online privacy management.

### Good routing signals

Potential fit for:

- corporate websites collecting personal data,
- ecommerce,
- web forms,
- cookie/privacy policy concerns,
- legal notices,
- online service compliance.

Sources: `S05`, `S09`, `S08`.

---

## SERVICE: `digital_rights_privacy`

**Display name:** Privacidad en internet y derechos digitales

### What official sources support

Official service pages list areas such as:

- protection of digital identity,
- privacy of data on the internet,
- right to be forgotten,
- right to digital disconnection,
- consulting on data protection in new technologies.

### Good routing signals

Potential fit when the lead explicitly asks about:

- online privacy,
- removal/management of personal information online,
- digital identity,
- right to be forgotten,
- digital-disconnection policies.

Sources: `S02`, `S03`.

---

## SERVICE: `security_incident_support`

**Display name:** Gestión/notificación de incidencias y soporte en protección de datos

### What official sources support

Ático34 protection-data consulting pages include:

- incident notification/management,
- planning and response around security incidents/breaches,
- assistance before complaints/claims and AEPD-related situations.

### Good routing signals

Potential fit for:

- suspected personal-data breach,
- loss/exposure/access to personal data,
- need to assess an incident,
- AEPD contact/claim connected with data protection.

### Mandatory safety rule

Security incidents and authority proceedings should normally set:

```text
requires_human_review = true
```

The system must not issue definitive response deadlines or legal conclusions unless the exact case has been verified by a professional.

Sources: `S02`, `S04`.

---

## SERVICE: `aepd_claims_defense`

**Display name:** Defensa ante reclamaciones / asistencia en inspecciones AEPD

### What official sources support

Ático34 lists defense against complaints/reclamations and assistance in inspections by the Spanish Data Protection Agency (AEPD).

### Good routing signals

- formal complaint,
- AEPD communication,
- inspection,
- data-protection dispute,
- explicit need for legal defense/advice.

### Mandatory safety rule

Always favor professional review.

Sources: `S02`, `S04`.

---

## SERVICE: `privacy_training`

**Display name:** Formación y sensibilización en protección de datos

### What official sources support

Ático34 lists online/presential training for workers and management, training/sensitization as part of consulting, and educational resources.

### Good routing signals

- staff mishandling personal data,
- need to train employees/managers,
- internal privacy awareness program,
- training associated with broader adaptation.

Sources: `S02`, `S04`.

---

## SERVICE: `compliance_consulting`

**Display name:** Servicios / consultoría de Compliance

### What official sources support

Ático34 describes compliance services covering organization of regulatory compliance and plans/programs with continuing advice.

Its official compliance material references experience in areas including:

- data protection,
- equality plans,
- workplace-harassment prevention,
- time tracking,
- anti-money-laundering,
- criminal-offense prevention systems,
- whistleblowing/internal reporting channel management.

Official pages also describe compliance in labor, financial and criminal areas.

### Good routing signals

- request for a broader compliance program,
- internal policies/procedures,
- criminal/labor/financial compliance,
- prevention/monitoring of regulatory risks,
- request that crosses several compliance areas.

Sources: `S10`, `S11`.

---

## SERVICE: `whistleblowing_channel`

**Display name:** Canal de denuncias / sistema interno de información

### What official sources support

Ático34 offers an integrated whistleblowing-channel service and software with legal advice.

Official sources describe:

- implementation aligned with Ley 2/2023,
- confidential/anonymous reporting capabilities,
- software for channel management,
- legal advice by compliance specialists,
- support/maintenance,
- organizations with 50 or more employees as a core statutory trigger, while other legal/sector obligations may also apply.

### Good routing signals

- company asks whether it needs a whistleblowing channel,
- company has 50+ employees,
- current channel is only an email inbox or lacks structured management,
- need for anonymous/confidential reporting,
- need for channel software and legal support.

### Boundary

Employee count alone is useful routing data, but final applicability and implementation requirements should be confirmed by a professional, especially where sector-specific rules may apply.

Sources: `S12`, `S13`, `S14`.

---

## SERVICE: `time_tracking`

**Display name:** Control horario / registro de jornada

### What official sources support

Ático34 currently highlights control horario as a solution area and publishes detailed guidance around digital time tracking.

Official material states the current general obligation to keep daily working-time records and describes software/app-based tracking as useful for reliable, secure and auditable management.

### Good routing signals

- company needs employee time tracking,
- current system is manual/Excel/paper and difficult to audit,
- remote/hybrid/mobile workforce,
- concern over privacy/security in employee tracking,
- need to modernize registration/reporting.

### Boundary

Do not invent product capabilities not present in the controlled sources. Regulatory details can change and final advice belongs to professionals.

Sources: `S01`, `S15`.

---

## SERVICE: `ai_legal_compliance`

**Display name:** Asesoramiento legal y adaptación en Inteligencia Artificial / AI Act

### What official sources support

Ático34 identifies itself as a legaltech specialized in AI and offers legal advice in the use/regulation of artificial intelligence.

Official material describes assistance around:

- AI regulatory compliance,
- risk analysis,
- protection of personal data,
- internal training,
- ethical/legal AI use,
- measures and follow-up,
- management of rights around automated decisions.

Its TIC consulting page also lists legal/privacy-related work around AI.

### Good routing signals

- company is deploying or buying AI systems,
- concern about AI Act obligations,
- AI handling personal data,
- automated decisions,
- need for risk/compliance review,
- internal AI-use policy/training.

### Human-review rule

AI Act classification and legal obligations depend heavily on the specific system and role. Do not make a definitive classification from sparse intake data.

Sources: `S16`, `S17`, `S18`.

---

## SERVICE: `tic_privacy_consulting`

**Display name:** Consultoría TIC con enfoque jurídico/privacidad

### What official sources support

Ático34's TIC consulting area lists services related to:

- Cloud Computing,
- Big Data,
- Blockchain,
- IoT,
- Artificial Intelligence,

with legal/privacy analysis such as contracts, information flows, risk reports, impact assessments where applicable, privacy-by-design considerations and incident follow-up.

### Good routing signals

- cloud-provider/privacy contracts,
- major data/Big Data project,
- IoT processing,
- blockchain/privacy concerns,
- new technology with data-protection implications.

Sources: `S18`.

---

# 4. Additional knowledge useful for routing

## 4.1 Typical protection-data workflow described by Ático34

The current homepage presents a four-step service flow:

1. **Auditoría** — analyze current situation and produce a practical diagnosis.
2. **Documentación legal** — prepare necessary legal documents, contracts, clauses, consents and security measures adapted to the activity.
3. **Formación y asesoramiento** — provide expert legal/technical support.
4. **Seguimiento y evaluación** — monitor regulatory changes and maintain/update documentation.

### Demo relevance

The proposed Legal Intake AI should be positioned as an **earlier triage layer before a professional audit/consultation**, not as a replacement for the above process.

Source: `S01`.

---

## 4.2 Client diversity

Official pages state that Ático34 works with:

- organizations of different sizes,
- SMEs/microbusinesses,
- self-employed professionals,
- larger companies,
- public organizations,
- different business sectors.

### Demo relevance

Do not assume every lead is a corporation. Ask/derive:

```text
organization_type
sector
employee_count
processing/activity context
```

Sources: `S02`, `S03`.

---

# 5. Diagnostic routing examples

These examples are **demo routing guidance**, derived from the service catalog. They are not legal conclusions.

---

## Example A — Clinic with patient data

Input facts:

```text
sector = healthcare/clinic
employees = 12
personal data = patients
web form = yes
no complete data-protection review
```

Possible recommendations:

```text
rgpd_lopdgdd_consulting
risk_audit_eipd
web_privacy_lssi
atico34_lopd_software
```

Potential DPO considerations may merit:

```text
dpo_service
requires_human_review = true
```

if facts suggest the obligation needs professional assessment.

---

## Example B — 70-person company with no reporting channel

Potential recommendations:

```text
whistleblowing_channel
compliance_consulting
```

Human professional confirmation remains appropriate.

---

## Example C — New AI system processing customer data

Potential recommendations:

```text
ai_legal_compliance
tic_privacy_consulting
risk_audit_eipd
```

depending on actual purpose, data, system role and risk.

---

## Example D — Ecommerce with forms/cookies and outdated privacy texts

Potential recommendations:

```text
web_privacy_lssi
rgpd_lopdgdd_consulting
atico34_lopd_software
```

---

## Example E — Personal-data incident

Potential recommendations:

```text
security_incident_support
```

and:

```text
requires_human_review = true
```

If there is already an authority complaint/inspection:

```text
aepd_claims_defense
```

may also be relevant.

---

# 6. Missing-information strategy

When the lead does not supply enough information, prefer questions such as:

## General

- ¿A qué se dedica la empresa/organización?
- ¿Cuántas personas trabajan aproximadamente en ella?
- ¿Qué problema concreto queréis resolver?
- ¿Qué datos personales tratáis y de quién?
- ¿Contáis ya con algún servicio/documentación de protección de datos?

## Website/ecommerce

- ¿La web recoge datos mediante formularios?
- ¿Existe tienda online o contratación electrónica?
- ¿Utilizáis cookies o herramientas de analítica/publicidad?

## Whistleblowing/compliance

- ¿Cuántos empleados tiene la organización?
- ¿Existe actualmente un canal interno?
- ¿Qué necesidad concreta queréis cubrir: implantación, software, gestión o revisión?

## AI

- ¿Para qué proceso se utiliza o se quiere utilizar la IA?
- ¿La IA trata datos personales?
- ¿Toma o apoya decisiones sobre personas?
- ¿La solución es propia o de un proveedor externo?

## Security incident

- ¿Qué ha ocurrido?
- ¿Qué tipo de información podría haberse visto afectada?
- ¿Cuándo se detectó?
- ¿Sigue activo el incidente?

Do not attempt a full incident response inside the automated demo; escalate.

---

# 7. Recommendation constraints for the model

The diagnosis model MUST obey:

```text
1. service_id must exist in this document.
2. service_name must correspond to that service_id.
3. Each recommendation must include a short case-specific rationale.
4. Do not recommend every service.
5. Prefer 1–4 strongly relevant services.
6. If evidence is weak, lower confidence or request more information.
7. Never fabricate price, guarantee or specific contractual scope.
8. Never substitute the diagnosis for professional legal advice.
```

---

# 8. Official source register

All sources below are official Ático34 / Grupo Atico34 pages and were reviewed for this snapshot on 2026-08-31.

## S01 — Main website / company positioning

**Title:** Atico34 - Empresa de Protección de Datos  
https://protecciondatos-lopd.com/

Supports: company positioning, protection-data workflow, experience/client-scale statements, highlighted service areas.

---

## S02 — Protection-data services

**Title:** Servicios Protección de datos (LOPD-GDD y RGPD)  
https://protecciondatos-lopd.com/auditoria/servicios-lopd-rgpd/

Supports: RGPD/LOPDGDD adaptation, privacy-internet services, audits, risks/EIPD, incidents, AEPD support, compliance, training.

---

## S03 — Málaga office / service page

**Title:** Empresa de protección de datos en Málaga  
https://protecciondatos-lopd.com/malaga/

Supports: local Málaga presence, service workflow and local protection-data offering.

---

## S04 — Protection-data consultancy

**Title:** Consultoría de protección de datos LOPD/RGPD  
https://protecciondatos-lopd.com/auditoria/consultoria-proteccion-datos/

Supports: personalized consulting, audit, policies, DPIA/EIPD, DPO, training, security measures, incidents, contracts, monitoring.

---

## S05 — Atico34 LOPD software

**Title:** Software protección de datos RGPD/LOPD — Atico34 LOPD  
https://protecciondatos-lopd.com/empresas/software-rgpd-lopd/

Supports: product identity and described platform capabilities.

---

## S06 — RGPD implementation / online platform

**Title:** Implantación RGPD: Guía práctica  
https://protecciondatos-lopd.com/empresas/implantacion-rgpd/

Supports: client access to online protection-data management platform and ongoing advisory framing.

---

## S07 — DPO

**Title:** Delegado de Protección de Datos (DPO)  
https://protecciondatos-lopd.com/empresas/delegado-proteccion-datos-dpo/

Supports: DPO role and DPO service context.

---

## S08 — Audit & Assurance

**Title:** Auditoría & Assurance  
https://protecciondatos-lopd.com/auditoria/

Supports: Data Protection and ecommerce-related audit/service categories.

---

## S09 — LSSI

**Title:** Auditoría LSSI y Asesoría LSSI-CE para empresas  
https://protecciondatos-lopd.com/empresas/auditoria-lssi/

Supports: website/ecommerce/app/service legal compliance and LSSI advisory.

---

## S10 — Compliance services

**Title:** Servicios Compliance para empresas  
https://protecciondatos-lopd.com/empresas/compliance/servicios/

Supports: compliance service areas and ongoing advice.

---

## S11 — Compliance specialist / areas

**Title:** Especialista en Compliance: Qué es y funciones  
https://protecciondatos-lopd.com/empresas/compliance/especialista/

Supports: labor/financial/criminal compliance and channel-management context.

---

## S12 — Whistleblowing channel service

**Title:** Canal de denuncias. Solución integral para empresas  
https://protecciondatos-lopd.com/auditoria/canal-denuncias/

Supports: integrated channel service, legal framing, confidentiality/anonymity.

---

## S13 — Whistleblowing service details

**Title:** Servicio para el canal de denuncias  
https://protecciondatos-lopd.com/empresas/compliance/canal-denuncias/servicio/

Supports: software, legal assistance, support and maintenance.

---

## S14 — Whistleblowing obligations

**Title:** Canal de denuncias obligatorio para empresas — Ley 2/2023  
https://protecciondatos-lopd.com/empresas/compliance/canal-denuncias/obligatorio/

Supports: 50+ employee general trigger and main channel requirements/context.

---

## S15 — Time tracking

**Title:** Control horario de trabajadores  
https://protecciondatos-lopd.com/empresas/control-horario-trabajadores/

Supports: current time-recording context, security/traceability themes and software-based tracking.

---

## S16 — Legal AI advice

**Title:** Asesoramiento legal en el uso de la inteligencia artificial  
https://protecciondatos-lopd.com/empresas/inteligencia-artificial/ley/asesoramiento/

Supports: AI regulatory/legal advice, data protection and internal training.

---

## S17 — AI and personal-data management

**Title:** Inteligencia Artificial y Protección de datos  
https://protecciondatos-lopd.com/empresas/inteligencia-artificial-gestion-de-datos/

Supports: transparency, human supervision, audit/review and data-protection themes around AI.

---

## S18 — TIC consulting

**Title:** Tecnologías de la Información y Comunicación  
https://protecciondatos-lopd.com/consultoria/tic/

Supports: Cloud Computing, Big Data, Blockchain, IoT and AI legal/privacy consulting areas.

---

# 9. Snapshot maintenance

This file is intentionally static for the interview demo.

If the project evolves beyond the demo:

1. Re-verify official pages.
2. Update `snapshot date`.
3. Record source changes.
4. Add/remove service IDs only through a reviewed change.
5. Add automated tests ensuring diagnosis output only uses approved service IDs.
