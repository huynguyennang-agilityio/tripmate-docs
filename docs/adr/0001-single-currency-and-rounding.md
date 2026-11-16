# One currency per trip; split remainders go by join order

In the MVP every Expense and Settlement of a trip is recorded in a single Trip currency, stored as an integer number of that currency's smallest unit. Only then does the invariant "all Balances sum to zero" hold deterministically; multi-currency (EXP-11) stays P2.

When an equal split leaves a remainder (for example 100,000 VND across 3 Participants), the leftover units go one each to the Participants in the order they joined the trip, the Owner who created it first. The payer gets no special treatment. The order must be fixed so the same Expense always splits the same way on every client and every recalculation.

## Considered Options

- Payer absorbs the remainder first: rejected; the group wanted a rule that does not depend on who paid.
- Random allocation: rejected as non-deterministic and untestable.
