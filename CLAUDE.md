# TripMate Docs -- Rules for Contributors and AI Agents

This repository holds TripMate's product documents. Code lives in
separate repositories. These rules apply to every change, by people or
by AI agents such as Claude Code.

## What is here

| File | Purpose |
|------|---------|
| [GLOSSARY.md](GLOSSARY.md) | Domain terms. Use these words everywhere; avoid the listed alternatives. |
| [product-vision.md](product-vision.md) | What TripMate is and why. |
| [prd.md](prd.md) | What the MVP must do: requirements, business rules, acceptance criteria. |
| [mvp-roadmap.md](mvp-roadmap.md) | Phases, milestones, release gates. |
| [product-workflow.md](product-workflow.md) | How we go from problem to release, and which document belongs to which stage. |
| [docs/adr](docs/adr/) | Architecture and product decision records. |

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

## Versioning

Every change to a document must:

1. Bump the `**Version:**` line in its header (minor step, e.g. 1.5 to
   1.6).
2. Add a row to the document's Version History table at the end:
   version, date (YYYY-MM-DD), what changed.
3. Update cross-references that name a version (for example the roadmap
   says which PRD version it follows).
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

## Artifact copies

Some documents also have an artifact view. The file in this repository
is the source of truth; the artifact is updated in the same change.

| Document | Artifact |
|----------|----------|
| prd.md | [English PRD](https://claude.ai/artifact/Jk5fPQpKv96euPj6Kw124U), [Vietnamese reference translation](https://claude.ai/artifact/DzZcZN3J7kNEAf5tZLWvCs) |
| product-workflow.md | [TripMate Product Workflow](https://claude.ai/artifact/8yk7w1MUE79bXX58HL1QhA) |

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
