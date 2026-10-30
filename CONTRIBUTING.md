# Contributing to D-ND Physics Lab

Useful contributions improve a reproducible public reading, explain a current
mechanism, or supply an experiment with attributable inputs and controls.

## Local checks

```bash
python -m unittest discover -s tests -v
python -m physics_lab verify examples/synthetic-corpus.json
python -m physics_lab trace examples/synthetic-corpus.json --index 2
```

The test suite is offline. It uses synthetic records, with no provider or
operational Lab access. The real corpus can be read separately through the
documented `fetch` command; do not commit downloaded data or local reports.

## Public reader changes

Preserve unknown optional source fields, exact open resultant values,
recorded identities and provenance. A new schema needs an explicit supported
contract, not silent coercion. Contact tracing must distinguish missing,
unresolved and explicitly empty contact metadata. Changes to formatting must
not invent a scientific classification, translation or causal link.

## Experiments and research questions

New experiments should provide input provenance, a deterministic reproduction
path, controls, actual output and the claim's scope. Keep exploratory
interpretation distinct from established mathematics and physical evidence.
The original seven experiments remain historical; changes to their behavior
need a separately identified scientific reason and versioned evidence.

Questions and pull requests do not enter the private Lab's field or start an
occurrence automatically. The operational owner selects any such effect.

## Reporting a private-data exposure

Do not paste credentials, private paths, source documents or raw provider logs
into a public issue. Use the author's contact at [d-nd.com](https://d-nd.com/about)
and describe the affected public surface without reproducing sensitive data.
