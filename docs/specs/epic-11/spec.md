# TripMate -- EPIC-11 Spec: Platform Foundation

**Document type:** Epic Spec\
**Product:** TripMate\
**Status:** Approved\
**Version:** 2.2\
**Stage:** 2--4, epic level\
**Epic:** EPIC-11, first part, Phase 1\
**Page version:** [TripMate EPIC-11 Spec artifact](https://claude.ai/artifact/U3abYrK3zy9Fm2CaQETpT2)

Terms follow [GLOSSARY.md](../../../GLOSSARY.md). This spec builds the
first part of EPIC-11, the platform every endpoint and every screen
uses ([mvp-roadmap.md](../../../mvp-roadmap.md), section 6.1). It does
not repeat what other documents own; it links to them:

| Topic | Owned by |
|-------|----------|
| Containers, modules and their rules, background work, hosting on Render | [architecture.md](../../architecture.md), sections 3, 4, 9, 10 |
| Request conventions, the error format, how the contract moves between repositories | [api-design.md](../../api-design.md), sections 2, 4, 6 |
| Tokens, the access guard, capabilities, rate limits | [security.md](../../security.md), sections 2 and 3 |
| `outbox_events`, `outbox_trip_seqs`, `idempotency_keys`, migrations | [data-model.md](../../data-model.md), sections 6 and 8 |
| Test levels and what runs when | [test-strategy.md](../../test-strategy.md), sections 2 to 4 |
| Card kinds, task files, risk levels, the four agents, and the Definition of Done | [docs/development-flow.md](../../development-flow.md), sections 1 to 3 |

This spec answers *what the platform gives every epic, how it is
built, and in which order its cards run*. The cards themselves, with
their scope and test cases, are in the task file of each repository
(section 6).

## 1. Scope

| In this part (Phase 1) | Out of this part |
|------------------------|------------------|
| The backend skeleton: layout, the three processes, configuration, the database session, migrations | Trip-scoped capability checks, which need `trip_members` (EPIC-02 plugs them into the guard) |
| The request pipeline: request ID, device ID, the access declaration, token check, rate limits, errors, idempotency | The WebSocket gateway (5.2) |
| The outbox, the Taskiq worker, the scheduler, cleanup jobs | Hardening, load tests, the security assessment, the release plan: EPIC-11, second part, Phase 7 |
| Logs, traces, metrics, error reporting, and the P95 alert | Navigation shells and shared screens: EPIC-10 |
| The local stack in Docker, and production on Render; staging is added before the beta | The Desktop window and installers: EPIC-12 (DESK-01, DESK-07) |
| CI in all five code repositories, the flow checks, and the contract pipeline with draft and released tags | |
| Web and Mobile foundations: project, generated client, mock mode, translations | |

## 2. What the Platform Gives Every Epic

### 2.1 Backend layout

One package per module of [architecture.md](../../architecture.md),
section 4, all with the same shape, so a card names its files the same
way in every module.

```text
tripmate-backend/
├── app/
│   ├── main.py            API process (FastAPI)
│   ├── worker.py          Worker process (Taskiq)
│   ├── scheduler.py       Scheduler process
│   ├── platform/          access, errors, idempotency, outbox, jobs, config, db, logging
│   └── <module>/          identity, trips, money, ...
│       ├── api.py         Routes: access declaration, request and response schemas
│       ├── schemas.py     Pydantic models; the contract is generated from them
│       ├── service.py     The module's public interface
│       ├── <rule>.py      Pure domain rules, named as in architecture.md, section 4
│       ├── repository.py  Queries; every trip-scoped query takes a trip ID
│       ├── models.py      Tables
│       ├── jobs.py        Taskiq jobs
│       └── events.py      Handlers for other modules' events
├── migrations/            Alembic
├── tests/                 unit, property, integration, api, contract
├── .claude/agents/        The test, code, test-check, and diff-review agent roles
├── Dockerfile             One image for the three processes
├── render.yaml            Render blueprint
├── compose.yaml           Local PostgreSQL and Redis
└── CLAUDE.md              Setup, commands, coding conventions
```

- `platform` imports no other module. A module imports only another
  module's `service.py` and its data types; import-linter fails CI
  otherwise.
- A module registers with `platform` at start-up (its routes, jobs,
  event handlers, due-work queries, error codes), so `platform` never
  imports it. `platform` finds the modules by scanning `app/`, so
  adding a module changes no shared file.
- The layout is made for cards that run at the same time. The
  skeleton creates one file for each part of `platform` (access,
  errors, rate limits, idempotency, outbox, jobs, logging), holding
  only its interface, so each later card fills its own file. Every
  dependency of 4.1 is in the lock file from the skeleton on, and each
  card's tests are in their own files, named with the card.

### 2.2 The request pipeline

Every request passes the same steps, in this order.

```mermaid
flowchart LR
    R["Request"] --> ID["Request ID,<br/>device ID"]
    ID --> AU["Access declaration:<br/>public, signed in,<br/>or a capability"]
    AU --> RL["Rate limits"]
    RL --> IK["Idempotency key<br/>(creates)"]
    IK --> TX["Handler in one<br/>transaction:<br/>change, Audit log,<br/>outbox"]
    TX --> RS["Response,<br/>stored for the key"]
```

| Step | Rule |
|------|------|
| Request ID | A new ID for every request, returned in `X-Request-Id` and written in every log line and error |
| Device ID | `X-Device-Id` is required on every request except the health check; a missing or malformed one returns `400 request.invalid` |
| Access declaration | Every route declares `public`, `signed_in`, or a capability of [security.md](../../security.md), section 3.2. A route with no declaration fails a test in CI. |
| Token check | For any route that is not `public`: the EdDSA access token's signature and expiry are checked, and `identity` is asked through its registered hook whether the session is still active. A failure returns `401 auth.not_signed_in` or `401 auth.token_expired`. |
| Capability | For a capability route, the guard asks `trips` for the caller's membership (registered by EPIC-02). Until then only `public` and `signed_in` routes exist. |
| Rate limits | The general ceiling of [security.md](../../security.md), section 2.2, on every route; a route can add its own limit with its key. Counters live in Redis. A limit returns `429 rate.limited` with `Retry-After`. When Redis does not answer, a rate-limited route returns `503 server.unavailable`. |
| Idempotency | Every `POST` that creates a record declares it; the platform applies 2.4. |
| Transaction | The handler runs in one database transaction. The change, its Audit log entries, and its outbox events are written together or not at all. |

### 2.3 Errors

- Every error a module returns is one exception type with a status,
  a code, `params`, and `fields`; the platform turns it into the format
  of [api-design.md](../../api-design.md), section 4.1.
- A request that breaks its schema returns `400 request.invalid` with
  one entry in `fields` per problem.
- Anything unexpected returns `500 server.error` with the request ID
  and no detail; the full error goes to error reporting (2.6).
- A module registers the codes it can return. A test fails when a
  registered code has no text in both languages in the pinned
  contracts version. Until CT2 adds tags, the backend pins
  `tripmate-contracts` by commit SHA in its file `contracts-ref`; the
  CI job `error-codes` checks that commit out and runs the check.

Codes this epic adds:

| Status | Code | When |
|--------|------|------|
| `400` | `request.idempotency_key_required` | A create `POST` with no `Idempotency-Key` |
| `409` | `request.idempotency_in_progress` | The same key arrives while the first request is still running |
| `400` | `request.field_missing` | Field code in `fields` of `request.invalid`: a value is missing |
| `400` | `request.field_invalid` | Field code in `fields` of `request.invalid`: any other problem, also a body that is not JSON |
| `404` | `request.not_found` | No route has this path |
| `405` | `request.method_not_allowed` | The route does not take this method |
| `500` | `server.error` | Anything unexpected |
| `503` | `server.unavailable` | The health check finds PostgreSQL or Redis unreachable; a rate limit cannot be counted |

`request.invalid`, `request.idempotency_mismatch`, `rate.limited`,
`auth.not_signed_in`, and `auth.token_expired` already exist
([api-design.md](../../api-design.md), section 4.2;
[data-model.md](../../data-model.md), section 6.3).

### 2.4 Idempotency keys

The rules are in [data-model.md](../../data-model.md), section 6.3.
This epic builds them:

| Case | Answer |
|------|--------|
| A new key | The request runs; its status and body are stored with the key |
| The same key and the same body | The stored response, without running the request again |
| The same key and a different body | `409 request.idempotency_mismatch` |
| The same key while the first request runs | `409 request.idempotency_in_progress`; the client retries later |
| The request fails with `5xx` | Nothing is stored, so a retry runs again |

A key belongs to the signed-in user. Before sign-in, for registering,
it belongs to the device ID.

### 2.5 Outbox, worker, and scheduler

- A module adds a domain event with one call inside its transaction;
  `trip_seq` is assigned in the same transaction
  ([data-model.md](../../data-model.md), section 6.2).
- The worker publishes new events in `id` order to the trip's Redis
  channel and sets `published_at`. It runs a few seconds after each
  commit and every few seconds as a sweep
  ([architecture.md](../../architecture.md), section 10).
- Handlers registered by other modules run as Taskiq jobs, one per
  event and handler, and are idempotent.
- The scheduler wakes every minute, runs each registered due-work
  query against PostgreSQL, and enqueues what is due. It keeps no
  timers of its own.
- Cleanup runs daily: idempotency keys after 24 hours, published
  outbox rows after 7 days.

### 2.6 Logs, traces, metrics, and errors

| Signal | What this epic builds |
|--------|-----------------------|
| Logs | JSON lines with request ID, user ID, and trip ID. No email, name, token, or request body; a test checks a log line made from a sign-in request. |
| Traces | OpenTelemetry across the API, the worker, PostgreSQL, Redis, and outgoing HTTP calls |
| Metrics | Request rate, errors, and latency per endpoint; queue depth and job age; outbox rows waiting |
| Errors | Error reporting with the release tag, on the backend, Web, and Mobile |
| Alerts | P95 latency over 500 ms, error rate, job age over 5 minutes, outbox not draining ([architecture.md](../../architecture.md), section 9.4) |

### 2.7 Configuration, secrets, and the health check

- All settings come from environment variables, read once at start-up
  and checked; the app does not start with a missing setting.
- Secrets live only in Render environment groups and GitHub Actions
  secrets. The repositories are public, so `.env.example` lists every
  setting with no value, and a secret scan runs in CI.
- `GET /v1/health` is `public` and returns `200` with the release
  version when PostgreSQL and Redis answer, or `503
  server.unavailable`. Render uses it to decide when an instance takes
  traffic.

### 2.8 Environments

Until the beta there are two environments
([architecture.md](../../architecture.md), section 9.2).

| Environment | What runs | Data | How it starts |
|-------------|-----------|------|---------------|
| Local | `compose.yaml`: the API, worker, and scheduler from the backend image, PostgreSQL, Redis. Web and Mobile run against it. | Seed data ([test-strategy.md](../../test-strategy.md), section 3) | `docker compose up` |
| CI | The same `compose.yaml`, for the end-to-end smoke set | Seed data | On every pull request |
| Production, until the beta | On Render, from `render.yaml`: one web instance on the free plan that runs the API, the worker, and the scheduler together, Postgres and Key Value on their free plans, and the Web static site | The product owner and one or two first users | A tagged release, by hand |
| Production, from the beta | Two API instances, one worker, one scheduler, Postgres with point-in-time recovery, Key Value, and the Web static site | Real | A tagged release, by hand |

- The backend image is published to GitHub Container Registry for
  every release tag; a client's `compose.yaml` runs the image of the
  release its pinned contract came from.
- Migrations run in production as Render's pre-deploy step; a failing
  migration stops the deploy and the previous version keeps serving.
- A rollback is a redeploy of the previous image.
- Until the beta, production has no point-in-time recovery and stops
  for a few seconds at each deploy. The three processes still start
  from the one image with their own commands, so moving them to
  separate instances before the beta changes `render.yaml` only.
- The free web instance sleeps when no request comes for a while, and
  the worker and the scheduler sleep with it: the first request after
  a pause is slow, and a job or a due reminder waits until the
  instance wakes. This is accepted while only the product owner and
  one or two first users use it; F11 moves to a paid plan before the
  beta.
- The monthly cost limit is 10 USD until the beta
  ([mvp-roadmap.md](../../../mvp-roadmap.md), section 3). F11 first
  checks that Render's free Postgres plan can hold the data that long;
  if it cannot, the card stops and asks the product owner.
- Staging joins `render.yaml` before the beta (Phase 7), for release
  candidates, Desktop update tests, and the AI evaluation with live
  providers.

### 2.9 CI in every code repository

| Repository | Every pull request runs |
|------------|-------------------------|
| `tripmate-backend` | Ruff, mypy, unit and property tests, integration and API tests against PostgreSQL and Redis service containers, import-linter, one migration head, the access declaration test, the error code text check, Schemathesis against the contract, pip-audit, secret scan, image build |
| `tripmate-contracts` | The breaking-change check against the last tag and the latest draft, the translation check (every key in both languages, valid ICU) |
| `tripmate-web` | ESLint, TypeScript, Vitest, the static build, the generated client and messages against the pinned contracts version |
| `tripmate-mobile` | `flutter analyze`, `flutter test`, the generated client and ARB files against the pinned contracts version, an Android build |
| `tripmate-desktop` | `cargo clippy`, `cargo test` |

The end-to-end smoke set runs in CI against the stack of 2.8: in
`tripmate-backend` with the latest Web release, and in `tripmate-web`
with the backend image of its pinned release.

Every code repository also runs the flow checks of 2.12.

When a repository's CI exists, its checks become required on `main`,
next to the branch protection already set.

### 2.10 The contract pipeline

How drafts and releases work is in
[api-design.md](../../api-design.md), section 6. This epic builds it:

```mermaid
flowchart LR
    M["Merge to main in<br/>tripmate-backend"] --> G["CI generates<br/>openapi.json"]
    G --> P["Pull request in<br/>tripmate-contracts"]
    P --> Q{"Any operation<br/>marked x-stub?"}
    Q -->|Yes| D["Tag a draft:<br/>contracts-vX.Y.Z-draft.N"]
    Q -->|No| V["Tag a release:<br/>contracts-vX.Y.Z"]
```

- A stub route is marked `x-stub: true` in the generated contract and
  returns `501`. Every response schema of a stub carries an example,
  which the mock modes of Web and Mobile return.
- The pull request in `tripmate-contracts` is opened with a token kept
  in the backend's GitHub Actions secrets.

### 2.11 Web and Mobile foundations

| | Web | Mobile |
|---|-----|--------|
| Project | Next.js App Router, TypeScript strict, static export ([ADR-0007](../../adr/0007-web-client-is-a-static-build.md)) | Flutter, with two flavors, `dev` and `prod`, so both apps can be installed on one phone |
| API client | Generated from the pinned contracts version with Orval: typed client, TanStack Query hooks | Generated from the pinned contracts version with OpenAPI Generator, `dart-dio` |
| Mock mode | MSW handlers generated with the client, on when `NEXT_PUBLIC_API_MODE=mock` and in screen tests | A Dio interceptor that answers from the contract's examples, on when built with `--dart-define=API_MODE=mock` and in widget tests |
| Headers sent on every request | `X-Device-Id`; `Idempotency-Key` on creates, kept for retries of the same action | The same |
| Translations | `next-intl` messages generated from the files under `translations/` | ARB files generated from the same source |
| Where it runs | `localhost:3000` against the local stack; in production, a Render static site with every `/join/*` path served the join page | The `dev` flavor against the local stack (`10.0.2.2:8000` from the Android emulator, `localhost:8000` from the iOS simulator); `prod` against production |

A mock card ([docs/development-flow.md](../../development-flow.md),
section 1) runs in mock mode; its integration card switches the same
screens to the real API by configuration only.

**Mobile project conventions.** MF1 sets them up and writes them in
the `CLAUDE.md` of `tripmate-mobile`; every later Mobile card follows
them.

| Topic | Rule |
|-------|------|
| Flutter version | Pinned to 3.38.5 (Dart 3.10.4), the same in CI and on every machine |
| State | `flutter_bloc`: a Cubit for a simple screen, a Bloc for a flow with many events; tested with `bloc_test` |
| Folder layout | By feature: `lib/app/` (flavors, `API_MODE`, router, theme), `lib/core/` (API, translations, storage), `lib/features/<feature>/{data,logic,ui}/`; `test/` mirrors `lib/` |
| Routing | `go_router`, which also opens the `/join/*` Universal Links and App Links |
| Flavors | On Android and iOS. `prod`: application ID `com.tripmate.app`, name "TripMate". `dev`: `com.tripmate.app.dev`, name "TripMate Dev". |
| Lint | `flutter_lints`; CI runs `flutter analyze --fatal-infos --fatal-warnings` |

### 2.12 The flow checks

The rules of [docs/development-flow.md](../../development-flow.md),
section 2.3, are held by five checks. This epic builds them.

| Check | How it works |
|-------|--------------|
| Failing first | Checks out each commit with the trailer `Agent: test` in turn and runs the tests it adds. Each must fail: a test failure or error (pytest exit 1 or 2), or its own module failing to import. A test commit that only changes existing tests, such as a correction after the code, is not asked to fail. |
| Test lock | Locks the tests that the test commits add and every other file under `tests/` that they add or change, such as a `conftest.py` or a helper. The check fails when a commit without the trailer changes, skips, or deletes a locked test or file, or adds or changes any `conftest.py`; and when a test commit changes a file outside `tests/`. |
| Requirement-to-test report | Collects every test name, reads the requirement ID in it, and compares with `tests/requirement-ids.txt`, the P0 IDs in scope. The first card of each epic adds that epic's IDs. The report is kept with the CI run. |
| Mutation | Runs mutation testing on the rule files the pull request changes. A surviving mutant fails the check unless the pull request description lists it under `## Surviving mutants`, one line with its name and a reason. Editing the description runs the check again. Backend only. |
| Risk gate | Matches the changed files against the repository's path list for the High items of development-flow.md, section 2.1. A match, or a path no rule names, needs the label `human-approved`, added after the newest commit reached the pull request; a push removes the label (development-flow.md, section 2.1). |

- The checks are scripts with their own tests, kept in
  `tripmate-backend` and offered as one reusable workflow. The other
  code repositories call it with their own path list, test command,
  and test file pattern; failing first runs each test file of another
  language that a test commit adds, and Python tests per function (F15).
- The path list, the workflows, each `CLAUDE.md`, and the agent roles
  are on the path list themselves.
- On the backend path list, each module's `schemas.py`, `api.py`, and
  `events.py`, all of `app/platform/`, and `app/main.py`,
  `app/worker.py`, and `app/scheduler.py` are High.
- A pull request is judged by the checks of its base, never by its own
  copy: the risk gate runs from `main`'s workflow on
  `pull_request_target`, so a pull request cannot change the check that
  reviews it.
- How each check works in the backend, with its known limits, is in
  the [backend's `CLAUDE.md`, section "Flow checks"](https://github.com/huynguyennang-agilityio/tripmate-backend/blob/main/CLAUDE.md#flow-checks).

## 3. Acceptance Criteria

Each criterion has at least one test named with its requirement
([docs/development-flow.md](../../development-flow.md), section 3).
The requirements are the cross-cutting rows of
[test-strategy.md](../../test-strategy.md), section 5.11.

| Requirement | Criterion | Levels |
|-------------|-----------|--------|
| Business rules 3 and 4, access | A route with no access declaration fails the build | A |
| Business rules 3 and 4, access | A `signed_in` route refuses a missing, expired, or forged token, and a token of an ended session | A |
| Input validation | A request that breaks its schema returns `400 request.invalid` with its fields; the cases are generated from the contract | C, A |
| Integrity | A command that fails part way writes no record, no Audit log entry, and no outbox event | I |
| Idempotency | Each case of 2.4 returns the answer in its row | I, A |
| Realtime | An outbox event is published only after its transaction commits, in `id` order, once per event | I |
| Background work | A job run twice changes nothing the second time; the scheduler enqueues due work after a restart | I |
| Language tests | A registered error code with no text in either language fails CI | C |
| Cross-client API contract tests | A breaking change against the last tag or the latest draft fails CI in `tripmate-contracts`; Web and Mobile build against the pinned version | C |
| Data protection | A log line from a sign-in request holds no email, password, or token | U |
| Performance | The P95 latency metric and its alert exist in production | M |
| Development flow | A test that passes before its code exists, and a locked test that a later commit weakens, each fail CI | U |
| Development flow | A P0 requirement in scope with no test fails CI | U |
| Development flow | A pull request that reaches a High path cannot merge without the product owner's label | U |

## 4. Technical Design

### 4.1 Backend stack

| Concern | Choice |
|---------|--------|
| Language and packages | Python 3.13, `uv` with a lock file |
| Web framework | FastAPI on Uvicorn, Pydantic v2 |
| Database | SQLAlchemy 2 with `asyncpg`; Alembic for migrations |
| Background jobs | Taskiq with `taskiq-redis` ([architecture.md](../../architecture.md), section 12.1) |
| Logs and traces | `structlog`; OpenTelemetry SDK, its OTLP exporter, and its instrumentation for FastAPI, SQLAlchemy, and Redis |
| Error reporting | `sentry-sdk` with its FastAPI integration |
| Tokens and passwords | PyJWT with `cryptography` for EdDSA access tokens; `argon2-cffi` for Argon2id password hashes ([security.md](../../security.md), section 2) |
| Quality | Ruff, mypy in strict mode, import-linter |
| Tests | pytest, Hypothesis, Schemathesis, an HTTP test client; `mutmut` for mutation testing |
| Supply chain | pip-audit, a secret scan, Dependabot |

The skeleton (F1) puts every library in this table in the lock file,
so later cards that run at the same time do not change it.

### 4.2 Data

The tables are in [data-model.md](../../data-model.md), section 6.
F3 sets up Alembic with an empty first migration; F7 and F8 then
create `idempotency_keys` and the outbox tables in their own
migrations. F8 creates `outbox_events` and `outbox_trip_seqs`, the
counter that gives each trip's events their `trip_seq` without a gap
(data-model.md, section 6.2). `outbox_events.trip_id` and
`outbox_trip_seqs.trip_id` get their foreign keys in the EPIC-02
migration that creates `trips`.

`idempotency_keys` holds `device_id` next to `user_id`, which is empty
before sign-in (2.4); data-model.md says so in the same change.

### 4.3 Each repository's `CLAUDE.md` and agent roles

The skeleton card of each repository writes its `CLAUDE.md`: setup,
commands, coding conventions, and a pointer to `../tripmate-docs/` for
the glossary, prd.md, the architecture documents, and the spec of the
epic being built ([architecture.md](../../architecture.md), section
11). This closes the open question of
[docs/development-flow.md](../../development-flow.md), section 5.2.

The same card writes the four agent roles in `.claude/agents/`: the
test agent, the code agent, the test-check agent, and the diff-review
agent, each with what it reads, what it may change, and what it never
does
([docs/development-flow.md](../../development-flow.md), section 2.3).

Each `CLAUDE.md` also points to the shared rules in the `CLAUDE.md` of
`tripmate-docs`, and each repository has a `.gitattributes` that fixes
line endings, because the work runs on macOS and on Windows
([docs/development-flow.md](../../development-flow.md), section 1).

## 5. Decisions and Open Questions

### 5.1 Decisions made in this spec

| Decision | Alternatives set aside | Why |
|----------|------------------------|-----|
| Web and Mobile foundations are in this epic | In EPIC-10, cross-platform experience | The mock cards of EPIC-01 need a project, a generated client, and mock mode before they start |
| A route is a stub when the contract marks it `x-stub` | A label on the pull request; a separate draft branch | The contract itself says what is not built yet, so the tag follows from the file |
| Mock responses come from the contract's examples | Hand-written mock data in each client | One source for both clients; a stub without examples fails CI |
| An idempotency key before sign-in belongs to the device ID | No key on register; a key with no owner | Register creates a record and api-design.md asks for a key on every create |
| The WebSocket gateway is built with the first epic that sends an event to a screen | In this epic | The outbox already publishes to Redis; the gateway's rules (subscriptions, Former members) need trips |
| Two environments until the beta: local in Docker, and production | A preview per pull request and a staging environment from Phase 1 | A team of two reviews in CI and locally; production has no real users before the beta. It saves the Render Pro plan and a second server to keep running. Staging is added before the beta. |
| Mobile has two flavors; mock mode is a build setting | One flavor per environment, and one for mock | A flavor is needed only to install two apps on one phone |
| Sentry takes errors from the backend, Web, and Mobile; Grafana Cloud takes traces, metrics, and alerts; both on free plans | Sentry alone; Google Cloud Observability with Firebase Crashlytics; a self-hosted stack | Both take OpenTelemetry and need no payment card. Sentry has SDKs for all three clients with release tags, and Grafana alerts on P95, job age, and the outbox. |
| A fine-grained GitHub token opens the pull request in `tripmate-contracts`, stored as the backend secret `CONTRACTS_TOKEN` | A GitHub App | Five minutes to set up, limited to one repository. The product owner creates it with Contents and Pull requests set to read and write and a one-year expiry, and renews it before it expires. The publishing job runs only on pushes to `main`, never on a pull request, so a changed workflow cannot reach the token. |
| TripMate gets its own `.com` domain through Cloudflare Registrar, bought by the product owner before the beta; production uses `app.` and `api.` under it | `onrender.com` addresses; a free or first-year-discount domain | The Web refresh cookie is `SameSite=Strict` and needs the Web client and the API on one site ([security.md](../../security.md), section 2.1). Invitation links and app links carry the domain, so it must not change once real users have them. Before the beta, production has no real users and runs on `onrender.com`; locally both are `localhost`. |
| The flow checks are scripts with their own tests, shared as one reusable workflow from `tripmate-backend` | A copy in each repository; a marketplace action | One place to change a gate, and the gate is tested like any other code |
| A test commit is marked by a trailer in its message | A separate branch or pull request for tests | One pull request per card stays the rule; the trailer is enough for CI to tell the two kinds of commit apart |
| The requirement IDs in scope are a file in each code repository | CI reads prd.md from `tripmate-docs` | A code repository's CI needs nothing outside it, and the scope grows epic by epic |
| A rate-limited route returns `503 server.unavailable` when Redis does not answer | Let the request through without counting | A limit that cannot be counted is not skipped: sign-in and sign-up limits are a security control |
| Until the beta, production is one instance for the three processes, with free Postgres and Key Value plans | The full setup from the first deploy | One or two people use it before the beta, and the monthly cost limit is 10 USD. The cost: no point-in-time recovery, and a short stop at each deploy. The full setup returns before the beta. |
| Until the beta, the one web instance is on Render's free plan | The Starter plan, about 7 USD a month, which never sleeps | Starter would leave about 3 USD a month for Claude and Google Maps. The cost: the instance sleeps when idle, so the first request is slow and jobs wait until it wakes (2.8). |
| The skeleton makes one file per part of `platform`, finds modules by scanning, and installs every dependency at once | Each card creates what it needs | Cards that run at the same time must not change the same file. The lock file and the app's start-up file are where two cards would otherwise meet. |
| Translations are one file per area in each language, `translations/en/<area>.json` | One `en.json` and one `vi.json` | Web, Mobile, and the backend add keys at the same time, from three machines; one file per area keeps their changes apart |
| The Web and Mobile skeleton cards need no contract; generated messages and the flow checks move to WF2 and MF2 | WF1 and MF1 wait for CT1 | The three machines start on the first day instead of two waiting for the backend's first three cards |
| Mobile uses `flutter_bloc`, `go_router`, a folder per feature, and a pinned Flutter version (2.11) | Riverpod; Navigator with hand-written deep links; folders per layer; the latest stable Flutter in CI | Cubits and Blocs are tested with `bloc_test` from a state and an event, which suits tests written before the code. `go_router` opens the join links. A folder per feature keeps cards that run at the same time apart. A pinned version gives CI and every machine the same result. |
| MF1 has one automated test, MF1-4, next to its manual cases | Manual cases only | `flutter test` needs a test to run, and the test agent needs a case that fails before the code exists |

### 5.2 Open questions

| Question | Proposed answer | Needed by |
|----------|-----------------|-----------|
| Is the WebSocket gateway part of EPIC-02 or EPIC-03? | EPIC-02, if its exit criterion "Web and Mobile display consistent trip information" needs live updates; otherwise EPIC-03 | EPIC-02 spec |

## 6. Tasks

The cards of this epic are in one task file per code repository
([docs/development-flow.md](../../development-flow.md), section 1).
Each task there holds its scope, what it leaves out, its risk level
with the reason, its Done when, its test cases, and its manual checks.
This section keeps what spans repositories: the order of the cards,
the checkpoints, and which machine runs what.

| Repository | Task file | Cards |
|------------|-----------|-------|
| `tripmate-backend` | [tasks/EPIC-11.md](https://github.com/huynguyennang-agilityio/tripmate-backend/blob/main/tasks/EPIC-11.md) | F1 to F15 |
| `tripmate-contracts` | [tasks/EPIC-11.md](https://github.com/huynguyennang-agilityio/tripmate-contracts/blob/main/tasks/EPIC-11.md) | CT1, CT2 |
| `tripmate-web` | [tasks/EPIC-11.md](https://github.com/huynguyennang-agilityio/tripmate-web/blob/main/tasks/EPIC-11.md) | WF1 to WF3 |
| `tripmate-mobile` | [tasks/EPIC-11.md](https://github.com/huynguyennang-agilityio/tripmate-mobile/blob/main/tasks/EPIC-11.md) | MF1, MF2 |
| `tripmate-desktop` | [tasks/EPIC-11.md](https://github.com/huynguyennang-agilityio/tripmate-desktop/blob/main/tasks/EPIC-11.md) | DF1 |

Most cards of this epic are High, because they build what the High
list protects: CI, the checks, hosting, the access guard, and
migrations. F1, F2, and F14 come first, so the checks exist before the
other cards start. WF1 and MF1 need no contract and start on the first
day.

```mermaid
flowchart LR
    F1 --> F2 --> F14
    F2 --> F13
    F14 --> F15
    F14 --> CT1
    F14 --> DF1
    F1 --> F3
    F1 --> F4 --> F5 --> F6
    F3 --> F7
    F5 --> F7
    F3 --> F8
    F7 --> F9
    F8 --> F9
    F4 --> F10
    F9 --> F11
    F10 --> F11
    CT1 --> F4
    CT1 --> F12
    F2 --> F12 --> CT2
    CT1 --> CT2
    WF1 --> WF2
    CT2 --> WF2
    F15 --> WF2
    WF2 --> WF3
    F11 --> WF3
    MF1 --> MF2
    CT2 --> MF2
    F15 --> MF2
```

### 6.1 Checkpoints

| After | The product owner checks |
|-------|--------------------------|
| F14 | On throwaway pull requests: a test that passes before its code, a locked test weakened by a later commit, and a migration with no label each fail CI. From here a Low card merges on its own. |
| F5 | A `signed_in` test route answers with each error of 2.3, and removing its declaration fails CI |
| F11 | `docker compose up` runs the whole stack, and the health check answers locally and in production |
| CT2, WF2, MF2 | A stub route becomes a draft tag, and the test screen on Web and on Mobile shows its example in mock mode. EPIC-01 can start with B0. |

### 6.2 Machines and parallel work

The work runs on three machines, one per group of repositories
([docs/development-flow.md](../../development-flow.md), section 1), so
no two machines change the same code repository.

| Wave | Mac 1: backend and contracts | Mac 2: Mobile | Windows: Web and Desktop |
|------|------------------------------|---------------|--------------------------|
| 1 | F1, then F2, then F14 | MF1 | WF1 |
| 2 | CT1, F3, F13 | -- | DF1 |
| 3 | F4, F8, F12, F15, then CT2 | MF2 | WF2 |
| 4 | F5, F10, then F6 and F7 | -- | -- |
| 5 | F9, then F11 | -- | WF3 |

- Cards in one cell of Mac 1 after wave 1 can run at the same time,
  each in its own git worktree and its own session.
- Two cards with a migration, F7 and F8, merge one after the other;
  the second one rebases so there is one migration head.
- The product owner reviews the backend's pull requests first: the
  other two machines wait on the contract.

## 7. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-11-20 | First version: scope of the first part of EPIC-11, what the platform gives every epic (backend layout, request pipeline, errors, idempotency, outbox and background work, observability, configuration and health check, Render environments, CI, the contract pipeline, Web and Mobile foundations), two environments until the beta (local and production), acceptance criteria, technical design, decisions and open questions, and 20 cards with checkpoints. |
| 1.1 | 2026-11-20 | The product owner answered three open questions, now decisions in section 5.1: Sentry and Grafana Cloud on free plans; a fine-grained GitHub token for contract pull requests, used only on pushes to `main`; a `.com` domain through Cloudflare Registrar, bought before the beta. |
| 1.2 | 2026-11-23 | Follows the new development flow. Every card has a risk level (section 6); all but F6 are High. Section 7 is new: the test cases of every card, with error and edge cases and their expected results. Section 2.12 and two new cards build the flow checks: F13, the requirement-to-test report, and F14, failing first, test lock, mutation, and the risk gate, with the agent roles. F14 now comes before CT1 and DF1. Each skeleton card also writes the agent roles. One open question added: rate limits when Redis does not answer. 22 cards. |
| 1.3 | 2026-11-23 | Approved by the product owner, with the proposed answer on rate limits: a rate-limited route returns `503 server.unavailable` when Redis does not answer (2.2, 2.3, decision in 5.1, case F6-6). The WebSocket gateway question stays open for the EPIC-02 spec. |
| 1.4 | 2026-11-23 | The product owner set the monthly cost limit to 10 USD until the beta. Section 2.8: until the beta, production is one instance that runs the API, the worker, and the scheduler, with free Postgres and Key Value plans; the full setup returns before the beta. Card F11 follows, checks the free Postgres plan first, and gains case F11-6. Decision added to 5.1. |
| 1.5 | 2026-11-23 | The work runs on three machines, and cards run at the same time. New 6.7: which machine builds what, in which wave. The skeleton (F1) makes one file per part of `platform`, finds modules by scanning, and installs every dependency (2.1; cases F1-7, F1-8). WF1 and MF1 need no contract and start on the first day; generated messages and the flow checks move to WF2 and MF2, with their cases. Translations are one file per area in each language. CI checks for one migration head (case F2-6). Every repository has a `.gitattributes`. Three decisions added to 5.1. |
| 1.6 | 2026-11-23 | The product owner set the Mobile project conventions (2.11): Flutter 3.38.5 pinned, `flutter_bloc`, `go_router`, a folder per feature, flavors on Android and iOS with their application IDs, and `flutter_lints` with warnings as errors. MF1 follows them and gains case MF1-4, an automated test of the flavor name. Section 6.7: no two machines change the same code repository; `tripmate-docs` may be changed from any machine. Two decisions added to 5.1. |
| 1.7 | 2026-11-23 | Section 4.1 lists the libraries later cards need, so the skeleton puts them all in the lock file: the OpenTelemetry exporter and instrumentation, `sentry-sdk`, PyJWT with `cryptography`, and `argon2-cffi`. Until the beta, the one production web instance is on Render's free plan, which sleeps when idle (2.8, decision added to 5.1). The table of decisions in 5.1 is one table again, so the page shows all its rows. |
| 1.8 | 2026-11-25 | Follows development-flow.md: the cards and their test cases move to a task file in each code repository, with each card's scope, what it leaves out, the reason for its risk level, and its manual checks. Section 6 keeps the order of the cards, the checkpoints (6.1), and the machines (6.2), and links the five task files; section 7, Test Cases, is removed, and the Version History is now section 7. Each skeleton card writes four agent roles (4.3): test, code, test-check, and diff review. |
| 1.9 | 2026-11-26 | Section 2.12 says what the flow checks do as built in F14: failing first checks each test commit in turn and accepts a failure, an error, or the test's own module failing to import; the test lock also covers the support files under `tests/` that a test commit added or changed and any `conftest.py`, and a test commit changes files under `tests/` only; surviving mutants are listed under `## Surviving mutants` in the pull request description; `human-approved` counts only when added after the newest commit, and a push removes it; the backend's High paths; the risk gate runs from `main`'s workflow, so a pull request cannot change the check that reviews it. Section 4.2: F7 and F8 create `idempotency_keys` and `outbox_events` in their own migrations after the empty first one. |
| 2.0 | 2026-11-26 | Section 4.2 and the table of what other documents own: F8 creates `outbox_trip_seqs` next to `outbox_events`, and the EPIC-02 migration adds the foreign key on the `trip_id` of both tables. |
| 2.1 | 2026-11-26 | New card F15, as the product owner decided during CT1: failing first read only Python tests, so it learns each repository's test file pattern and runs the added test files of any language. Section 2.12, the order of the cards, and wave 3 follow. |
| 2.2 | 2026-11-26 | Section 2.3, as the product owner decided during F4: the backend pins `tripmate-contracts` by commit SHA until CT2, and F4 adds four codes: the two field codes of `request.invalid`, `request.not_found`, and `request.method_not_allowed`. |
