# Physics Lab and D-ND_LAB compatibility

Reconciled 30 October 2026 against D-ND_LAB
`560ae94f295eb17bbf54a0fa50d4b6febd625e96` and this repository's original
`cca0794984f1e613c42c4a43bd960a1853b95231`.

## Two executable routes

The **current regenerative Lab** is implemented in MM-DND and exposed at
[AI Lab](https://d-nd.com/ai-lab). This repository's `physics_lab/` reads its
public corpus. It requires neither D-ND_LAB nor an LLM account.

The **D-ND_LAB installable engine** has a separate domain cycle and carries
its own `domains/physics/` implementation, experiments and historical
bootstrap. Its 223 physics-domain files at the inspected revision include
archival records; file count is not a competence or evidence measure.
Running that engine does not reproduce the current regenerative MM-DND Lab.

The shared inheritance is functional: source provenance, controls, falsifying
observations, reusable instruments and memory. Fixed phases, prompts, topic
taxonomies, historical scores and promotion contracts do not transfer into
the regenerative Lab merely through shared genealogy.

## Use the engine's shipped physics domain

The engine already ships its physics domain. A second clone of this repository
is unnecessary. Follow its
[installation guide](https://github.com/GrazianoGuiducci/D-ND_LAB/blob/560ae94f295eb17bbf54a0fa50d4b6febd625e96/docs/INSTALL_PROCEDURE.md)
and [physics directory](https://github.com/GrazianoGuiducci/D-ND_LAB/tree/560ae94f295eb17bbf54a0fa50d4b6febd625e96/domains/physics).
Provider credentials, charges, scheduling and external effects belong to that
installation. This reconciliation did not execute a provider or engine cycle.

## Preserve the original standalone domain

The old instructions cloned this repository directly to
`domains/physics`, but its config is nested one directory further, at
`domain/config.json`. D-ND_LAB's loader expects
`domains/<domain>/config.json`. That clone layout therefore did not match the
loader contract.

For an explicit **historical** experiment, preserve the existing engine domain
and stage this repository's `domain/` contents into a separate disposable
engine checkout under `domains/physics/`, with the original experiment scripts
under `domains/physics/tools/`. Do not overwrite an installed live domain.
The configuration must validate against the engine's `config.schema.json`
before any run. Configuration validation is not a complete cycle test.

The seven original `tools/exp_*.py` scripts and the files in `domain/` other
than its orientation README retain their original Git source blobs. Their
dependencies and scientific claims remain those of their historical context.
They are not wired into the current public reader or the regenerative owner.

## Compatibility contract

| Object | Owner | Relationship to current Lab |
| --- | --- | --- |
| Public projection v0.1/v0.2 | MM-DND public projector | Read by this toolkit without mutation. |
| Open resultant carrier v0.1 | MM-DND | Value preserved exactly; no required scientific classification added. |
| Domain config and old experiments here | Historical physics package | Preserved, documented and separately schema-checked. |
| Engine physics domain and bootstrap | D-ND_LAB | Separate installable distribution and dated evidence. |
| Private researcher, deposits and operational controls | MM-DND | Remain private and operationally independent. |

The corresponding D-ND_LAB documentation reaches this same boundary. No
automatic synchronization, shared mutable data directory or runtime dependency
is introduced between the repositories.
