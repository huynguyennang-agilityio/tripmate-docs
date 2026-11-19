# Google Maps Platform, behind a provider interface

**Page version:** [TripMate ADR-0006 Google Maps artifact](https://claude.ai/artifact/2p2MuMoScA9HtFTf6jDgnJ)

Place search, place details, and travel times between Itinerary items come from Google Maps Platform (Places API and Routes API). Every call goes through one provider interface in the backend's `places` module, and clients never ask Google for this data themselves; only map display uses a separate, restricted client key. The product owner chose Google on 2026-11-18.

The interface is there because the choice is only partly reversible: another provider can be added without touching other modules, but every place TripMate stores is a Google place ID.

## Considered Options

- Goong (a Vietnamese provider) and Mapbox: set aside by the product owner.
- Calling the provider straight from each client: rejected; the server key would ship inside three clients, and the backend could not apply quotas.

## Consequences

- Google's terms limit what may be stored. The place ID is kept; other place content and travel times are cached only as long as the terms allow and are fetched again when needed ([data-model.md](../data-model.md), section 7).
- Usage is free up to a monthly allowance for each kind of request and billed above it (in November 2026: 1,000 to 10,000 requests a month, depending on the kind). A billing account is needed from the first request, and a budget only alerts, so daily request limits are set on the Google Cloud project.
- Changing provider later needs a new adapter and a one-time re-match of every stored place, because place IDs do not carry over.
- When Google cannot be reached, search and travel times degrade and manual planning still works ([architecture.md](../architecture.md), section 6.3).
