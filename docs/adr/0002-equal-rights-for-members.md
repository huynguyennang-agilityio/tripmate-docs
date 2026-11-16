# Members have equal rights; the Owner only manages membership

Every Member can change the trip's state (Confirm, Cancel, Archive, and undo those), and can edit or delete any Expense, Settlement, booking or task; every such change is written to an audit log. The Owner keeps only membership management: removing Members, creating and revoking the Invitation, and handing ownership to another Member. The Owner has no extra say in decisions. Why: TripMate is for groups of friends who trust each other, and the goal is that nobody is "the one who decides". Mistakes are covered by undoable Cancel/Archive and by the audit log showing who did what, not by restricting who can act.

A Proposal becomes a Decision when more than half of the current Members vote Yes, and becomes Rejected when more than half vote No. The threshold is recomputed whenever someone joins or leaves. Proposals never expire; the Author can withdraw one. When a Proposal about an Itinerary item becomes a Decision, other open Proposals about the same item become Outdated. AI-drafted Proposals are authored by the Member who asked for them, and nobody gets a Vote automatically.

The Itinerary is edited directly in every state except Confirmed. While Confirmed, every change must go through a Proposal, so the agreed plan cannot shift under the group before departure. Once the trip is Ongoing, Members edit directly again, because changes on the road (a closed restaurant, rain) cannot wait for a vote.

## Considered Options

- Owner can decide a Proposal early: rejected; it contradicts the equal-rights goal.
- Only the Owner can Cancel or Archive: rejected; undo plus audit log is enough protection.
- Lock Expenses once Settlements exist: rejected; fixing mistakes easily matters more, and Balances are always recalculated.
- Only the two people in a Settlement may edit it: rejected for consistency with equal rights.
- Every Itinerary item always needs a Proposal: rejected; it slows down early brainstorming and on-the-road changes.

## Consequences

- PRD TRIP-06, section 3.2 and business rule 1 describe the Owner as managing trip settings and must be updated.
- Audit logging is mandatory for every state and financial change, since it is the main safeguard.
- A Member joining or leaving can decide or reject an open Proposal without anyone casting a new Vote.
