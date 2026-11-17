# TripMate -- Solution Options and Prioritisation

**Document type:** Solution Options\
**Product:** TripMate\
**Status:** Draft\
**Version:** 1.1\
**Stage:** 2. Brainstorming / PRD / Spec

Terms follow [GLOSSARY.md](../GLOSSARY.md). This document answers *why
the MVP looks the way it does*: which ways of solving each problem were
considered, which one was chosen, and why features are in or out of the
MVP. It does not define requirements. [prd.md](../prd.md) says what the
product must do; decisions that are hard to reverse are recorded in
[docs/adr](adr/), and this document links to them instead of repeating
them.

## 1. Problems to Solve

The problems come from [product-vision.md](../product-vision.md),
section 2. Each one has an ID used in the sections below.

| ID | Problem |
|----|---------|
| P1 | Important decisions are buried in long conversations. |
| P2 | Ideas, votes, and agreed plans are difficult to tell apart. |
| P3 | Itineraries become outdated when plans change. |
| P4 | Booking information and responsibilities are scattered. |
| P5 | Members cannot easily see who has paid and who owes money. |
| P6 | One person ends up organizing and deciding for everyone. |
| P7 | With many people planning at once, ideas are raised twice or lost, and a plan everyone voted for can still be impossible in a day or over the Budget. |

## 2. Solution Options by Problem

Each row shows the option chosen for the MVP and the options that were
considered and set aside. "Not recorded" means the alternatives were
discussed but never written down; section 5 lists them as open.

### 2.1 Group decisions (P1, P2, P6)

| Question | Chosen | Set aside | Why | Source |
|----------|--------|-----------|-----|--------|
| Who decides for the group? | A Proposal becomes a Decision when more than half of the current Members vote Yes | The Owner decides a Proposal early | Nobody should be "the one who decides" | [ADR-0002](adr/0002-equal-rights-for-members.md) |
| Who may change trip state, Expenses, bookings and tasks? | Every Member, with undo and an audit log | Only the Owner may Cancel or Archive | Undo plus the audit log protect against mistakes without ranking Members | [ADR-0002](adr/0002-equal-rights-for-members.md) |
| Can Confirm be undone? | Yes, by any Member; the trip returns to Planning and the change is audited | Confirm is one-way; undoing Confirm needs a majority vote | Plans change in a group of friends, and undo plus the audit log is how every other state change is protected | [ADR-0002](adr/0002-equal-rights-for-members.md) |
| How are ideas kept apart from agreed plans? | Proposals, Votes and Decisions with explicit states | Not recorded | Ideas and agreed plans must be easy to tell apart (P2) | [prd.md](../prd.md) FR-03 |

### 2.2 Keeping the Itinerary current (P3)

| Question | Chosen | Set aside | Why | Source |
|----------|--------|-----------|-----|--------|
| How is the Itinerary changed? | Direct edits in every state except Confirmed; while Confirmed, changes need a Proposal | Every Itinerary item always needs a Proposal | Always voting slows early brainstorming and changes on the road | [ADR-0002](adr/0002-equal-rights-for-members.md) |
| How does the group see progress during the trip? | Items marked Visited or Skipped, and spending against the Budget | Not recorded | Progress should be visible while travelling | [prd.md](../prd.md) FR-05 |
| Does a trip that nobody confirmed still start? | Yes: a trip in Planning or Confirmed becomes Ongoing on its start date | Only a Confirmed trip becomes Ongoing | Nothing should block the group on the day they leave | [prd.md](../prd.md) FR-02 |

### 2.3 Sensible plans from many people (P7)

| Question | Chosen | Set aside | Why | Source |
|----------|--------|-----------|-----|--------|
| How are good ideas kept from getting lost in the chat? | AI idea capture on request, turning chat ideas into drafts a Member can publish as Proposals | Not recorded | Good ideas get lost in the chat (P7) | [prd.md](../prd.md) v1.2 |
| Is idea capture required for the MVP? | Yes, P0 | P1, built only if capacity permits | It answers the core problem of ideas lost in chat, and the MVP acceptance scenario may only use P0 requirements | [prd.md](../prd.md) section 10 |
| Who sees a Saved place? | Every Member of the trip; Saved places are P0 | A personal list for each Member; P1 | The group is the planning unit, and a Nudge must offer everyone the same quick choices | [prd.md](../prd.md) FR-05 |
| How is the same idea not raised twice? | Duplicate warnings when creating a Proposal, and Duplicate marking | Not recorded | Many people plan at the same time | [prd.md](../prd.md) v1.2 |
| How is the group stopped from voting for an impossible plan? | Feasibility warnings for time and Budget before Members vote; warnings never block | Not recorded | A voted plan can still be impossible in a day or over the Budget | [prd.md](../prd.md) section 12 |
| How does the group know what the trip is still missing? | A Readiness checklist of Gaps from deterministic rules, with timed Nudges that never block | Not recorded | Not recorded | [prd.md](../prd.md) section 10, FR-10 |
| When may TripMate nudge the group? | After 10 quiet minutes, by stage group, batched, at most once per day | Not recorded | Nudges must not interrupt or annoy the group | [prd.md](../prd.md) section 10 |
| How do Members answer a Nudge? | Up to four quick choices plus "Other…"; free text that changes the plan becomes a Proposal | Not recorded | Not recorded | [prd.md](../prd.md) section 10 |
| How may the AI change the plan? | Only through Proposals the group votes on | Silent edits by the AI | The group, not the AI, decides | [product-vision.md](../product-vision.md) section 6 |

### 2.4 Bookings and responsibilities (P4)

| Question | Chosen | Set aside | Why | Source |
|----------|--------|-----------|-----|--------|
| How are bookings handled? | Manual booking records | Booking provider integrations, automated booking changes | Provider integrations are complex; records are enough for the MVP | [mvp-roadmap.md](../mvp-roadmap.md) section 10 |
| How are responsibilities shared? | Task assignment and status tracking | Not recorded | Responsibilities are scattered across chat today | [prd.md](../prd.md) FR-07 |

### 2.5 Money (P5)

| Question | Chosen | Set aside | Why | Source |
|----------|--------|-----------|-----|--------|
| How many currencies may a trip use? | One Trip currency, stored in its smallest unit | Multiple currencies within one trip (kept for later) | Only then do all Balances sum to zero deterministically | [ADR-0001](adr/0001-single-currency-and-rounding.md) |
| Who gets the remainder of an equal split? | Participants in join order | The payer first; random allocation | The rule must not depend on who paid and must be testable | [ADR-0001](adr/0001-single-currency-and-rounding.md) |
| How is the group settled up? | A Settlement plan routed through the Member with the largest positive Balance | General minimum-cash-flow matching; paying back each Expense to its payer | At most one transfer per Member, and easy to explain | [ADR-0004](adr/0004-hub-settlement-plan.md) |
| Can a Member leave while owing or being owed? | Yes; they become a Former member and stay in the Settlement plan | Leaving only at a zero Balance | Blocking departure recovers no money | [ADR-0003](adr/0003-members-may-leave-with-a-balance.md) |
| Can an Expense be edited after settlement has started? | Yes, by any Member; Balances are recalculated and the change is audited | Lock Expenses once Settlements exist | Fixing mistakes easily matters more | [ADR-0002](adr/0002-equal-rights-for-members.md) |
| What can a Former member with a Balance still see? | The Expenses they took part in, their own Balance and the Settlement plan, read-only, until their Balance is zero | No access after leaving; letting them record their own Settlements | A person who owes must be able to see why; a person outside the trip should not write to its money records | [ADR-0003](adr/0003-members-may-leave-with-a-balance.md) |
| Does TripMate move money? | No; it records Settlements only | Payment processing, holding user funds | Payments need legal and operational review | [product-vision.md](../product-vision.md) section 9, [mvp-roadmap.md](../mvp-roadmap.md) section 11 |

### 2.6 Joining, reach and platforms

| Question | Chosen | Set aside | Why | Source |
|----------|--------|-----------|-----|--------|
| How do friends join a trip? | One Invitation shared as a link, an 8-character code, or a QR code | Link only (until v1.6) | Not recorded | [prd.md](../prd.md) v1.6 |
| Can non-members see a trip? | No public read-only links in the MVP | Public read-only Itinerary links | Not recorded | [prd.md](../prd.md) section 10 |
| Which clients ship in the MVP? | Responsive Web (Next.js), Flutter Mobile, and a Tauri Desktop app | Flutter for the Web client; Desktop after the MVP | Next.js suits browser planning; Desktop is also the team's Rust learning track | [mvp-roadmap.md](../mvp-roadmap.md) section 2 |
| How is the backend structured? | A FastAPI modular monolith | Microservices | Not recorded | [mvp-roadmap.md](../mvp-roadmap.md) section 2 |
| Which notifications are sent? | Nudges in the discussion on every client and as native notifications on Desktop (P0); personal in-app notifications are P1 | Personal in-app notifications as P0; mobile push and email notifications | Nudges carry what the trip is missing; personal notifications can follow after the MVP | [prd.md](../prd.md) section 10 |
| Which languages? | Vietnamese and English, following the device language | An in-app language setting; translating Member content | Not recorded | [prd.md](../prd.md) section 10 |

## 3. MVP Prioritisation

### 3.1 In the MVP

The full list is [prd.md](../prd.md) section 4.1. Each item traces back
to the problems above:

| Feature group | Problems |
|---------------|----------|
| Trips, Invitation and membership | P6 |
| Discussion, Proposals and majority voting | P1, P2, P6 |
| Duplicate warnings, Feasibility warnings, Readiness checklist and Nudges | P7 |
| AI place discovery, Itinerary drafts and idea capture | P7 |
| Itinerary, map and trip progress | P3 |
| Booking records and tasks | P4 |
| Expenses, Balances and the Settlement plan | P5 |
| Web, Mobile and Desktop clients in Vietnamese and English | All |

### 3.2 Deferred

The full list is [prd.md](../prd.md) section 4.2; later opportunities
are in [mvp-roadmap.md](../mvp-roadmap.md) section 11.

| Feature | Why not in the MVP |
|---------|--------------------|
| Direct flight or hotel purchase, full marketplace | Outside the product's purpose ([product-vision.md](../product-vision.md) section 9) |
| Payment processing, bank integrations | Needs legal and operational review |
| Automated booking changes, booking email import | Provider complexity; manual records first |
| Multiple currencies within one trip | Breaks the deterministic Balance invariant ([ADR-0001](adr/0001-single-currency-and-rounding.md)) |
| Mobile push and email notifications | Not recorded |
| Public social feed, public read-only trip links | Not recorded |
| An in-app language setting | Not recorded |

### 3.3 Scoring

Impact, effort, risk and feasibility have not been scored for any
feature yet. The MVP scope above was set by discussion. Scoring is
listed as open in section 5.

## 4. How This Document Changes

- When a new problem or feature is brainstormed, add it to section 1 or
  2 with the options considered, even if it is set aside.
- When an option becomes a hard-to-reverse decision, record it as an
  ADR and link to it here.
- When a feature moves in or out of the MVP, update section 3 and
  [prd.md](../prd.md) in the same change.

## 5. Open Items

- **Alternatives not recorded.** For rows marked "Not recorded", write
  down the options that were considered, or confirm there were none.
- **Feature ideas set aside before the PRD.** Ideas dropped during early
  brainstorming are not written down anywhere yet.
- **Reasons for some deferrals.** Mobile push and email, the public feed
  and read-only links, and the language setting have no recorded
  reason.
- **Scoring.** Impact, effort, risk and feasibility scores for the MVP
  features and the main deferred ones.

## 6. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-11-17 | First version: problems P1 to P7, chosen and set-aside options from the PRD, the ADRs and the roadmap, MVP and deferred features with reasons, open items. |
| 1.1 | 2026-11-17 | Decisions from PRD v1.9 with the options set aside: undo of Confirm, a trip starting without Confirm, idea capture and Saved places as P0, what a Former member can still see, and which notifications are P0. |
