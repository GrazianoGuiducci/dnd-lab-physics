# Public Physics Lab toolkit validation — 30 October 2026

Executor: Codex/TM9. This receipt covers the public companion and its reader;
it does not certify the scientific claims recorded by the Lab.

## Exercised local result

- 39 offline tests pass, including strict JSON, source identity, legacy
  compatibility, open resultant shapes, recorded contact, unresolved contacts,
  snapshot comparison, HTML escaping, output preservation, download rejection
  and Unicode output on a non-UTF-8 console.
- A real read-only capture using `python -m physics_lab fetch` preserved the
  exact public response and wrote a matching SHA-256 receipt.
- The real corpus passes the reader contract and expected-checksum check.
- E726 resolves a recorded source contact to E018 with matching event identity;
  no chronological edge was inferred.
- The generated offline HTML exposes all 726 occurrences. Browser inspection
  confirms E726 expands to its resultant and complete public record, with the
  recorded deposit digest visible. It contains zero scripts and zero external
  resources, with no horizontal overflow at the inspected desktop size.
- Both the standalone historical config and D-ND_LAB's shipped physics config
  validate against the inspected engine's `config.schema.json`; all three
  configured model input paths exist. No engine/provider cycle was run.
- Fourteen original source blobs, including LICENSE, six domain inputs and
  seven experiment scripts, are preserved. Git source identity is compared
  with the original commit; platform checkout line endings are not confused
  with a source change.

## Exact public snapshot

```text
source: https://d-nd.com/data/lab/regenerative/latest.json
retrieved_at: 2026-10-30T14:17:41.020062+00:00
schema: mm_dnd.regenerative_lab_public_projection.v0.2
bytes: 4824970
sha256: fecdf48575cc0fd39bdd3ee537e56fab75515c9035ae201b429db3be2bb93337
occurrences: 726
latest recorded observed_at: 2026-09-24T19:13:45+00:00
E726 recorded deposit SHA-256: ef4ac839c6a1fecaaaa24a31e21327a822f6749ecbc438420bbbdfad5908b961
```

The last digest is recorded metadata, not recomputation of the unavailable
private deposit. Acquisition today does not imply that a new occurrence ran
today. Later public snapshots can change independently of this repository.

## Source preservation and reconciliation

The original standalone source is
`cca0794984f1e613c42c4a43bd960a1853b95231`; the inspected D-ND_LAB source is
`560ae94f295eb17bbf54a0fa50d4b6febd625e96`. The new D-ND_LAB changes are
documentation-only and distinguish its installable domain from MM-DND's
current regenerative implementation. Its engine, domain config, bootstrap,
experiments and license remain unchanged.

The operational Lab was observed read-only. No provider, occurrence, source
arrival, deposit, memory, scheduler, service, website deploy, DOI or historical
release action was performed by this update. Private source and preservation
receipts remain in the private owner guide; they are not copied here.

## Reproducible checks

```bash
python -m unittest discover -s tests -v
python -m physics_lab verify examples/synthetic-corpus.json
python -m physics_lab trace examples/synthetic-corpus.json --index 2
python -m physics_lab verify corpus.json --expected-sha256 fecdf48575cc0fd39bdd3ee537e56fab75515c9035ae201b429db3be2bb93337
```

The last command applies only to the exact captured snapshot above. A later
live capture should use its own receipt. GitHub Actions exercises the offline
suite on Windows and Linux with Python 3.11 and 3.13; actual run status is
available in the repository's Actions checks and remains distinct from these
local results.

## Follow-up: coherent current view and public E729

The earlier sections record the initial E726 inspection and 39-test source.
The corrected reader now passes **48 local offline tests**, including current
state/time/next-relation agreement, open object relations, continuity flags,
private-marker object keys and preservation of declared public-view metadata.

The owner projector passed 13 focused local tests. A provider-free,
network-isolated reconstruction on the VPS ran as an unprivileged account
against copies of all 729 deposits. All recorded deposit digests matched.
The public export preserves 728 original resultant values exactly. In E727
only a private filesystem source reference is replaced by an explicit
placeholder, with its JSON pointer and transformation declared in the carrier.
The private deposit and its original digest are unchanged.

The 726 earlier event contents agree with the prior public file. E726's
provenance filename is corrected to the ledger's zero-padded basename; its
deposit digest and source identity agree. Consequently `compare` reports E726
as changed, three new event IDs, no removed IDs and a non-identical prefix.
This is an attributed projection difference, not a rewritten occurrence.

```text
source: https://d-nd.com/data/lab/regenerative/latest.json
retrieved_at: 2026-10-30T21:22:15.357190+00:00
schema: mm_dnd.regenerative_lab_public_projection.v0.2
bytes: 4912886
sha256: 5fb25a9f37a47233f0f4422ed21180fe9e1913d6a0dafd7ea8d39591f817d011
occurrences: 729
latest recorded observed_at: 2026-09-25T20:39:47+00:00
```

The corrected toolkit fetched and verified these served HTTPS bytes against
the candidate artifact. Browser inspection of the live Lab showed 729 events,
opened E727 and displayed its public source placeholder; no configured private
filesystem marker appeared in the inspected text and no console error was
recorded. No THIA/provider request was sent.

Private owner checks confirmed all 729 deposit digests, ledger, current state,
memory/control state and saved model plan preserved across activation. No new
Lab occurrence, provider call, scheduler change or service restart accompanied
the repair. The previous public file remains recoverable in the owner's
maintenance backup. The public corpus and private administrative receipts are
not committed in this repository. Scientific statements retain their original
research status; these checks concern projection and consumer behavior.
