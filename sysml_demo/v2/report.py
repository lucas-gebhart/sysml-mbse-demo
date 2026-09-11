"""Migration gap report: per-construct mapping table + per-element detail, Markdown and JSON."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import asdict

from ..model import Model
from .profile import ProfileIndex
from .transform import CLEAN, DECISION, LOSSY, UNSUPPORTED, TransformResult
from .validate import ValidationResult

STATUS_ORDER = [CLEAN, LOSSY, DECISION, UNSUPPORTED]
STATUS_LABEL = {
    CLEAN: "Clean",
    LOSSY: "Lossy",
    DECISION: "Needs decision",
    UNSUPPORTED: "No equivalent",
}
STATUS_MEANING = {
    CLEAN: "semantics preserved in the generated SysML v2",
    LOSSY: "emitted, but some information was dropped or approximated (see note)",
    DECISION: "emitted in a provisional form; a systems engineer must choose the final v2 construct",
    UNSUPPORTED: "no SysML v2 equivalent, or tool-specific; not emitted",
}

# Headline gaps that every v1 -> v2 migration hits, independent of the model
STANDING_GAPS = [
    (
        "Diagrams / layout",
        "SysML v2 interchange carries semantics, not diagram layout. Views must be re-authored "
        "in the target tool (Cameo 2026x v2 plugin generates views from the model).",
    ),
    (
        "Custom profile stereotypes",
        "Carried as `metadata def`s so every tagged element keeps its classification and tag values, "
        "but the tool-side behaviour (icons, validation rules, DSL customisations, derived properties, "
        "table definitions) is not expressible in v2 and has to be re-created.",
    ),
    (
        "Satisfy / Verify",
        "v2 `satisfy ... by` requires a part *usage*; v1 satisfies typically point at Blocks (definitions). "
        "Emitted as tagged dependencies until the satisfying usage is chosen.",
    ),
    (
        "Item flows between blocks",
        "v2 flows need a common part context; v1 InformationFlows drawn between features of unrelated "
        "blocks are kept as tagged dependencies.",
    ),
    (
        "Activity / state-machine internals",
        "Action and transition graphs are structurally different in v2 (succession-based). "
        "Signatures are migrated; bodies flagged for re-modelling.",
    ),
    ("Operations", "v2 has no operations; emitted as nested actions for review."),
    (
        "Units / quantity kinds",
        "MagicDraw ISO-80000 / SI library imports map to the v2 `ISQ` and `SI` libraries but need an explicit mapping table.",
    ),
    ("Instance specifications", "v2 has no instances; use individuals/snapshots or attribute defaults."),
    ("PackageMerge", "No v2 support (per the OMG transformation document)."),
]


def build_report(
    model: Model,
    result: TransformResult,
    validation: ValidationResult | None,
    profile: ProfileIndex | None = None,
    subset: str | None = None,
) -> dict:
    counts = Counter(r.status for r in result.records)
    by_construct: dict[str, Counter] = defaultdict(Counter)
    notes: dict[str, Counter] = defaultdict(Counter)
    for r in result.records:
        by_construct[r.v1_construct][r.status] += 1
        if r.note:
            notes[r.v1_construct][r.note] += 1
    table = []
    for construct, c in sorted(by_construct.items(), key=lambda kv: -sum(kv[1].values())):
        worst = next(s for s in reversed(STATUS_ORDER) if c[s])
        v2s = Counter(r.v2_construct for r in result.records if r.v1_construct == construct)
        table.append(
            {
                "v1_construct": construct,
                "v2_construct": ", ".join(k for k, _ in v2s.most_common(3)),
                "count": sum(c.values()),
                "clean": c[CLEAN],
                "lossy": c[LOSSY],
                "decision": c[DECISION],
                "unsupported": c[UNSUPPORTED],
                "worst": worst,
                "notes": [n for n, _ in notes[construct].most_common(3)],
            }
        )
    custom = {}
    if profile is not None:
        for name, info in profile.stereotypes.items():
            used = [r for r in result.records if r.v1_construct.startswith(f"{name} (") or f"<<{name}>>" in r.v1_construct]
            custom[name] = {
                "root": info.root,
                "parents": info.parents,
                "tags": info.tags,
                "applied": len(used),
                "in_v2_profile": name in result.metadata_defs,
            }
    return {
        "model": model.name,
        "subset": subset,
        "source": {"exporter": model.exporter, "elements": len(model.elements)},
        "totals": {s: counts[s] for s in STATUS_ORDER} | {"records": len(result.records)},
        "validation": None
        if validation is None
        else {
            "ok": validation.ok,
            "errors": len(validation.errors),
            "warnings": len(validation.warnings),
            "sysml_lines": sum(len(c.splitlines()) for c in result.cells),
        },
        "table": table,
        "custom_profile": custom,
        "standing_gaps": [{"topic": t, "detail": d} for t, d in STANDING_GAPS],
        "records": [asdict(r) for r in result.records],
    }


def _pct(n: int, d: int) -> str:
    return f"{100 * n / d:.0f}%" if d else "-"


def render_markdown(rep: dict) -> str:
    t = rep["totals"]
    total = t["records"]
    out = [f"# SysML v1 → v2 migration gap report: {rep['model']}" + (f" / {rep['subset']}" if rep["subset"] else ""), ""]
    out.append(f"Source: {rep['source']['exporter'] or 'XMI'} export, {rep['source']['elements']} model elements.  ")
    if rep["validation"]:
        v = rep["validation"]
        out.append(
            f"Generated SysML v2: {v['sysml_lines']} lines, pilot-implementation validation "
            f"**{'PASSED' if v['ok'] else 'FAILED'}** ({v['errors']} errors, {v['warnings']} warnings)."
        )
    else:
        out.append("Generated SysML v2: pilot-implementation validation **NOT RUN** (re-run without `--no-validate`).")
    out += ["", "## Summary", "", "| Status | Elements | Share | Meaning |", "|---|---:|---:|---|"]
    for s in STATUS_ORDER:
        out.append(f"| {STATUS_LABEL[s]} | {t[s]} | {_pct(t[s], total)} | {STATUS_MEANING[s]} |")
    out += [
        "",
        "```",
        "  v1 model ──► normalise ──► map ──► SysML v2 text ──► pilot validator",
        f"  {rep['source']['elements']:>6} el.            {t[CLEAN]:>5} clean      {t[LOSSY]:>5} lossy",
        f"                                {t[DECISION]:>5} decision   {t[UNSUPPORTED]:>5} no equivalent",
        "```",
        "",
    ]
    out += [
        "## Mapping table (per construct)",
        "",
        "| v1 construct | v2 construct | n | clean | lossy | decision | none | notes |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rep["table"]:
        out.append(
            f"| {row['v1_construct']} | {row['v2_construct']} | {row['count']} | {row['clean']} | {row['lossy']} | "
            f"{row['decision']} | {row['unsupported']} | {'; '.join(row['notes'])} |"
        )
    if rep["custom_profile"]:
        out += [
            "",
            "## Custom profile",
            "",
            "Each stereotype resolves through its generalisation chain to a SysML base concept, which decides the v2 construct:",
            "",
            "| Stereotype | Extends | SysML root | Tags | Applied | v2 |",
            "|---|---|---|---|---:|---|",
        ]
        for name, info in sorted(rep["custom_profile"].items(), key=lambda kv: (-kv[1]["applied"], kv[0])):
            v2 = {
                "Block": "part def + metadata",
                "Requirement": "requirement + metadata",
                "Property": "metadata on usage",
                "Comment": "comment + metadata",
                "Dependency": "tagged dependency",
                "Trace": "tagged dependency",
                "Verify": "tagged dependency",
                "Behavior": "action/verification def",
            }.get(info["root"], "metadata")
            out.append(
                f"| {name} | {', '.join(info['parents']) or '-'} | {info['root'] or '?'} | {', '.join(info['tags']) or '-'} | "
                f"{info['applied']} | {v2} |"
            )
    out += ["", "## Standing gaps (independent of this model)", ""]
    for g in rep["standing_gaps"]:
        out.append(f"- **{g['topic']}** — {g['detail']}")
    decisions = [r for r in rep["records"] if r["status"] == DECISION]
    if decisions:
        out += ["", f"## Decisions required ({len(decisions)})", "", "| Element | v1 | Proposed v2 | Why |", "|---|---|---|---|"]
        for r in decisions[:60]:
            out.append(f"| {r['qualified_name']} | {r['v1_construct']} | {r['v2_construct']} | {r['note']} |")
        if len(decisions) > 60:
            out.append(f"| … {len(decisions) - 60} more in the JSON report | | | |")
    lossy = [r for r in rep["records"] if r["status"] == LOSSY]
    if lossy:
        out += ["", f"## Lossy mappings ({len(lossy)})", "", "| Element | v1 | v2 | What was lost |", "|---|---|---|---|"]
        for r in lossy[:60]:
            out.append(f"| {r['qualified_name']} | {r['v1_construct']} | {r['v2_construct']} | {r['note']} |")
        if len(lossy) > 60:
            out.append(f"| … {len(lossy) - 60} more in the JSON report | | | |")
    unsupported = Counter(r["v1_construct"] for r in rep["records"] if r["status"] == UNSUPPORTED)
    if unsupported:
        out += ["", "## Not migrated", ""]
        for k, n in unsupported.most_common():
            out.append(f"- {k}: {n}")
    return "\n".join(out) + "\n"


def render_json(rep: dict) -> str:
    return json.dumps(rep, indent=2)
