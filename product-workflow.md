# TripMate -- Product Workflow

**Document type:** Product Workflow\
**Product:** TripMate\
**Status:** Proposed\
**Version:** 2.2\
**Visual version:** [TripMate Product Workflow artifact](https://claude.ai/artifact/8yk7w1MUE79bXX58HL1QhA)\
**Live status:** [TripMate Build Tracker](https://claude.ai/artifact/2ZRasgxPpxxeR2WH3SjmxU)

Terms follow [GLOSSARY.md](GLOSSARY.md). This file is the source of
truth for how TripMate is built; the artifact shows the same content as
an interactive page and is updated with every version of this file.

This document describes the process only. It changes when the process
changes. Where the work stands today, which documents exist, and the
daily reports live in the Build Tracker.

## 1. Overview

Seven stages take TripMate from the user's problem to a product that is
operated and improved. Work moves forward, but any stage can send work
back when it finds a problem it cannot solve on its own. It is not a
strict waterfall.

```mermaid
flowchart TD
    S1["Stage 1: Discovery & Strategy"] --> S2["Stage 2: Brainstorming / PRD / Spec"]
    S2 --> S3["Stage 3: UI/UX & Software Architecture"]
    S3 --> S4["Stage 4: SOW / Planning"]
    S4 --> S5["Stage 5: AI-native SDLC"]
    S5 --> S6["Stage 6: Hardening / Deployment / Launch"]
    S6 --> S7["Stage 7: Maintenance & Iteration"]

    S7 -. new opportunities, feedback .-> S1
    S5 -. requirement or design gaps .-> S2
    S5 -. UX or architecture issues .-> S3
    S6 -. release defects .-> S5
```

Solid arrows lead to the next stage; dotted arrows are feedback loops.
Section 5 lists every loop.

## 2. Two Levels of Planning

TripMate is never specified in full detail up front. Planning happens
at two levels.

| Level | When | Covers |
|-------|------|--------|
| Product level | Once for the MVP; updated when a later stage sends work back | Vision and strategy; PRD and MVP scope; high-level epic breakdown; product-level UX/UI; high-level architecture; initial roadmap; overall test and AI evaluation strategy |
| Epic level, just in time | Before each epic | Review the epic and its requirements; finish the feature spec; finish the epic's UX flow and UI; confirm technical design and dependencies; break down into tasks; add acceptance criteria and test mapping; update test plan and AI evaluation cases; build through the AI-native SDLC |

```mermaid
flowchart TB
    subgraph Specify["Specify and design"]
        direction LR
        A[Prioritised epic] --> B[Feature spec] --> C[Epic UX/UI design] --> D[Technical design]
    end
    subgraph Deliver["Plan, build, release"]
        direction LR
        E[Tasks & test planning] --> F[AI-native SDLC] --> G[Epic verification] --> H[Integration / release]
    end
    Specify --> Deliver
```

Steps may overlap, but before a task is implemented its requirements,
design, and acceptance criteria must be clear.

## 3. Stages

Every stage gate is approved by the product owner.

### Stage 1 -- Discovery & Market Research & Strategy

**Goal:** Understand the real problem, the target users, the market,
and the opportunity; decide what TripMate should solve and why.

- **Activities:** discover and validate the problem; user research,
  interviews, and surveys; target users and personas; competitor and
  market analysis; pain points, unmet needs, and market gaps; product
  vision and strategy; value proposition and positioning; business
  model and revenue opportunities; goals, success metrics, and
  principles; non-goals and assumptions to test.
- **Deliverables:** Problem Statement, User Research Findings, User
  Personas, Competitor Analysis, Market Research, Product Vision,
  Product Strategy, Value Proposition, Product Positioning, Business
  Model Hypothesis, Success Metrics, Product Principles, Assumptions &
  Risks.
- **Documents:** [product-vision.md](product-vision.md);
  `docs/discovery.md`.
- **Ready to move on when:** at least five conversations or tests with
  real groups are done; each core assumption is marked validated,
  rejected, or still open; vision, goals, non-goals, and principles are
  written and each goal has a metric.

### Stage 2 -- Brainstorming / PRD / Spec

**Goal:** Turn the opportunity and strategy into a solution, an MVP
scope, and requirements that can be built and tested.

- **Activities:**
  - *Brainstorming:* explore solution directions and feature options;
    weigh impact, effort, risk, and feasibility; prioritise the MVP; set
    scope and out of scope.
  - *PRD:* goals and users; capabilities and feature groups;
    product-level user stories and use cases; functional and
    non-functional requirements; MVP scope and dependencies; high-level
    acceptance criteria linked to success metrics.
  - *Feature spec, just in time per epic:* behaviour and business rules;
    preconditions and postconditions; validation and permissions; errors
    and edge cases; state transitions; API or integration expectations;
    detailed acceptance criteria.
- **Deliverables:** Brainstorming Notes / Solution Options, Feature
  List, MVP Scope & Prioritization, PRD, Epic / Feature Breakdown,
  Feature Specifications, Acceptance Criteria, Scope & Out-of-scope,
  Requirements-to-Metric Mapping.
- **Documents:** [docs/solution-options.md](docs/solution-options.md);
  [prd.md](prd.md); `docs/specs/<epic>/spec.md`;
  [GLOSSARY.md](GLOSSARY.md).
- **Ready to move on when:** every P0 requirement has acceptance
  criteria; MVP scope and out of scope are agreed; the epic about to be
  built has a feature spec.

### Stage 3 -- UI/UX & Software Architecture Design

**Goal:** Design the user experience and the technical architecture so
the product is consistent, feasible, and able to grow.

- **Activities:**
  - *Product-level UX/UI (first):* information architecture; global
    user journey; navigation; high-level core flows and wireframes;
    design system foundation; overall prototype of the key flows;
    initial usability review. This is not a design of every screen.
  - *Epic-level UX/UI (per epic):* review the epic's spec; detailed
    flows and wireframes; high-fidelity UI; interactive prototype;
    usability testing; design review and refinement; design handoff.
    Design follows the MVP and its dependencies; not every epic is
    designed before development starts.
  - *Software architecture:* architecture style and system boundaries;
    module boundaries; Web, Mobile, Desktop, and Backend
    responsibilities; data model; API contracts; authentication and
    authorization; real-time communication; third-party integrations;
    caching and background jobs; security, privacy, and data
    protection; observability; performance, scalability, and
    reliability; key decisions as ADRs.
- **Deliverables:** Product Information Architecture, Global User
  Journey, Navigation Map, High-level User Flow Diagrams, Design System
  Foundation, High-level Wireframes, Overall Product Prototype, Initial
  Usability Findings, Epic Design Packages, Software Architecture
  Document, Component / Module Design, Database ERD, API Contracts,
  Integration Design, Security Architecture, Deployment /
  Infrastructure Overview, ADRs.
- **Documents:** prototype canvases; `docs/ux-review.md`;
  `docs/architecture.md`; [docs/adr](docs/adr/); the technical design
  section of each `docs/specs/<epic>/spec.md`.
- **Ready to move on when:** every core journey can be clicked through;
  key states are designed; a usability test is done and serious issues
  are fixed or decided; the architecture is reviewed and the data model
  and API contracts are ready for the next epic.

### Stage 4 -- SOW / Planning

**Goal:** Turn the agreed scope and design into a plan that can be
tracked, estimated, and controlled.

- **Activities:**
  - *Scope of work:* scope, deliverables, milestones, timeline,
    responsibilities, assumptions, constraints, dependencies, and
    acceptance conditions. TripMate is a small internal project, so a
    short scope and plan replaces a formal SOW.
  - *Development planning:* Product → Epic → Feature → Task breakdown;
    dependencies and order; estimates; milestones and release plan;
    ownership; risks and mitigation; Definition of Done.
  - *Test strategy:* test levels (unit, integration, contract,
    end-to-end); test types (functional, regression, security,
    performance, usability); environments and test data; ownership.
    Every acceptance criterion has at least one test or a recorded
    reason for the exception.
  - *AI evaluation plan:* golden dataset; metrics and thresholds; output
    quality and structured output; tool calling and retrieval;
    grounding; prompt injection and unsafe tool behaviour; latency,
    tokens, and cost; regression evaluation and release gates.
- **Deliverables:** SOW / Project Scope, Development Plan, Epic /
  Feature / Task Breakdown, Dependency Map, Estimates & Milestones,
  Risk Register, Definition of Done, Test Strategy,
  Requirements-to-Test Matrix, AI Evaluation Plan, Golden Dataset
  (initial version), Release Plan.
- **Documents:** [mvp-roadmap.md](mvp-roadmap.md);
  `docs/test-strategy.md`; tasks as issues.
- **Ready to move on when:** every epic is ordered with its
  dependencies; every task for the next epic has scope, dependencies,
  and a test; the Definition of Done and AI release gates are written.

### Stage 5 -- AI-native SDLC

**Goal:** Build each task, feature, and epic with AI help while keeping
human oversight, independent verification, and quality gates.

```mermaid
flowchart TD
    A[Backlog issue / task] --> B[AI analyses and plans]
    B --> C{Human approves plan?}
    C -->|No| D[Revise plan] --> B
    C -->|Yes| E[AI implementation] --> F[Automated tests & verification]
    F --> G[Independent AI review] --> H[Human review]
    H --> I{All quality gates pass?}
    I -->|No| J[Fix issues] --> E
    I -->|Yes| K[Merge request approved] --> L[Merge]
```

- **Activities:**
  - *Task preparation:* pick a task with clear scope, linked to its
    epic, feature spec, design, and acceptance criteria; note
    dependencies and test expectations; create the issue and branch.
  - *AI analysis and planning:* the AI reads the requirement, the
    codebase, and conventions; analyses impact; proposes a plan with the
    files to change and a test plan. A person approves the plan before
    implementation.
  - *Implementation:* within the task's scope; follows architecture,
    coding standards, and security constraints; tests change with the
    code.
  - *Verification:* unit, integration, contract, end-to-end, and
    regression tests; static analysis and lint; security checks; UI and
    design QA where relevant; AI evaluation where relevant.
  - *Review:* an independent AI review, then a human code review, for
    correctness, tests, readability, security, and scope. Reviewers do
    not change code during a review-only pass.
  - *Git workflow:* issue → branch → commit → merge request; tests and
    lint run before a merge request is opened or updated.
- **Quality gates:** acceptance criteria met; related tests pass; no
  open Critical or High defect; security checks pass; AI evaluation
  meets its threshold for AI features; no unapproved out-of-scope
  change; human approval done.
- **Deliverables:** Implemented Code, Automated Tests, Test /
  Evaluation Results, AI Review Findings, Human Review Approval, Merge
  Request, Updated Technical Documentation.
- **Documents:** `docs/development-flow.md` (the detailed loop and the
  Definition of Done); code repositories.

### Stage 6 -- Hardening / Deployment / Launching

**Goal:** Make sure the product is safe, stable, and ready to operate
before users get it.

- **Activities:**
  - *Security:* authentication and authorization review; OWASP checks;
    API security and input validation; secret management; rate
    limiting and abuse prevention; dependency scanning; prompt
    injection and tool boundary checks.
  - *Performance and reliability:* load and stress tests; profiling;
    timeouts, retries, and circuit breakers; idempotency and duplicate
    requests; failure recovery; database tuning.
  - *Operations:* structured logging; metrics and tracing; dashboards
    and alerts; backup and restore checks; disaster recovery; incident
    response.
  - *AI hardening:* model timeouts and fallbacks; token and cost limits;
    tool permission boundaries; human approval for risky actions;
    structured output validation; AI regression evaluation.
  - *Deployment preparation:* environments; database migrations; CI/CD
    and release pipeline; feature flags; rollback; monitoring readiness;
    app store, desktop signing, and web release.
  - *Launch:* internal testing → closed beta → soft launch → public
    launch, with feedback collection and issue triage.
- **Deliverables:** Security Assessment, Performance / Load Test
  Results, Operational Readiness Checklist, Deployment Runbook,
  Migration & Rollback Plan, Monitoring / Alerting Setup, Release
  Candidate, Launch Checklist, Release Notes, Launch Feedback Summary.
- **Documents:** `docs/release-plan.md`.
- **Ready to move on when:** the release gates in the roadmap pass;
  beta groups complete a trip end to end; operations are stable.

### Stage 7 -- Maintenance & Iteration

**Goal:** Watch the product's health, handle operational issues, and
keep improving from real data and feedback.

- **Activities:**
  - *Monitoring and operations:* availability, errors, and latency;
    infrastructure and database health; API and integration failures;
    AI quality, latency, and cost; incidents and production bugs.
  - *Product analytics:* activation and onboarding; feature adoption;
    engagement and retention; conversion; journey drop-off.
  - *Feedback and improvement:* collect feedback; analyse support
    issues; find usability problems; prioritise fixes and improvements;
    update the roadmap and backlog.
  - *Technical maintenance:* security patches; dependency upgrades;
    database and infrastructure maintenance; technical debt;
    performance and reliability.
- **Deliverables:** Product Analytics Reports, User Feedback Summary,
  Incident / Bug Reports, Maintenance Backlog, Technical Debt Backlog,
  Updated Product Roadmap, Iteration Plan.
- **Documents:** updates to [mvp-roadmap.md](mvp-roadmap.md),
  [prd.md](prd.md), and `docs/discovery.md`; backlog as issues.

## 4. Recommended Approach for TripMate

1. Finish product-level discovery, vision, strategy, and PRD at a level
   that sets direction.
2. Agree the MVP and the priority epics.
3. Do product-level UX/UI and high-level software architecture.
4. Write the development plan, test strategy, and AI evaluation plan at
   product level.
5. For each priority epic, finish the spec, detailed design, technical
   design, and task breakdown just in time.
6. Build the epic through the AI-native SDLC with independent
   verification and human approval.
7. Harden, release, and launch as readiness allows.
8. Watch data and feedback, and keep iterating.

**Core principle:** set the overall direction and design first, then
deliver epic by epic. Not every detail is specified up front, but every
epic must be clear before implementation starts.

## 5. Feedback Loops

When a stage finds a problem it cannot solve on its own, the work goes
back to the stage that owns the decision. The fix is made there, its
document gets a new version, and the work moves forward again.

| Found | Go back to | Update |
|-------|------------|--------|
| Problem or market assumptions are wrong | 1. Discovery & Strategy | discovery.md, product-vision.md |
| Product scope or requirements are unclear | 2. PRD / Spec | prd.md, epic spec |
| A UX flow or the UI does not meet the need | 3. UI/UX Design | Prototype, ux-review.md |
| The architecture does not meet the requirements | 3. Software Architecture | architecture.md, ADR |
| Scope, estimates, or dependencies are not feasible | 4. Planning | mvp-roadmap.md |
| Implementation or tests find a defect | 5. AI-native SDLC | Code, tests |
| A production issue needs a code fix | 5. AI-native SDLC | Code, tests |
| Deployment or operational readiness is not met | 6. Hardening / Deployment | release-plan.md |
| User feedback opens a new opportunity | 1. Discovery or 2. PRD / Spec | discovery.md or prd.md |

## 6. Document Map

One document per question, created only when there is real content for
it. Every change bumps the document's version, adds a row to its
version history, and is tagged in this repository. Which documents
exist today, and their versions, is shown in the Build Tracker.

| Document | Answers | Stage |
|----------|---------|-------|
| [GLOSSARY.md](GLOSSARY.md) | What do our words mean? | All |
| `docs/discovery.md` | Whose problem, what evidence, which competitors and market, which strategy and business model, which assumptions are still open? | 1 |
| [product-vision.md](product-vision.md) | What is the product and why build it? Vision, value, positioning, goals, metrics, principles | 1 |
| [docs/solution-options.md](docs/solution-options.md) | Which ways of solving each problem were considered, which was chosen, and why features are in or out of the MVP? | 2 |
| [prd.md](prd.md) | What must it do? MVP scope, requirements, business rules, acceptance criteria | 2 |
| `docs/specs/<epic>/spec.md` | How does this epic behave, how is it built, how is it verified? One file: behaviour, rules, acceptance criteria, technical design, tasks | 2--4 |
| Prototype canvases | How will people use it? | 3 |
| `docs/ux-review.md` | What did testing show and what changed? | 3 |
| `docs/architecture.md` | How is the system organised? Modules, data model, API contracts, security, infrastructure | 3 |
| [docs/adr](docs/adr/) | Why this decision over the alternatives? | 3 |
| [mvp-roadmap.md](mvp-roadmap.md) | In what order and by when? Phases, milestones, risks, release gates | 4 |
| `docs/test-strategy.md` | How is TripMate tested? Test levels, requirements-to-test mapping, AI evaluation plan and golden dataset | 4 |
| `docs/development-flow.md` | How does a task go from issue to merged? Definition of Done | 5 |
| `docs/release-plan.md` | How do we harden, ship, roll back, and measure? | 6 |

**Rules**

- **The PRD is not a technical spec.** The PRD says what the product
  does; the epic spec says how the system does it.
- **One technical design per epic.** It lives inside the epic spec.
  There is no separate detailed design document; a design review is a
  meeting, not a document.
- **Traceability through IDs.** Tests carry the requirement ID in their
  name (for example `RDY-03`), so the requirements-to-test table is
  generated instead of maintained by hand.
- **ADRs only for real trade-offs** that are hard to reverse and would
  surprise a future reader.

## 7. Working with Claude Code

**Give it the right context**

- Each code repository has a `CLAUDE.md` that points to the glossary,
  the PRD, and the current epic spec.
- Tasks link to the spec section and requirement IDs they implement.
- If a task needs a decision the spec does not make, Claude Code stops
  and asks instead of guessing.

**Verify what it builds**

- Automated tests and an independent AI review run before any human
  review.
- AI features (idea capture, Itinerary drafts, Gap revisions) get
  evaluation sets with expected outcomes, run on every change.
- A person approves every plan, every stage gate, and every merge.

## 8. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-11-17 | First version: eight stages, feedback loops, two planning levels, current status, document map, Claude Code practices. |
| 1.1 | 2026-11-17 | Status corrected: only stage 4 (UX/UI Design) is in progress; all other stages are not started. |
| 2.0 | 2026-11-17 | Seven-stage workflow: Discovery & Strategy, Brainstorming / PRD / Spec, UI/UX & Software Architecture, SOW / Planning, AI-native SDLC, Hardening / Deployment / Launch, Maintenance & Iteration. Adds the AI-native SDLC loop and quality gates, the epic execution loop, and `docs/test-strategy.md` in the document map. Current status and next steps moved to the Build Tracker. |
| 2.1 | 2026-11-17 | Document map: added docs/solution-options.md for stage 2 (brainstorming notes and solution options). |
| 2.2 | 2026-11-17 | Diagrams only, no process changed: the overview no longer shows "Unsupported markdown: list" in the stage boxes (labels now read "Stage 1: ..."), and the overview and the epic loop are laid out so they stay readable at page width. |
