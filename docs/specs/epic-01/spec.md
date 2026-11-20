# TripMate -- EPIC-01 Spec: Authentication and User Profiles

**Document type:** Epic Spec\
**Product:** TripMate\
**Status:** Proposed\
**Version:** 1.3\
**Stage:** 2--4, epic level\
**Epic:** EPIC-01, Phase 1\
**Page version:** [TripMate EPIC-01 Spec artifact](https://claude.ai/artifact/CDUhq8v5rqC2f3neCN53Rs)

Terms follow [GLOSSARY.md](../../../GLOSSARY.md). The requirements are
FR-01 in [prd.md](../../../prd.md). This spec does not repeat what other
documents own; it links to them:

| Topic | Owned by |
|-------|----------|
| Passwords, tokens, sessions, rate limits | [security.md](../../security.md), section 2 |
| Endpoints and the error format | [api-design.md](../../api-design.md), sections 3.1 and 4 |
| Tables `users`, `credentials`, `sessions` | [data-model.md](../../data-model.md), section 2.1 |
| Where authentication runs, and why | [ADR-0005](../../adr/0005-authentication-built-into-the-backend.md) |
| Screens Welcome, Profile setup, Profile | [information-architecture.md](../../information-architecture.md), section 2 |
| What each test level proves | [test-strategy.md](../../test-strategy.md), section 5.1 |

This spec answers *how accounts behave in the MVP, how they are built,
and which cards build them*.

## 1. Scope

| In this epic | Priority | Out of this epic |
|--------------|----------|------------------|
| AUTH-01 register and sign in with email and password | P0 | Social sign-in, AUTH-05 (P1) |
| AUTH-02 sign out, and see and end signed-in devices | P0 | Password reset by email, AUTH-06 (P1, after the MVP) |
| AUTH-03 view and edit the profile: display name | P0 | Avatar, AUTH-04 (P1) |
| | | Changing the email, deleting the account, email verification |

The P1 items get their sections in a later version of this spec, in the
change that schedules them ([test-strategy.md](../../test-strategy.md),
section 5.12).

## 2. Behaviour

### 2.1 Register (AUTH-01)

```mermaid
flowchart LR
    W["Welcome"] --> R["Register:<br/>email, password,<br/>display name"]
    R -->|valid| S["Signed in"] --> P["Profile setup"] --> T["My trips"]
    R -->|invalid| R
    W --> L["Sign in:<br/>email, password"]
    L -->|valid| T
    L -->|wrong| L
```

| Rule | Detail |
|------|--------|
| Email | Trimmed; compared without case (`citext`); one account per email |
| Password | At least 10 characters, not on the list of common passwords ([security.md](../../security.md), section 2) |
| Display name | Required at registration: 1 to 40 characters after trimming, any script, no line breaks |
| After registering | The user is signed in at once: the response carries the tokens, as sign-in does |
| First screen | Profile setup, then My trips. If the user came from an Invitation link, the Invitation preview follows ([information-architecture.md](../../information-architecture.md), section 7.1) |

### 2.2 Sign in (AUTH-01)

| Rule | Detail |
|------|--------|
| Wrong email or wrong password | The same answer, `401 auth.invalid_credentials`, so the screen never says which one was wrong |
| Too many attempts | `429 rate.limited` with `Retry-After`, keyed by email and by IP address ([security.md](../../security.md), section 2.2) |
| Result | A new session for this device, an access token, and a refresh token |

### 2.3 Sessions and sign out (AUTH-02)

```mermaid
stateDiagram-v2
    [*] --> Active: sign in or register
    Active --> Active: refresh (token replaced)
    Active --> Ended: sign out on this device
    Active --> Ended: ended from another device
    Active --> Ended: replaced refresh token presented again
    Active --> Ended: 30 days with no refresh
    Ended --> [*]
```

| Rule | Detail |
|------|--------|
| One session per device | Named from the device type and the client, for example "iPhone · TripMate app" or "Chrome on macOS · Web" |
| Refresh | The refresh token is replaced at every use; the old one stops working at once |
| Reuse of an old refresh token | Ends that whole session. The device that presented it must sign in again. |
| Sign out | Ends this device's session and clears its tokens; the user lands on Welcome |
| Devices list | On Profile: every active session with its name and last use; the current one is marked and cannot be ended from the list |
| End a device | Ends that session at once; its next request fails with `401 auth.token_expired`, and its refresh fails with `401 auth.session_ended` |
| Sign out other devices | Ends every session except the current one |
| Access token expiry | 15 minutes. A client refreshes once on `401 auth.token_expired`, then retries the request once. If the refresh fails, the user lands on Welcome. |

### 2.4 Profile (AUTH-03)

| Rule | Detail |
|------|--------|
| What the profile shows | Display name, email (read only), the number of trips by group, signed-in devices, Sign out |
| What can be edited | The display name, with the rules of 2.1 |
| Who | Only the user, through `/v1/me`; there is no endpoint that reads or edits another user's profile |
| Where a display name shows | Everywhere the user appears in a trip, for every Member, after the next load or realtime update |

### 2.5 Errors this epic adds

| Status | Code | When |
|--------|------|------|
| `400` | `request.invalid` with `fields` | Email malformed; password or display name breaks a rule. Field codes: `auth.password_too_short`, `auth.password_too_common`, `profile.display_name_invalid` |
| `401` | `auth.invalid_credentials` | Wrong email or password |
| `401` | `auth.session_ended` | A refresh for a session that was ended or revoked |
| `409` | `auth.email_taken` | Register with an email that has an account |

`auth.not_signed_in` and `auth.token_expired` already exist
([api-design.md](../../api-design.md), section 4.2). Every code has text
in both languages before its card is Done.

## 3. Acceptance Criteria

Each criterion has at least one test named with its requirement ID
([docs/development-flow.md](../../development-flow.md), section 3).

| ID | Criterion | Levels |
|----|-----------|--------|
| AUTH-01 | A user registers with email, password, and display name, and is signed in | I, A, S, E |
| AUTH-01 | A password is stored only as an Argon2id hash; a short or common password is refused | U, I |
| AUTH-01 | An email that differs only in case is the same account | I, A |
| AUTH-01 | Wrong email and wrong password give the same answer | A |
| AUTH-01 | Sign-in and sign-up are rate limited | A |
| AUTH-02 | A refresh replaces the refresh token, and the old one no longer works | I, A |
| AUTH-02 | Presenting a replaced refresh token ends the session | I, A |
| AUTH-02 | Sign out ends the session at once | A |
| AUTH-02 | A user lists their devices and ends another one; that device's next refresh fails | A |
| AUTH-02 | Each client keeps the refresh token where [security.md](../../security.md), section 2.1, says, and never in `localStorage` | S, M |
| AUTH-03 | A user reads and edits only their own profile | A |
| AUTH-03 | A changed display name shows in every trip of the user | I, S |
| FR-01 | Every endpoint except register, sign-in, refresh, and the health check refuses a missing, expired, or forged token (generated from the contract) | A |

## 4. Technical Design

### 4.1 Module and dependencies

All backend work is in the `identity` module
([architecture.md](../../architecture.md), section 4). It needs the
EPIC-11 platform foundation first: the access guard, error codes,
idempotency keys, structured logging, and CI
([EPIC-11 spec](../epic-11/spec.md)).

### 4.2 Endpoints

The endpoints are listed in [api-design.md](../../api-design.md),
section 3.1. This epic builds all of them except
`GET /v1/me/readiness-summary` (EPIC-13).

| Endpoint | Token | Idempotency-Key | Notes |
|----------|-------|-----------------|-------|
| `POST /v1/auth/register` | None | Required | Returns the same body as sign-in, with `201` |
| `POST /v1/auth/login` | None | Not taken (5.2) | |
| `POST /v1/auth/refresh` | Refresh token | Not taken (5.2) | Web sends the cookie; Mobile and Desktop send the token in the body |
| `POST /v1/auth/logout` | Access | -- | Web also clears the cookie |
| `GET /v1/auth/sessions`, `DELETE /v1/auth/sessions/{id}`, `POST /v1/auth/sessions/end-others` | Access | -- | `end-others` is new in this epic; api-design.md lists it in the same change |
| `GET /v1/me`, `PATCH /v1/me` | Access | -- | No `If-Match`: only the user changes their profile |

### 4.3 Data

The tables are in [data-model.md](../../data-model.md), section 2.1.
This epic adds:

- `sessions.last_used_at`, updated at each refresh, for the devices
  list.
- `sessions.replaced_token_hash`, the previous refresh token's hash, so
  a reused token can be recognized and its session ended.

Account changes are not trip-scoped, so they write no Audit log entry;
sign-in, sign-out, and session ends are written to the structured log
without the email ([security.md](../../security.md), section 4).

### 4.4 Clients

| Client | Work |
|--------|------|
| Web | Welcome, Register, Sign in, Profile setup, Profile with devices; refresh on `401 auth.token_expired`; refresh cookie as in security.md |
| Mobile | The same screens; refresh token in `flutter_secure_storage` |
| Desktop | The Web screens; one Rust command that stores, reads, and deletes the refresh token in the operating system's store |

## 5. Decisions and Open Questions

### 5.1 Decisions made in this spec

| Decision | Alternatives set aside | Why |
|----------|------------------------|-----|
| The display name is asked at registration and is P0 | Only with AUTH-04, which is P1 | A Member must be shown by name in the discussion, in Votes, and in Expenses; avatar stays P1 |
| Register says when an email is taken | The same answer whether or not the account exists | The user needs to know to sign in instead. Sign-up is rate limited to 5 per hour per IP address, which keeps guessing slow. |
| No email verification in the MVP | Verify the email before the first sign-in | No email service is chosen before AUTH-06 ([architecture.md](../../architecture.md), section 12.2); an unverified email is never used to link a Google or Apple account ([security.md](../../security.md), section 2) |
| No Audit log entry for account changes | Audit sign-ins | The Audit log is per trip (business rule 13); account events go to the structured log |

### 5.2 Open questions

| Question | Proposed answer | Needed by |
|----------|-----------------|-----------|
| Do sign-in and refresh take an `Idempotency-Key`? [api-design.md](../../api-design.md), section 2, asks for one on every `POST` that creates a record, and a session is a record. | No. A repeated sign-in makes one more session, which the user can end; a repeated refresh is refused as a reused token. api-design.md names the exception in the same change. | AUTH-01 card |
| prd.md, AUTH-06, says a user who forgets their password "signs in with Google or Apple", but both are P1. What does the MVP offer? | Nothing in the app; the product owner resets the password by hand on request during the beta | Phase 7 |

## 6. Tasks

Each row is one card on the [TripMate board](https://trello.com/b/zsxAnzsz/tripmate),
with the ID of the row in its title, for example
`B2 AUTH-01 Register`. Every card is one behaviour a user or a test
can see working, small enough for one focused session:

| Size | Means |
|------|-------|
| XS | One rule or one setting |
| S | One endpoint or one screen, with its tests |
| M | One behaviour across a few parts, for example an endpoint with its table change and rate limit |

A card that would be larger is split before it moves to ToDo. Every
card also meets the Definition of Done
([docs/development-flow.md](../../development-flow.md), section 3); the
files it changes are named in its plan, in step 2 of that flow.

The backend and the clients are built at the same time: B0 publishes a
draft contract, Web and Mobile build every screen against a mock API
generated from it (cards ending in `a`), and each screen is switched
to the real API once the contract is released (cards ending in `b`).
The card kinds are defined in
[docs/development-flow.md](../../development-flow.md), section 1.

```mermaid
flowchart LR
    F["EPIC-11<br/>foundation"] --> B0 --> C0
    B0 --> B1 --> B2 --> B3 --> B4 --> B6
    B3 --> B5
    B2 --> B7
    B5 --> B8
    B6 --> B8
    B7 --> B8
    B8 --> C1
    C0 --> WA["W1a to W6a<br/>Web, mock"]
    C0 --> MA["M1a to M6a<br/>Mobile, mock"]
    C1 --> WB["W1b to W6b<br/>Web, integration"]
    C1 --> MB["M1b to M6b<br/>Mobile, integration"]
    WA --> WB
    MA --> MB
    WB --> D1 --> D2
```

### 6.1 Backend: `tripmate-backend`, module `identity`

| ID | Card | Size | Depends on | Done when |
|----|------|------|------------|-----------|
| B0 | `AUTH-01 Accounts contract stub` | S | EPIC-11 foundation | Every endpoint of 4.2 exists with its request and response schemas and the error codes of 2.5, and returns `501`; CI publishes the draft contract |
| B1 | `AUTH-01 Account tables and input rules` | S | B0 | Migration for `users`, `credentials`, `sessions` with the fields of 4.3; Argon2id hashing; the email, password, and display name rules of 2.1 as unit tests |
| B2 | `AUTH-01 Register` | M | B1 | `POST /v1/auth/register` with `Idempotency-Key` returns `201` and tokens; `409 auth.email_taken`, also for an email in other case; sign-up rate limit |
| B3 | `AUTH-01 Sign in` | S | B2 | `POST /v1/auth/login` makes a session; wrong email and wrong password both give `401 auth.invalid_credentials`; rate limits by email and by IP address |
| B4 | `AUTH-02 Refresh with token rotation` | M | B3 | `POST /v1/auth/refresh` replaces the refresh token and sets `last_used_at`; a replaced token ends the session; an ended session gives `401 auth.session_ended` |
| B5 | `AUTH-02 Sign out` | XS | B3 | `POST /v1/auth/logout` ends the session at once and clears the Web cookie |
| B6 | `AUTH-02 Devices list and ending devices` | M | B4 | `GET /v1/auth/sessions` marks the current one; `DELETE /v1/auth/sessions/{id}` refuses the current one; `POST /v1/auth/sessions/end-others`; an ended device's next refresh fails |
| B7 | `AUTH-03 Read and edit the profile` | S | B2 | `GET` and `PATCH /v1/me` with the display name rules; no way to read another user; the new name shows in a trip |
| B8 | `FR-01 Protected endpoints test` | S | B5, B6, B7 | A test generated from the contract: every endpoint except register, sign-in, refresh, and the health check refuses a missing, expired, or forged token |

### 6.2 Contract: `tripmate-contracts`

| ID | Card | Size | Depends on | Done when |
|----|------|------|------------|-----------|
| C0 | `AUTH-01 Accounts contract draft` | XS | B0 | The draft `openapi.json` is tagged, for example `contracts-v1.1.0-draft.1`; every error code of 2.5 has text in both languages |
| C1 | `AUTH-01 Accounts contract release` | XS | B8 | The released `openapi.json` is tagged; the contract check against the last draft passes |

### 6.3 Web: `tripmate-web`

| ID | Card | Size | Depends on | Done when | Design |
|----|------|------|------------|-----------|--------|
| W1a | `AUTH-01 Welcome and Register (Web, mock)` | S | C0 | Register shows each field error of 2.5 in both languages and signs the user in | [Web prototype](https://claude.ai/artifact/4prwGmgBsXBv5Jvnc3aEUo) |
| W1b | `AUTH-01 Welcome and Register (Web, integration)` | XS | C1, W1a | The account is created on the local stack; a taken email shows `auth.email_taken` | [Web prototype](https://claude.ai/artifact/4prwGmgBsXBv5Jvnc3aEUo) |
| W2a | `AUTH-01 Sign in (Web, mock)` | S | W1a | Sign in, with the one wrong-credentials message and the rate limit message | [Web prototype](https://claude.ai/artifact/4prwGmgBsXBv5Jvnc3aEUo) |
| W2b | `AUTH-01 Sign in (Web, integration)` | S | C1, W2a | Sign in works on the local stack; the start of journey J2 passes | [Web prototype](https://claude.ai/artifact/4prwGmgBsXBv5Jvnc3aEUo) |
| W3a | `AUTH-02 Token refresh and sign out (Web, mock)` | S | W2a | One refresh on `401 auth.token_expired`, then one retry; a failed refresh or Sign out lands on Welcome; no token in `localStorage` | [Web prototype](https://claude.ai/artifact/4prwGmgBsXBv5Jvnc3aEUo) |
| W3b | `AUTH-02 Token refresh and sign out (Web, integration)` | S | C1, W3a | The refresh cookie works with the local stack; a reused token ends the session | [Web prototype](https://claude.ai/artifact/4prwGmgBsXBv5Jvnc3aEUo) |
| W4a | `AUTH-03 Profile setup (Web, mock)` | S | W2a | Shown once after registering, then My trips, or the Invitation preview when the user came from a link | [Web prototype](https://claude.ai/artifact/4prwGmgBsXBv5Jvnc3aEUo) |
| W4b | `AUTH-03 Profile setup (Web, integration)` | XS | C1, W4a | The display name is saved on the local stack | [Web prototype](https://claude.ai/artifact/4prwGmgBsXBv5Jvnc3aEUo) |
| W5a | `AUTH-03 Profile and display name (Web, mock)` | S | W4a | Profile shows the fields of 2.4; editing the display name follows the rules of 2.1 | [Web prototype](https://claude.ai/artifact/4prwGmgBsXBv5Jvnc3aEUo) |
| W5b | `AUTH-03 Profile and display name (Web, integration)` | XS | C1, W5a | The edited name is read back from `GET /v1/me` | [Web prototype](https://claude.ai/artifact/4prwGmgBsXBv5Jvnc3aEUo) |
| W6a | `AUTH-02 Devices on Profile (Web, mock)` | S | W3a, W5a | List with the current device marked; end one device; sign out other devices | [Web prototype](https://claude.ai/artifact/4prwGmgBsXBv5Jvnc3aEUo) |
| W6b | `AUTH-02 Devices on Profile (Web, integration)` | XS | C1, W6a | Ending a device on the local stack signs that device out | [Web prototype](https://claude.ai/artifact/4prwGmgBsXBv5Jvnc3aEUo) |

### 6.4 Mobile: `tripmate-mobile`

| ID | Card | Size | Depends on | Done when | Design |
|----|------|------|------------|-----------|--------|
| M1a | `AUTH-01 Welcome and Register (Mobile, mock)` | S | C0 | As W1a, with widget tests | [Mobile prototype](https://claude.ai/artifact/MS8Hfa77SzLyhwFwnfFAen) |
| M1b | `AUTH-01 Welcome and Register (Mobile, integration)` | XS | C1, M1a | As W1b | [Mobile prototype](https://claude.ai/artifact/MS8Hfa77SzLyhwFwnfFAen) |
| M2a | `AUTH-01 Sign in (Mobile, mock)` | S | M1a | As W2a, with widget tests | [Mobile prototype](https://claude.ai/artifact/MS8Hfa77SzLyhwFwnfFAen) |
| M2b | `AUTH-01 Sign in (Mobile, integration)` | S | C1, M2a | As W2b | [Mobile prototype](https://claude.ai/artifact/MS8Hfa77SzLyhwFwnfFAen) |
| M3a | `AUTH-02 Token refresh and sign out (Mobile, mock)` | S | M2a | Refresh token only in `flutter_secure_storage`; refresh and sign out as W3a; tests for storage and refresh | [Mobile prototype](https://claude.ai/artifact/MS8Hfa77SzLyhwFwnfFAen) |
| M3b | `AUTH-02 Token refresh and sign out (Mobile, integration)` | S | C1, M3a | As W3b | [Mobile prototype](https://claude.ai/artifact/MS8Hfa77SzLyhwFwnfFAen) |
| M4a | `AUTH-03 Profile setup (Mobile, mock)` | S | M2a | As W4a, with widget tests | [Mobile prototype](https://claude.ai/artifact/MS8Hfa77SzLyhwFwnfFAen) |
| M4b | `AUTH-03 Profile setup (Mobile, integration)` | XS | C1, M4a | As W4b | [Mobile prototype](https://claude.ai/artifact/MS8Hfa77SzLyhwFwnfFAen) |
| M5a | `AUTH-03 Profile and display name (Mobile, mock)` | S | M4a | As W5a, with widget tests | [Mobile prototype](https://claude.ai/artifact/MS8Hfa77SzLyhwFwnfFAen) |
| M5b | `AUTH-03 Profile and display name (Mobile, integration)` | XS | C1, M5a | As W5b | [Mobile prototype](https://claude.ai/artifact/MS8Hfa77SzLyhwFwnfFAen) |
| M6a | `AUTH-02 Devices on Profile (Mobile, mock)` | S | M3a, M5a | As W6a, with widget tests | [Mobile prototype](https://claude.ai/artifact/MS8Hfa77SzLyhwFwnfFAen) |
| M6b | `AUTH-02 Devices on Profile (Mobile, integration)` | XS | C1, M6a | As W6b | [Mobile prototype](https://claude.ai/artifact/MS8Hfa77SzLyhwFwnfFAen) |

### 6.5 Desktop: `tripmate-desktop`

Desktop has no screens of its own, so its cards are not split.

| ID | Card | Size | Depends on | Done when | Design |
|----|------|------|------------|-----------|--------|
| D1 | `AUTH-02 Refresh token command (Desktop)` | S | W3b; the DESK-01 shell | One Rust command stores, reads, and deletes the refresh token in the operating system's store: Keychain, Windows Credential Manager, or Secret Service on Linux ([security.md](../../security.md), section 2.1); `cargo test` passes | [Desktop prototype](https://claude.ai/artifact/UHEF5bSEzMDa4k2z62cRRJ) |
| D2 | `AUTH-02 Stay signed in after restart (Desktop)` | S | D1 | The Web build uses the command on Desktop. Checked by hand on macOS, Windows, and Ubuntu LTS: restart keeps the user signed in, and Sign out removes the token. On Linux with no Secret Service, the app still works and asks the user to sign in at each start. | [Desktop prototype](https://claude.ai/artifact/UHEF5bSEzMDa4k2z62cRRJ) |

### 6.6 Checkpoints

| After | The product owner checks |
|-------|--------------------------|
| C0 | The draft contract: every request, response, and error code the screens need, before the mock cards start |
| B3 and W2a | Register and sign in through the API on the local stack, and the same screens against the mock |
| B8 | Every backend row of section 3 has a passing test, before the contract is released |
| The last card | Every row of section 3 has a passing test on every client it names; sign in, edit the profile, and end a device on Web, Mobile, and Desktop |

## 7. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-11-20 | First version: scope (AUTH-01 to AUTH-03; AUTH-04 to AUTH-06 later), behaviour for register, sign-in, sessions and profile, the error codes it adds, acceptance criteria by requirement ID, technical design, decisions and open questions, and 23 cards of size XS to M with checkpoints. |
| 1.1 | 2026-11-20 | Section 6: the backend and the clients are built at the same time. B0 publishes a draft contract (C0); every Web and Mobile card is split into a mock card against the draft and an integration card against the released contract (C1). 37 cards; checkpoints in their own table. |
| 1.2 | 2026-11-20 | Cards D1 and D2 cover Linux: the refresh token goes to Secret Service, D2 is checked by hand on Ubuntu LTS as well, and without a Secret Service the user signs in at each start. D2 is now size S. |
| 1.3 | 2026-11-20 | Integration cards work against the local stack in Docker instead of a preview backend; section 4.1 links the EPIC-11 spec for the foundation. |
