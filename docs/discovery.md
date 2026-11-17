# TripMate -- Discovery

**Document type:** Discovery\
**Product:** TripMate\
**Status:** Draft\
**Version:** 1.0\
**Stage:** 1. Discovery & Strategy

Terms follow [GLOSSARY.md](../GLOSSARY.md). This document answers
*what we still need to learn before we trust the plan*: which
assumptions TripMate rests on, how each one will be tested, and what
real groups told us. What the product is and why is in
[product-vision.md](../product-vision.md); this document does not
repeat it.

## 1. Where Stage 1 Stands

Stage 1 of the [product workflow](../product-workflow.md) is finished
when these three conditions hold.

| Condition | Today |
|-----------|-------|
| At least five conversations or tests with real groups | 0 of 5 recorded |
| Each core assumption is marked validated, rejected, or still open | Listed in section 3; all still open |
| Vision, goals, non-goals, and principles are written, and each goal has a metric | Written in [product-vision.md](../product-vision.md); two of the seven metrics are proposed and not agreed yet |

```mermaid
flowchart TD
    A["List the assumptions"] --> B["Test with five real groups"]
    B --> C["Mark each assumption"]
    C --> D{"Any rejected?"}
    D -->|Yes| E["Change the vision or the PRD"]
    D -->|No| F["Stage 1 closes"]
    E --> F
```

## 2. The Problems We Believe Exist

The seven problems are listed once, in
[product-vision.md](../product-vision.md) section 2, and carry the IDs
P1 to P7 in [solution-options.md](solution-options.md) section 1. They
come from the team's own experience of group trips. No outside group
has confirmed them yet.

## 3. Core Assumptions

Each assumption is something that must be true for TripMate to work as
designed. Status is one of **Open**, **Validated**, or **Rejected**.

| ID | Assumption | If it is false | How to test | Status |
|----|------------|----------------|-------------|--------|
| A1 | Groups of friends lose decisions and ideas in chat often enough to want a tool for it (P1, P2, P7). | The core problem is too small to build for. | Ask each group how their last trip was planned and what went wrong. | Open |
| A2 | A group will plan in a shared workspace next to their usual messaging app. | Nobody opens TripMate after the first day. | Let a group plan a real trip in the prototype and watch where the discussion happens. | Open |
| A3 | Friends accept that nobody decides alone, including the person who started the trip. | Groups want one organiser with the final say. | Run majority voting in the prototype and ask the person who would normally organise. | Open |
| A4 | Members will vote in the app instead of agreeing informally in chat. | Proposals stall without a majority. | Count Proposals that reach a Decision during the test. | Open |
| A5 | Nudges help more than they annoy. | Groups mute or ignore TripMate. | Show Nudges in the prototype and ask each Member how they felt about them. | Open |
| A6 | Groups trust an AI-drafted Itinerary enough to use it as a starting point. | The assistant is ignored and its cost is wasted. | Offer an AI draft as a Proposal and see whether the group votes on it or rewrites it. | Open |
| A7 | Idea capture finds the ideas the group cares about. | A P0 feature produces drafts nobody publishes. | Run idea capture on the group's real discussion and count the drafts they publish. | Open |
| A8 | Members record Expenses during the trip, not only afterwards. | Spending against the Budget is empty while travelling. | Ask how the group tracked money on their last trip, and at what moment. | Open |
| A9 | "Pay whoever paid the most" is seen as fair and easy to follow. | The Settlement plan is disputed. | Show a Settlement plan for a sample trip and ask each Member to explain what they owe. | Open |
| A10 | Groups will enter booking details by hand. | Booking records stay empty and Preparation Gaps are wrong. | Ask the group to record one real booking and time it. | Open |
| A11 | Members plan on a computer often enough for a desktop app to matter. | Desktop work in every phase is spent on few users. | Ask which device each Member used to plan their last trip. | Open |

## 4. Conversations and Tests

At least five sessions with real groups are needed. Testing the
prototype with four or five friends who are planning a real trip
counts, one session per group. The prototypes are linked from the
[README](../README.md#live-pages).

For each session record the date, who the group was (size, how well
they know each other, where they were going), what they did, what was
learned, and which assumptions it touches.

| # | Date | Group | Method | What we learned | Assumptions touched |
|---|------|-------|--------|-----------------|---------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

No session has been recorded yet.

## 5. Not Covered Yet

The workflow lists these Stage 1 deliverables. None of them is written.

- Competitor analysis and market research.
- Product strategy and business model hypothesis.
- A risk list for the assumptions that turn out false.

## 6. How This Document Changes

- After each session, fill in a row in section 4 and update the status
  of every assumption it touches in section 3.
- When an assumption is rejected, change
  [product-vision.md](../product-vision.md) or [prd.md](../prd.md) in
  the same change and say so in section 4.
- When the three conditions in section 1 hold, set the status of this
  document and of the vision to Approved and close Stage 1 in the
  Build Tracker.

## 7. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-11-17 | First version: Stage 1 conditions and where they stand, assumptions A1 to A11 (all open), an empty log for five sessions, and the deliverables not covered yet. |
