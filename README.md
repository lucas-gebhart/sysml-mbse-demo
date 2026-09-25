# sysml-mbse-demo

Internal tooling for the Cameo / Teamwork Cloud MBSE capability demo: ingest a SysML v1 model
exported from MagicDraw/Cameo, answer systems-engineering questions about it, generate SysML v2
textual notation with a validated migration-gap report, and link/impact-analyse across
independently owned models.

This repo is the rehearsal harness. The customer sees the live session, the reports and the pilot
proposal, not the code. See `docs/RUNBOOK.md` for the demo script.

## Layout

```
sysml_demo/
  ingest.py        .mdzip / XMI / XML -> Model (elements, stereotypes, tags, refs, diagrams, docs)
  model.py         normalised element index + navigation helpers
  queries.py       overview, requirements table, trace, structure, interfaces, profile usage, health check
  link.py          cross-model concept matching (with rationale + disagreements), impact traversal, Mermaid
  thread.py        federated requirement -> function -> allocated -> product -> test RVTM, proposed Verify links + XMI/CSV patch
  cyber.py         STPA-Sec risk scenario -> attack tree -> requirements -> ATT&CK/D3FEND -> candidate NIST 800-53 gap analysis
  data/            nist80053_d3fend.json – authored D3FEND-tactic/technique -> NIST SP 800-53r5 starting table
  conform.py       rules extracted from reference models (style guide, UTP, mission meta model, markings) -> conformance + cross-org links
  v2/profile.py    resolve custom stereotypes through their generalisation chain to a SysML base concept
  v2/transform.py  SysML v1 -> v2 textual notation; every element gets a clean/lossy/decision/unsupported record
  v2/validate.py   run the generated text through the OMG pilot-implementation kernel, parse diagnostics
  v2/report.py     migration gap report (Markdown + JSON)
  cli.py           `python -m sysml_demo <command>` – the entry points used live
models/            public source models (see models/README.md for provenance)
examples/          committed sample outputs (CSRM + DELS reports, generated .sysml, impact graph)
examples/ignite/   IGNITE Berserker outputs: RVTM + proposed Verify links (thread), cyber gap analysis (cyber), conformance + reference links (conform)
scripts/           setup_sysml_kernel.sh – installs the pilot kernel into a micromamba env
tests/             pytest suite (synthetic fixture + the real models)
```

## Setup

```bash
pip install -e ".[dev]"          # or, on older pip without PEP 660: pip install pytest ruff mypy jupyter_client
bash scripts/setup_sysml_kernel.sh      # SysML v2 pilot kernel (~2 min, conda-forge). Optional; --no-validate works without it.
pytest -q && ruff check . && mypy sysml_demo
```

## Commands

```bash
python -m sysml_demo overview      models/CSRM.mdzip
python -m sysml_demo requirements  models/CSRM.mdzip --filter Mission
python -m sysml_demo trace         models/CSRM.mdzip "Subsystem Requirement Name"
python -m sysml_demo structure     models/CSRM.mdzip "CubeSat Mission Enterprise" --depth 3
python -m sysml_demo interfaces    models/DELS.xml Queue Router
python -m sysml_demo profile       models/CSRM.mdzip --profile models/CSRM-Profile.mdzip
python -m sysml_demo health        models/CSRM.mdzip --profile models/CSRM-Profile.mdzip
python -m sysml_demo migrate       models/CSRM.mdzip --profile models/CSRM-Profile.mdzip --out out
python -m sysml_demo migrate       models/CSRM.mdzip --profile models/CSRM-Profile.mdzip --subset "Power Subsystem" --out out
python -m sysml_demo show-v2       models/CSRM.mdzip --profile models/CSRM-Profile.mdzip --subset "Power Subsystem"
python -m sysml_demo link          models/CSRM.mdzip models/DELS.xml
python -m sysml_demo impact        models/CSRM.mdzip models/DELS.xml "Power Subsystem" --mermaid out/impact.mmd
python -m sysml_demo thread        ~/ignite/"Beserker System Level Test Model.mdzip" --federate \
                                   --with ~/ignite/"Berserker Allocated Baseline Model.mdzip" \
                                   --with ~/ignite/"Berserker Product Baseline Library.mdzip" --out out --stem berserker
```

Every command also accepts `--federate` (follow the project's Cameo `projectUsages` and load the
mounted `.mdzip` files found next to it, recursively) and `--with OTHER.mdzip` (load an explicit
extra project). Federated loads resolve cross-project references, so `health` distinguishes real
dangling references from references into unloaded or Cameo-bundled modules, and reports mounted
projects that are missing on disk. Python: `load(path, federate=True)` / `load_federation([...])`.

## Closing the digital thread (`thread`)

`thread` builds a requirements verification traceability matrix across a federated set of
baselines: for every SysML requirement (and subtype) it follows requirement → Satisfy / Refine /
Trace / Allocate → activity or block in the functional baseline → Allocate / swimlane / owner →
functional block → Realization / generalization / typed part → allocated-baseline block → the same
again → product-baseline block, and records which UTP `TestCase` / `TestProcedure` touches any
element in that chain (call closure, Dependency, Allocate, swimlane, typed pin / `ResourceInformation`
test data) plus any existing `Verify`. Every hop is an existing relationship; the only inferred
mapping is a `same-name (heuristic)` block match used when nothing realises a block, and it is
labelled as such. Empty hops are marked `GAP:`; rows are `full` / `partial` / `none` and summarised
per requirement package.

For requirements without a `Verify`, `thread` ranks candidate tests by structural evidence (the
test calls / depends on / is allocated to something in the chain), lexical overlap (requirement
`Text` and name vs. test name, documentation, called test activities and test data; HTML stripped,
stopwords dropped, requirement Ids such as `C-1.29` boosted) and existing `Trace` links between the
pair. Every proposal carries `high` / `medium` / `low` and a rationale string that starts with
`HEURISTIC PROPOSAL (not in model)`. Outputs (`--out DIR`, `--stem NAME`):

- `<stem>_rvtm.{md,csv,json}` – the matrix, one row per requirement, one column per hop
- `<stem>_proposed_verify.{md,json}` – ranked proposals (`--min-confidence low|medium|high`)
- `<stem>_proposed_verify.xmi` – SysML v1 XMI fragment: one `uml:Abstraction` (client = test,
  supplier = requirement) + `sysml:Verify` per proposal of confidence ≥ medium, using the real
  `xmi:id`s of the loaded elements, for review and import
- `<stem>_proposed_verify.csv` – the same pairs as `source id,target id,relationship` for Cameo's CSV import

`--requirement ID` prints one requirement's chain as an ASCII tree with its gaps, touching tests
and proposals instead of writing files. Committed IGNITE output is under `examples/ignite/`
(`berserker_*`); the source `.mdzip` files are never modified. The IGNITE-gated tests run when
`IGNITE_MODELS_DIR` points at the unzipped model set and skip otherwise.

### Cyber resiliency gap analysis (`cyber`)

```bash
python -m sysml_demo cyber "ignite/Berserker Cyber Res. Model.mdzip" --federate --list
python -m sysml_demo cyber "ignite/Berserker Cyber Res. Model.mdzip" --federate --scenario "selected location" --out examples/ignite
```

For one STPA-Sec risk scenario (default: the adversary-selected-location scenario) the command walks
Loss ← Hazard ← Security constraint ← Controller / Hazardous control action ← Loss scenario ← Risk
scenario → probabilistic attack tree → leaf nodes (P(success) 90 % CI, EML tags), then for every leaf
reports the cybersecurity requirements it reaches through model relationships (Trace/Satisfy/Refine on the
leaf, loss scenario, HCA or controller; Trace → function → Allocate → block paths), proposed ATT&CK
techniques (lexical match on the D3FEND profile, boosted by explicit `Txxxx` ids), the D3FEND defensive
techniques reachable through D3FEND associations (directly or via shared digital artifacts), and candidate
NIST SP 800-53r5 controls from `sysml_demo/data/nist80053_d3fend.json`. Leaves are ranked by
P(success) × no-requirement × no-countermeasure. It also reports how many Berserker elements actually carry a
D3FEND stereotype (from data) and whether the reached requirements are referenced by the assurance case.

Outputs: ASCII tree on stdout; `cyber_<RS>.md` / `.mmd`, `cyber_gaps.{md,json}`,
`cyber_candidate_nist_controls.{md,csv}` and `nist_controls_candidate.xmi` (Requirement-stereotyped
classes with Id + Text, importable into the empty NIST project) in `--out`. Everything heuristic carries a
confidence and a rationale; only relationships found in the model are called model links. `--min-confidence`
sets the threshold that counts as coverage. The NIST table is an authored starting point for review, not an
official MITRE/NIST mapping.

## Standards conformance (`conform`)

`conform` checks a delivery against rules read out of reference models rather than hard-coded ones:
Style Guide prose (package/comment documentation: diagram naming, required views, dependency
matrices, swimlanes, Country properties …), the `Mission_Profile` stereotypes and their OCL
constraints, the UML Testing Profile's «validationRule» constraints (68 in UTP 2.1), and the
classification enumerations / marking stereotypes. Rules that map onto a structural check run
(pass / fail / n.a. with offending qualified names); the rest are listed verbatim as "not automatable".
The federated `health` result is folded in as delivery completeness (real `dangling-ref`s, mounted
projects missing on disk). Optional `--capybara` / `--ujtl` reference models are matched against the
delivery's mission-level content with `link.match` (candidates filtered by kind so UJTL's 30k elements
stay fast) and one measure is walked with `link.cross_impact` into the delivery's test procedures and
requirements.

```bash
python -m sysml_demo conform ROOT.mdzip --reference StyleGuide.mdzip --rules-only        # print the extracted rule set
python -m sysml_demo conform ROOT.mdzip --federate --with Allocated.mdzip --with Product.mdzip \
    --reference StyleGuide.mdzip --reference MissionMetaModel.mdzip --reference UTP.mdzip --reference Classification.mdzip \
    --ujtl UJTL.mdzip --capybara CapyBARA.mdzip --out out/conform --prefix delivery
```

Writes `reference_rules.md`, `<prefix>_conformance.{md,json}`, `<prefix>_reference_links.{md,json}` and
`<prefix>_impact.mmd` (or `--mermaid PATH`) into `--out`; `--prefix` defaults to a slug of the root
model name. Every proposed link carries the matcher's rationale, confidence and disagreements; none is
presented as a model fact. Sample output from the IGNITE Berserker delivery is committed under
`examples/ignite/`.

## What the migration does and does not claim

The transformer follows the OMG SysML v1-to-v2 transformation mapping for the structural,
requirements and interface subset (blocks, value types, parts, ports, interface blocks, flow
properties, connectors, requirements, satisfy/verify/derive/refine/trace, comments, enumerations,
custom stereotypes as `metadata def`). Output is validated by the pilot implementation; current
results: CSRM 0 errors / 0 warnings, DELS 0 errors / 47 warnings (inherited duplicate members
from the source model's redefinition style).

Every source element gets a mapping record. The gap report distinguishes:

- **clean** – direct v2 equivalent emitted
- **lossy** – emitted, but information dropped (activity internals, opaque constraints, expression multiplicities, some redefinitions)
- **decision** – emitted as a placeholder that needs a human choice (satisfy/verify target usage, cross-definition item flows, unstereotyped classes, allocations)
- **unsupported** – no v2 equivalent produced (diagrams and layout, MagicDraw customisations/DSL, derived properties, PackageMerge, tables/matrices)

Diagram layout never migrates; v2 views/viewpoints and target-tool layout are re-authored.
Custom profile *semantics* migrate as metadata; tool-side behaviour (icons, validation rules,
derived properties, tables) does not.

## Not in this repo (pilot scope)

- Teamwork Cloud REST (`/osmc`) adapter – the live-ingest path into the customer's 19.x server.
  The ingest layer is deliberately file-format based so the adapter slots in behind `load()`.
- Opening generated `.sysml` in Cameo/CATIA Magic 2026x SysML v2 (round-trip proof).
