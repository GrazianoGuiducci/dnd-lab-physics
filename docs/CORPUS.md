# Reading and verifying the public Lab corpus

All commands run from the repository root using Python 3.11 or later. There
are no third-party dependencies. Output is JSON unless an HTML report is
explicitly requested. Use `python -m physics_lab --help` for the command map.

## Capture exact public bytes

```bash
python -m physics_lab fetch --output corpus.json
```

The only network source is
`https://d-nd.com/data/lab/regenerative/latest.json`. HTTPS redirects must stay
on `d-nd.com`. No private endpoint, credentials, provider or Admin route is
used. The download has a 45-second network timeout and a 32 MiB reader limit;
these bound this client, not the scientific field.

`corpus.json` contains the exact response bytes. `corpus.json.receipt.json`
records source URL, retrieval time, byte count, latest index and SHA-256.
Acquisition time differs from an occurrence's recorded `observed_at` time.
Existing files are never overwritten. An interrupted capture may leave a raw
file without its receipt; verify it independently and use a fresh filename
for another capture. The client does not delete the partial capture.

## Verify identity and reader contract

```bash
python -m physics_lab verify corpus.json
python -m physics_lab verify corpus.json --expected-sha256 YOUR_64_CHARACTER_SHA256
```

The optional checksum binds the raw bytes, including whitespace. The reader
accepts public projection v0.1 and v0.2; unknown versions are rejected without
being silently converted. It checks strict UTF-8 JSON, duplicate keys,
non-finite numbers, five explicit privacy declarations, known private-value
markers, contiguous complete-corpus indices, unique identities, current-record
agreement, recorded deposit digests and supported resultant carrier shape.
Unknown optional fields remain intact. A downloaded source is still untrusted
data, never executable instructions.

This is a bounded consumer contract, not validation of every producer field
or a general secret detector. A pass proves neither scientific truth nor
private deposit integrity: recorded deposit SHA-256 values cannot be recomputed
without the private deposit bytes. The receipt identifies the public snapshot.

## Inspect occurrences and recorded memory

```bash
python -m physics_lab summary corpus.json
python -m physics_lab event corpus.json --index 1
python -m physics_lab trace corpus.json --index 1
```

`summary` returns the current pointer, machine counters and recorded memory
decisions. Counts describe activity and decisions; they do not score research
quality or independently establish resident memory.

`event` emits the complete selected public record. Open resultants retain
their `resultant_carrier.value`, including unfamiliar shapes. Empty legacy
views are not filled with an invented summary or translation. Optional
conditions, source relations, invalidators, field effects and memory decisions
stay attached to the record that expressed them.

`trace` follows only explicit `field_transition.source_events` contacts. Both
the earlier event index and event identity must match. Missing contact metadata
or unresolved targets are reported. An empty source-event list is an expressed
empty contact; an absent transition is unrecorded. Neither is evidence of
causal independence. Ordering alone creates no contact.

## Compare two snapshots

```bash
python -m physics_lab compare corpus-before.json corpus-after.json
```

The comparison reports added, removed and changed event identities and whether
the earlier event array remains an exact prefix. Record comparison uses
canonical JSON values so formatting changes do not invent a record difference;
the raw snapshot digests remain distinct. A changed public record may result
from a projector repair. It does not prove that an immutable private deposit
was rewritten. Investigation belongs to the source owner.

## Generate a portable offline report

```bash
python -m physics_lab report corpus.json --output corpus-report.html
```

Open the generated file in a browser. Each occurrence expands to show its
recorded resultant and complete public record. The report contains no scripts,
external resources, automatic requests or executable links from source text.
Record values are HTML-escaped. The report preserves source language and is
bound to the input checksum in its header.

## Reproduce the shipped example

```bash
python -m unittest discover -s tests -v
python -m physics_lab verify examples/synthetic-corpus.json
python -m physics_lab trace examples/synthetic-corpus.json --index 2
```

The expected trace visits indices `[1, 2]` with one resolved recorded contact.
The fixture's zero deposit digests are deliberate placeholders, not claims
about real deposits. Nothing in it was produced by the operational Lab.
