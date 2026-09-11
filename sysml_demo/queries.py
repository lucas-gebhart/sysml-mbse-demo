"""Systems-engineering questions over a loaded model, plus the model health check."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field

from .ingest import strip_html
from .model import TRACE_STEREOTYPES, Element, Model

PLACEHOLDER_RE = re.compile(r"^\s*(shall statement|to be populated|tbp|tbd|requirement (a|b )?name|breaker)?\s*\.?$", re.I)
NOISE_STEREOTYPES = {"HyperlinkOwner", "NumberOwner", "Customization", "auxiliaryResource", "CustomImageHolder"}


# --------------------------------------------------------------------------- overview
def overview(m: Model) -> dict:
    roots = [e for e in m.of_type("Model")]
    top = []
    for r in roots:
        for cid in r.children:
            c = m.get(cid)
            if c and c.kind in ("Package", "Profile") and c.name:
                top.append((c.name, sum(1 for _ in m.descendants(cid))))
    diag = Counter(d.diagram_type or "unknown" for d in m.diagrams())
    stereo = {p: dict(sorted(v.items(), key=lambda kv: -kv[1])) for p, v in m.stereotype_summary().items()}
    return {
        "name": m.name,
        "source": m.source,
        "exporter": m.exporter,
        "elements": len(m.elements),
        "top_level_packages": top,
        "types": m.type_summary(),
        "diagrams": dict(diag.most_common()),
        "profiles": stereo,
        "requirements": len(m.requirements()),
        "blocks": len(m.blocks()),
    }


# --------------------------------------------------------------------------- relationships
def relationships(m: Model, el: Element) -> list[tuple[str, str, Element]]:
    """(stereotype-or-kind, direction, other-end) for every Abstraction/Dependency touching el."""
    out = []
    for rel in m.incoming(el.id, "client") + m.incoming(el.id, "supplier"):
        if rel.kind not in ("Abstraction", "Dependency", "Realization", "Usage"):
            continue
        label = next((s for s in rel.stereotype_names() if s in TRACE_STEREOTYPES or s not in NOISE_STEREOTYPES), rel.kind)
        if el.id in rel.refs.get("client", []):
            for sid in rel.refs.get("supplier", []):
                other = m.get(sid)
                if other:
                    out.append((label, "->", other))
        if el.id in rel.refs.get("supplier", []):
            for cid in rel.refs.get("client", []):
                other = m.get(cid)
                if other:
                    out.append((label, "<-", other))
    return out


def requirements_table(m: Model) -> list[dict]:
    rows = []
    for r in m.requirements():
        rels = relationships(m, r)
        rows.append(
            {
                "id": r.tag("Id") or "",
                "name": r.name,
                "stereotype": r.stereotype_names()[0] if r.stereotypes else "",
                "text": strip_html(r.tag("Text") or ""),
                "package": (m.package_of(r.id) or Element("", "")).name,
                "satisfied_by": [o.name for l, d, o in rels if l == "Satisfy" and d == "<-"],
                "verified_by": [o.name for l, d, o in rels if l == "Verify" and d == "<-"],
                "derived_from": [o.name for l, d, o in rels if l == "DeriveReqt" and d == "->"],
                "derives": [o.name for l, d, o in rels if l == "DeriveReqt" and d == "<-"],
                "refined_by": [o.name for l, d, o in rels if l == "Refine" and d == "<-"],
                "traces": [o.name for l, d, o in rels if l == "Trace"],
                "element": r,
            }
        )
    return rows


@dataclass
class TraceNode:
    element: Element
    via: str
    direction: str
    depth: int
    children: list[TraceNode] = field(default_factory=list)


def trace(m: Model, start: Element, max_depth: int = 6) -> tuple[TraceNode, list[str]]:
    """Walk every trace-type relationship from `start`; report where the chain stops."""
    root = TraceNode(start, "", "", 0)
    seen = {start.id}
    breaks: list[str] = []

    def walk(node: TraceNode) -> None:
        if node.depth >= max_depth:
            return
        rels = relationships(m, node.element)
        if not rels and node.depth > 0:
            kinds = node.element.stereotype_names()
            if not any(k in ("VerificationActivity", "TestCase", "Verify") for k in kinds):
                breaks.append(f"{node.element.name} ({', '.join(kinds) or node.element.kind}) has no further trace")
        for label, direction, other in rels:
            if other.id in seen:
                continue
            seen.add(other.id)
            child = TraceNode(other, label, direction, node.depth + 1)
            node.children.append(child)
            walk(child)

    walk(root)
    labels = set()

    def collect(n: TraceNode) -> None:
        labels.add(n.via)
        for c in n.children:
            collect(c)

    collect(root)
    if "Satisfy" not in labels:
        breaks.append("no Satisfy relationship anywhere in the chain: nothing in the architecture claims to satisfy this")
    if "Verify" not in labels:
        breaks.append("no Verify relationship / verification activity reached: the requirement is unverified in the model")
    return root, breaks


def render_trace(m: Model, node: TraceNode, indent: int = 0) -> list[str]:
    tag = f"[{node.via} {node.direction}] " if node.via else ""
    st = ",".join(s for s in node.element.stereotype_names() if s not in NOISE_STEREOTYPES)
    lines = [f"{'  ' * indent}{tag}{node.element.name} <<{st or node.element.kind}>>"]
    for c in node.children:
        lines.extend(render_trace(m, c, indent + 1))
    return lines


# --------------------------------------------------------------------------- structure & interfaces
def parts(m: Model, block: Element) -> list[tuple[Element, Element | None]]:
    out = []
    for cid in block.children:
        c = m.get(cid)
        if c and c.kind in ("Property", "Port"):
            out.append((c, m.type_of(c)))
    return out


def structure_tree(m: Model, block: Element, depth: int = 3, _ancestors: frozenset[str] = frozenset()) -> dict:
    """Composite decomposition; a type is only cut off when it recurs on its own ancestry path."""
    ancestors = _ancestors | {block.id}
    node: dict = {"name": block.name, "stereotypes": [s for s in block.stereotype_names() if s not in NOISE_STEREOTYPES], "parts": []}
    if depth == 0:
        return node
    for prop, typ in parts(m, block):
        if prop.kind == "Property" and prop.attrs.get("aggregation") == "composite" and typ and typ.kind == "Class":
            if typ.id in ancestors:
                child = {"name": typ.name, "stereotypes": [], "parts": [], "cycle": True}
            else:
                child = structure_tree(m, typ, depth - 1, ancestors)
            child["role"] = prop.name
            node["parts"].append(child)
    return node


def interfaces_between(m: Model, a: Element, b: Element) -> dict:
    """Ports/connectors/item flows crossing between the subtree of a and the subtree of b.

    Falls back to associations and dependencies when the model has no ports (CSRM is a
    reference model at the structural level and defines no ports/connectors)."""

    def closure(root: Element) -> set[str]:
        """root plus every type reachable through composite part properties (not refs/values/ports)."""
        ids = {root.id}
        stack = [root]
        while stack:
            cur = stack.pop()
            for prop, typ in parts(m, cur):
                if prop.kind == "Property" and prop.attrs.get("aggregation") == "composite" and typ and typ.id not in ids:
                    ids.add(typ.id)
                    stack.append(typ)
        return ids

    sa, sb = closure(a), closure(b)
    ports_a = [p for i in sa for p in m.elements[i].children if m.elements[p].kind == "Port"]
    ports_b = [p for i in sb for p in m.elements[i].children if m.elements[p].kind == "Port"]
    connectors, flows, assocs = [], [], []
    for c in m.of_type("Connector"):
        roles = {r for end in c.children for r in m.elements[end].refs.get("role", [])}
        if roles & set(ports_a) and roles & set(ports_b):
            connectors.append(c)
    for f in m.of_type("InformationFlow"):
        src = set(f.refs.get("informationSource", []))
        tgt = set(f.refs.get("informationTarget", []))
        if (src & (sa | set(ports_a)) and tgt & (sb | set(ports_b))) or (src & (sb | set(ports_b)) and tgt & (sa | set(ports_a))):
            flows.append(f)
    for assoc in m.of_type("Association"):
        ends = [m.get(e) for e in assoc.refs.get("memberEnd", [])]
        end_types = [m.type_of(e) for e in ends if e]
        types = {t.id for t in end_types if t}
        if types & sa and types & sb:
            assocs.append(assoc)
    return {
        "a": a.name,
        "b": b.name,
        "ports_a": [m.elements[p] for p in ports_a],
        "ports_b": [m.elements[p] for p in ports_b],
        "connectors": connectors,
        "flows": flows,
        "associations": assocs,
    }


def profile_usage(m: Model) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = defaultdict(list)
    where: dict[tuple[str, str], Counter] = defaultdict(Counter)
    kinds: dict[tuple[str, str], Counter] = defaultdict(Counter)
    for el in m.elements.values():
        for s in el.stereotypes:
            pkg = m.package_of(el.id)
            where[(s.profile, s.name)][pkg.name if pkg else "?"] += 1
            kinds[(s.profile, s.name)][el.kind] += 1
    for (prof, name), pkgs in sorted(where.items(), key=lambda kv: (kv[0][0], -sum(kv[1].values()))):
        out[prof].append(
            {"stereotype": name, "count": sum(pkgs.values()), "applies_to": dict(kinds[(prof, name)]), "top_packages": pkgs.most_common(3)}
        )
    return dict(out)


# --------------------------------------------------------------------------- health check
@dataclass
class Finding:
    check: str
    severity: str
    element: Element | None
    detail: str


def health_check(m: Model, profile: Model | None = None) -> list[Finding]:
    f: list[Finding] = []
    reqs = m.requirements()
    for r in reqs:
        text = strip_html(r.tag("Text") or "")
        if PLACEHOLDER_RE.match(text):
            f.append(Finding("requirement-text", "warn", r, f"placeholder or empty text: {text!r}"))
        if not r.tag("Id"):
            f.append(Finding("requirement-id", "warn", r, "no Id tag"))
    table = requirements_table(m)
    for row in table:
        if not row["satisfied_by"]:
            f.append(Finding("requirement-unsatisfied", "info", row["element"], "no Satisfy relationship"))
        if not row["verified_by"]:
            f.append(Finding("requirement-unverified", "info", row["element"], "no Verify relationship"))

    connected = {r for c in m.of_type("Connector") for end in c.children for r in m.elements[end].refs.get("role", [])}
    for p in m.of_type("Port"):
        if p.id not in connected:
            f.append(Finding("port-unconnected", "warn", p, f"port on {m.elements[p.owner].name if p.owner else '?'} has no connector"))

    names: dict[tuple[str, str], list[Element]] = defaultdict(list)
    for e in m.of_type("Class"):
        if e.name:
            names[(e.kind, e.name.strip().lower())].append(e)
    for (kind, _), els in names.items():
        if len(els) > 1:
            f.append(
                Finding(
                    "duplicate-name",
                    "info",
                    els[0],
                    f"{len(els)} {kind} elements named {els[0].name!r} in: "
                    + "; ".join(sorted({(m.package_of(e.id) or Element("", "", "?")).name for e in els})),
                )
            )

    typed_by: Counter[str] = Counter()
    for p in m.of_type("Property", "Port", "Parameter"):
        t = m.type_of(p)
        if t:
            typed_by[t.id] += 1
    for e in m.blocks():
        kids = [m.elements[c] for c in e.children if c in m.elements]
        if typed_by[e.id] == 0 and not m.incoming(e.id) and not any(k.kind in ("Property", "Generalization") for k in kids):
            f.append(Finding("orphan-block", "info", e, "not typed, referenced, generalized or decomposed anywhere"))

    for pkg in m.of_type("Package"):
        if not pkg.children and pkg.name:
            f.append(Finding("empty-package", "info", pkg, "package has no contents"))

    for e in m.elements.values():
        for k, targets in e.refs.items():
            for tid in targets:
                if tid not in m.elements:
                    f.append(Finding("dangling-ref", "warn", e, f"{k} -> {tid} not in this file (shared module or broken)"))

    if profile is not None:
        defined = {s.name for s in profile.of_type("Stereotype")}
        applied = {s.name for e in m.elements.values() for s in e.stereotypes}
        for name in sorted(defined - applied):
            f.append(Finding("stereotype-unused", "info", None, f"profile defines <<{name}>> but the model never applies it"))
    return f


def health_summary(findings: list[Finding]) -> list[tuple[str, str, int]]:
    c = Counter((x.check, x.severity) for x in findings)
    return sorted([(k[0], k[1], n) for k, n in c.items()], key=lambda t: (t[1] != "warn", -t[2]))
