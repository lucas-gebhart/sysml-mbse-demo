# Live demo runbook — Cameo/TWC 19.x customer

Target: 25–30 min live, then pilot close. Every command below runs in < 1 s except `migrate` with
validation (~4 s). Rehearse once from a clean shell before the session; keep `examples/` open in a
second window as the backup if anything misbehaves.

## Framing (2 min)

- Two public models, deliberately from two owners and two tool vintages:
  - **CSRM** — INCOSE/OMG CubeSat System Reference Model, Cameo `.mdzip` with its own OMG-standard
    profile (5 sub-profiles, 53 stereotypes). This is the "your model, your customisations" stand-in.
  - **DELS** — NIST Discrete Event Logistics Systems library, XMI exported from **MagicDraw 19.0**
    (the customer's vintage), SysML 1.4, ports/connectors/flows/activities/state machines.
- Same ingest code handles `.mdzip`, vendor XMI and neutral XMI. The Teamwork Cloud REST hook is the
  "same thing, live in your environment" step (pilot).
- Set expectations up front: **no one has lossless automatic v1→v2 migration.** What we show is a
  transformation of the structural/requirements/interface subset that *validates*, plus an honest,
  element-by-element gap report. That report is the deliverable.

## Part 1 — Understand the model (8 min)

Q1 "What system is this, what are the major subsystems, how is the model organised?"
```
python -m sysml_demo overview  models/CSRM.mdzip
python -m sysml_demo structure models/CSRM.mdzip "CubeSat Mission Enterprise" --depth 3
```
Evidence: 1704 elements / 143 blocks / 69 requirements / 253 diagrams; exporter version read from the
file; profile usage counts per stereotype; enterprise → space/ground segment → 9 CubeSat subsystems
→ hardware/software/procedures components. Point out we read *their* stereotypes
(`<<Segment>>`, `<<Subsystem>>`, `<<Component>>`), not just UML.

Q2 "List the mission requirements and which blocks satisfy them. Which have no satisfy at all?"
```
python -m sysml_demo requirements models/CSRM.mdzip --filter Mission
```
Evidence: table with Id / stereotype / package / satisfied-by / verified-by. Nothing is satisfied —
CSRM is a *reference* model with template requirements. Say so: "the tool reports what is there;
on your model these columns fill in."

Q3 "Describe the interfaces between the space segment and the ground segment."
```
python -m sysml_demo interfaces models/CSRM.mdzip "Space Segment" "Ground Segment"
python -m sysml_demo interfaces models/DELS.xml Queue Router
```
Evidence: CSRM defines *no* ports/connectors at that boundary (a finding in itself); DELS shows
2 connectors + 2 item flows (`flow for Task`) between Queue and Router with the port lists.
Caveat: association-level fallback is reported explicitly when a model has no ports.

Q4 "What does the CSRM profile add on top of SysML, and where is it applied?"
```
python -m sysml_demo profile models/CSRM.mdzip --profile models/CSRM-Profile.mdzip
```
Evidence: each stereotype resolved through its generalisation chain to the SysML base concept
(`Component → Block`, `MissionRequirement → ExtRequirement → Requirement`), tag definitions, and
application counts. This is the bridge into migration: the base concept decides the v2 construct.

Q5 "Trace requirement 7 (Subsystem Requirement Name) from mission need to verification. Where does it break?"
```
python -m sysml_demo trace models/CSRM.mdzip "Subsystem Requirement Name"
```
Evidence: Trace → Refine → DeriveReqt chain up to Stakeholder Concern; explicit breaks: no Satisfy
anywhere, no Verify reached. Accepts requirement Id or name.

Q6 "Run a model health check."
```
python -m sysml_demo health models/CSRM.mdzip --profile models/CSRM-Profile.mdzip
python -m sysml_demo health models/DELS.xml
```
Evidence (CSRM): 145 dangling refs (shared-module boundary), 68 requirements without text,
69 unsatisfied / 69 unverified, 26 empty packages, 22 unused profile stereotypes, 20 orphan blocks,
10 duplicate names. DELS: 7 unconnected ports. Frame dangling refs honestly: file exports lose
cross-project links — the TWC pilot resolves those server-side.

## Part 2 — Migrate (8 min)

Q7 "If we move this to SysML v2, what maps cleanly, what's lossy, what has no equivalent?"
```
python -m sysml_demo migrate models/CSRM.mdzip --profile models/CSRM-Profile.mdzip --out out
```
Then open `out/CSRM.migration.md`. Evidence: 1566 lines of v2, **pilot validation PASSED 0/0**,
1342 mapping records → clean 1040 / lossy 12 / decision 42 / unsupported 248. Walk the construct
table (Package, Comment, PartProperty, Component(custom) → `part def + metadata`, Diagram: Generic
Table → unsupported) and the custom-profile table. Show the JSON exists for tooling.

Q8 "Take the power subsystem, generate the SysML v2 and validate it."
```
python -m sysml_demo show-v2 models/CSRM.mdzip --profile models/CSRM-Profile.mdzip --subset "Power Subsystem"
python -m sysml_demo migrate models/CSRM.mdzip --profile models/CSRM-Profile.mdzip --subset "Power Subsystem" --out out
```
Evidence: `#Subsystem part def 'Power Subsystem' { part batteries : ...Batteries; ... }` inside its
original package path, declaration-only stubs for referenced components, validation 0/0.
Mention: names with spaces are quoted per v2 grammar; `#Subsystem` is their stereotype carried as
metadata.

Q9 (planted honesty check) "Can you migrate the diagrams?"
Answer, no command: **No.** 253 diagrams are recorded as *unsupported* in the report. v1 diagrams
are layout over model elements; v2 has views/viewpoints as model elements and the target tool owns
layout. The semantics behind the diagrams (the blocks, parts, requirements) do migrate; the
pictures are re-authored in 2026x. Same for MagicDraw customisations (DSL, derived properties,
tables, validation rules): recorded, not converted.

Optional second data point: `python -m sysml_demo migrate models/DELS.xml --out out` — a 19.0
export with ports/flows/activities/state machines: 0 errors, 47 warnings (inherited duplicate
members from the source model's redefinition style — shown, not hidden), lossy records on activity
internals and opaque constraints.

## Part 3 — Multi-model (6 min)

Q10 "Which DELS concepts correspond to CSRM's ground/operations elements? Where do they disagree?"
```
python -m sysml_demo link models/CSRM.mdzip models/DELS.xml
```
Evidence: ~20 candidate links with confidence, *why* (shared terms, synonyms, structural
corroboration) and *disagreements* (kind, stereotype, term, interfaces, decomposition, ownership).
E.g. `Facility ↔ PLANT::Facility::Facility` 1.00, disagreement: `<<Facility>>` vs `<<Block>>`.
Stress that links are proposals with rationale, meant for an engineer to accept/reject.

Q11 "If the power subsystem changes, what's affected across both models?"
```
python -m sysml_demo impact models/CSRM.mdzip models/DELS.xml "Power Subsystem" --mermaid out/impact.mmd
```
Evidence: local chain CubeSat → Space Segment → CubeSat Mission Enterprise. `Power Subsystem` itself
has no DELS counterpart; the bridge is its owning package `L3_Subsystems ↔ PLANT::Resource::Subsystems`
(1.00, shown as "(owning package)" with the term/ownership disagreements). Say so out loud: a change
inside a package is a change to what that package represents in the other model. Render
`out/impact.mmd` (committed copy in `examples/impact.mmd`) if a visual helps. For a denser DELS-side
blast radius use `impact ... "Facility"` (Resource → 30+ dependents).
Voice track: this is the drift check that runs on a schedule in the pilot.

Q12 "Across the Berserker functional, allocated, product and test baselines — which requirements are
actually verified, and what's missing?" (IGNITE set unzipped flat into `~/ignite/`; the root file name
really is spelled `Beserker`)
```
python -m sysml_demo thread ~/ignite/"Beserker System Level Test Model.mdzip" --federate \
    --with ~/ignite/"Berserker Allocated Baseline Model.mdzip" \
    --with ~/ignite/"Berserker Product Baseline Library.mdzip" --out out --stem berserker
python -m sysml_demo thread ~/ignite/"Beserker System Level Test Model.mdzip" --federate \
    --with ~/ignite/"Berserker Allocated Baseline Model.mdzip" \
    --with ~/ignite/"Berserker Product Baseline Library.mdzip" --requirement C-1.29
```
Evidence (committed copy in `examples/ignite/berserker_*`): 11 projects load in ~2 s, `MI Style
Guide.mdzip` is reported missing (it is not in the set); 265 requirements, 245 without Satisfy; the
233 FSA requirements have **no** `Verify` at all (the only 6 Verify links belong to CapyBARA's own
requirements); 10 full chains, 129 partial, 126 with no outgoing link. The `--requirement C-1.29`
tree is the live moment: `Final Systems Check` → Satisfy ← activity `Final Systems Check` → Allocate →
`Executive Control Subsystem` → Realization ← `Allocated Nav Controller` (via port) → Realization ←
`Curtiss-Wright Parvus DuraCOR Pi`; the activity is called by `Launch UAV`, which `Launch UAS Op
Test Procedure` depends on — so the tool proposes that procedure as the Verify client with
confidence `high`, and says `HEURISTIC PROPOSAL (not in model)` in the rationale. Point at
`berserker_proposed_verify.xmi` / `.csv`: the ≥ medium proposals as `uml:Abstraction` + `sysml:Verify`
against the real `xmi:id`s, ready for an engineer to review and import — the `.mdzip` files are untouched.

## Open floor (3 min)

- "Ask anything you'd want to know about your own 19.x model." — `overview`, `structure`,
  `interfaces`, `trace`, `health` are safe for arbitrary names (partial match, Id or name).
- "What customisations do you have in your profile?" — segue to the pilot.

## Pilot close (3 min)

Read-only, low-risk, 2–3 sessions of our effort:
1. TWC 19.x REST (`/osmc`) read access to one project (or an `.mdzip` export if REST is off the table).
2. Deliver on *their* model: overview + health report, migration gap report (same format as today),
   v2 text for one subsystem validated by the pilot implementation, and — if they have a target
   2026x install — proof that it opens there.
3. One cross-model link: their requirements source (DOORS/Jama export) or a second TWC project.

Do not promise: lossless migration, diagram migration, tool-customisation migration, or write
access to their TWC.

## Known caveats to have ready

- CSRM `.mdzip` was last saved in Cameo 2024x; the vendor-neutral `CSRM.xmi` and DELS (19.0) cover
  the older-export path. All three load through the same code.
- CSRM has no ports; interface questions on CSRM fall back to associations. Use DELS for
  port/flow-level interface questions.
- `dangling-ref` counts are dominated by shared-module boundaries in file exports.
- Requirement `satisfy`/`verify` in v2 need a *usage*; v1 relationships to a block are emitted as
  tagged dependencies and recorded as *decision* items.

## Backup

`examples/` holds the committed outputs for every command above. If the kernel is unavailable,
add `--no-validate`; the report then says validation was not run rather than pretending.
