# The Settlement plan routes money through the biggest creditor

The Settlement plan uses the Member with the largest positive Balance as a hub. Every Member with a negative Balance sends their whole debt to the hub, and the hub then sends each other Member with a positive Balance what they are owed. For example, if A paid for most things and B paid only slightly more than their share, everyone pays A, and A sends B the small difference.

Why: this needs at most one transfer per Member (n − 1 in total, often fewer), and it is easy to explain: "pay whoever paid the most". A general minimum-transfers algorithm can sometimes save a transfer, but it produces pairings that look arbitrary ("why do I pay C? I never shared anything with C"), which works against the goal of a settlement everyone sees as fair.

## Considered Options

- General minimum-cash-flow matching: rejected; marginally fewer transfers, but harder to understand.
- Pay back each Expense to its payer directly: rejected; far more transfers.

## Consequences

- Ties for the largest Balance are broken by join order, so the plan is deterministic.
- The hub may receive and forward large sums; the UI should show the hub why they are passing money on.
