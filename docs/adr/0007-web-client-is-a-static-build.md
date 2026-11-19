# The Web client is a static build with no server rendering

**Page version:** [TripMate ADR-0007 Static Web Build artifact](https://claude.ai/artifact/F2Xm35mpu9KMUtjechuCdm)

The Web client is built with Next.js static export: a fixed set of HTML, JavaScript, and CSS files served from a CDN, with no server rendering, no Next.js API routes, and no server actions. Every page gets its data by calling the TripMate API from the browser. Why: the Desktop client wraps exactly this build in a native window (DESK-01), so one build serves browsers and Desktop; and nothing in TripMate is public, so server rendering would add no search or link-preview value.

## Considered Options

- Server rendering for the Web, with a separate build for Desktop: rejected; two builds of the same screens to keep in step, for a benefit TripMate does not use.

## Consequences

- Screens are written to fetch on the client from the start. Adding server rendering later would mean reworking how every screen loads its data.
- Paths with a variable part, such as the Invitation link, are resolved in the browser: the CDN serves the join page for every `/join/*` path.
- No secret can live in the Web client, and the Web refresh token is an `HttpOnly` cookie set by the API, not by a Next.js server ([security.md](../security.md), section 2.1).
- If TripMate later gets public pages, such as a read-only shared Itinerary (out of scope for the MVP), this is the decision to revisit.
