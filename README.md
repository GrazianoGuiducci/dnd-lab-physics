# dnd-lab-physics

The physics research domain for [D-ND_LAB](https://github.com/GrazianoGuiducci/D-ND_LAB) — first applied lab built with the D-ND modus.

> The engine is generic. The content is here.

## What it is

`D-ND_LAB` is the **engine**: agent loop, falsifier counter-pole, cimitero, trajectory evaluator, SSP pipeline (Scoperte → Soluzioni → Prodotti). Domain-agnostic Python.

`dnd-lab-physics` is the **content** for the physics applied lab:
- `domain/` — `assertions.py` (verifiable claims), `seed_tensions.json` (research questions to explore), `context.md` (lab identity prompt), `config.json` (capabilities + verifier policy), `cimitero.md` (archived falsified claims), `tension_to_category.json` (semantic categories).
- `tools/` — experiment scripts produced by past cycles (`exp_markov_transition.py`, `exp_dipole_classifier.py`, `exp_z12813_sequential_info.py`, ...).

You install the engine once. Each domain (this one is physics) lives in its own repo.

## Topics covered

- Prime gap structure: residues mod 6, Markov transition matrices, structural zeros
- Spectral signatures of dipolar order in number sequences
- Markov memory layers (pair vs triple correlations)
- Phase transitions in GUE-Poisson crossover
- Detection of hidden sequential information (z=12,813 finding)

The lab runs in continuous cycles, generates discoveries, falsifies them with a counter-pole, and packages what survives as installable Python kernels (see [d-nd-seed kernels](https://github.com/GrazianoGuiducci/d-nd-seed/tree/main/kernels)).

## Live demo

The physics lab is currently running at [lab.d-nd.com/dashboard/](https://lab.d-nd.com/dashboard/). Read-only public view of the field, knowledge graph, falsifier output, cimitero, and trajectory of all cycles.

## Install

Requires the engine first.

```bash
# 1. Install the engine
curl -fsSL https://raw.githubusercontent.com/GrazianoGuiducci/D-ND_LAB/main/install.sh | bash

# 2. Add this domain
cd ~/.d-nd-lab/domains
git clone https://github.com/GrazianoGuiducci/dnd-lab-physics.git physics
# physics/domain/ is what the engine reads as the domain config
# physics/tools/ contains the experiment scripts already built

# 3. Run a cycle
cd ~/.d-nd-lab
docker compose run --rm lab
```

See [D-ND_LAB INSTALL_PROCEDURE.md](https://github.com/GrazianoGuiducci/D-ND_LAB/blob/main/docs/INSTALL_PROCEDURE.md) for the full procedure including environment, provider chain, and dashboard setup.

## Contributing

This repo holds the configuration of the physics lab as it exists today. Contributions:

- **New experiment scripts** (`tools/exp_*.py`) — welcome via PR if reproducible and documented.
- **Tension proposals** (`domain/seed_tensions.json`) — open an issue first; tensions feed the lab's research direction.
- **Cimitero entries** (`domain/cimitero.md`) — only added by the lab itself when claims are falsified.

Don't modify `assertions.py` or `context.md` directly — those are the lab identity, changed only by the operator.

## License

MIT. See [LICENSE](LICENSE).

## Related

- [D-ND_LAB](https://github.com/GrazianoGuiducci/D-ND_LAB) — the engine (domain-agnostic)
- [d-nd-seed](https://github.com/GrazianoGuiducci/d-nd-seed) — installable kernels produced by labs (including this one)
- [d-nd.com](https://d-nd.com) — D-ND mathematical model and research
- [lab.d-nd.com](https://lab.d-nd.com) — Lab D-ND landing + applications + dashboard
