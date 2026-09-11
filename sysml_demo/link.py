"""Cross-model linkage: match concepts between two independently owned models, report where they
disagree, and walk change impact across the link graph.

The matcher is deliberately transparent (token overlap + a small domain synonym table + structural
corroboration) so every link carries a rationale a systems engineer can accept or reject.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field

from .model import Element, Model
from .queries import NOISE_STEREOTYPES, relationships

# domain synonyms, normalised to a canonical token
SYNONYMS = {
    "operations": "operation",
    "ops": "operation",
    "operational": "operation",
    "facility": "facility",
    "station": "facility",
    "site": "facility",
    "segment": "segment",
    "resource": "resource",
    "asset": "resource",
    "equipment": "resource",
    "component": "component",
    "part": "component",
    "subsystem": "component",
    "product": "product",
    "material": "product",
    "item": "product",
    "payload": "product",
    "task": "task",
    "job": "task",
    "order": "task",
    "activity": "task",
    "process": "process",
    "requirement": "requirement",
    "rqt": "requirement",
    "rqts": "requirement",
    "req": "requirement",
    "controller": "control",
    "control": "control",
    "command": "control",
    "communication": "comm",
    "communications": "comm",
    "comm": "comm",
    "comms": "comm",
    "link": "comm",
    "storage": "store",
    "store": "store",
    "buffer": "store",
    "queue": "store",
    "transport": "transport",
    "transporter": "transport",
    "delivery": "transport",
    "launch": "transport",
    "power": "power",
    "energy": "power",
    "electrical": "power",
    "battery": "power",
    "batteries": "power",
    "schedule": "schedule",
    "scheduler": "schedule",
    "plan": "schedule",
    "planning": "schedule",
    "capability": "capability",
    "function": "capability",
    "functional": "capability",
    "state": "state",
    "status": "state",
    "mode": "state",
    "data": "data",
    "information": "data",
    "telemetry": "data",
    "measurement": "data",
    "structure": "structure",
    "structural": "structure",
    "structures": "structure",
}
STOP = {"the", "of", "and", "a", "an", "for", "to", "in", "on", "def", "definition", "model", "library", "l1", "l2", "l3", "l4"}
PREFIX_RE = re.compile(r"^\s*(?:L?\d+(?:\.\d+)*[_\s-]+|\d+\s*-\s*)")
SPLIT_RE = re.compile(r"[^A-Za-z0-9]+|(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")

LINKABLE_KINDS = ("Class", "Package", "Activity", "Interface", "Signal", "DataType", "Enumeration")


def _stem(t: str) -> str:
    return t[:-1] if t.endswith("s") and len(t) > 3 and t not in SYNONYMS else t


def raw_tokens(name: str) -> set[str]:
    name = PREFIX_RE.sub("", name)
    return {_stem(tok.lower()) for tok in SPLIT_RE.split(name) if tok and tok.lower() not in STOP and not tok.isdigit()}


def canon(t: str) -> str:
    return SYNONYMS.get(t, SYNONYMS.get(t + "s", t))


def tokens(name: str) -> set[str]:
    return {canon(t) for t in raw_tokens(name)}


@dataclass
class Link:
    a: Element
    b: Element
    confidence: float
    rationale: list[str]
    disagreements: list[str] = field(default_factory=list)

    def as_dict(self, ma: Model, mb: Model) -> dict:
        return {
            "a": ma.qualified_name(self.a.id),
            "a_kind": _kind_label(self.a),
            "b": mb.qualified_name(self.b.id),
            "b_kind": _kind_label(self.b),
            "confidence": round(self.confidence, 2),
            "rationale": self.rationale,
            "disagreements": self.disagreements,
        }


def _kind_label(e: Element) -> str:
    st = [s for s in e.stereotype_names() if s not in NOISE_STEREOTYPES]
    return f"{e.kind}<<{','.join(st)}>>" if st else e.kind


def _features(m: Model, e: Element) -> dict[str, set[str]]:
    props = [m.elements[c] for c in e.children if m.elements[c].kind in ("Property", "Port")]
    return {
        "parts": {p.name.lower() for p in props if p.kind == "Property" and p.attrs.get("aggregation") == "composite" and p.name},
        "ports": {p.name.lower() for p in props if p.kind == "Port" and p.name},
        "values": {p.name.lower() for p in props if p.kind == "Property" and p.attrs.get("aggregation") != "composite" and p.name},
        "generals": {g.lower() for g in m.generals(e)},
    }


def match(ma: Model, mb: Model, min_confidence: float = 0.5, kinds: tuple[str, ...] = LINKABLE_KINDS) -> list[Link]:
    cand_a = [e for e in ma.of_type(*kinds) if e.name and not e.has_stereotype("Requirement", "ExtRequirement", "MissionRequirement")]
    cand_b = [e for e in mb.of_type(*kinds) if e.name]
    tok_b: dict[str, set[str]] = defaultdict(set)
    rb = {e.id: raw_tokens(e.name) for e in cand_b}
    tb = {e.id: {canon(t) for t in rb[e.id]} for e in cand_b}
    for e in cand_b:
        for t in tb[e.id]:
            tok_b[t].add(e.id)
    links: list[Link] = []
    for a in cand_a:
        ra = raw_tokens(a.name)
        ta = {canon(t) for t in ra}
        if not ta:
            continue
        hits: set[str] = set()
        for t in ta:
            hits |= tok_b[t]
        for bid in hits:
            b = mb.elements[bid]
            exact = ra & rb[bid]
            syn = (ta & tb[bid]) - {canon(t) for t in exact}
            conf = (len(exact) + 0.6 * len(syn)) / len(ta | tb[bid])
            rationale = []
            if exact:
                rationale.append(f"shared terms: {', '.join(sorted(exact))}")
            if syn:
                pairs = [
                    f"{x}~{y}" for x in sorted(ra - exact) for y in sorted(rb[bid] - exact) if canon(x) == canon(y) and canon(x) in syn
                ]
                rationale.append(f"synonyms: {', '.join(pairs)}")
            if a.name.lower() == b.name.lower():
                conf = max(conf, 0.95)
                rationale.append("identical name")
            if a.kind == b.kind:
                conf += 0.05
            else:
                conf -= 0.25
            fa, fb = _features(ma, a), _features(mb, b)
            for k in ("parts", "ports", "values"):
                common = fa[k] & fb[k]
                if common:
                    conf += 0.1
                    rationale.append(f"both own {k} {sorted(common)}")
            if conf < min_confidence:
                continue
            links.append(Link(a, b, min(conf, 1.0), rationale, _disagreements(ma, a, mb, b, fa, fb)))
    links.sort(key=lambda l: (-l.confidence, l.a.name, l.b.name))
    return links


def _disagreements(ma: Model, a: Element, mb: Model, b: Element, fa: dict, fb: dict) -> list[str]:
    out = []
    if a.kind != b.kind:
        out.append(f"kind: {ma.name} models it as {a.kind}, {mb.name} as {b.kind}")
    sa = {s for s in a.stereotype_names() if s not in NOISE_STEREOTYPES}
    sb = {s for s in b.stereotype_names() if s not in NOISE_STEREOTYPES}
    if sa != sb:
        out.append(f"stereotype: <<{','.join(sorted(sa)) or '-'}>> vs <<{','.join(sorted(sb)) or '-'}>>")
    if a.name != b.name:
        out.append(f"term: {a.name!r} vs {b.name!r}")
    if fa["ports"] and not fb["ports"]:
        out.append(f"interfaces: {ma.name} exposes ports {sorted(fa['ports'])}; {mb.name} exposes none")
    elif fb["ports"] and not fa["ports"]:
        out.append(f"interfaces: {mb.name} exposes ports {sorted(fb['ports'])}; {ma.name} exposes none")
    elif fa["ports"] and fb["ports"] and not (fa["ports"] & fb["ports"]):
        out.append(f"interfaces: port names disjoint ({sorted(fa['ports'])} vs {sorted(fb['ports'])})")
    only_a, only_b = fa["parts"] - fb["parts"], fb["parts"] - fa["parts"]
    if fa["parts"] and fb["parts"] and (only_a or only_b):
        out.append(f"decomposition: only in {ma.name}: {sorted(only_a)[:4]}; only in {mb.name}: {sorted(only_b)[:4]}")
    pa, pb = ma.package_of(a.id), mb.package_of(b.id)
    if pa and pb and tokens(pa.name) and tokens(pb.name) and not (tokens(pa.name) & tokens(pb.name)):
        out.append(f"ownership: lives under {pa.name!r} vs {pb.name!r}")
    return out


# --------------------------------------------------------------------------- impact / drift
@dataclass
class ImpactNode:
    model: str
    element: Element
    via: str
    depth: int


def impact(m: Model, start: Element, max_depth: int = 3) -> list[ImpactNode]:
    """Everything in `m` that would be affected if `start` changed: owners of features typed by it,
    connectors/flows touching it, trace relationships, specialisations, and owning composites."""
    seen = {start.id}
    frontier = [ImpactNode(m.name, start, "", 0)]
    out: list[ImpactNode] = []

    def push(el: Element | None, via: str, depth: int) -> None:
        if el is None or el.id in seen or not el.name:
            return
        seen.add(el.id)
        frontier.append(ImpactNode(m.name, el, via, depth))

    while frontier:
        n = frontier.pop(0)
        if n.depth:
            out.append(n)
        if n.depth >= max_depth:
            continue
        el, d = n.element, n.depth + 1
        for user in m.incoming(el.id, "type"):
            push(m.elements.get(user.owner or ""), f"{user.kind.lower()} '{user.name}' typed by {el.name}", d)
        for g in m.incoming(el.id, "general"):
            push(m.elements.get(g.owner or ""), f"specialises {el.name}", d)
        if el.kind in ("Property", "Port"):
            for end in m.incoming(el.id, "role") + m.incoming(el.id, "partWithPort"):
                push(m.elements.get(end.owner or ""), f"connector on {el.name}", d)
            for fl in m.incoming(el.id, "informationSource") + m.incoming(el.id, "informationTarget"):
                push(fl, f"item flow through {el.name}", d)
        for label, direction, other in relationships(m, el):
            push(other, f"{label} {direction}", d)
        for c in el.children:
            ch = m.elements.get(c)
            if ch and ch.kind == "Port":
                for end in m.incoming(ch.id, "role"):
                    conn = m.elements.get(end.owner or "")
                    push(m.elements.get(conn.owner or "") if conn else None, f"connector on port {ch.name}", d)
    return out


def cross_impact(ma: Model, mb: Model, start: Element, links: list[Link], max_depth: int = 3) -> dict:
    local = impact(ma, start, max_depth)
    touched = {start.id} | {n.element.id for n in local}
    bridged = [l for l in links if l.a.id in touched]
    remote: dict[str, list[ImpactNode]] = {}
    for l in bridged:
        remote[l.b.id] = impact(mb, l.b, max_depth - 1)
    return {"start": start, "local": local, "links": bridged, "remote": remote}


def render_impact(ma: Model, mb: Model, res: dict) -> list[str]:
    lines = [
        f"Change: {ma.qualified_name(res['start'].id)}  ({_kind_label(res['start'])})",
        "",
        f"Affected in {ma.name} ({len(res['local'])}):",
    ]
    for n in res["local"]:
        lines.append(f"  {'  ' * (n.depth - 1)}- {n.element.name} [{_kind_label(n.element)}]  <- {n.via}")
    lines += ["", f"Crosses into {mb.name} via {len(res['links'])} link(s):"]
    for l in res["links"]:
        lines.append(f"  {l.a.name}  ~{l.confidence:.2f}~  {mb.qualified_name(l.b.id)}   ({'; '.join(l.rationale)})")
        for n in res["remote"].get(l.b.id, []):
            lines.append(f"    {'  ' * (n.depth - 1)}- {n.element.name} [{_kind_label(n.element)}]  <- {n.via}")
        if l.disagreements:
            lines.append("    disagreements: " + " | ".join(l.disagreements))
    return lines


def mermaid(ma: Model, mb: Model, res: dict, limit: int = 40) -> str:
    def nid(prefix: str, e: Element) -> str:
        return prefix + re.sub(r"\W", "_", e.id)[-12:]

    def label(e: Element) -> str:
        return e.name.replace('"', "'")

    out = ["graph LR", f"  subgraph {ma.name}", f'    {nid("a", res["start"])}["{label(res["start"])}"]:::changed']
    for n in res["local"][:limit]:
        out.append(f'    {nid("a", n.element)}["{label(n.element)}"]')
    out.append("  end")
    out.append(f"  subgraph {mb.name}")
    for l in res["links"]:
        out.append(f'    {nid("b", l.b)}["{label(l.b)}"]')
        for n in res["remote"].get(l.b.id, [])[:limit]:
            out.append(f'    {nid("b", n.element)}["{label(n.element)}"]')
    out.append("  end")
    for n in res["local"][:limit]:
        out.append(f"  {nid('a', res['start'])} --> {nid('a', n.element)}")
    for l in res["links"]:
        out.append(f'  {nid("a", l.a)} -. "{l.confidence:.2f}" .-> {nid("b", l.b)}')
        for n in res["remote"].get(l.b.id, [])[:limit]:
            out.append(f"  {nid('b', l.b)} --> {nid('b', n.element)}")
    out.append("  classDef changed fill:#f96,stroke:#333")
    return "\n".join(out)
