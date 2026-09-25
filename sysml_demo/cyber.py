"""Cyber resiliency gap analysis over an STPA-Sec model.

For one risk scenario: walk Loss <- Hazard <- SecurityConstraint <- Controller / HazardousControlAction
<- LossScenario <- RiskScenario -> probabilistic attack tree -> leaf nodes, find the cybersecurity
requirements the model already ties to each leaf, propose ATT&CK techniques / D3FEND countermeasures
(heuristic, confidence-scored) and candidate NIST SP 800-53r5 controls, and report the gaps.

Stereotype names below are the ones actually applied in the IGNITE Berserker Cyber model
(STPA-Sec Profile (Plug and Play) + D3FEND_SE_SysML_0.0.4-ALPHA); nothing is assumed from SysML.
Everything under "proposed" / "candidate" is a heuristic, never an existing model relationship.
"""

from __future__ import annotations

import csv
import io
import json
import math
import re
from collections import Counter, defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path
from xml.sax.saxutils import quoteattr

from . import queries
from .ingest import strip_html
from .model import TRACE_STEREOTYPES, Element, Model

# --------------------------------------------------------------------------- vocabulary (learned from the profiles)
ST_RISK_SCENARIO = "Risk_Scenario"
ST_LOSS_SCENARIO = "Loss_Scenario"
ST_HCA = ("Hazardous_Control_Action", "Unsafe_Control_Action")
ST_HAZARD = "Hazard"
ST_LOSS = "Loss"
ST_CONSTRAINT = "Security_Constraint"
ST_CONTROLLER = "Controller"
ST_RESPONSIBILITY = "Responsibility"
ST_CONTROL_ACTION = "Control_Action"
ST_CONTROLLER_CONSTRAINT = "Controller_Constraint"
ST_RISK = "Risk"
ST_PAS = "Probability_of_Attack_Success"
ST_LEAF = "PAT_Leaf_Node"
ST_MIDDLE = "PAT_Middle_Node"
GATES = ("And", "Or")
EML_STEREOTYPES = ("Mission_Impact", "Percent_Systems_Impacted", "Probability_of_Adversary_Attack")
ASSURANCE_STEREOTYPES = ("Goal", "SolutionEvidence", "Strategy", "Assumption")
D3_OFFENSIVE = "Offensive_Technique"
D3_DEFENSIVE = "Defensive_Technique"
D3_ARTIFACT = "Digital_Artifact"
D3_TACTIC = "Defensive_Tactic"
D3_ASSOCIATION = "D3FEND_Association"
D3_STEREOTYPES = (D3_OFFENSIVE, D3_DEFENSIVE, D3_ARTIFACT, D3_TACTIC, "Offensive_Tactic", "Weakness", D3_ASSOCIATION)
REQ_LINKS = TRACE_STEREOTYPES | {"Dependency", "Abstraction"}  # what counts as "the model ties a requirement to X"

DEFAULT_SCENARIO = "adversary selected location"  # RS-2: adversary flies the AV where they want (ground-station / AV-link)
CONF = {"high": 3, "medium": 2, "low": 1}
TID_RE = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")
_SPLIT = re.compile(r"[^a-z0-9]+")
STOP = set(
    """
    the a an of to and or in on for by with via from into at is are be that this it its as may can will shall not no their they them
    through using use used uses adversary adversaries attacker attackers system systems av uas uav fly flies flying location selected
    select mission operations operation degrade degrades provide provides provided perform performs gain gains get gets which when where
    then than other such also any all one two more most if so up down out over under own e g i s t mq 99 berserker citation successfully
    attack attacks cyber connected sipr send sends give gives choice required during
    """.split()
)

# Curated domain hints: leaf/loss-scenario phrase -> ATT&CK technique ids. These are proposals authored for this
# demo (rationale says so); they exist because pure token overlap cannot bridge e.g. "man-in-the-middle" -> T1557.
ATTACK_HINTS: dict[str, list[str]] = {
    "man-in-the-middle": ["T1557"],
    "man in the middle": ["T1557"],
    "mitm": ["T1557"],
    "in the middle of": ["T1557"],
    "breaks encryption": ["T1600", "T1557"],
    "unencrypted mode": ["T1600", "T1562"],
    "encryption key": ["T1552.004", "T1557"],
    "command link key": ["T1552.004", "T1557"],
    "steals key": ["T1552.004"],
    "insider": ["T1078"],
    "supply chain": ["T1195", "T1195.002"],
    "spoof": ["T1557", "T1036"],
    "jamming": ["T1498", "T1499"],
    "denial of service": ["T1498", "T1499"],
    "dos ": ["T1498", "T1499"],
    "blocks": ["T1498"],
    "malicious command": ["T1059", "T1565"],
    "malicious commands": ["T1059", "T1565"],
    "alters": ["T1565"],
    "cyber attack on ground station": ["T1190", "T1133"],
    "traditional-it": ["T1190", "T1133"],
    "logical access": ["T1078", "T1133"],
    "maintenance port": ["T1200"],
    "usb": ["T1091", "T1200"],
    "firmware": ["T1542"],
    "secure boot": ["T1542"],
    "gps": ["T1557"],
}


# --------------------------------------------------------------------------- small helpers
def _name(e: Element) -> str:
    return " ".join(strip_html(e.name).split())


def _id(e: Element) -> str:
    return e.tag("ID") or e.tag("Id") or e.tag("id") or ""


def _label(e: Element, width: int = 0) -> str:
    n = _name(e)
    i = _id(e)
    s = f"{i} {n}" if i and not n.startswith(i) else n
    return s if not width or len(s) <= width else s[: width - 1] + "…"


def _num(v: str | None) -> float | None:
    if v is None:
        return None
    try:
        return float(v)
    except ValueError:
        return None


def _rels(m: Model, e: Element) -> list[tuple[str, str, Element]]:
    return queries.relationships(m, e)


def _linked(m: Model, e: Element, label: str | None, direction: str | None, *stereos: str) -> list[Element]:
    out: list[Element] = []
    seen: set[str] = set()
    for lab, d, o in _rels(m, e):
        if label is not None and lab != label:
            continue
        if direction is not None and d != direction:
            continue
        if stereos and not o.has_stereotype(*stereos):
            continue
        if o.id not in seen:
            seen.add(o.id)
            out.append(o)
    return out


def _sort_key(e: Element) -> tuple[int, str]:
    mnum = re.search(r"(\d+)", _id(e))
    return (int(mnum.group(1)) if mnum else 10**9, _name(e))


# Security-vocabulary canonicalisation so that e.g. a leaf about an "unencrypted" link meets a "Cryptographic Module" requirement.
CANON = {
    "unencrypt": "encryption", "encrypt": "encryption", "encryption": "encryption", "decrypt": "encryption",
    "crypto": "encryption", "cryptographic": "encryption", "cryptography": "encryption", "cipher": "encryption",
    "key": "key", "keying": "key", "authenticat": "authentication", "authentication": "authentication",
    "mfa": "authentication", "login": "authentication", "credential": "authentication", "password": "authentication",
    "spoof": "spoof", "spoofing": "spoof", "comm": "communication", "communication": "communication",
    "datalink": "communication", "gp": "gps", "nav": "navigation", "navigation": "navigation",
    "insider": "insider", "boot": "boot", "firmware": "firmware", "software": "software", "ofp": "software",
    "maintenance": "maintenance", "mx": "maintenance", "logistic": "maintenance", "port": "port",
}  # fmt: skip


def _tokens(text: str) -> set[str]:
    out = set()
    for t in _SPLIT.split(text.lower()):
        if not t or t in STOP or t.isdigit():
            continue
        if t in CANON:
            out.add(CANON[t])
            continue
        if len(t) > 5 and t.endswith("ing"):
            t = t[:-3]
        elif len(t) > 4 and t.endswith("ed"):
            t = t[:-2]
        elif len(t) > 4 and t.endswith("es"):
            t = t[:-2]
        elif len(t) > 3 and t.endswith("s"):
            t = t[:-1]
        out.add(CANON.get(t, t))
    return out


def _is_cyber_requirement(m: Model, r: Element) -> bool:
    qn = m.qualified_name(r.id).lower()
    return "cyber" in qn or "security" in qn


# --------------------------------------------------------------------------- data model
@dataclass
class TreeNode:
    element: Element
    gate: str  # And / Or / "" for the root
    children: list[TreeNode] = field(default_factory=list)

    @property
    def is_leaf(self) -> bool:
        return self.element.has_stereotype(ST_LEAF) or not self.children


@dataclass
class ReqLink:
    requirement: Element
    kind: str  # direct | allocation | lexical
    confidence: str
    rationale: str
    ids: list[str] = field(default_factory=list)  # same-named duplicates across projects (FSA copy vs cyber copy)

    @property
    def label(self) -> str:
        return f"{'/'.join(self.ids) or _id(self.requirement)} {_name(self.requirement)}".strip()


@dataclass
class AttackMatch:
    technique: Element
    tid: str
    confidence: str
    score: float
    rationale: str

    @property
    def label(self) -> str:
        return _name(self.technique)


@dataclass
class Countermeasure:
    technique: Element
    tactic: str
    via: str  # direct | artifact
    confidence: str
    rationale: str
    from_tids: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return _name(self.technique)


@dataclass
class NistCandidate:
    control: str
    d3fend: str
    matched: str  # table entry that matched
    level: str  # technique | family | tactic
    tactic: str
    confidence: str
    source_confidence: str  # confidence of the D3FEND countermeasure this was derived from
    entry_rationale: str  # rationale text of the matched table entry

    @property
    def rationale(self) -> str:
        return (
            f"{self.level} entry '{self.matched}' in nist80053_d3fend.json: {self.entry_rationale} "
            f"(D3FEND countermeasure was {self.source_confidence}-confidence)"
        )


@dataclass
class Leaf:
    element: Element
    gate_path: list[str]
    in_tree: bool
    loss_scenarios: list[Element] = field(default_factory=list)
    hcas: list[Element] = field(default_factory=list)
    hazards: list[Element] = field(default_factory=list)
    losses: list[Element] = field(default_factory=list)
    controllers: list[Element] = field(default_factory=list)
    constraints: list[Element] = field(default_factory=list)
    requirements: list[ReqLink] = field(default_factory=list)
    other_requirements: int = 0  # non-cyber requirements reachable on the same model paths
    attack: list[AttackMatch] = field(default_factory=list)
    countermeasures: list[Countermeasure] = field(default_factory=list)
    anchored_artifacts: list[tuple[Element, Element]] = field(default_factory=list)  # (Berserker block, D3FEND artifact)
    nist: list[NistCandidate] = field(default_factory=list)

    @property
    def name(self) -> str:
        return _name(self.element)

    @property
    def p_low(self) -> float | None:
        return _num(self.element.tag("_90CI_Low"))

    @property
    def p_high(self) -> float | None:
        return _num(self.element.tag("_90CI_High"))

    @property
    def p_mid(self) -> float:
        lo, hi = self.p_low, self.p_high
        if lo is None and hi is None:
            return 0.0
        return ((lo or 0.0) + (hi if hi is not None else lo or 0.0)) / 2

    @property
    def sensitivity(self) -> float | None:
        return _num(self.element.tag("TotalRiskSensitivity"))

    @property
    def p_text(self) -> str:
        lo, hi = self.p_low, self.p_high
        if lo is None and hi is None:
            return "P=?"
        return f"P={lo if lo is not None else '?'}–{hi if hi is not None else '?'}"

    def covered_requirements(self, min_conf: str) -> list[ReqLink]:
        return [r for r in self.requirements if CONF[r.confidence] >= CONF[min_conf]]

    def covered_countermeasures(self, min_conf: str) -> list[Countermeasure]:
        return [c for c in self.countermeasures if CONF[c.confidence] >= CONF[min_conf]]

    def status(self, min_conf: str) -> str:
        r, c = bool(self.covered_requirements(min_conf)), bool(self.covered_countermeasures(min_conf))
        return "both" if r and c else "requirement-only" if r else "countermeasure-only" if c else "GAP"

    def gap_score(self, min_conf: str) -> float:
        no_req = 0 if self.covered_requirements(min_conf) else 1
        no_cm = 0 if self.covered_countermeasures(min_conf) else 1
        return self.p_mid * no_req * no_cm


@dataclass
class Scenario:
    element: Element
    risk: Element | None
    roots: list[TreeNode]
    eml: dict[str, str]
    loss_scenarios: list[Element]
    hcas: list[Element]
    hazards: list[Element]
    losses: list[Element]
    constraints: list[Element]
    controllers: list[Element]
    controller_constraints: list[Element]
    leaves: list[Leaf]
    constraints_by_hazard: dict[str, list[Element]] = field(default_factory=dict)
    assurance: list[dict] = field(default_factory=list)
    assurance_referenced: list[str] = field(default_factory=list)  # requirements the assurance case does reference (whole model)
    d3fend_applied: dict[str, int] = field(default_factory=dict)
    min_confidence: str = "medium"

    @property
    def name(self) -> str:
        return _name(self.element)

    @property
    def sid(self) -> str:
        return _id(self.element)

    @property
    def slug(self) -> str:
        base = self.sid or self.name[:40]
        return re.sub(r"[^A-Za-z0-9]+", "-", base).strip("-") or "scenario"

    def ranked(self) -> list[Leaf]:
        mc = self.min_confidence
        return sorted(
            self.leaves,
            key=lambda lf: (
                -lf.gap_score(mc),
                -(lf.p_mid * ((not lf.covered_requirements(mc)) + (not lf.covered_countermeasures(mc)))),
                -lf.p_mid,
                lf.name,
            ),
        )

    def coverage(self) -> dict[str, int]:
        mc = self.min_confidence
        c = Counter(lf.status(mc) for lf in self.leaves)
        return {
            "leaves": len(self.leaves),
            "in_tree": sum(1 for lf in self.leaves if lf.in_tree),
            "requirement": sum(1 for lf in self.leaves if lf.covered_requirements(mc)),
            "requirement_model_link": sum(1 for lf in self.leaves if any(r.kind in ("direct", "function") for r in lf.requirements)),
            "countermeasure": sum(1 for lf in self.leaves if lf.covered_countermeasures(mc)),
            "both": c["both"],
            "requirement_only": c["requirement-only"],
            "countermeasure_only": c["countermeasure-only"],
            "neither": c["GAP"],
        }


# --------------------------------------------------------------------------- scenarios
def risk_scenarios(m: Model) -> list[Element]:
    """Real risk scenarios (have an Id or something rolls up to them), not the profile's metamodel class."""
    out = [
        e
        for e in m.with_stereotype(ST_RISK_SCENARIO)
        if (_id(e) or _linked(m, e, "Roll_Up_To", "<-")) and not any(a.kind == "Profile" for a in m.owner_chain(e.id))
    ]
    return sorted(out, key=_sort_key)


def find_scenario(m: Model, needle: str | None) -> Element:
    scen = risk_scenarios(m)
    if not scen:
        raise SystemExit(f"no <<{ST_RISK_SCENARIO}>> elements in {m.name}")
    n = (needle or DEFAULT_SCENARIO).lower()
    for s in scen:
        if _id(s).lower() == n:
            return s
    hits = [s for s in scen if n in _name(s).lower() or n in _id(s).lower()]
    if hits:
        return hits[0]
    if needle is None:
        return scen[0]
    raise SystemExit(f"no risk scenario matching {needle!r}; try --list")


# --------------------------------------------------------------------------- attack tree
def _gate_children(m: Model, node: Element) -> list[tuple[str, Element]]:
    out = []
    for rel in m.incoming(node.id, "supplier"):
        gate = next((g for g in GATES if rel.has_stereotype(g)), None)
        if gate is None:
            continue
        for cid in rel.refs.get("client", []):
            c = m.get(cid)
            if c is not None:
                out.append((gate, c))
    return out


def _build_tree(m: Model, root: Element, gate: str = "", seen: set[str] | None = None) -> TreeNode:
    seen = seen if seen is not None else set()
    node = TreeNode(root, gate)
    seen.add(root.id)
    for g, c in _gate_children(m, root):
        if c.id in seen:
            node.children.append(TreeNode(c, g + " (shared)"))
            continue
        node.children.append(_build_tree(m, c, g, seen))
    return node


def attack_tree_roots(m: Model, scenario: Element) -> tuple[Element | None, list[TreeNode], dict[str, str]]:
    """The <<Risk>> element that depends on the scenario, its P(attack success) subtree(s) and the EML tags of its siblings."""
    risk = next((r for r in _linked(m, scenario, None, "<-", ST_RISK)), None)
    eml: dict[str, str] = {}
    roots: list[TreeNode] = []
    if risk is None:
        return None, roots, eml
    for gate, c in _gate_children(m, risk):
        if c.has_stereotype(ST_PAS):
            roots.append(_build_tree(m, c, gate))
        elif c.has_stereotype(*EML_STEREOTYPES):
            for s in c.stereotypes:
                for k, v in s.tags.items():
                    if k not in ("MCIterations", "SensitivityPercentOffset"):
                        eml[k] = v
    return risk, roots, eml


def _tree_leaves(node: TreeNode, path: list[str] | None = None) -> list[tuple[Element, list[str]]]:
    path = path or []
    if node.is_leaf and node.gate:
        return [(node.element, path)]
    out = []
    for c in node.children:
        out.extend(_tree_leaves(c, path + [f"{c.gate or '·'} {_name(c.element)}"] if not c.is_leaf else path))
    return out


# --------------------------------------------------------------------------- STPA-Sec chain
def _chain_for_loss_scenario(m: Model, ls: Element) -> dict[str, list[Element]]:
    hcas = _linked(m, ls, "Leads_to", "->", *ST_HCA)
    hazards: list[Element] = []
    losses: list[Element] = []
    constraints: list[Element] = []
    controllers: list[Element] = []
    ccs: list[Element] = []
    seen: set[str] = set()

    def add(lst: list[Element], els: list[Element]) -> None:
        for e in els:
            if e.id not in seen:
                seen.add(e.id)
                lst.append(e)

    for hca in hcas:
        hz = _linked(m, hca, "Causes", "->", ST_HAZARD)
        add(hazards, hz)
        for h in hz:
            add(losses, _linked(m, h, "Causes", "->", ST_LOSS))
            add(constraints, _linked(m, h, "Mitigates", "<-", ST_CONSTRAINT))
        add(ccs, _linked(m, hca, "Prevents", "<-", ST_CONTROLLER_CONSTRAINT))
        for ca in _linked(m, hca, None, "<-", ST_CONTROL_ACTION):
            for resp in _linked(m, ca, "Enforces", "->", ST_RESPONSIBILITY):
                add(controllers, _linked(m, resp, "AssignedTo", "->", ST_CONTROLLER))
        add(controllers, _linked(m, hca, "AssignedTo", "->", ST_CONTROLLER))
    return {
        "hcas": hcas,
        "hazards": hazards,
        "losses": losses,
        "constraints": constraints,
        "controllers": controllers,
        "controller_constraints": ccs,
    }


def walk(m: Model, scenario: Element) -> Scenario:
    """Traverse the STPA-Sec chain and attack tree(s) of one risk scenario. Model relationships only."""
    risk, roots, eml = attack_tree_roots(m, scenario)
    loss_scenarios = sorted(_linked(m, scenario, "Roll_Up_To", "<-", ST_LOSS_SCENARIO), key=_sort_key)
    ls_chain = {ls.id: _chain_for_loss_scenario(m, ls) for ls in loss_scenarios}

    leaves: dict[str, Leaf] = {}
    for root in roots:
        for el, path in _tree_leaves(root):
            leaves.setdefault(el.id, Leaf(el, path, True))
    for ls in loss_scenarios:
        for el in _linked(m, ls, None, "->", ST_LEAF):
            leaves.setdefault(el.id, Leaf(el, [f"(linked from {_id(ls) or 'loss scenario'}, outside the tree)"], False))

    def merge(dst: list[Element], src: list[Element]) -> None:
        have = {e.id for e in dst}
        for e in src:
            if e.id not in have:
                have.add(e.id)
                dst.append(e)

    agg: dict[str, list[Element]] = defaultdict(list)
    for lf in leaves.values():
        lss = _linked(m, lf.element, None, "<-", ST_LOSS_SCENARIO)
        lf.loss_scenarios = sorted(lss, key=_sort_key)
        for ls in lss:
            ch = ls_chain.get(ls.id) or _chain_for_loss_scenario(m, ls)
            merge(lf.hcas, ch["hcas"])
            merge(lf.hazards, ch["hazards"])
            merge(lf.losses, ch["losses"])
            merge(lf.controllers, ch["controllers"])
            merge(lf.constraints, ch["constraints"])
    for ch in ls_chain.values():
        for k, v in ch.items():
            merge(agg[k], v)

    ordered = sorted(leaves.values(), key=lambda lf: (not lf.in_tree, -lf.p_mid, lf.name))
    by_hazard = {h.id: _linked(m, h, "Mitigates", "<-", ST_CONSTRAINT) for h in agg["hazards"]}
    return Scenario(
        element=scenario,
        risk=risk,
        roots=roots,
        eml=eml,
        loss_scenarios=loss_scenarios,
        hcas=sorted(agg["hcas"], key=_sort_key),
        hazards=sorted(agg["hazards"], key=_sort_key),
        losses=sorted(agg["losses"], key=_sort_key),
        constraints=sorted(agg["constraints"], key=_sort_key),
        controllers=sorted(agg["controllers"], key=_sort_key),
        controller_constraints=sorted(agg["controller_constraints"], key=_sort_key),
        leaves=ordered,
        constraints_by_hazard=by_hazard,
    )


# --------------------------------------------------------------------------- requirement coverage
def _requirement_index(m: Model) -> dict[str, Element]:
    return {r.id: r for r in m.requirements()}


def _activities_of_action(m: Model, action: Element) -> list[Element]:
    out = []
    for bid in action.refs.get("behavior", []):
        b = m.get(bid)
        if b is not None:
            out.append(b)
    for anc in m.owner_chain(action.id):
        if anc.kind == "Activity":
            out.append(anc)
            break
    return out


def requirement_links(m: Model, lf: Leaf, reqs: dict[str, Element], cyber_only: bool = True) -> tuple[list[ReqLink], int]:
    """Requirements the model ties to this leaf: directly, or through the loss scenario's traced functions and their allocation."""
    found: dict[str, ReqLink] = {}
    other = 0

    def add(req: Element, kind: str, conf: str, why: str) -> None:
        nonlocal other
        if cyber_only and not _is_cyber_requirement(m, req):
            other += 1
            return
        key = _name(req).lower()
        rid = _id(req)
        if key in found:
            if rid and rid not in found[key].ids:
                found[key].ids.append(rid)
            if CONF[conf] > CONF[found[key].confidence]:
                found[key].confidence, found[key].kind, found[key].rationale = conf, kind, why
            return
        found[key] = ReqLink(req, kind, conf, why, [rid] if rid else [])

    anchors: list[tuple[str, Element]] = [("leaf", lf.element)]
    anchors += [("loss scenario", ls) for ls in lf.loss_scenarios]
    anchors += [("HCA", h) for h in lf.hcas]
    anchors += [("controller", c) for c in lf.controllers]
    for role, a in anchors:
        for lab, d, o in _rels(m, a):
            if o.id in reqs and lab in REQ_LINKS:
                add(o, "direct", "high", f"{lab} {d} {role} {_label(a, 60)} (model relationship)")

    for ls in lf.loss_scenarios:
        for lab, _d, act in _rels(m, ls):
            if lab != "Trace" or not act.kind.endswith("Action"):
                continue
            for activity in _activities_of_action(m, act):
                fn = _name(activity) or _name(act) or "<unnamed>"
                for l2, d2, o in _rels(m, activity):
                    if o.id in reqs and l2 in REQ_LINKS:
                        add(o, "function", "medium", f"{_id(ls)} traces to function '{fn}'; requirement {l2} {d2} that function")
                    elif l2 == "Allocate" and d2 == "->" and o.has_stereotype("Block"):
                        for l3, _d3, r in _rels(m, o):
                            if r.id in reqs and l3 in REQ_LINKS:
                                add(
                                    r,
                                    "allocation",
                                    "low",
                                    f"{_id(ls)} traces to function '{fn}' allocated to block '{_name(o)}'; "
                                    f"requirement {l3} → that block (same subsystem only)",
                                )
    return sorted(found.values(), key=lambda r: (-CONF[r.confidence], r.label)), other


def lexical_requirement_links(m: Model, lf: Leaf, reqs: dict[str, Element], existing: list[ReqLink]) -> list[ReqLink]:
    """Proposed (low-confidence) requirement matches by token overlap between leaf/loss-scenario text and requirement name+text."""
    text = " ".join([lf.name] + [_name(ls) for ls in lf.loss_scenarios])
    lt = _tokens(text)
    have = {_name(r.requirement).lower() for r in existing}
    for rl in existing:
        if rl.kind != "allocation":
            continue
        name_common = lt & _tokens(_name(rl.requirement))
        common = name_common | (lt & _tokens(strip_html(rl.requirement.tag("Text") or "")))
        if name_common and len(common) >= 2:
            rl.kind, rl.confidence = "allocation+text", "medium"
            rl.rationale += f"; proposed: the requirement text shares {sorted(common)} with the leaf (heuristic, not a model link)"
    out: dict[str, ReqLink] = {}
    for r in reqs.values():
        if not _is_cyber_requirement(m, r) or _name(r).lower() in have:
            continue
        rt = _tokens(_name(r) + " " + strip_html(r.tag("Text") or ""))
        common = lt & rt
        if len(common) < 2:
            continue
        key = _name(r).lower()
        if key in out:
            rid = _id(r)
            if rid and rid not in out[key].ids:
                out[key].ids.append(rid)
            continue
        out[key] = ReqLink(
            r, "lexical", "low", f"proposed: shared terms {sorted(common)} (text overlap, not a model relationship)", [_id(r)]
        )
    return sorted(out.values(), key=lambda r: (-len(r.rationale), r.label))[:5]


# --------------------------------------------------------------------------- D3FEND / ATT&CK
@dataclass
class D3fendIndex:
    offensive: list[Element]
    defensive: list[Element]
    by_tid: dict[str, Element]
    by_name: dict[str, Element]
    idf: dict[str, float]
    name_tokens: dict[str, set[str]]
    doc_tokens: dict[str, set[str]]
    neighbours: dict[str, list[tuple[str, Element]]]  # element id -> (association name, other end)
    parents: dict[str, list[str]]  # defensive technique name -> parent technique names

    @property
    def available(self) -> bool:
        return bool(self.offensive)

    def tactic_of(self, dt: Element) -> str:
        for name, other in self.neighbours.get(dt.id, []):
            if name == "enables" and other.has_stereotype(D3_TACTIC):
                return _name(other)
        for p in self.parents.get(_name(dt), []):
            pe = self.by_name.get(p.lower())
            if pe is not None:
                t = self.tactic_of(pe)
                if t:
                    return t
        return ""


def _tid_of(e: Element) -> str:
    mt = TID_RE.search(_name(e))
    return e.tag("d3fClass") or (mt.group(0) if mt else "")


def _plain_name(e: Element) -> str:
    return _name(e).split(":")[0].strip()


def build_d3fend_index(m: Model) -> D3fendIndex:
    offensive = m.with_stereotype(D3_OFFENSIVE)
    defensive = m.with_stereotype(D3_DEFENSIVE)
    by_tid = {_tid_of(o): o for o in offensive if _tid_of(o)}
    by_name = {_plain_name(d).lower(): d for d in defensive}
    name_tokens = {o.id: _tokens(_plain_name(o)) for o in offensive}
    doc_tokens = {o.id: _tokens(strip_html(o.doc)[:1500]) for o in offensive}
    df: Counter[str] = Counter(t for toks in name_tokens.values() for t in toks)
    n = max(len(offensive), 1)
    idf = {t: math.log((n + 1) / (c + 1)) + 1 for t, c in df.items()}
    neighbours: dict[str, list[tuple[str, Element]]] = defaultdict(list)
    for assoc in m.with_stereotype(D3_ASSOCIATION):
        ends = []
        for pid in assoc.refs.get("memberEnd", []):
            p = m.get(pid)
            t = m.type_of(p) if p is not None else None
            if t is not None:
                ends.append(t)
        if len(ends) == 2:
            neighbours[ends[0].id].append((assoc.name, ends[1]))
            neighbours[ends[1].id].append((assoc.name, ends[0]))
    parents = {_plain_name(d): m.generals(d) for d in defensive}
    return D3fendIndex(offensive, defensive, by_tid, by_name, idf, name_tokens, doc_tokens, neighbours, parents)


def match_attack(idx: D3fendIndex, text: str, limit: int = 3) -> list[AttackMatch]:
    """Lexical ATT&CK match: explicit Txxxx ids > full-name phrase > weighted name-token overlap (+doc support) > curated hints."""
    low = text.lower()
    lt = _tokens(text)
    out: dict[str, AttackMatch] = {}

    def put(t: Element, conf: str, score: float, why: str) -> None:
        tid = _tid_of(t)
        cur = out.get(t.id)
        if cur is None or (CONF[conf], score) > (CONF[cur.confidence], cur.score):
            out[t.id] = AttackMatch(t, tid, conf, round(score, 2), why)

    for tid in TID_RE.findall(text):
        if tid in idx.by_tid:
            put(idx.by_tid[tid], "high", 1.0, f"explicit ATT&CK id {tid} in the text")
    for t in idx.offensive:
        nt = idx.name_tokens[t.id]
        if not nt:
            continue
        plain = _plain_name(t).lower()
        if len(nt) >= 2 and plain in low:
            put(t, "high", 1.0, f"technique name '{_plain_name(t)}' appears verbatim in the text")
            continue
        common = nt & lt
        if not common:
            continue
        score = sum(idx.idf[x] for x in common) / sum(idx.idf[x] for x in nt)
        doc_hits = sorted((lt & idx.doc_tokens[t.id]) - common, key=lambda x: -idx.idf.get(x, 1.0))[:4]
        score += min(0.15, 0.05 * len(doc_hits))
        if score < 0.5:
            continue
        why = f"name tokens {sorted(common)} overlap"
        if doc_hits:
            why += f"; documentation also mentions {doc_hits}"
        conf = "medium" if score >= 0.75 and len(nt) >= 2 else "low"
        if len(nt) < 2:
            why += " (single-word technique name: capped at low)"
        put(t, conf, score, why)
    for phrase, tids in ATTACK_HINTS.items():
        if phrase in low:
            for tid in tids:
                if tid in idx.by_tid:
                    put(idx.by_tid[tid], "medium", 0.6, f"curated hint in cyber.py: phrase '{phrase.strip()}' → {tid} (heuristic)")
    ranked = sorted(out.values(), key=lambda a: (-CONF[a.confidence], -a.score, a.tid))
    return ranked[:limit]


def countermeasures_for(idx: D3fendIndex, matches: list[AttackMatch], limit: int = 6) -> list[Countermeasure]:
    """Follow D3FEND associations: offensive technique -May X-> defensive technique, and offensive -> artifact <- defensive."""
    found: dict[str, Countermeasure] = {}

    def put(dt: Element, tactic: str, via: str, conf: str, why: str, tid: str) -> None:
        cur = found.get(dt.id)
        if cur is None:
            found[dt.id] = Countermeasure(dt, tactic or idx.tactic_of(dt), via, conf, why, [tid])
        else:
            if tid not in cur.from_tids:
                cur.from_tids.append(tid)
            if (CONF[conf], via == "direct") > (CONF[cur.confidence], cur.via == "direct"):
                cur.confidence, cur.via, cur.rationale = conf, via, why

    lower = {"high": "medium", "medium": "low", "low": "low"}
    for am in matches:
        techs = [(am.technique, "")]
        parent = idx.by_tid.get(am.tid.split(".")[0]) if "." in am.tid else None
        if parent is not None:
            techs.append((parent, f" (via parent technique {_tid_of(parent)})"))
        for tech, note in techs:
            for name, other in idx.neighbours.get(tech.id, []):
                if name.startswith("May ") and other.has_stereotype(D3_DEFENSIVE):
                    put(other, name[4:], "direct", am.confidence, f"D3FEND: '{_plain_name(other)}' {name} {am.tid}{note}", am.tid)
                elif other.has_stereotype(D3_ARTIFACT):
                    for n2, dt in idx.neighbours.get(other.id, []):
                        if dt.has_stereotype(D3_DEFENSIVE) and not n2.startswith("May "):
                            put(
                                dt,
                                "",
                                "artifact",
                                lower[am.confidence],
                                f"D3FEND: {am.tid} {name} artifact '{_plain_name(other)}', which '{_plain_name(dt)}' {n2}{note}",
                                am.tid,
                            )
    ranked = sorted(found.values(), key=lambda c: (-CONF[c.confidence], c.via != "direct", -len(c.from_tids), c.label))
    return ranked[:limit]


def anchored_artifacts(m: Model, lf: Leaf) -> list[tuple[Element, Element]]:
    """D3FEND digital artifacts the Berserker architecture already traces to, reached from this leaf's loss scenarios
    (loss scenario -Trace- action -> activity -Allocate-> functional block <-Realization- allocated block -Trace-> artifact)."""
    out: dict[tuple[str, str], tuple[Element, Element]] = {}
    for ls in lf.loss_scenarios:
        for lab, _d, act in _rels(m, ls):
            if lab != "Trace" or not act.kind.endswith("Action"):
                continue
            for activity in _activities_of_action(m, act):
                for l2, d2, blk in _rels(m, activity):
                    if l2 != "Allocate" or d2 != "->":
                        continue
                    for l3, d3, ab in _rels(m, blk):
                        if l3 not in ("Realization", "Trace") or d3 != "<-":
                            continue
                        for l4, d4, art in _rels(m, ab):
                            if l4 == "Trace" and d4 == "->" and art.has_stereotype(D3_ARTIFACT):
                                out[(ab.id, art.id)] = (ab, art)
    return sorted(out.values(), key=lambda p: (_name(p[0]), _name(p[1])))


def d3fend_applied_outside(m: Model) -> dict[str, int]:
    """How many D3FEND stereotypes are applied to elements outside the D3FEND project itself (expected: 0)."""
    d3_projects = {e.project for e in m.with_stereotype(D3_DEFENSIVE, D3_OFFENSIVE)}
    c: Counter[str] = Counter()
    for st in D3_STEREOTYPES:
        for e in m.with_stereotype(st):
            if e.project not in d3_projects:
                c[st] += 1
    return dict(c)


# --------------------------------------------------------------------------- assurance case
def assurance_support(m: Model, req: Element) -> list[tuple[str, Element, str]]:
    """(how, assurance element, confidence) for Goal/Evidence that reference the requirement: relationship, ownership, or one Trace hop."""
    out: list[tuple[str, Element, str]] = []
    for lab, d, o in _rels(m, req):
        if o.has_stereotype(*ASSURANCE_STEREOTYPES):
            out.append((f"{lab} {d}", o, "high"))
    for anc in m.owner_chain(req.id):
        if anc.has_stereotype(*ASSURANCE_STEREOTYPES):
            out.append(("owned by", anc, "high"))
    for lab, d, o in _rels(m, req):
        if lab in TRACE_STEREOTYPES and o.has_stereotype("Requirement"):
            for l2, d2, g in _rels(m, o):
                if g.has_stereotype(*ASSURANCE_STEREOTYPES):
                    out.append((f"{lab} {d} {_label(o, 40)} {l2} {d2}", g, "medium"))
    return out


def assurance_referenced_requirements(m: Model) -> list[str]:
    """Labels of every requirement any assurance-case Goal/Strategy/Evidence relates to or owns, model-wide."""
    out: dict[str, str] = {}
    for g in m.with_stereotype(*ASSURANCE_STEREOTYPES):
        for lab, _d, o in _rels(m, g):
            if o.has_stereotype("Requirement"):
                out[o.id] = f"{_label(g, 40)} {lab} {_label(o, 60)}"
        for cid in g.children:
            c = m.get(cid)
            if c is not None and c.has_stereotype("Requirement"):
                out[c.id] = f"{_label(g, 40)} owns {_label(c, 60)}"
    return sorted(out.values())


# --------------------------------------------------------------------------- NIST 800-53 candidates
def load_nist_table() -> dict:
    with resources.files("sysml_demo").joinpath("data/nist80053_d3fend.json").open(encoding="utf-8") as fh:
        return json.load(fh)


def nist_candidates(cms: list[Countermeasure], idx: D3fendIndex | None, table: dict | None = None) -> list[NistCandidate]:
    """Candidate controls for D3FEND countermeasures: exact technique entry, else a parent/family entry, else the tactic default."""
    table = table or load_nist_table()
    entries = {e["d3fend"].lower(): e for e in table["entries"]}
    out: dict[tuple[str, str], NistCandidate] = {}
    for cm in cms:
        name = cm.label.split(":")[0].strip()
        chain = [(name, "technique", "medium")]
        queue = list(idx.parents.get(name, []) if idx else [])
        seen = set()
        while queue:
            p = queue.pop(0)
            if p in seen:
                continue
            seen.add(p)
            chain.append((p, "family", "low"))
            if idx:
                queue.extend(idx.parents.get(p, []))
        if cm.tactic:
            chain.append((cm.tactic, "tactic", "low"))
        for key, level, conf in chain:
            e = entries.get(key.lower())
            if e is None:
                continue
            conf = "low" if CONF[cm.confidence] < CONF["medium"] else conf
            for ctrl in e["nist"]:
                k = (ctrl, name)
                if k not in out:
                    out[k] = NistCandidate(
                        ctrl,
                        name,
                        e["d3fend"],
                        level,
                        e.get("tactic", cm.tactic),
                        conf,
                        cm.confidence,
                        e["rationale"],
                    )
            break
    return sorted(out.values(), key=lambda n: (-CONF[n.confidence], n.control, n.d3fend))


# --------------------------------------------------------------------------- analysis driver
def analyse(m: Model, scenario: Element, min_confidence: str = "medium", idx: D3fendIndex | None = None) -> Scenario:
    sc = walk(m, scenario)
    sc.min_confidence = min_confidence
    reqs = _requirement_index(m)
    idx = idx or build_d3fend_index(m)
    table = load_nist_table()
    for lf in sc.leaves:
        links, other = requirement_links(m, lf, reqs)
        lf.requirements = links + lexical_requirement_links(m, lf, reqs, links)
        lf.other_requirements = other
        if idx.available:
            text = " ".join([lf.name, strip_html(lf.element.doc)] + [_name(ls) + " " + strip_html(ls.doc) for ls in lf.loss_scenarios])
            lf.attack = match_attack(idx, text)
            lf.countermeasures = countermeasures_for(idx, lf.attack)
            lf.anchored_artifacts = anchored_artifacts(m, lf)
            lf.nist = nist_candidates(lf.covered_countermeasures(min_confidence), idx, table)
    seen: set[str] = set()
    for lf in sc.leaves:
        for rl in lf.requirements:
            if rl.kind == "lexical" or rl.requirement.id in seen:
                continue
            seen.add(rl.requirement.id)
            sup = assurance_support(m, rl.requirement)
            sc.assurance.append(
                {
                    "requirement": rl.label,
                    "supported": bool(sup),
                    "support": [f"{how} {_label(g, 70)} [{conf}]" for how, g, conf in sup],
                }
            )
    sc.assurance_referenced = assurance_referenced_requirements(m)
    sc.d3fend_applied = d3fend_applied_outside(m)
    return sc


# --------------------------------------------------------------------------- rendering: ASCII
def _ids(els: list[Element], n: int = 6) -> str:
    s = ", ".join(_id(e) or _name(e)[:25] for e in els[:n])
    return s + (f" (+{len(els) - n})" if len(els) > n else "")


def render_ascii(sc: Scenario) -> list[str]:
    mc = sc.min_confidence
    cov = sc.coverage()
    L: list[str] = []
    L.append(f"{sc.sid or 'Risk scenario'}  {sc.name}")
    L.append(
        f"│  loss scenarios {len(sc.loss_scenarios)} → HCAs {len(sc.hcas)} → hazards {len(sc.hazards)} → losses {len(sc.losses)}"
        f"   controllers {len(sc.controllers)}   security constraints {len(sc.constraints)}"
    )
    for lo in sc.losses:
        L.append(f"│  Loss   {_label(lo, 100)}")
    for h in sc.hazards:
        L.append(f"│  Hazard {_label(h, 90)}   mitigated by {_ids(sc.constraints_by_hazard.get(h.id, []), 3) or '-'}")
    L.append(f"│  Controllers: {', '.join(_label(c, 30) for c in sc.controllers[:10])}{' …' if len(sc.controllers) > 10 else ''}")
    if sc.eml:
        L.append("│  EML: " + ", ".join(f"{k}={v}" for k, v in sorted(sc.eml.items())))
    L.append("│")
    if not sc.roots:
        L.append("│  (no <<Risk>> attack tree attached to this scenario)")
    for root in sc.roots:
        L.append(f"├─ [{root.gate or 'root'}] {_name(root.element)}  <<{ST_PAS}>>")
        _render_tree(sc, root, "│  ", L)
    extra = [lf for lf in sc.leaves if not lf.in_tree]
    if extra:
        L.append("├─ leaves reached from this scenario's loss scenarios but sitting in other trees:")
        for lf in extra:
            L.append(f"│  ● {_leaf_line(sc, lf)}")
    L.append("│")
    L.append(
        f"└─ coverage @≥{mc}: {cov['leaves']} leaves ({cov['in_tree']} in this tree) — requirement {cov['requirement']} "
        f"(of which {cov['requirement_model_link']} by a direct model relationship), D3FEND countermeasure {cov['countermeasure']}, "
        f"both {cov['both']}, neither {cov['neither']}"
    )
    L.append("")
    L.append("Leaf detail (ranked by P(success) × no-requirement × no-countermeasure):")
    for i, lf in enumerate(sc.ranked(), 1):
        L.append(f"{i:>2}. {lf.status(mc):<19} {lf.p_text:<16} {lf.name}")
        L.append(
            f"      via {' → '.join(_id(x) or _name(x)[:30] for x in lf.loss_scenarios)} → HCA {_ids(lf.hcas, 3) or '-'} → "
            f"H {_ids(lf.hazards, 4) or '-'} → L {_ids(lf.losses, 4) or '-'}; controllers {_ids(lf.controllers, 4) or '-'}"
        )
        reqs = lf.covered_requirements(mc)
        if reqs:
            for r in reqs[:4]:
                L.append(f"      req  [{r.confidence}] {r.label[:70]}  — {r.rationale[:90]}")
            if len(reqs) > 4:
                L.append(f"      req  … +{len(reqs) - 4} more")
        else:
            prop = [r for r in lf.requirements if r.kind == "lexical"]
            alloc = [r for r in lf.requirements if r.kind == "allocation"]
            L.append(f"      req  GAP — no cyber requirement reaches this leaf, its loss scenario or its function at ≥{mc}")
            if alloc:
                L.append(f"      req    {len(alloc)} reach only the same subsystem via block Allocate (low, e.g. {alloc[0].label[:50]})")
            if prop:
                L.append(f"      req    {len(prop)} lexical proposal(s) (low, e.g. {prop[0].label[:50]})")
        for a in lf.attack[:3]:
            L.append(f"      att  [{a.confidence}] {a.label[:60]}  — {a.rationale[:80]}")
        cms = lf.covered_countermeasures(mc)
        if cms:
            for c in cms[:4]:
                L.append(f"      d3f  [{c.confidence}] {c.tactic or '?'}: {c.label}  — {c.rationale[:80]}")
        else:
            L.append("      d3f  GAP — no D3FEND countermeasure reachable at this confidence")
        if lf.nist:
            ctrls = sorted({n.control for n in lf.nist})
            L.append(f"      nist candidates: {', '.join(ctrls[:10])}{' …' if len(ctrls) > 10 else ''}")
    return L


def _artifacts_by_block(lf: Leaf) -> list[dict]:
    by_block: dict[str, list[str]] = defaultdict(list)
    for b, a in lf.anchored_artifacts:
        by_block[_name(b)].append(_name(a))
    return [{"block": b, "artifacts": len(arts), "examples": sorted(arts)[:6]} for b, arts in sorted(by_block.items())]


def _leaf_line(sc: Scenario, lf: Leaf) -> str:
    mc = sc.min_confidence
    r = lf.covered_requirements(mc)
    c = lf.covered_countermeasures(mc)
    flags = ("R" if r else "·") + ("D" if c else "·")
    sens = f" sens={lf.sensitivity:g}" if lf.sensitivity is not None else ""
    return f"{lf.name[:78]:<78} {lf.p_text}{sens} [{flags}]"


def _render_tree(sc: Scenario, node: TreeNode, ind: str, L: list[str]) -> None:
    by_id = {lf.element.id: lf for lf in sc.leaves}
    _render_children(sc, node, ind, L, by_id)


def _render_children(sc: Scenario, node: TreeNode, ind: str, L: list[str], by_id: dict[str, Leaf]) -> None:
    for i, c in enumerate(node.children):
        last = i == len(node.children) - 1
        branch = "└─ " if last else "├─ "
        if c.is_leaf:
            lf = by_id.get(c.element.id)
            L.append(f"{ind}{branch}[{c.gate}] ● {_leaf_line(sc, lf) if lf else _name(c.element)}")
        else:
            L.append(f"{ind}{branch}[{c.gate}] {_name(c.element)}")
            _render_children(sc, c, ind + ("   " if last else "│  "), L, by_id)


# --------------------------------------------------------------------------- rendering: Mermaid
def render_mermaid(sc: Scenario) -> str:
    mc = sc.min_confidence
    ids: dict[str, str] = {}

    def nid(e: Element) -> str:
        if e.id not in ids:
            ids[e.id] = f"n{len(ids)}"
        return ids[e.id]

    def lab(e: Element, n: int = 60) -> str:
        return _label(e, n).replace('"', "'")

    out = ["graph LR"]
    out.append(f'  {nid(sc.element)}["{lab(sc.element)}"]:::rs')
    for lo in sc.losses:
        out.append(f'  {nid(lo)}["{lab(lo)}"]:::loss')
    for h in sc.hazards:
        out.append(f'  {nid(h)}["{lab(h)}"]:::hz')
    for c in sc.constraints:
        out.append(f'  {nid(c)}["{lab(c)}"]:::sc')
    for ctl in sc.controllers[:12]:
        out.append(f'  {nid(ctl)}["{lab(ctl, 40)}"]:::ctl')
    for ls in sc.loss_scenarios:
        out.append(f'  {nid(ls)}["{lab(ls, 70)}"]:::ls')
        out.append(f"  {nid(ls)} -- Roll_Up_To --> {nid(sc.element)}")
    for lf in sc.leaves:
        st = lf.status(mc)
        cls = {"both": "ok", "GAP": "gap"}.get(st, "part")
        out.append(f'  {nid(lf.element)}["{lab(lf.element, 70)}<br/>{lf.p_text}"]:::{cls}')
        for ls in lf.loss_scenarios:
            if ls.id in ids:
                out.append(f"  {nid(ls)} -.-> {nid(lf.element)}")
        for r in lf.covered_requirements(mc)[:3]:
            if r.requirement.id not in ids:
                out.append(f'  {nid(r.requirement)}["{lab(r.requirement, 50)}"]:::req')
            out.append(f"  {nid(lf.element)} -. {r.kind} .-> {nid(r.requirement)}")
        for cm in lf.covered_countermeasures(mc)[:2]:
            if cm.technique.id not in ids:
                out.append(f'  {nid(cm.technique)}["D3FEND {lab(cm.technique, 40)}"]:::d3f')
            out.append(f"  {nid(lf.element)} -. proposed .-> {nid(cm.technique)}")
    for root in sc.roots:
        out.append(f'  {nid(root.element)}["{lab(root.element, 60)}"]:::pas')
        out.append(f"  {nid(sc.element)} --> {nid(root.element)}")
        _mermaid_tree(root, out, nid, lab)
    seen_edges: set[tuple[str, str]] = set()
    for lf in sc.leaves:
        for h in lf.hazards:
            for lo in lf.losses:
                if (h.id, lo.id) not in seen_edges and lo.id in ids and h.id in ids:
                    seen_edges.add((h.id, lo.id))
                    out.append(f"  {nid(h)} -- Causes --> {nid(lo)}")
        for c in lf.constraints:
            for h in lf.hazards:
                if (c.id, h.id) not in seen_edges and c.id in ids:
                    seen_edges.add((c.id, h.id))
                    out.append(f"  {nid(c)} -- Mitigates --> {nid(h)}")
        for ls in lf.loss_scenarios:
            for h in lf.hazards:
                if (ls.id, h.id) not in seen_edges and ls.id in ids:
                    seen_edges.add((ls.id, h.id))
                    out.append(f"  {nid(ls)} -- Leads_to/Causes --> {nid(h)}")
    out += [
        "  classDef rs fill:#333,color:#fff",
        "  classDef loss fill:#f88",
        "  classDef hz fill:#fc8",
        "  classDef sc fill:#cfc",
        "  classDef ctl fill:#eee",
        "  classDef ls fill:#ffd",
        "  classDef pas fill:#ddf",
        "  classDef ok fill:#9f9",
        "  classDef part fill:#ff9",
        "  classDef gap fill:#f66,color:#fff",
        "  classDef req fill:#cef",
        "  classDef d3f fill:#ecf,stroke-dasharray: 3 3",
    ]
    return "\n".join(out)


def _mermaid_tree(node: TreeNode, out: list[str], nid: Callable[[Element], str], lab: Callable[[Element, int], str]) -> None:
    for c in node.children:
        if not c.is_leaf:
            out.append(f'  {nid(c.element)}["{lab(c.element, 60)}"]:::pas')
            _mermaid_tree(c, out, nid, lab)
        out.append(f"  {nid(node.element)} -- {c.gate.split()[0]} --> {nid(c.element)}")


# --------------------------------------------------------------------------- rendering: Markdown / JSON / CSV / XMI
def _md(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def render_markdown(sc: Scenario, m: Model, command: str) -> str:
    mc = sc.min_confidence
    cov = sc.coverage()
    o: list[str] = []
    o.append(f"# Cyber resiliency gap analysis — {sc.sid} {sc.name}")
    o.append("")
    o.append(
        f"Model: `{m.name}` ({len(m.elements)} elements from {len(m.projects)} project(s)"
        + (f"; missing: {', '.join(m.missing_projects)}" if m.missing_projects else "")
        + ")  "
    )
    o.append(f"Command: `{command}`  ")
    o.append(f"Coverage threshold: proposals below **{mc}** confidence are listed but not counted as coverage.")
    o.append("")
    o.append(
        "> Everything in the *STPA-Sec chain* and *requirement (direct / allocation)* columns is read from model relationships. "
        "ATT&CK, D3FEND, lexical-requirement and NIST lines are **heuristic proposals** with a confidence and a rationale; "
        "none of them exists in the model."
    )
    o.append("")
    o.append("## Summary")
    o.append("")
    o.append("| leaves | with cyber requirement | with D3FEND countermeasure | both | neither |")
    o.append("|---|---|---|---|---|")
    o.append(f"| {cov['leaves']} | {cov['requirement']} | {cov['countermeasure']} | {cov['both']} | {cov['neither']} |")
    o.append("")
    d3 = sum(sc.d3fend_applied.values())
    o.append(
        f"D3FEND stereotypes applied to non-D3FEND (Berserker) elements: **{d3}**"
        + (f" ({', '.join(f'{k} {v}' for k, v in sc.d3fend_applied.items())})" if d3 else " — the D3FEND profile is mounted but unused.")
    )
    o.append("")
    o.append("## STPA-Sec chain")
    o.append("")
    o.append(f"- Risk scenario: **{sc.sid} {sc.name}** ({len(sc.loss_scenarios)} loss scenarios roll up to it)")
    if sc.risk is not None:
        o.append(
            f"- Attack tree: **{_name(sc.risk)}** ← And ← {', '.join(_name(r.element) for r in sc.roots)}"
            + (f"; EML: {', '.join(f'{k}={v}' for k, v in sorted(sc.eml.items()))}" if sc.eml else "")
        )
    o.append("- Losses: " + "; ".join(_label(x) for x in sc.losses))
    o.append("- Hazards: " + "; ".join(_label(x) for x in sc.hazards))
    o.append("- Security constraints: " + "; ".join(_label(x) for x in sc.constraints))
    o.append(f"- Controllers ({len(sc.controllers)}): " + ", ".join(_label(x) for x in sc.controllers))
    o.append(f"- Hazardous control actions: {len(sc.hcas)}; controller constraints: {len(sc.controller_constraints)}")
    o.append("")
    o.append("```text")
    ascii_lines = render_ascii(sc)
    o.extend(ascii_lines[: _ascii_tree_end(ascii_lines)])
    o.append("```")
    o.append("")
    o.append("## Leaf gap table (ranked by P(success) × no-requirement × no-countermeasure)")
    o.append("")
    o.append(
        "| # | status | leaf | P(success) 90% CI | sensitivity | loss scenario | cyber requirement(s) | "
        "ATT&CK (confidence) | D3FEND countermeasure (confidence) |"
    )
    o.append("|---|---|---|---|---|---|---|---|---|")
    for i, lf in enumerate(sc.ranked(), 1):
        reqs = lf.covered_requirements(mc)
        rq = "<br/>".join(f"{_md(r.label[:60])} [{r.confidence}]" for r in reqs[:4]) or "**GAP**"
        att = "<br/>".join(f"{_md(a.label)} [{a.confidence}]" for a in lf.attack) or "-"
        cms = lf.covered_countermeasures(mc)
        cm = "<br/>".join(f"{_md(c.label)} ({c.tactic}) [{c.confidence}]" for c in cms[:4]) or "**GAP**"
        o.append(
            f"| {i} | {lf.status(mc)} | {_md(lf.name)} | {lf.p_text[2:]} | {lf.sensitivity if lf.sensitivity is not None else '-'} | "
            f"{_md(', '.join(_id(x) or _name(x)[:30] for x in lf.loss_scenarios))} | {rq} | {att} | {cm} |"
        )
    o.append("")
    o.append("## Leaf details")
    o.append("")
    for i, lf in enumerate(sc.ranked(), 1):
        o.append(f"### {i}. {lf.name}")
        o.append("")
        o.append(f"- {lf.p_text}, TotalRiskSensitivity={lf.sensitivity}, gate path: {' → '.join(lf.gate_path) or '(root)'}")
        o.append("- Loss scenario(s): " + "; ".join(_label(x) for x in lf.loss_scenarios))
        o.append(f"- HCAs: {_ids(lf.hcas, 8) or '-'}; hazards: {_ids(lf.hazards) or '-'}; losses: {_ids(lf.losses) or '-'}")
        o.append("- Controllers: " + (", ".join(_label(x) for x in lf.controllers) or "-"))
        o.append(f"- Requirements ({lf.other_requirements} further non-cyber requirements share the same allocation paths):")
        for r in lf.requirements:
            o.append(f"  - [{r.confidence}] **{_md(r.label)}** — {r.kind}: {_md(r.rationale)}")
        if not lf.requirements:
            o.append("  - none")
        o.append("- ATT&CK techniques (heuristic):")
        for a in lf.attack:
            o.append(f"  - [{a.confidence} {a.score}] **{_md(a.label)}** — {_md(a.rationale)}")
        if not lf.attack:
            o.append("  - none matched")
        o.append("- D3FEND countermeasures (heuristic, via D3FEND associations):")
        for c in lf.countermeasures:
            o.append(f"  - [{c.confidence}] **{_md(c.label)}** ({c.tactic or '?'}, {c.via}) — {_md(c.rationale)}")
        if not lf.countermeasures:
            o.append("  - none reachable")
        if lf.anchored_artifacts:
            arts = Counter(_name(a) for _b, a in lf.anchored_artifacts)
            blks = sorted({_name(b) for b, _a in lf.anchored_artifacts})
            o.append(
                f"- D3FEND artifacts the Allocated Baseline already traces to on this path (model Trace links): "
                f"{', '.join(f'{a} ({n})' for a, n in arts.most_common(8))} from block(s) {', '.join(blks)}"
            )
        if lf.nist:
            o.append("- Candidate NIST SP 800-53r5 controls: " + ", ".join(sorted({n.control for n in lf.nist})))
        o.append("")
    o.append("## Assurance case")
    o.append("")
    if sc.assurance:
        unsupported = [a for a in sc.assurance if not a["supported"]]
        o.append(f"{len(sc.assurance)} requirement(s) in the chain; {len(unsupported)} with no assurance-case Goal/Evidence reference.")
        o.append("")
        o.append(
            f"For context, the assurance case references {len(sc.assurance_referenced)} requirement(s) model-wide"
            + (": " + "; ".join(_md(x) for x in sc.assurance_referenced[:12]) if sc.assurance_referenced else "")
            + (" …" if len(sc.assurance_referenced) > 12 else "")
            + "."
        )
        o.append("")
        o.append("| requirement | supported | by |")
        o.append("|---|---|---|")
        for row in sc.assurance:
            o.append(f"| {_md(row['requirement'])} | {'yes' if row['supported'] else '**no**'} | {_md('; '.join(row['support'])) or '-'} |")
    else:
        o.append("No requirements reached from this scenario, so nothing to check.")
    o.append("")
    o.append("## Method and assumptions")
    o.append("")
    o.append(
        "- Attack tree: `<<Risk>>` element that depends on the risk scenario → `And` children with `<<Probability_of_Attack_Success>>` "
        "→ `And`/`Or` dependencies down to `<<PAT_Leaf_Node>>`. P(success) is the leaf's `_90CI_Low`–`_90CI_High` tag pair; "
        "the ranking uses the CI midpoint."
    )
    o.append("- Leaves linked from the scenario's loss scenarios but living in another risk's tree are included and marked.")
    o.append(
        "- Requirement coverage counts only requirements whose package path contains 'cyber' or 'security'; "
        "other requirements on the same paths are counted separately."
    )
    o.append(
        "- `direct` = Trace/Satisfy/Refine/Allocate/Dependency between the requirement and the leaf, loss scenario, HCA or controller. "
        "`allocation` = loss scenario –Trace– action → activity –Allocate→ block ←Allocate/Satisfy– requirement (all model links, medium)."
    )
    o.append(
        "- ATT&CK matching is lexical (explicit Txxxx id > verbatim technique name > IDF-weighted name-token overlap "
        "with documentation support > "
        "curated phrase hints listed in `cyber.py`). D3FEND countermeasures follow the profile's "
        "`May Harden/Detect/Isolate/…` associations "
        "and offensive→artifact←defensive paths; sub-techniques fall back to their parent."
    )
    o.append("- NIST candidates come from `sysml_demo/data/nist80053_d3fend.json` (authored starting point, see its header).")
    return "\n".join(o) + "\n"


def _ascii_tree_end(lines: list[str]) -> int:
    for i, l in enumerate(lines):
        if l.startswith("Leaf detail"):
            return i - 1
    return len(lines)


def _grouped_links(links: list[ReqLink]) -> list[dict]:
    """Requirement links sharing one kind/confidence/rationale (e.g. the same allocation path) collapsed into one row."""
    groups: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    for r in links:
        groups[(r.kind, r.confidence, r.rationale)].append(r.label)
    return [
        {"kind": k, "confidence": c, "rationale": why, "requirements": sorted(labels)}
        for (k, c, why), labels in sorted(groups.items(), key=lambda kv: (-CONF[kv[0][1]], kv[0][0], kv[0][2]))
    ]


def gaps_json(sc: Scenario, m: Model, command: str) -> dict:
    """Machine-readable gap table. Requirement links below the threshold and the NIST table text are kept compact
    (the full per-link rationale is in cyber_<scenario>.md) so the file stays small enough to commit."""
    mc = sc.min_confidence
    nist_entries = {n.matched: f"[{n.level}] {n.entry_rationale}" for lf in sc.leaves for n in lf.nist}
    return {
        "scenario": {"id": sc.sid, "name": sc.name, "model": m.name, "projects": len(m.projects), "missing_projects": m.missing_projects},
        "command": command,
        "min_confidence": mc,
        "coverage": sc.coverage(),
        "d3fend_stereotypes_applied_outside_d3fend": sc.d3fend_applied,
        "chain": {
            "losses": [_label(x) for x in sc.losses],
            "hazards": [_label(x) for x in sc.hazards],
            "security_constraints": [_label(x) for x in sc.constraints],
            "controllers": [_label(x) for x in sc.controllers],
            "loss_scenarios": [_label(x) for x in sc.loss_scenarios],
            "hazardous_control_actions": len(sc.hcas),
        },
        "leaves": [
            {
                "rank": i,
                "leaf": lf.name,
                "in_scenario_tree": lf.in_tree,
                "gate_path": lf.gate_path,
                "p_low": lf.p_low,
                "p_high": lf.p_high,
                "p_mid": round(lf.p_mid, 6),
                "total_risk_sensitivity": lf.sensitivity,
                "status": lf.status(mc),
                "gap_score": round(lf.gap_score(mc), 6),
                "loss_scenarios": [_label(x) for x in lf.loss_scenarios],
                "hcas": [_id(x) or _name(x) for x in lf.hcas],
                "hazards": [_label(x) for x in lf.hazards],
                "losses": [_label(x) for x in lf.losses],
                "controllers": [_label(x) for x in lf.controllers],
                "requirements": [
                    {"requirement": r.label, "kind": r.kind, "confidence": r.confidence, "rationale": r.rationale}
                    for r in lf.covered_requirements(mc)
                ],
                "requirements_below_threshold": _grouped_links([r for r in lf.requirements if CONF[r.confidence] < CONF[mc]]),
                "other_requirements_on_path": lf.other_requirements,
                "attack_techniques": [
                    {"technique": a.label, "id": a.tid, "confidence": a.confidence, "score": a.score, "rationale": a.rationale}
                    for a in lf.attack
                ],
                "d3fend_countermeasures": [
                    {
                        "technique": c.label,
                        "tactic": c.tactic,
                        "via": c.via,
                        "from": c.from_tids,
                        "confidence": c.confidence,
                        "rationale": c.rationale,
                        "counted": CONF[c.confidence] >= CONF[mc],
                    }
                    for c in lf.countermeasures
                ],
                "anchored_d3fend_artifacts": _artifacts_by_block(lf),
                "nist_candidates": [
                    f"{n.control} [{n.confidence}] for D3FEND '{n.d3fend}' via {n.level} entry '{n.matched}' "
                    f"(countermeasure was {n.source_confidence})"
                    for n in lf.nist
                ],
            }
            for i, lf in enumerate(sc.ranked(), 1)
        ],
        "nist_table_entries": dict(sorted(nist_entries.items())),
        "assurance": sc.assurance,
        "assurance_referenced_requirements_model_wide": sc.assurance_referenced,
    }


def render_gaps_markdown(sc: Scenario, command: str) -> str:
    mc = sc.min_confidence
    cov = sc.coverage()
    o = [
        f"# Gap table — {sc.sid} {sc.name}",
        "",
        f"Command: `{command}`  ",
        f"Threshold: ≥{mc}. Heuristic columns are proposals, not model facts.",
        "",
    ]
    o.append(
        f"{cov['leaves']} leaves: {cov['requirement']} with a cyber requirement, {cov['countermeasure']} with a D3FEND countermeasure, "
        f"{cov['both']} both, **{cov['neither']} neither**. D3FEND stereotypes on Berserker elements: {sum(sc.d3fend_applied.values())}."
    )
    o.append("")
    o.append("| # | leaf | P(success) | mitigating requirement(s) | ATT&CK technique(s) | D3FEND countermeasure(s) | status |")
    o.append("|---|---|---|---|---|---|---|")
    for i, lf in enumerate(sc.ranked(), 1):
        rq = "; ".join(f"{_md(r.label[:50])} [{r.confidence}]" for r in lf.covered_requirements(mc)[:3]) or "**GAP**"
        at = "; ".join(f"{_md(a.tid or a.label)} [{a.confidence}]" for a in lf.attack) or "-"
        cm = "; ".join(f"{_md(c.label)} [{c.confidence}]" for c in lf.covered_countermeasures(mc)[:3]) or "**GAP**"
        o.append(f"| {i} | {_md(lf.name)} | {lf.p_text[2:]} | {rq} | {at} | {cm} | {lf.status(mc)} |")
    o.append("")
    return "\n".join(o) + "\n"


def render_nist_markdown(sc: Scenario, table: dict, command: str) -> str:
    rows = _nist_rows(sc)
    o = [
        f"# Candidate NIST SP 800-53r5 controls — {sc.sid} {sc.name}",
        "",
        f"Command: `{command}`  ",
        f"Source table: `sysml_demo/data/nist80053_d3fend.json` — {table['_meta']['status']}.",
        "",
        "These are **candidates** derived from heuristic D3FEND countermeasure proposals; every row carries the confidence "
        "of the weakest link.",
        "",
    ]
    o.append("| control | # leaves | D3FEND countermeasure(s) | matched entry (level) | confidence | leaves |")
    o.append("|---|---|---|---|---|---|")
    for r in rows:
        o.append(
            f"| {r['control']} | {r['leaf_count']} | {_md(', '.join(r['d3fend']))} | {_md(r['matched'])} ({r['level']}) | "
            f"{r['confidence']} | {_md('; '.join(r['leaves']))} |"
        )
    o.append("")
    return "\n".join(o) + "\n"


def _nist_rows(sc: Scenario) -> list[dict]:
    agg: dict[str, dict] = {}
    for lf in sc.leaves:
        for n in lf.nist:
            r = agg.setdefault(
                n.control,
                {
                    "control": n.control,
                    "d3fend": [],
                    "matched": n.matched,
                    "level": n.level,
                    "confidence": n.confidence,
                    "leaves": [],
                    "rationale": n.rationale,
                },
            )
            if n.d3fend not in r["d3fend"]:
                r["d3fend"].append(n.d3fend)
            if lf.name not in r["leaves"]:
                r["leaves"].append(lf.name)
            if CONF[n.confidence] > CONF[r["confidence"]]:
                r["confidence"], r["matched"], r["level"], r["rationale"] = n.confidence, n.matched, n.level, n.rationale
    rows = sorted(agg.values(), key=lambda r: (-len(r["leaves"]), -CONF[r["confidence"]], r["control"]))
    for r in rows:
        r["leaf_count"] = len(r["leaves"])
    return rows


def render_nist_csv(sc: Scenario) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(
        ["scenario", "control", "leaf_count", "d3fend_countermeasures", "matched_entry", "level", "confidence", "rationale", "leaves"]
    )
    for r in _nist_rows(sc):
        w.writerow(
            [
                sc.sid,
                r["control"],
                r["leaf_count"],
                "; ".join(r["d3fend"]),
                r["matched"],
                r["level"],
                r["confidence"],
                r["rationale"],
                "; ".join(r["leaves"]),
            ]
        )
    return buf.getvalue()


def render_nist_xmi(sc: Scenario) -> str:
    """Stub XMI an engineer could import into the empty NIST project: <<Requirement>> classes with Id + Text per candidate control."""
    rows = _nist_rows(sc)
    pkg_id = f"nist_cand_{sc.slug}"
    o = [
        "<?xml version='1.0' encoding='UTF-8'?>",
        "<xmi:XMI xmlns:uml='http://www.omg.org/spec/UML/20131001' xmlns:xmi='http://www.omg.org/spec/XMI/20131001'",
        "         xmlns:sysml='http://www.omg.org/spec/SysML/20181001/SysML'>",
        "  <xmi:Documentation><xmi:exporter>sysml_demo cyber</xmi:exporter>"
        "<xmi:exporterVersion>0.1</xmi:exporterVersion></xmi:Documentation>",
        "  <!-- CANDIDATE controls proposed by heuristic D3FEND mapping; review before import. Not written into any .mdzip. -->",
        f"  <uml:Model xmi:id='{pkg_id}_model' name='NIST SP 800-53r5 Security Controls'>",
        f"    <packagedElement xmi:type='uml:Package' xmi:id='{pkg_id}' name={quoteattr(f'Candidate controls for {sc.sid} {sc.name}')}>",
    ]
    stereo = []
    for i, r in enumerate(rows):
        cid = f"{pkg_id}_c{i}"
        text = (
            f"[CANDIDATE, {r['confidence']} confidence] Implement {r['control']} for {sc.sid}. Proposed from D3FEND "
            f"{', '.join(r['d3fend'])} (table entry '{r['matched']}', {r['level']}); relevant attack-tree leaves: "
            f"{'; '.join(r['leaves'])}. "
            f"Rationale: {r['rationale']}"
        )
        o.append(f"      <packagedElement xmi:type='uml:Class' xmi:id='{cid}' name={quoteattr(r['control'])}/>")
        stereo.append(f"  <sysml:Requirement xmi:id='{cid}_st' base_Class='{cid}' Id={quoteattr(r['control'])} Text={quoteattr(text)}/>")
    o.append("    </packagedElement>")
    o.append("  </uml:Model>")
    o.extend(stereo)
    o.append("</xmi:XMI>")
    return "\n".join(o) + "\n"


def write_outputs(sc: Scenario, m: Model, out_dir: Path, command: str, mermaid_path: Path | None = None) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    table = load_nist_table()
    files = {
        out_dir / f"cyber_{sc.slug}.md": render_markdown(sc, m, command),
        (mermaid_path or out_dir / f"cyber_{sc.slug}.mmd"): render_mermaid(sc),
        out_dir / "cyber_gaps.md": render_gaps_markdown(sc, command),
        out_dir / "cyber_gaps.json": json.dumps(gaps_json(sc, m, command), indent=1),
        out_dir / "cyber_candidate_nist_controls.md": render_nist_markdown(sc, table, command),
        out_dir / "cyber_candidate_nist_controls.csv": render_nist_csv(sc),
        out_dir / "nist_controls_candidate.xmi": render_nist_xmi(sc),
    }
    for p, text in files.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return list(files)
