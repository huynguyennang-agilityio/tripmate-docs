# TripMate -- UX Review

**Document type:** UX Review\
**Product:** TripMate\
**Status:** Draft\
**Version:** 1.1\
**Stage:** 3. UI/UX Design

Terms follow [GLOSSARY.md](../GLOSSARY.md). This document answers
*what did testing show, and what changed*: every usability problem
found in the prototypes, how serious it is, and the fix. The rules a fix
must follow are in [prd.md](../prd.md); whether a product assumption
held is recorded in [docs/discovery.md](discovery.md), not here.

## 1. How Findings Are Recorded

Each finding comes from a source: a review of the prototypes by the
product owner, or a test session recorded in section 4 of
docs/discovery.md.

| Field | Meaning |
|-------|---------|
| ID | `UX-` and a number, never reused. |
| Where | The place from docs/information-architecture.md, and the trip state if it matters. |
| Problem | What the user cannot do or gets wrong, in their words where possible. |
| Severity | **Blocker**: the user cannot finish the task. **Major**: the user finishes, but with a wrong result or real effort. **Minor**: friction or wording. |
| Rule | The requirement the prototype does not follow yet, if any. |
| Fix | What changes, and on which platforms. |
| Status | **Open**, **Fixed** (with the prototype version), or **Won't fix** (with the reason). |

Fixes are shipped in batches, so the prototypes change once per batch
and every platform changes together (section 3).

## 2. Findings

### 2.1 Owner review, 2026-11-18

The product owner walked through the Mobile prototype on the Phú Quốc
4D3N sample trip.

| ID | Where | Problem | Severity | Rule | Fix | Status |
|----|-------|---------|----------|------|-----|--------|
| UX-01 | Plan, Itinerary item, Planning | "I want to change Vinpearl Safari, but I can't": an item cannot be opened, edited or removed. | Blocker | ITN-03, ITN-04 | Tapping an item opens the Itinerary item place: time, notes, order, Estimated cost, Remove. Available in Planning, Ongoing, Completed, Cancelled and Archived. | Fixed (batch 1) |
| UX-02 | Plan, Itinerary item, Confirmed | There is no way to ask the group to change an item once the trip is Confirmed. | Blocker | COL-11 | The Itinerary item shows Propose a change, which opens a new Proposal to remove or replace the item, already filled in. | Fixed (batch 1) |
| UX-03 | Chat, Proposal card | A new Proposal shows 0 Yes; the Author has to vote on their own Proposal. | Major | Voting rules (FR-03) | The Author's Vote is Yes when the Proposal is created or published; the card shows it and lets the Author change it. | Fixed (batch 1) |
| UX-04 | Chat, Proposal card | A 2–2 vote in a group of four stays Open forever. | Major | Voting rules (FR-03) | A tie once every current Member has voted closes the Proposal as Rejected, with a Chat line that says it was a tie. | Fixed (batch 1) |
| UX-05 | Create trip, Edit trip, Money | The Budget is entered as a group total; people think per person. | Major | Budget rules (FR-02), EXP-12 | The Budget field is per person and shows the group Budget beside it. Money shows the group total against the group Budget and the Member's own share against the Budget per person. | Fixed (batch 1) |
| UX-06 | Plan, Itinerary item, Planning | One Member can remove an item the group voted in, and the others do not notice. | Major | Editing rules by trip state (FR-05) | When an item that came from a Decision is edited, reordered or removed, a line is posted in Chat, for example "Chi removed Vinpearl Safari from Day 2 (decided 3 of 4)". | Fixed (batch 1) |
| UX-07 | Edit trip (Trip details) | Name, destination, dates and Day window are shown but cannot be changed; only the Budget has a field, labelled for the whole group. | Major | TRIP-02 | Each field in Trip details can be edited by any Member: name, destination, dates, Day window and Trip currency; the Budget field is per person (UX-05). The currency locks once an Expense or Settlement exists; new dates that leave out a day with items list those items and move them to Saved places, or open a Proposal when the trip is Confirmed (Trip detail rules, FR-02). | Fixed (batch 1) |

## 3. Fix Batches

| Batch | Findings | Platforms | Status |
|-------|----------|-----------|--------|
| 1 | UX-01 to UX-07 | Mobile, Web, Desktop | Fixed on 2026-11-18: Mobile prototype version 20, Web version 13, Desktop version 7. New boards: Itinerary item and Confirmed: Propose a change. |

## 4. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-11-18 | Fix batch 1 shipped on Mobile, Web and Desktop: UX-01 to UX-07 are Fixed. UX-06 now follows the editing rule added to prd.md. |
| 1.0 | 2026-11-18 | First version: how findings are recorded, seven findings from the product owner's review of the Mobile prototype (UX-01 to UX-07), and fix batch 1. |
