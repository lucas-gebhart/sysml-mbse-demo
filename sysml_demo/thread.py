"""Close the digital thread: requirement -> function -> allocated block -> product block -> test.

Builds a requirements verification traceability matrix (RVTM) over a (federated) model and proposes the
missing ``Verify`` links with evidence.  Everything reported as a *hop* is an existing relationship in the
loaded data; everything under *proposed* is a heuristic and is labelled as such in every rationale string.

Hops (one row per requirement):

* ``functions``  -- elements the requirement is Satisfied / Refined / Traced / Allocated to (the functional baseline).
* ``parents``    -- activities whose CallBehaviorAction calls a function activity (the FSA decomposition one level up).
* ``blocks``     -- blocks those functions are allocated to (Allocate, swimlane ``represents``, owning block) or
                    the function itself when it is a block.
* ``allocated``  -- blocks in *another* project that realise / specialise / are typed by a functional block
                    (same-name match is the last resort and flagged as heuristic).
* ``product``    -- the same step again from the allocated block into the product baseline.
* ``tests``      -- UTP ``TestCase`` / ``TestProcedure`` elements whose call closure, dependencies, allocations,
                    swimlanes or typed pins touch any element in the chain.
* ``verified_by`` -- existing ``Verify`` relationships (supplier = requirement).
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

from .ingest import strip_html
from .model import BLOCK_STEREOTYPES, Element, Model
from .queries import NOISE_STEREOTYPES, relationships

TEST_STEREOTYPES = ("TestCase", "TestProcedure")
FUNCTION_LABELS = {"Satisfy", "Refine", "Trace", "Allocate"}
FUNCTION_KINDS = {"Activity", "Class", "Component", "StateMachine", "Interaction", "Signal", "Interface", "Node"}
REALIZE_LABELS = {"Realization", "Abstraction", "Refine", "Trace"}
CONFIDENCE_RANK = {"low": 0, "medium": 1, "high": 2}
MAX_PROPOSALS_PER_REQUIREMENT = 3

STOPWORDS = frozenset(
    """
    the and for that this with from into onto shall will must should may can are was were been being has have had not any all each per its
    than then when while where which who whom what how via upon within without between during after before under over about also both
    either such these those there their they them our you your one two able use used using provide provides provided requirement
    requirements system systems test tests testing procedure procedures case operational operator step steps perform performs performed
    ensure ensures order based following required capability capable including include includes least less more most e.g i.e etc n/a tbd
    and/or berserker beserker mq-99 mq99 uas uav
    """.split()
)
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9\-/\.]*[a-z0-9]|[a-z0-9]")


def tokens(text: str) -> set[str]:
    """Lower-cased word tokens minus stopwords and bare numbers (HTML already stripped by the caller)."""
    out = set()
    for t in TOKEN_RE.findall(text.lower()):
        if len(t) < 3 or t in STOPWORDS or t.replace(".", "").replace("-", "").replace("/", "").isdigit():
            continue
        out.add(t)
    return out


def _norm_name(name: str) -> str:
    n = re.sub(r"\s+", " ", name.strip().lower())
    return re.sub(r"^(allocated|product|physical|functional)\s+", "", n)


def _lane(partition: Element) -> str:
    return f"swimlane '{partition.name}'" if partition.name else "swimlane"


def _is_block(el: Element) -> bool:
    return el.kind == "Class" and el.has_stereotype(*BLOCK_STEREOTYPES)


def _label(el: Element) -> str:
    st = ",".join(s for s in el.stereotype_names() if s not in NOISE_STEREOTYPES)
    return f"{el.name or '<unnamed>'} <<{st or el.kind}>>" + (f" [{el.project}]" if el.project else "")


def _ref(el: Element) -> dict:
    return {"id": el.id, "name": el.name, "type": ",".join(el.stereotype_names()) or el.kind, "project": el.project}


def _short(el: Element) -> dict:
    return {"id": el.id, "name": el.name}


def _json(data: dict) -> str:
    """Compact-but-diffable JSON: one top-level list entry per line."""
    key = "rows" if "rows" in data else "proposals"
    head = {k: v for k, v in data.items() if k != key}
    lines = ["{"]
    for k, v in head.items():
        lines.append(f"{json.dumps(k)}: {json.dumps(v, indent=1)},")
    lines.append(f"{json.dumps(key)}: [")
    items = data[key]
    for i, item in enumerate(items):
        lines.append(json.dumps(item, separators=(",", ":")) + ("," if i < len(items) - 1 else ""))
    lines += ["]", "}"]
    return "\n".join(lines) + "\n"


def req_id(req: Element) -> str:
    return (req.tag("Id") or req.tag("id") or "").strip()


def req_text(req: Element) -> str:
    return strip_html(req.tag("Text") or req.tag("text") or "")


# --------------------------------------------------------------------------- chain model
@dataclass
class Hop:
    element: Element
    via: str  # relationship that produced the hop, e.g. "Satisfy <-", "Realization <-", "same-name"
    source: str  # id of the element this hop was reached from
    heuristic: bool = False  # True only for the same-name fallback

    def as_dict(self) -> dict:
        return {**_ref(self.element), "via": self.via, "from": self.source, "heuristic": self.heuristic}


@dataclass
class TestTouch:
    test: Element
    target: Element
    role: str  # requirement | function | block | allocated | product
    evidence: str  # e.g. "calls Activity 'Final Systems Check'"
    edge: str  # call | dependency | allocate | trace | type | partition


@dataclass
class Chain:
    requirement: Element
    satisfied_by: list[Element] = field(default_factory=list)
    verified_by: list[Element] = field(default_factory=list)
    refined_by: list[Element] = field(default_factory=list)
    derived_from: list[Element] = field(default_factory=list)
    derives: list[Element] = field(default_factory=list)
    traced: list[tuple[str, Element]] = field(default_factory=list)  # (direction, other)
    functions: list[Hop] = field(default_factory=list)
    parents: list[Hop] = field(default_factory=list)
    blocks: list[Hop] = field(default_factory=list)
    allocated: list[Hop] = field(default_factory=list)
    product: list[Hop] = field(default_factory=list)
    tests: list[TestTouch] = field(default_factory=list)

    @property
    def status(self) -> str:
        if not self.functions:
            return "none"
        if self.blocks and self.allocated and self.product and self.tests:
            return "full"
        return "partial"

    def roles(self) -> dict[str, str]:
        """element id -> hop role, for every element in the chain."""
        out = {self.requirement.id: "requirement"}
        levels = (
            ("function", self.functions),
            ("parent", self.parents),
            ("block", self.blocks),
            ("allocated", self.allocated),
            ("product", self.product),
        )
        for role, hops in levels:
            for h in hops:
                out.setdefault(h.element.id, role)
        return out

    def test_elements(self) -> list[Element]:
        seen: dict[str, Element] = {}
        for t in self.tests:
            seen.setdefault(t.test.id, t.test)
        return list(seen.values())

    def as_dict(self, m: Model) -> dict:
        req = self.requirement
        pkg = m.package_of(req.id)
        return {
            "requirement": {**_ref(req), "req_id": req_id(req), "package": pkg.name if pkg else "", "text": req_text(req)},
            "status": self.status,
            "satisfied_by": [_short(e) for e in self.satisfied_by],
            "verified_by": [_short(e) for e in self.verified_by],
            "refined_by": [_short(e) for e in self.refined_by],
            "derived_from": [_short(e) for e in self.derived_from],
            "derives": [_short(e) for e in self.derives],
            "traced": [{**_short(e), "direction": d} for d, e in self.traced],
            "functions": [h.as_dict() for h in self.functions],
            "parents": [h.as_dict() for h in self.parents],
            "blocks": [h.as_dict() for h in self.blocks],
            "allocated": [h.as_dict() for h in self.allocated],
            "product": [h.as_dict() for h in self.product],
            "tests": self._tests_dict(),
        }

    def _tests_dict(self) -> list[dict]:
        grouped: dict[str, dict] = {}
        for t in self.tests:
            g = grouped.setdefault(t.test.id, {**_ref(t.test), "touches": []})
            g["touches"].append({"element": t.target.name, "role": t.role, "evidence": t.evidence})
        return list(grouped.values())


# --------------------------------------------------------------------------- test index
@dataclass
class TestInfo:
    element: Element
    touched: dict[str, list[tuple[str, str]]] = field(default_factory=lambda: defaultdict(list))  # target id -> [(evidence, edge)]
    data_items: list[Element] = field(default_factory=list)  # ResourceInformation / test-data items typing pins
    core_tokens: set[str] = field(default_factory=set)  # own name + documentation
    ext_tokens: set[str] = field(default_factory=set)  # + called test activities + data items
    ext_text: str = ""

    def touch(self, target: Element, evidence: str, edge: str) -> None:
        if (evidence, edge) not in self.touched[target.id]:
            self.touched[target.id].append((evidence, edge))


def _typed_descendants(m: Model, root: Element) -> list[tuple[Element, Element]]:
    out = []
    for d in m.descendants(root.id):
        if d.kind in (
            "InputPin",
            "OutputPin",
            "ActivityParameterNode",
            "Property",
            "Port",
            "Parameter",
            "CentralBufferNode",
            "DataStoreNode",
        ):
            t = m.type_of(d)
            if t is not None:
                out.append((d, t))
    return out


def build_test_index(m: Model) -> list[TestInfo]:
    """Everything each TestCase / TestProcedure reaches: calls (transitively through same-project activities that are
    not themselves test cases / procedures), dependencies, allocations, swimlanes and typed pins."""
    tests = m.with_stereotype(*TEST_STEREOTYPES)
    test_ids = {t.id for t in tests}
    out = []
    for t in tests:
        info = TestInfo(t)
        texts = [t.name, strip_html(t.doc)]
        info.core_tokens = tokens(" ".join(texts))
        seen = {t.id}
        frontier = [t]
        while frontier:
            x = frontier.pop()
            if x is not t:
                texts += [x.name, strip_html(x.doc)]
            for label, direction, other in relationships(m, x):
                if other.id in seen or other.kind in ("Comment", "Diagram"):
                    continue
                edge = "allocate" if label == "Allocate" else "trace" if label == "Trace" else "dependency"
                info.touch(other, f"{label} {direction} {other.kind} '{other.name}'", edge)
            for d in m.descendants(x.id):
                if d.kind == "CallBehaviorAction":
                    for bid in d.refs.get("behavior", []):
                        beh = m.get(bid)
                        if beh is None:
                            continue
                        info.touch(beh, f"calls {beh.kind} '{beh.name}'", "call")
                        if beh.id not in seen and beh.id not in test_ids and beh.project == t.project:
                            seen.add(beh.id)
                            frontier.append(beh)
                elif d.kind == "ActivityPartition":
                    for rid in d.refs.get("represents", []):
                        rep = m.get(rid)
                        if rep is not None:
                            info.touch(rep, f"{_lane(d)} represents {rep.kind} '{rep.name}'", "partition")
            for pin, typ in _typed_descendants(m, x):
                if typ.has_stereotype("ResourceInformation", "TestData", "DataPool", "DataPartition"):
                    if typ not in info.data_items:
                        info.data_items.append(typ)
                else:
                    info.touch(typ, f"pin '{pin.name}' typed by {typ.kind} '{typ.name}'", "type")
        texts += [f"{d.name} {strip_html(d.doc)}" for d in info.data_items]
        info.ext_text = " ".join(texts).lower()
        info.ext_tokens = tokens(info.ext_text)
        out.append(info)
    return out


# --------------------------------------------------------------------------- chain building
def _realizers(m: Model, target: Element, forbidden_projects: set[str], cross_project: bool) -> list[Hop]:
    """Blocks that realise / specialise / are typed by ``target`` (or by one of its ports), in another project."""
    hops: dict[str, Hop] = {}

    def ok(el: Element) -> bool:
        return _is_block(el) and el.id != target.id and (not cross_project or el.project not in forbidden_projects)

    def add(el: Element, via: str, heuristic: bool = False) -> None:
        if ok(el) and el.id not in hops:
            hops[el.id] = Hop(el, via, target.id, heuristic)

    def owning_block(el: Element) -> Element | None:
        cur: Element | None = el
        while cur is not None and not _is_block(cur):
            cur = m.get(cur.owner) if cur.owner else None
        return cur

    def allocated_blocks(act: Element) -> list[Element]:
        outb = [o for lab, d, o in relationships(m, act) if lab == "Allocate" and d == "->" and _is_block(o)]
        for d in m.descendants(act.id):
            if d.kind == "ActivityPartition":
                outb += [r for rid in d.refs.get("represents", []) if (r := m.get(rid)) is not None and _is_block(r)]
        return outb

    ends = [target] + [c for cid in target.children if (c := m.get(cid)) is not None and c.kind == "Port"]
    for end in ends:
        suffix = "" if end is target else f" (via port '{end.name}')"
        for label, direction, other in relationships(m, end):
            if direction != "<-" or label not in REALIZE_LABELS:
                continue
            if _is_block(other):
                add(other, f"{label} <-{suffix}")
            elif other.kind == "Activity" and label == "Realization":
                for b in allocated_blocks(other):
                    add(b, f"{label} <- Activity '{other.name}' allocated to")
            else:
                ob = owning_block(other)
                if ob is not None:
                    add(ob, f"{label} <-{suffix} owner of '{other.name}'")
        for gen in m.incoming(end.id, "general"):
            if gen.kind == "Generalization" and gen.owner and (sub := m.get(gen.owner)) is not None:
                add(sub, f"Generalization <-{suffix}")
        for prop in m.incoming(end.id, "type"):
            if prop.kind in ("Property", "Port") and prop.owner and (ob := m.get(prop.owner)) is not None:
                add(ob, f"part '{prop.name}' typed by{suffix}")
    if not hops:
        want = _norm_name(target.name)
        if len(want) >= 4:
            for b in m.blocks():
                if _norm_name(b.name) == want:
                    add(b, "same-name (heuristic)", heuristic=True)
    return list(hops.values())


def build_chain(m: Model, req: Element, tests: list[TestInfo], requirement_ids: set[str]) -> Chain:
    c = Chain(req)
    cross = len(m.projects) > 1
    test_ids = {t.element.id for t in tests}
    funcs: dict[str, Hop] = {}
    for label, direction, other in relationships(m, req):
        is_req = other.id in requirement_ids
        if label == "Satisfy" and direction == "<-":
            c.satisfied_by.append(other)
        elif label == "Verify" and direction == "<-":
            c.verified_by.append(other)
        elif label == "Refine" and not is_req:
            c.refined_by.append(other)
        elif label == "DeriveReqt":
            (c.derived_from if direction == "->" else c.derives).append(other)
        elif label == "Trace":
            c.traced.append((direction, other))
        if label in FUNCTION_LABELS and not is_req and other.kind in FUNCTION_KINDS and other.id not in test_ids:
            if other.id in funcs:
                funcs[other.id].via += f", {label} {direction}"
            else:
                funcs[other.id] = Hop(other, f"{label} {direction}", req.id)
    c.functions = list(funcs.values())

    parents: dict[str, Hop] = {}
    for f in c.functions:
        if f.element.kind != "Activity":
            continue
        for call in m.incoming(f.element.id, "behavior"):
            if call.kind != "CallBehaviorAction":
                continue
            caller = next((a for a in m.owner_chain(call.id) if a.kind == "Activity"), None)
            if caller is None or caller.id in funcs or caller.id in test_ids or caller.project != f.element.project:
                continue
            if caller.id not in parents:
                parents[caller.id] = Hop(caller, f"called by (calls '{f.element.name}')", f.element.id)
    c.parents = list(parents.values())

    blocks: dict[str, Hop] = {}
    for f in c.functions:
        el = f.element
        if _is_block(el):
            continue  # the function is a block already; allocated hops hang off it directly
        for label, direction, other in relationships(m, el):
            if label == "Allocate" and direction == "->" and _is_block(other) and other.id not in blocks:
                blocks[other.id] = Hop(other, "Allocate ->", el.id)
        for d in m.descendants(el.id):
            if d.kind == "ActivityPartition":
                for rid in d.refs.get("represents", []):
                    r = m.get(rid)
                    if r is not None and _is_block(r) and r.id not in blocks:
                        blocks[r.id] = Hop(r, f"{_lane(d)} represents", el.id)
        owner = m.get(el.owner) if el.owner else None
        if owner is not None and _is_block(owner) and owner.id not in blocks:
            blocks[owner.id] = Hop(owner, "owned behavior of", el.id)
    c.blocks = list(blocks.values())

    upstream = {h.element.project for h in c.functions + c.blocks} | {req.project}
    alloc: dict[str, Hop] = {}
    for b in [h.element for h in c.functions if _is_block(h.element)] + [h.element for h in c.blocks]:
        for hop in _realizers(m, b, upstream, cross):
            alloc.setdefault(hop.element.id, hop)
    c.allocated = list(alloc.values())

    upstream |= {h.element.project for h in c.allocated}
    prod: dict[str, Hop] = {}
    for h in c.allocated:
        for hop in _realizers(m, h.element, upstream, cross):
            prod.setdefault(hop.element.id, hop)
    c.product = list(prod.values())

    roles = c.roles()
    order = {"requirement": 0, "function": 1, "parent": 2, "block": 3, "allocated": 4, "product": 5}
    for ti in tests:
        for tid, evs in ti.touched.items():
            if tid in roles and tid != ti.element.id:
                target = m.elements[tid]
                for evidence, edge in evs:
                    c.tests.append(TestTouch(ti.element, target, roles[tid], evidence, edge))
    c.tests.sort(key=lambda t: (order[t.role], t.test.name))
    return c


def build_chains(m: Model, tests: list[TestInfo] | None = None) -> list[Chain]:
    tests = build_test_index(m) if tests is None else tests
    reqs = m.requirements()
    ids = {r.id for r in reqs}
    chains = [build_chain(m, r, tests, ids) for r in reqs]
    chains.sort(key=lambda c: (c.requirement.project, m.qualified_name(c.requirement.id)))
    return chains


# --------------------------------------------------------------------------- proposals
@dataclass
class Proposal:
    requirement: Element
    test: Element
    confidence: str
    score: float
    structural: list[str]
    lexical: list[str]
    trace: list[str]

    @property
    def rationale(self) -> str:
        parts = []
        if self.structural:
            parts.append("structural: " + "; ".join(self.structural))
        if self.lexical:
            parts.append("lexical: " + "; ".join(self.lexical))
        if self.trace:
            parts.append("existing link: " + "; ".join(self.trace))
        return "HEURISTIC PROPOSAL (not in model) - " + " | ".join(parts)

    def as_dict(self) -> dict:
        return {
            "requirement": {**_ref(self.requirement), "req_id": req_id(self.requirement)},
            "test": _ref(self.test),
            "confidence": self.confidence,
            "score": round(self.score, 3),
            "rationale": self.rationale,
        }


_ROLE_WEIGHT = {"requirement": 1.0, "function": 1.0, "parent": 0.9, "block": 0.6, "allocated": 0.6, "product": 0.6}
_EDGE_WEIGHT = {"call": 1.0, "dependency": 1.0, "trace": 1.0, "allocate": 0.9, "partition": 0.5, "type": 0.4}


def _score(m: Model, chain: Chain, ti: TestInfo) -> Proposal | None:
    req = chain.requirement
    roles = chain.roles()
    structural: list[str] = []
    struct_max = 0.0
    for tid, evs in ti.touched.items():
        role = roles.get(tid)
        if role is None or tid == ti.element.id:
            continue
        target = m.elements[tid]
        for evidence, edge in evs:
            w = _ROLE_WEIGHT[role] * _EDGE_WEIGHT[edge]
            if edge == "allocate" and _is_block(target):
                w = min(w, 0.6)  # a test activity performed by / allocated to a block says little about which function it checks
            struct_max = max(struct_max, w)
            how = "the requirement itself" if role == "requirement" else f"{role} hop '{target.name}'"
            structural.append(f"{ti.element.stereotype_names()[0] if ti.element.stereotypes else ti.element.kind} {evidence} = {how}")
    struct_score = struct_max + min(0.1 * (len(structural) - 1), 0.3) if structural else 0.0

    rt = tokens(f"{req.name} {req_text(req)}")
    lexical: list[str] = []
    lex = 0.0
    shared_core = rt & ti.core_tokens
    shared_ext = rt & ti.ext_tokens
    if rt:
        lex = max(len(shared_core) / len(rt), 0.5 * len(shared_ext) / len(rt))
        shared = shared_core or shared_ext
        if shared and lex >= 0.1:
            where = "test name/doc" if shared_core else "called test activities / test data"
            lexical.append(f"{len(shared)}/{len(rt)} requirement tokens in {where}: {', '.join(sorted(shared)[:8])}")
    rid = req_id(req)
    id_hit = (
        bool(rid)
        and len(rid) >= 3
        and not rid.isdigit()
        and re.search(r"(?<![\w.\-])" + re.escape(rid.lower()) + r"(?![\w.\-])", ti.ext_text) is not None
    )
    if id_hit:
        lexical.append(f"requirement Id '{rid}' appears in test text")
    name_hit = len(req.name) >= 8 and req.name.lower() in ti.ext_text
    if name_hit:
        lexical.append(f"requirement name '{req.name}' appears verbatim in test text")

    trace: list[str] = []
    for label, direction, other in relationships(m, req):
        if other.id == ti.element.id:
            trace.append(f"{label} {direction} '{other.name}'")

    score = struct_score + lex + (0.5 if id_hit else 0.0) + (0.3 if name_hit else 0.0) + (0.8 if trace else 0.0)
    strong = struct_max >= 0.9
    medium_struct = struct_max >= 0.5
    if strong or id_hit or trace or (medium_struct and len(shared_core) >= 2 and len(shared_core) / len(rt) >= 0.2):
        conf = "high"
    elif medium_struct or name_hit or (lex >= 0.35 and len(shared_core | shared_ext) >= 3) or (struct_max > 0 and lex >= 0.15):
        conf = "medium"
    elif struct_max > 0 or (lex >= 0.15 and len(shared_core | shared_ext) >= 2):
        conf = "low"
    else:
        return None
    return Proposal(req, ti.element, conf, score, structural, lexical, trace)


def propose_verify(m: Model, chains: list[Chain], tests: list[TestInfo], min_confidence: str = "low") -> list[Proposal]:
    """Ranked Verify proposals for every requirement without an existing Verify (top N per requirement)."""
    floor = CONFIDENCE_RANK[min_confidence]
    out: list[Proposal] = []
    for c in chains:
        if c.verified_by:
            continue
        cands = [p for ti in tests if (p := _score(m, c, ti)) is not None and CONFIDENCE_RANK[p.confidence] >= floor]
        cands.sort(key=lambda p: (-CONFIDENCE_RANK[p.confidence], -p.score, p.test.name))
        out.extend(cands[:MAX_PROPOSALS_PER_REQUIREMENT])
    return out


# --------------------------------------------------------------------------- summary
def summarize(m: Model, chains: list[Chain], proposals: list[Proposal]) -> dict:
    status = Counter(c.status for c in chains)
    by_pkg: dict[str, Counter] = defaultdict(Counter)
    for c in chains:
        pkg = m.package_of(c.requirement.id)
        key = f"{c.requirement.project or m.name} :: {pkg.name if pkg else '?'}"
        by_pkg[key]["total"] += 1
        by_pkg[key][c.status] += 1
        by_pkg[key]["verified"] += bool(c.verified_by)
        by_pkg[key]["satisfied"] += bool(c.satisfied_by)
        by_pkg[key]["tested"] += bool(c.tests)
    verify_rels = [e for e in m.with_stereotype("Verify")]
    return {
        "model": m.name,
        "projects": dict(m.projects),
        "missing_projects": list(m.missing_projects),
        "requirements": len(chains),
        "with_satisfy": sum(1 for c in chains if c.satisfied_by),
        "without_satisfy": sum(1 for c in chains if not c.satisfied_by),
        "with_verify": sum(1 for c in chains if c.verified_by),
        "without_verify": sum(1 for c in chains if not c.verified_by),
        "verify_relationships_in_model": len(verify_rels),
        "with_function_hop": sum(1 for c in chains if c.functions),
        "with_allocated_hop": sum(1 for c in chains if c.allocated),
        "with_product_hop": sum(1 for c in chains if c.product),
        "with_test_touch": sum(1 for c in chains if c.tests),
        "status": {"full": status["full"], "partial": status["partial"], "none": status["none"]},
        "by_package": {k: dict(v) for k, v in sorted(by_pkg.items())},
        "test_elements": len(m.with_stereotype(*TEST_STEREOTYPES)),
        "proposals": Counter(p.confidence for p in proposals),
        "requirements_with_proposal": len({p.requirement.id for p in proposals}),
    }


# --------------------------------------------------------------------------- rendering
def _cell(items: list[str], gap: str) -> str:
    return "; ".join(dict.fromkeys(items)) if items else f"GAP: {gap}"


def _row(m: Model, c: Chain) -> dict[str, str]:
    req = c.requirement
    pkg = m.package_of(req.id)
    return {
        "Id": req_id(req),
        "Requirement": req.name,
        "Package": pkg.name if pkg else "",
        "Project": req.project,
        "Status": c.status,
        "Satisfied by": _cell([e.name for e in c.satisfied_by], "no Satisfy"),
        "Refined by": _cell([e.name for e in c.refined_by], "no Refine"),
        "Derived": _cell([f"from {e.name}" for e in c.derived_from] + [f"derives {e.name}" for e in c.derives], "no DeriveReqt"),
        "Traced": _cell([f"{d} {e.name}" for d, e in c.traced], "no Trace"),
        "Function (FSA)": _cell(
            [f"{h.element.name} [{h.via}]" for h in c.functions], "no Satisfy/Refine/Trace/Allocate to a function or block"
        ),
        "Parent function": _cell([f"{h.element.name} [{h.via}]" for h in c.parents], "no activity calls the function"),
        "Functional block": _cell(
            [f"{h.element.name} [{h.via}]" for h in c.blocks] + [h.element.name for h in c.functions if _is_block(h.element)],
            "function not allocated to a block",
        ),
        "Allocated block": _cell(
            [f"{h.element.name} [{h.via}]" for h in c.allocated], "no allocated-baseline block realises the functional block"
        ),
        "Product block": _cell(
            [f"{h.element.name} [{h.via}]" for h in c.product], "no product-baseline block realises the allocated block"
        ),
        "Tests touching chain": _cell([f"{t.test.name} ({t.evidence})" for t in c.tests], "no test case / procedure touches the chain"),
        "Verified by": _cell([e.name for e in c.verified_by], "no Verify"),
    }


def rvtm_rows(m: Model, chains: list[Chain]) -> list[dict[str, str]]:
    return [_row(m, c) for c in chains]


def _md_escape(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def _md_table(header: list[str], rows: list[list[str]]) -> list[str]:
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(_md_escape(str(c)) for c in r) + " |" for r in rows]
    return out


def render_rvtm_md(m: Model, chains: list[Chain], summary: dict) -> str:
    L = [f"# Requirements verification traceability matrix - {m.name}", ""]
    L.append(f"Projects loaded ({len(summary['projects'])}): " + ", ".join(f"{k} ({v})" for k, v in summary["projects"].items()))
    if summary["missing_projects"]:
        L.append(f"Mounted but missing on disk: {', '.join(summary['missing_projects'])}")
    L += ["", "## Summary", ""]
    L += [
        f"- Requirements: **{summary['requirements']}**",
        f"- With Satisfy: {summary['with_satisfy']} - without: **{summary['without_satisfy']}**",
        f"- With Verify: {summary['with_verify']} - without: **{summary['without_verify']}** "
        f"({summary['verify_relationships_in_model']} Verify relationships exist anywhere in the loaded projects)",
        f"- Function hop present: {summary['with_function_hop']}; allocated-baseline hop: {summary['with_allocated_hop']}; "
        f"product-baseline hop: {summary['with_product_hop']}; touched by a test: {summary['with_test_touch']}",
        f"- Chain status: full **{summary['status']['full']}**, partial **{summary['status']['partial']}**, "
        f"none **{summary['status']['none']}**",
        f"- Test cases / procedures in scope: {summary['test_elements']}",
        "",
        "`full` = function, functional block, allocated block, product block and at least one test touching the chain; "
        "`partial` = some hop present; `none` = no Satisfy/Refine/Trace/Allocate from the requirement at all. "
        "`GAP:` marks an empty hop. Every hop is an existing relationship in the loaded data "
        "(rows tagged `same-name (heuristic)` are the only inferred mapping).",
        "",
        "## Per requirement package",
        "",
    ]
    L += _md_table(
        ["Project :: package", "Requirements", "Full", "Partial", "None", "Satisfied", "Verified", "Tested"],
        [
            [
                k,
                v.get("total", 0),
                v.get("full", 0),
                v.get("partial", 0),
                v.get("none", 0),
                v.get("satisfied", 0),
                v.get("verified", 0),
                v.get("tested", 0),
            ]
            for k, v in summary["by_package"].items()
        ],
    )
    L += ["", "## Matrix", ""]
    rows = rvtm_rows(m, chains)
    if rows:
        header = list(rows[0])
        L += _md_table(header, [[r[h] for h in header] for r in rows])
    return "\n".join(L) + "\n"


def write_rvtm_csv(m: Model, chains: list[Chain], path: Path) -> None:
    rows = rvtm_rows(m, chains)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["Id"])
        w.writeheader()
        w.writerows(rows)


def render_proposals_md(m: Model, proposals: list[Proposal], summary: dict, min_confidence: str) -> str:
    L = [f"# Proposed Verify links - {m.name}", ""]
    L += [
        "Every row is a **heuristic proposal**, not an existing model relationship. Confidence: `high` = structural evidence "
        "on the function hop (the test calls / depends on the activity that satisfies the requirement), the requirement Id "
        "appears in the test text, or an existing Trace links the pair; `medium` = structural evidence on a downstream block "
        "or strong text overlap; `low` = weak text overlap or a typed-pin / swimlane touch only.",
        "",
        f"Requirements without Verify: {summary['without_verify']}; proposals (>= {min_confidence}): "
        + ", ".join(f"{k} {v}" for k, v in sorted(summary["proposals"].items(), key=lambda kv: -CONFIDENCE_RANK[kv[0]]))
        + f"; requirements covered: {summary['requirements_with_proposal']}.",
        "Proposals with confidence >= medium are also emitted as an XMI fragment and a Cameo-importable CSV next to this file.",
        "",
    ]
    L += _md_table(
        ["Req Id", "Requirement", "Proposed test (client)", "Kind", "Confidence", "Score", "Rationale"],
        [
            [
                req_id(p.requirement),
                p.requirement.name,
                p.test.name,
                ",".join(p.test.stereotype_names()) or p.test.kind,
                p.confidence,
                f"{p.score:.2f}",
                p.rationale,
            ]
            for p in proposals
        ],
    )
    return "\n".join(L) + "\n"


def _patch_id(p: Proposal, kind: str) -> str:
    return f"_proposed_{kind}_" + hashlib.sha1(f"{p.test.id}|{p.requirement.id}".encode()).hexdigest()[:16]


def render_patch_xmi(m: Model, proposals: list[Proposal]) -> str:
    """SysML v1 XMI fragment: one uml:Abstraction per proposal (client = test, supplier = requirement) plus its
    sysml:Verify stereotype application. Client/supplier reference the real xmi:ids of the loaded elements."""
    projects = sorted({p.test.project for p in proposals} | {p.requirement.project for p in proposals})
    L = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<xmi:XMI xmi:version="2.5.1" xmlns:xmi="http://www.omg.org/spec/XMI/20131001"',
        '         xmlns:uml="http://www.omg.org/spec/UML/20131001"',
        '         xmlns:sysml="http://www.omg.org/spec/SysML/20181001/SysML">',
        f"  <!-- Proposed Verify relationships for {escape(m.name)}: HEURISTIC, for engineering review. -->",
        f"  <!-- client / supplier idrefs point at elements in: {escape(', '.join(p for p in projects if p))} -->",
        f'  <uml:Package xmi:id="_proposed_verify_pkg" name="Proposed Verify links ({len(proposals)}, review before applying)">',
    ]
    for p in proposals:
        aid = _patch_id(p, "verify")
        name = f"verify: {p.test.name} -> {p.requirement.name}"
        body = f"confidence={p.confidence}; {p.rationale}"
        L += [
            f'    <packagedElement xmi:type="uml:Abstraction" xmi:id="{aid}" name={quoteattr(name)}>',
            f'      <client xmi:idref="{escape(p.test.id)}"/>',
            f'      <supplier xmi:idref="{escape(p.requirement.id)}"/>',
            f'      <ownedComment xmi:type="uml:Comment" xmi:id="{_patch_id(p, "comment")}" body={quoteattr(body)}/>',
            "    </packagedElement>",
        ]
    L.append("  </uml:Package>")
    for p in proposals:
        L.append(f'  <sysml:Verify xmi:id="{_patch_id(p, "stereo")}" base_Abstraction="{_patch_id(p, "verify")}"/>')
    L.append("</xmi:XMI>")
    return "\n".join(L) + "\n"


def write_patch_csv(proposals: list[Proposal], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source id", "target id", "relationship"])
        for p in proposals:
            w.writerow([p.test.id, p.requirement.id, "Verify"])


# --------------------------------------------------------------------------- single-requirement tree
def render_chain_tree(m: Model, c: Chain, proposals: list[Proposal]) -> list[str]:
    """ASCII tree in the ``queries.render_trace`` style, with GAP: lines where a hop is empty."""
    req = c.requirement
    rid = req_id(req)
    lines = [f"{rid + ' ' if rid else ''}{_label(req)}"]
    text = req_text(req)
    if text:
        lines.append(f"  Text: {text[:300]}{'...' if len(text) > 300 else ''}")
    for e in c.verified_by:
        lines.append(f"  [Verify <-] {_label(e)}")
    if not c.verified_by:
        lines.append("  GAP: no Verify relationship has this requirement as supplier (from loaded data)")
    for d, e in c.traced:
        if e.id not in {h.element.id for h in c.functions}:
            lines.append(f"  [Trace {d}] {_label(e)}")
    for e in c.derived_from:
        lines.append(f"  [DeriveReqt ->] {_label(e)}")

    def children(parent: str, hops: list[Hop]) -> list[Hop]:
        return [h for h in hops if h.source == parent]

    def render_hop(h: Hop, indent: int, next_levels: list[tuple[str, list[Hop], str]]) -> None:
        pad = "  " * indent
        flag = "  (heuristic name match)" if h.heuristic else ""
        lines.append(f"{pad}[{h.via}] {_label(h.element)}{flag}")
        for p in children(h.element.id, c.parents):
            lines.append(f"{pad}  [{p.via}] {_label(p.element)}")
        if not next_levels:
            return
        name, hops, gap = next_levels[0]
        kids = children(h.element.id, hops)
        if kids:
            for k in kids:
                render_hop(k, indent + 1, next_levels[1:])
        elif name == "block" and _is_block(h.element):
            # a block-valued function skips the "functional block" level
            kids = children(h.element.id, next_levels[1][1])
            if kids:
                for k in kids:
                    render_hop(k, indent + 1, next_levels[2:])
            else:
                lines.append(f"{pad}  GAP: {next_levels[1][2]} '{h.element.name}'")
        else:
            lines.append(f"{pad}  GAP: {gap} '{h.element.name}'")

    levels = [
        ("block", c.blocks, "function is not allocated to / owned by a block:"),
        ("allocated", c.allocated, "no allocated-baseline block realises / specialises / is typed by"),
        ("product", c.product, "no product-baseline block realises / specialises / is typed by"),
    ]
    if c.functions:
        for f in c.functions:
            render_hop(f, 1, levels)
    else:
        lines.append("  GAP: no Satisfy / Refine / Trace / Allocate from this requirement to an activity or block")
    lines.append("  Tests touching the chain (existing relationships):")
    if c.tests:
        for t in c.tests:
            lines.append(f"    {_label(t.test)}: {t.evidence} -> {t.role} hop")
    else:
        lines.append("    GAP: no TestCase / TestProcedure calls, depends on, is allocated to or types anything in the chain")
    mine = [p for p in proposals if p.requirement.id == req.id]
    lines.append(f"  Proposed Verify links (HEURISTIC, {len(mine)}):")
    for p in mine:
        lines.append(f"    [{p.confidence}] {_label(p.test)}  score={p.score:.2f}")
        lines.append(f"      {p.rationale}")
    if not mine and not c.verified_by:
        lines.append("    (no candidate reached the confidence floor)")
    return lines


def find_requirement(m: Model, needle: str) -> Element | None:
    reqs = m.requirements()
    n = needle.strip().lower()
    for r in reqs:
        if r.id == needle or req_id(r).lower() == n or r.name.lower() == n:
            return r
    hits = [r for r in reqs if n in r.name.lower() or n in req_id(r).lower()]
    hits.sort(key=lambda r: len(r.name))
    return hits[0] if hits else None


# --------------------------------------------------------------------------- driver
@dataclass
class ThreadResult:
    chains: list[Chain]
    tests: list[TestInfo]
    proposals: list[Proposal]
    summary: dict
    written: list[Path] = field(default_factory=list)


def run(m: Model, out_dir: Path | None = None, stem: str = "thread", min_confidence: str = "low") -> ThreadResult:
    tests = build_test_index(m)
    chains = build_chains(m, tests)
    proposals = propose_verify(m, chains, tests, min_confidence)
    summary = summarize(m, chains, proposals)
    res = ThreadResult(chains, tests, proposals, summary)
    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        patch = [p for p in proposals if CONFIDENCE_RANK[p.confidence] >= CONFIDENCE_RANK["medium"]]
        files: dict[str, str | None] = {
            f"{stem}_rvtm.md": render_rvtm_md(m, chains, summary),
            f"{stem}_rvtm.json": _json({"summary": summary, "rows": [c.as_dict(m) for c in chains]}),
            f"{stem}_proposed_verify.md": render_proposals_md(m, proposals, summary, min_confidence),
            f"{stem}_proposed_verify.json": _json(
                {"summary": summary, "min_confidence": min_confidence, "proposals": [p.as_dict() for p in proposals]}
            ),
            f"{stem}_proposed_verify.xmi": render_patch_xmi(m, patch),
        }
        for name, content in files.items():
            if content is not None:
                (out_dir / name).write_text(content, encoding="utf-8")
                res.written.append(out_dir / name)
        write_rvtm_csv(m, chains, out_dir / f"{stem}_rvtm.csv")
        write_patch_csv(patch, out_dir / f"{stem}_proposed_verify.csv")
        res.written += [out_dir / f"{stem}_rvtm.csv", out_dir / f"{stem}_proposed_verify.csv"]
    return res


def render_summary(summary: dict) -> list[str]:
    s = summary
    L = [
        f"{s['model']}: {s['requirements']} requirements across {len(s['projects'])} projects"
        + (f" (missing: {', '.join(s['missing_projects'])})" if s["missing_projects"] else ""),
        f"  Satisfy: {s['with_satisfy']} have / {s['without_satisfy']} lack    "
        f"Verify: {s['with_verify']} have / {s['without_verify']} lack  "
        f"({s['verify_relationships_in_model']} Verify relationships in loaded data)",
        f"  hops: function {s['with_function_hop']}  allocated {s['with_allocated_hop']}  "
        f"product {s['with_product_hop']}  tested {s['with_test_touch']}",
        f"  chain status: full {s['status']['full']}  partial {s['status']['partial']}  none {s['status']['none']}",
        "  proposed Verify: "
        + (", ".join(f"{k} {v}" for k, v in sorted(s["proposals"].items(), key=lambda kv: -CONFIDENCE_RANK[kv[0]])) or "none")
        + f"  ({s['requirements_with_proposal']} requirements covered)",
        "  per package:",
    ]
    for k, v in s["by_package"].items():
        L.append(
            f"    {k}: {v.get('total', 0)} reqs  full {v.get('full', 0)}  partial {v.get('partial', 0)}  "
            f"none {v.get('none', 0)}  verified {v.get('verified', 0)}"
        )
    return L
