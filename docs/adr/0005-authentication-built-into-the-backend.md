# Authentication is built into the backend

**Page version:** [TripMate ADR-0005 Authentication artifact](https://claude.ai/artifact/AnngZQmwf1Ax8GWodXwcvz)

TripMate keeps accounts, passwords, and sessions in its own backend instead of using a hosted identity service. Passwords are hashed with Argon2id, an access token lasts 15 minutes, and a refresh token is replaced at every use and stored as a hash in one session row per signed-in device. Social sign-in (AUTH-05) is Google and Sign in with Apple: the backend checks the provider's proof of identity and then issues the same TripMate session. The product owner chose this on 2026-11-18 and kept it on 2026-11-19 after weighing what social sign-in adds.

With it, accounts and sessions live in the same database as trip membership, any device can be signed out at once, and no outside service holds TripMate's users or stands in the sign-in path. The price is that the team writes and maintains the sign-in code itself.

## Considered Options

- A hosted identity service (Supabase Auth, Clerk, Auth0): set aside. Each sign-in provider would be a configuration switch instead of work on three clients, but user identities and sessions would live in a second system next to the trip database.

## Consequences

- Every sign-in provider is work on Web, Mobile, and Desktop. Google and Sign in with Apple ship together, because App Store Review Guideline 4.8 asks for an equivalent private option beside a third-party sign-in.
- Password reset by email (AUTH-06) is built by the team too, on an email service chosen with it.
- The sign-in code is reviewed in the security assessment before beta ([security.md](../security.md), sections 2 and 9).
- Moving to a hosted service later would mean moving every account and signing every device in again.
