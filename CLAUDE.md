# TripMate Docs -- Rules for Contributors and AI Agents

This repository holds TripMate's product documents. Code lives in
separate repositories. These rules apply to every change, by people or
by AI agents such as Claude Code.

## What is here

| File | Purpose |
|------|---------|
| [README.md](README.md) | Where to start: what to read for which question, how the documents fit together, and links to the live pages. |
| [GLOSSARY.md](GLOSSARY.md) | Domain terms. Use these words everywhere; avoid the listed alternatives. |
| [product-vision.md](product-vision.md) | What TripMate is and why. |
| [prd.md](prd.md) | What the MVP must do: requirements, business rules, acceptance criteria. |
| [mvp-roadmap.md](mvp-roadmap.md) | Phases, milestones, release gates. |
| [product-workflow.md](product-workflow.md) | How we go from problem to release, and which document belongs to which stage. |
| [docs/discovery.md](docs/discovery.md) | The assumptions TripMate rests on, how each is tested, and what real groups told us. |
| [docs/solution-options.md](docs/solution-options.md) | Which options were considered for each problem, and why features are in or out of the MVP. |
| [docs/information-architecture.md](docs/information-architecture.md) | Where things live in the product and how people move between them, for every platform: places, Navigation Map, navigation rules. |
| [docs/ux-review.md](docs/ux-review.md) | Usability problems found in the prototypes, how serious they are, and the fixes. |
| [docs/architecture.md](docs/architecture.md) | How the system is organised: drivers, containers, modules, change flow, integrations, clients, hosting, repositories. |
| [docs/data-model.md](docs/data-model.md) | What TripMate stores: entities, ERD, conventions, database constraints. |
| [docs/api-design.md](docs/api-design.md) | How clients talk to the backend: REST conventions, resources, error codes, realtime protocol, the contract across repositories. |
| [docs/security.md](docs/security.md) | How accounts, trips, and money records are kept safe: authentication, capabilities, data protection, threats. |
| [docs/test-strategy.md](docs/test-strategy.md) | How TripMate is tested: test levels, the requirements-to-test matrix, the AI evaluation plan. |
| [docs/ai-golden-dataset.md](docs/ai-golden-dataset.md) | The cases the AI assistant is evaluated on, and what is expected in each. |
| [docs/development-flow.md](docs/development-flow.md) | How a task goes from Trello card to merged: the board, the steps, the Definition of Done, defects. |
| [docs/specs/epic-01/spec.md](docs/specs/epic-01/spec.md) | EPIC-01: how accounts behave, how they are built, and which cards build them. |
| [docs/specs/epic-11/spec.md](docs/specs/epic-11/spec.md) | EPIC-11, first part: what the platform gives every epic, how it is built, and which cards build it. |
| [docs/adr](docs/adr/) | Architecture and product decision records. |

When a document is created, add it here and turn its box in the
README diagram from planned to existing.

## Writing

- Write all documents in English.
- Use the terms in GLOSSARY.md exactly. When a new domain term is
  settled, add it to the glossary in the same change.
- Keep documents free of duplicated content: link to the document that
  owns a topic instead of repeating it. The document map in
  product-workflow.md says which document owns what.
- Create a new document only when there is real content for it and it
  appears in the document map. Propose any new kind of document first.
- Write an ADR only for a decision that is hard to reverse, would
  surprise a future reader, and came from a real trade-off.
- Show before you tell. Use a Mermaid diagram for a lifecycle, a flow,
  or a timeline, and a table for anything compared across rows. Keep
  the rule itself in text or a table next to the diagram; the diagram
  illustrates the rule and does not replace it.
- Put each list item on its own line. Do not run a list into a
  paragraph.

## Versioning

Every change to a document must:

1. Bump the `**Version:**` line in its header (minor step, e.g. 1.5 to
   1.6).
2. Add a row to the document's Version History table at the end:
   version, date (YYYY-MM-DD), what changed.
3. Keep cross-references free of version numbers: write "scope follows
   prd.md", not "scope follows prd.md v1.8", so a change in one
   document does not force a new version of another.
4. Update the artifact copies listed below so they show the same
   version and content.

Old versions are kept as git tags, so never keep copies of old files.

| Document | Tag format |
|----------|------------|
| prd.md (and any change set led by the PRD) | `v<PRD version>`, e.g. `v1.6` |
| product-workflow.md | `workflow-v<version>` |
| Any other document changed on its own | `<file name>-v<version>`, e.g. `glossary-v1.4` |

Read an old version with `git show v1.5:prd.md`, compare with
`git diff v1.5 v1.6 -- prd.md`.

## Status

Every document header has a `**Status:**` line with one of three
values.

| Status | Meaning |
|--------|---------|
| Draft | Still being written. |
| Proposed | Complete and waiting for the product owner's approval. |
| Approved | The product owner has approved it. |

Only the product owner moves a document to Approved.

## Artifact copies

Some documents also have an artifact view. The file in this repository
is the source of truth; the artifact is updated in the same change.
Every new document gets an artifact view when it is created, listed
here and linked from the document's header as its page version.

| Document | Artifact |
|----------|----------|
| prd.md | [English PRD](https://claude.ai/artifact/Jk5fPQpKv96euPj6Kw124U) |
| product-workflow.md | [TripMate Product Workflow](https://claude.ai/artifact/8yk7w1MUE79bXX58HL1QhA) |
| docs/information-architecture.md | [TripMate Information Architecture](https://claude.ai/artifact/Uy8kTUhj6nb78edcH64pGS) |
| docs/architecture.md | [TripMate Software Architecture](https://claude.ai/artifact/JQa8y2nWNf9HWzzdtJ9ZiB) |
| docs/data-model.md | [TripMate Data Model](https://claude.ai/artifact/KBoRVLJ5qWK3f87PPDLV3H) |
| docs/api-design.md | [TripMate API Design](https://claude.ai/artifact/RNMJoX3cpUfRNwMYutf8Tf) |
| docs/security.md | [TripMate Security Architecture](https://claude.ai/artifact/7NLzrGuao8L27ey8CiTnvA) |
| mvp-roadmap.md | [TripMate MVP Roadmap](https://claude.ai/artifact/BRWph5dW3isKwQdLVt9ipd) |
| docs/test-strategy.md | [TripMate Test Strategy](https://claude.ai/artifact/9ES7U3oo9wzvNqkkpafWx9) |
| docs/ai-golden-dataset.md | [TripMate AI Golden Dataset](https://claude.ai/artifact/Lib799999zYpM9xTnkLzNh) |
| docs/development-flow.md | [TripMate Development Flow](https://claude.ai/artifact/NL1pqAnSqERZfZo5gje9eM) |
| docs/specs/epic-01/spec.md | [TripMate EPIC-01 Spec](https://claude.ai/artifact/CDUhq8v5rqC2f3neCN53Rs) |
| docs/specs/epic-11/spec.md | [TripMate EPIC-11 Spec](https://claude.ai/artifact/U3abYrK3zy9Fm2CaQETpT2) |
| docs/adr/0005-authentication-built-into-the-backend.md | [TripMate ADR-0005 Authentication](https://claude.ai/artifact/AnngZQmwf1Ax8GWodXwcvz) |
| docs/adr/0006-google-maps-platform-behind-a-provider-interface.md | [TripMate ADR-0006 Google Maps](https://claude.ai/artifact/2p2MuMoScA9HtFTf6jDgnJ) |
| docs/adr/0007-web-client-is-a-static-build.md | [TripMate ADR-0007 Static Web Build](https://claude.ai/artifact/F2Xm35mpu9KMUtjechuCdm) |

## Git workflow

`main` is protected: direct pushes and force pushes are blocked, and
every change goes through a pull request.

1. Create a branch from `main`: `docs/<topic>-v<version>`, e.g.
   `docs/prd-v1.6`.
2. Commit with a message that says what changed and the new version.
3. Push the branch and open a pull request into `main`.
4. Document pull requests need no reviewer: the author merges as soon
   as the pull request is open. Use a merge commit and delete the
   branch.
5. Pull `main`, tag the merge commit with the version tag, and push the
   tag.
