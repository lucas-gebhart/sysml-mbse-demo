"""Standards conformance of a contractor delivery against a reference layer, plus cross-organisation linking.

Part 1 extracts *checkable conventions* from reference models (a UAF style guide, the Mission Meta Model
profile, the OMG UML Testing Profile 2.1 with its validation rules, a classification profile). Every rule
quotes the text it was derived from and the qualified name of the element that carries it; rules that
match a known evaluator become executable, the rest are listed as "not automatable".

Part 2 evaluates the executable rules against a (federated) delivery and folds the loader's
delivery-completeness signals (missing mounted projects, dangling references) into the same report.

Part 3 reuses :mod:`sysml_demo.link` to propose links between the delivery's mission-level content and
reference concepts (CapyBARA threads/measures, Mission Meta Model concepts, UJTL operational activities)
and renders one cross-model impact graph. Links are heuristic proposals, never asserted model facts.
"""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from collections.abc import Callable, Iterable
from dataclasses import asdict, dataclass, field
from pathlib import Path

from . import link, queries
from .ingest import strip_html
from .model import Element, Model

# --------------------------------------------------------------------------- rules
Params = dict[str, list[str]]


@dataclass
class Rule:
    id: str
    source: str  # reference model the rule was read from
    element: str  # qualified name of the element carrying the text
    text: str  # verbatim text (or "[observed in exemplar] ..." for structural conventions)
    family: str
    severity: str = "warn"
    check: str = ""  # evaluator key; empty means "not automatable"
    params: Params = field(default_factory=dict)

    @property
    def automatable(self) -> bool:
        return bool(self.check)


@dataclass
class Outcome:
    checked: int
    offenders: list[str]
    detail: str = ""


@dataclass
class RuleResult:
    rule: Rule
    status: str  # pass | fail | n.a.
    checked: int
    failed: int
    examples: list[str]
    detail: str = ""

    def as_dict(self) -> dict:
        d = asdict(self.rule)
        d.pop("params")
        d["automatable"] = self.rule.automatable
        d.update(status=self.status, checked=self.checked, failed=self.failed, examples=self.examples, detail=self.detail)
        return d


CSS_RE = re.compile(r"\b\w+\s*\{[^}]*\}")
NORMATIVE_RE = re.compile(r"\b(should|must|shall|required|are (?:to )?be used|need to)\b", re.I)
NARRATIVE_RE = re.compile(
    r"Diagram Classification: *(UNCLASSIFIED|\(U\)|U\b|CUI|SECRET)|Authors?: [A-Z]\. |^This [^.]{0,60}diagram (describes|shows)"
)
OCL_RE = re.compile(r"self\.|->|\binv\b|oclIsKindOf")
EXPRESSION_DUMP_RE = re.compile(r"^(Body|true)\b")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\[«])")
MARKING_RE = re.compile(r"UNCLASSIFIED|\(U\)|Distribution [A-F]\b|\bCUI\b|CONTROLLED UNCLASSIFIED", re.I)
NOISE = queries.NOISE_STEREOTYPES | {"DiagramInfo", "DiagramTable", "MatrixFilter", "DiagramTableMapToDataSource", "CustomSort"}
EXAMPLE_LIMIT = 10


def clean(text: str) -> str:
    return " ".join(CSS_RE.sub("", html.unescape(strip_html(text))).split())


def _statements(body: str) -> list[str]:
    """Split guide prose into normative statements; non-normative sentences are kept as continuation."""
    out: list[str] = []
    for s in SENTENCE_RE.split(body):
        s = s.strip()
        if not s:
            continue
        if NORMATIVE_RE.search(s) or not out:
            out.append(s)
        else:
            out[-1] = out[-1] + " " + s
    return [s for s in out if NORMATIVE_RE.search(s)]


@dataclass(frozen=True)
class Binding:
    pattern: str
    check: str
    family: str
    severity: str = "warn"


STYLE_BINDINGS = (
    Binding(r"naming schema", "diagram_naming", "naming"),
    Binding(r"titles shorter than (\d+) characters", "diagram_title_length", "naming", "info"),
    Binding(r"Diagrams should use a Comment to capture", "diagram_metadata_comment", "documentation"),
    Binding(r"containment browser should be organi[sz]ed", "viewpoint_packages", "structure"),
    Binding(r"linked using the Implements relationship", "met_implements_mt", "relationship"),
    Binding(r"swimlanes", "activity_swimlanes", "behavior"),
    Binding(r"pins on each end should be typed", "pins_typed", "behavior"),
    Binding(r"Property a\w+ named Country", "asset_country_property", "structure", "info"),
    Binding(r"relate to Capabilities using the MapsToCapability", "oa_maps_to_capability", "relationship"),
    Binding(r"relate to Operational Activities using the IsCapableToPerform", "performer_is_capable", "relationship"),
    Binding(r"captured as a Resource Architecture", "resource_architecture_exists", "structure", "info"),
)
MMM_BINDINGS = (
    Binding(r"^(Client is incorrect for Defines|Defines\.client)", "defines_client", "relationship", "error"),
    Binding(r"^(Supplier is Incorrect for Defines|Defines\.supplier)", "defines_supplier", "relationship", "error"),
    Binding(r"^(Client is incorrect for Opposes|Opposes\.client)", "opposes_client", "relationship", "error"),
    Binding(r"^(Supplier is Incorrect for Opposes|Opposes\.supplier)", "opposes_supplier", "relationship", "error"),
)
UTP_BINDINGS = (
    Binding(r"^Minimal TestConfiguration$", "utp_min_test_configuration", "utp"),
    Binding(r"^Each TestCase returns a Verdict", "utp_verdict_return", "utp"),
    Binding(r"^TestCase with owned UseCases NOT allowed", "utp_no_owned_usecase", "utp"),
    Binding(r"^(TestCase|TestProcedure|TestExecutionSchedule) requires AT ?MOST ONE precondition", "utp_at_most_one_precondition", "utp"),
    Binding(
        r"^(TestCase|TestProcedure|TestExecutionSchedule) (guarantees|should guarantee) AT MOST one post ?condition",
        "utp_at_most_one_postcondition",
        "utp",
    ),
    Binding(r"^Precondition is NOT specified for (TestCase|TestProcedure|TestExecutionSchedule)", "utp_has_precondition", "utp"),
    Binding(r"^Behavior TestCase with nested Behavior TestCase NOT allowed", "utp_no_nested_testcase", "utp"),
    Binding(r"^Allowed (TestCase|TestProcedure) invocation scheme", "utp_invocation_scheme", "utp"),
    Binding(r"^TestCase must invoke AT LEAST ONE main TestProcedure", "utp_main_procedure", "utp"),
    Binding(
        r"^(TestCase|TestSet) (must refer to|should have) AT MOST one arbitration ?specification", "utp_at_most_one_arbitration", "utp"
    ),
    Binding(r"^TestProcedure must prescribe the execution order of AT LEAST one", "utp_procedure_not_empty", "utp"),
    Binding(r"^TestProcedure operates on a TestConfiguration", "utp_procedure_on_configuration", "utp"),
    Binding(r"^TestProcedure use of ProcedureInvocation", "utp_procedure_invocation_role", "utp"),
    Binding(r"^TestContext should specify AT MOST ONE (TestLevel|TestType)", "utp_at_most_one_tag", "utp"),
    Binding(r"^(TestObjective|TestRequirement) should ONLY be applied to Class", "utp_applied_to", "utp"),
    Binding(r"^(TestContext|TestSet) should NOT be applied to Profile", "utp_not_applied_to", "utp"),
    Binding(r"^TestLogElement extended metaclass restriction", "utp_not_applied_to", "utp"),
    Binding(r"^(Alternative|Loop|Negative|Parallel|Sequence) application in Activities", "utp_activity_node_kind", "utp"),
    Binding(r"^Restriction of Overrides client and supplier", "utp_overrides_ends", "utp"),
    Binding(r"^DataProvider must have a DataSpecification", "utp_dataprovider_spec", "utp"),
)
UTP_NODE_KIND = {
    "Alternative": "ConditionalNode",
    "Loop": "LoopNode",
    "Negative": "StructuredActivityNode",
    "Parallel": "ConditionalNode",
    "Sequence": "SequenceNode",
}
UTP_NOT_APPLIED = {"TestContext": "Profile", "TestSet": "Profile", "TestLogElement": "EnumerationLiteral"}
UAF_ASSET_STEREOTYPES = (
    "ResourceArtifact",
    "System",
    "CapabilityConfiguration",
    "ResourcePerformer",
    "Organization",
    "Post",
    "ResourceArchitecture",
    "NaturalResource",
    "Software",
)
FLOW_DIAGRAM_RE = re.compile(r"Activity|Process Flow|Internal Block|Internal Connectivity|Sequence|Interaction")
METACLASS_KINDS = {
    "Class": {"Class"},
    "Activity": {"Activity"},
    "Property": {"Property", "Port"},
    "Package": {"Package", "Model", "Profile"},
    "Dependency": {"Dependency", "Abstraction", "Realization", "Usage"},
    "Abstraction": {"Abstraction"},
    "InstanceSpecification": {"InstanceSpecification"},
    "Action": {"CallBehaviorAction", "OpaqueAction", "SendSignalAction", "AcceptEventAction", "Action"},
    "CallBehaviorAction": {"CallBehaviorAction"},
    "Comment": {"Comment"},
    "Enumeration": {"Enumeration"},
    "DataType": {"DataType"},
    "Constraint": {"Constraint"},
    "UseCase": {"UseCase"},
    "Actor": {"Actor"},
    "Diagram": {"Diagram"},
}


def _bind(text: str, bindings: Iterable[Binding]) -> tuple[Binding | None, Params]:
    for b in bindings:
        m = re.search(b.pattern, text, re.I)
        if m:
            return b, {"match": [g for g in m.groups() if g]}
    return None, {}


def _annotated(m: Model, c: Element) -> str:
    target = next((t for t in c.refs.get("annotatedElement", []) if t in m.elements), c.owner)
    return m.qualified_name(target) if target in m.elements else m.qualified_name(c.id)


def _prose_rules(m: Model, bindings: Iterable[Binding], prefix: str) -> list[Rule]:
    """One rule per normative statement found in Comment bodies / element documentation."""
    rules: list[Rule] = []
    seen: set[str] = set()
    sources: list[tuple[str, str]] = []
    for c in m.of_type("Comment"):
        sources.append((_annotated(m, c), clean(c.attrs.get("body", ""))))
    for e in m.of_type("Package", "Model", "Profile"):
        if e.doc and not any(m.elements[c].kind == "Comment" for c in e.children if c in m.elements):
            sources.append((m.qualified_name(e.id), clean(e.doc)))
    for where, body in sources:
        if not body or NARRATIVE_RE.search(body) or not NORMATIVE_RE.search(body):
            continue
        for text in _statements(body):
            if text in seen or len(text) < 25:
                continue
            seen.add(text)
            b, params = _bind(text, bindings)
            rules.append(
                Rule(
                    id=prefix,
                    source=m.name,
                    element=where,
                    text=text,
                    family=b.family if b else "guidance",
                    severity=b.severity if b else "warn",
                    check=b.check if b else "",
                    params=params,
                )
            )
    return rules


def _top_packages(m: Model, project: str | None = None) -> list[Element]:
    out = []
    for e in m.of_type("Package"):
        if project is not None and e.project != project:
            continue
        own = m.elements.get(e.owner) if e.owner else None
        if (own is None or own.kind == "Model") and not e.name.endswith("_shared"):
            out.append(e)
    return out


def _is_title_case(name: str) -> bool:
    words = [w for w in re.split(r"[\s_/-]+", name) if w and w[0].isalpha()]
    return bool(words) and all(w[0].isupper() for w in words)


def extract_style_guide(m: Model) -> list[Rule]:
    """Conventions from a Mission Architecture Style Guide exemplar: guide prose, legends, exemplar structure."""
    rules = _prose_rules(m, STYLE_BINDINGS, "SG")
    tops = _top_packages(m)
    expected = sorted({f"{t.name}<<{s}>>" for t in tops for s in t.stereotype_names() if s not in NOISE})
    for r in rules:
        if r.check == "viewpoint_packages":
            r.params["expected"] = expected
        if r.check == "diagram_naming":
            r.params["prefixes"] = sorted(
                set(re.findall(r"\b([A-Z][A-Z0-9]{1,4}) for \w+", r.text)) | set(re.findall(r"as follows: ([A-Z]{2,5})\b", r.text))
            )
    # legends: constraints whose constrained elements are the view packages they colour
    for c in m.of_type("Constraint"):
        owner = m.elements.get(c.owner or "")
        if owner is None or "view" not in owner.name.lower() or c.name.lower() not in ("required", "recommended"):
            continue
        views = [m.qualified_name(t) for t in c.refs.get("constrainedElement", []) if t in m.elements]
        if not views:
            continue
        rules.append(
            Rule(
                "SG",
                m.name,
                m.qualified_name(c.id),
                f"Legend «{owner.name}» marks these views as {c.name}: {', '.join(views)}",
                "views",
                "error" if c.name.lower() == "required" else "info",
                "required_views",
                {"views": [v.rsplit("::", 1)[-1] for v in views]},
            )
        )
    matrices = [d for d in m.diagrams() if "Matrix" in d.diagram_type]
    if matrices:
        rules.append(
            Rule(
                "SG",
                m.name,
                m.qualified_name(matrices[0].owner or matrices[0].id).split("::")[0],
                "[observed in exemplar] The style guide exemplar provides these dependency matrices: "
                + "; ".join(f"'{d.name}' ({d.diagram_type})" for d in matrices),
                "matrices",
                "warn",
                "dependency_matrices",
                {"matrices": [f"{d.diagram_type}|{d.name}" for d in matrices]},
            )
        )
    if tops and all(_is_title_case(t.name) for t in tops):
        rules.append(
            Rule(
                "SG",
                m.name,
                m.name,
                f"[observed in exemplar] All {len(tops)} top-level packages use Title Case names: " + ", ".join(t.name for t in tops),
                "naming",
                "info",
                "package_title_case",
            )
        )
    documented = [t for t in tops if t.doc]
    if tops and len(documented) * 2 >= len(tops):
        rules.append(
            Rule(
                "SG",
                m.name,
                m.name,
                f"[observed in exemplar] {len(documented)} of {len(tops)} top-level packages carry documentation "
                f"({', '.join(t.name for t in documented)})",
                "documentation",
                "info",
                "package_documentation",
            )
        )
    info = next((s for s in m.of_type("Stereotype") if re.sub(r"[\s_]", "", s.name.lower()) == "diagraminfo"), None)
    if info is not None:
        tags = [
            m.elements[c].name for c in info.children if m.elements[c].kind == "Property" and not m.elements[c].name.startswith("base_")
        ]
        applied = sum(1 for d in m.diagrams() if d.has_stereotype(info.name))
        rules.append(
            Rule(
                "CLS",
                m.name,
                m.qualified_name(info.id),
                f"Stereotype «{info.name}» carries the diagram marking tags {', '.join(tags)}; the exemplar applies it to "
                f"{applied} of {len(m.diagrams())} diagrams. Every diagram carries a classification marking.",
                "classification",
                "error",
                "diagram_classification",
            )
        )
    for e in m.of_type("Model") + tops:
        if e.doc and MARKING_RE.search(e.doc):
            sentence = next((s for s in SENTENCE_RE.split(clean(e.doc)) if MARKING_RE.search(s)), clean(e.doc)[:200])
            rules.append(
                Rule(
                    "CLS",
                    m.name,
                    m.qualified_name(e.id),
                    f'Model-level documentation states the overall classification / distribution: "{sentence}"',
                    "classification",
                    "warn",
                    "root_marking_statement",
                )
            )
            break
    return rules


def _constraint_text(m: Model, c: Element) -> str:
    parts = [clean(c.doc)] if c.doc else []
    for k in c.children:
        ch = m.elements.get(k)
        if ch is None:
            continue
        body = clean(ch.attrs.get("body", ""))
        if not body or body.startswith("<?xml"):
            continue
        if ch.kind == "OpaqueExpression":
            if EXPRESSION_DUMP_RE.match(body):
                continue
            parts.append(f"OCL: {body}" if OCL_RE.search(body) else body)
        elif ch.kind == "Comment" and body not in parts:
            parts.append(body)
    return " ".join(dict.fromkeys(p for p in parts if p))


def _constrained(m: Model, c: Element) -> list[str]:
    return [m.qualified_name(t) if t in m.elements else m.external_name(t) for t in c.refs.get("constrainedElement", [])]


def extract_utp(m: Model) -> list[Rule]:
    """The «validationRule» constraints of the UML Testing Profile (68 in UTP 2.1), plus the marking convention it applies."""
    rules: list[Rule] = []
    for c in m.of_type("Constraint"):
        if not c.has_stereotype("validationRule"):
            continue
        targets = _constrained(m, c)
        text = _constraint_text(m, c)
        b, params = _bind(c.name, UTP_BINDINGS)
        rules.append(
            Rule(
                "UTP",
                m.name,
                targets[0] if targets else m.qualified_name(c.id),
                f"{c.name}: {text}" if text else c.name,
                "utp",
                (c.tag("severity") or "error").replace("warning", "warn"),
                b.check if b else "",
                params,
            )
        )
    marking = next((s for s in m.of_type("Stereotype") if "marking" in s.name.lower()), None)
    if marking is not None:
        tags = [
            m.elements[c].name for c in marking.children if m.elements[c].kind == "Property" and not m.elements[c].name.startswith("base_")
        ]
        tops = _top_packages(m)
        applied = sum(1 for t in tops if t.has_stereotype(marking.name))
        rules.append(
            Rule(
                "CLS",
                m.name,
                m.qualified_name(marking.id),
                f"Stereotype «{marking.name}» carries the tags {', '.join(tags)}; the reference profile applies it to "
                f"{applied} of {len(tops)} top-level packages. Top-level packages carry a data-control marking.",
                "classification",
                "warn",
                "package_markings",
            )
        )
    return rules


def _metaclass(m: Model, st: Element) -> str:
    for c in st.children:
        ch = m.elements.get(c)
        if ch is not None and ch.kind == "Property" and ch.name.startswith("base_"):
            return ch.name[5:]
    return ""


def _specializations(m: Model, root: str) -> set[str]:
    """Names of stereotypes that generalize (transitively) to `root`, including root."""
    out = {root}
    changed = True
    while changed:
        changed = False
        for st in m.of_type("Stereotype"):
            if st.name not in out and set(m.generals(st)) & out:
                out.add(st.name)
                changed = True
    return out


def extract_mission_meta_model(m: Model) -> list[Rule]:
    """The Mission_Profile stereotypes (metaclass, specialisations, tags) and the profile's own constraints."""
    rules: list[Rule] = []
    profile = next((p for p in m.of_type("Profile") if "mission" in p.name.lower()), None)
    stereos = [s for s in m.of_type("Stereotype") if profile is None or any(o.id == profile.id for o in m.owner_chain(s.id))]
    names = [s.name for s in stereos if _metaclass(m, s)]
    if profile is not None and names:
        rules.append(
            Rule(
                "MMM",
                m.name,
                m.qualified_name(profile.id),
                f"Profile «{profile.name}» defines the mission-level vocabulary: {', '.join(names)}. "
                "Mission-level content of a delivery is typed with these stereotypes.",
                "vocabulary",
                "warn",
                "mission_profile_applied",
                {"stereotypes": names},
            )
        )
    for s in stereos:
        meta = _metaclass(m, s)
        if not meta:
            continue
        gens = m.generals(s)
        tags = [
            f"{m.elements[c].name}: {m.type_name_of(m.elements[c]) or '?'}"
            for c in s.children
            if m.elements[c].kind == "Property" and not m.elements[c].name.startswith("base_")
        ]
        text = f"«{s.name}» extends metaclass {meta}"
        if gens:
            text += f"; specializes «{'», «'.join(gens)}»"
        if tags:
            text += f"; tags: {', '.join(tags)}"
        if s.doc:
            text += f". {clean(s.doc)}"
        rules.append(
            Rule(
                "MMM",
                m.name,
                m.qualified_name(s.id),
                text,
                "stereotype",
                "error",
                "stereotype_metaclass",
                {"stereotype": [s.name], "metaclass": [meta]},
            )
        )
    for c in m.of_type("Constraint"):
        text = _constraint_text(m, c)
        if not text:
            continue
        b, params = _bind(c.name, MMM_BINDINGS)
        params["strategic"] = sorted(_specializations(m, "StrategicPhase"))
        params["opposable"] = sorted(_specializations(m, "OpposableElement"))
        targets = _constrained(m, c)
        rules.append(
            Rule(
                "MMM",
                m.name,
                targets[0] if targets else m.qualified_name(c.id),
                f"{c.name}: {text}",
                "relationship",
                "error",
                b.check if b else "",
                params,
            )
        )
    rules.extend(_prose_rules(m, (), "MMM"))
    return rules


def extract_classification(m: Model) -> list[Rule]:
    """Allowed marking values from a classification profile's enumerations."""
    rules: list[Rule] = []
    for en in m.of_type("Enumeration"):
        lits = [m.elements[c].name for c in en.children if m.elements[c].kind == "EnumerationLiteral"]
        if not lits or not re.search(r"classif|caveat|marking|distribution", en.name, re.I):
            continue
        doc = f" {clean(en.doc)}" if en.doc else ""
        rules.append(
            Rule(
                "CLS",
                m.name,
                m.qualified_name(en.id),
                f"Enumeration «{en.name}» defines the allowed values {', '.join(lits)}.{doc} "
                "Marking values are drawn from this enumeration.",
                "classification",
                "error",
                "classification_values",
                {"literals": lits, "enumeration": [en.name]},
            )
        )
    return rules


def detect_reference_kind(m: Model) -> str:
    stereos = {s.name for s in m.of_type("Stereotype")}
    if any(c.has_stereotype("validationRule") for c in m.of_type("Constraint")) and "TestCase" in stereos:
        return "utp"
    if "MissionEngineeringThread" in stereos and m.of_type("Profile"):
        return "mission-meta-model"
    if not stereos and any("classif" in e.name.lower() for e in m.of_type("Enumeration")):
        return "classification"
    return "style-guide"


EXTRACTORS: dict[str, Callable[[Model], list[Rule]]] = {
    "utp": extract_utp,
    "mission-meta-model": extract_mission_meta_model,
    "classification": extract_classification,
    "style-guide": extract_style_guide,
}


def extract_rules(references: Iterable[Model]) -> list[Rule]:
    """Extract rules from every reference model (kind auto-detected) and number them per family prefix."""
    rules: list[Rule] = []
    for m in references:
        rules.extend(EXTRACTORS[detect_reference_kind(m)](m))
    counter: Counter[str] = Counter()
    for r in rules:
        counter[r.id] += 1
        r.id = f"{r.id}-{counter[r.id]:02d}"
    return rules


# --------------------------------------------------------------------------- delivery scope
GENERIC_STEMS = {
    "model",
    "system",
    "level",
    "test",
    "library",
    "baseline",
    "profile",
    "architecture",
    "functional",
    "allocated",
    "product",
    "shared",
}


class Scope:
    """The part of a (federated) model that *is* the delivery, as opposed to the reference projects it mounts."""

    def __init__(self, model: Model, projects: Iterable[str] = ()):
        self.model = model
        self.projects = set(projects)
        self.elements = [e for e in model.elements.values() if not self.projects or e.project in self.projects]

    def kinds(self, *kinds: str) -> list[Element]:
        return [e for e in self.elements if e.kind in kinds]

    def stereotyped(self, *names: str) -> list[Element]:
        return [e for e in self.elements if e.has_stereotype(*names)]

    def diagrams(self) -> list[Element]:
        return self.kinds("Diagram")

    def top_packages(self) -> list[Element]:
        return [p for p in _top_packages(self.model) if not self.projects or p.project in self.projects]

    def qn(self, e: Element) -> str:
        return self.model.qualified_name(e.id)


def delivery_projects(m: Model, roots: Iterable[str], reference_stems: Iterable[str] = ()) -> set[str]:
    """Projects that form the delivery: the roots plus mounted projects sharing a distinctive name token with them,
    excluding profile projects and anything given as a reference model."""
    roots = list(roots)
    key: set[str] = set()
    for r in roots:
        key |= link.raw_tokens(r) - GENERIC_STEMS
    refs = {Path(s).stem for s in reference_stems}
    out = {r for r in roots if r in m.projects}
    for p in m.projects:
        if p in refs or p in out:
            continue
        if any(e.kind == "Profile" and e.project == p for e in m.of_type("Profile")):
            continue
        if link.raw_tokens(p) & key:
            out.add(p)
    return out


# --------------------------------------------------------------------------- evaluators
Check = Callable[[Scope, Rule], Outcome]
CHECKS: dict[str, Check] = {}


def check(name: str) -> Callable[[Check], Check]:
    def deco(fn: Check) -> Check:
        CHECKS[name] = fn
        return fn

    return deco


def _outgoing(s: Scope, e: Element, *stereos: str) -> list[Element]:
    return [r for r in s.model.incoming(e.id, "client") if r.has_stereotype(*stereos)]


def _children(s: Scope, e: Element, *kinds: str) -> list[Element]:
    return [s.model.elements[c] for c in e.children if c in s.model.elements and (not kinds or s.model.elements[c].kind in kinds)]


def _user_tags(e: Element) -> dict[str, str]:
    """Stereotype tags excluding MagicDraw's automatic DiagramInfo bookkeeping (Author, Creation_date, ...)."""
    return {k: v for st in e.stereotypes if st.name != "DiagramInfo" for k, v in st.tags.items() if v}


def _marking_tags(e: Element) -> dict[str, str]:
    return {k: v for k, v in _user_tags(e).items() if re.search(r"classif|marking|distribution|caveat", k, re.I)}


def _has_metadata_comment(s: Scope, d: Element) -> bool:
    if d.doc or _marking_tags(d) or any(re.search(r"narrative|author", k, re.I) for k in _user_tags(d)):
        return True
    owner = s.model.elements.get(d.owner or "")
    for c in _children(s, owner, "Comment") if owner else []:
        if re.search(r"classification", c.attrs.get("body", ""), re.I) and (
            not c.refs.get("annotatedElement") or d.id in c.refs["annotatedElement"]
        ):
            return True
    return False


@check("diagram_naming")
def _diagram_naming(s: Scope, r: Rule) -> Outcome:
    prefixes = set(r.params.get("prefixes", ["MET", "E2E", "SEQ", "OOB"]))
    pop = [d for d in s.diagrams() if FLOW_DIAGRAM_RE.search(d.diagram_type)]
    bad = [d for d in pop if (d.name.split() or [""])[0].upper() not in prefixes]
    return Outcome(
        len(pop),
        [f"{s.qn(d)} ({d.diagram_type})" for d in bad],
        f"activity/connectivity/sequence diagram names must start with one of {sorted(prefixes)}",
    )


@check("diagram_title_length")
def _diagram_title_length(s: Scope, r: Rule) -> Outcome:
    limit = int(r.params["match"][0]) if r.params.get("match") else 30
    pop = s.diagrams()
    bad = [d for d in pop if len(d.name) > limit]
    return Outcome(len(pop), [f"{s.qn(d)} ({len(d.name)} chars)" for d in bad], f"diagram titles longer than {limit} characters")


@check("diagram_metadata_comment")
def _diagram_metadata_comment(s: Scope, r: Rule) -> Outcome:
    pop = s.diagrams()
    bad = [d for d in pop if not _has_metadata_comment(s, d)]
    return Outcome(
        len(pop), [f"{s.qn(d)} ({d.diagram_type})" for d in bad], "diagrams without documentation / classification-narrative comment"
    )


@check("viewpoint_packages")
def _viewpoint_packages(s: Scope, r: Rule) -> Outcome:
    expected = r.params.get("expected", [])
    tops = s.top_packages()
    present = {t.name for t in tops} | {st for t in tops for st in t.stereotype_names()}
    missing = [x for x in expected if x.split("<<")[0] not in present and x.split("<<")[1].rstrip(">") not in present]
    return Outcome(len(expected), missing, f"delivery top-level packages: {', '.join(t.name for t in tops)}")


@check("met_implements_mt")
def _met_implements_mt(s: Scope, r: Rule) -> Outcome:
    pop = s.stereotyped("MissionEngineeringThread")
    bad = [e for e in pop if not _outgoing(s, e, "Implements")]
    return Outcome(len(pop), [s.qn(e) for e in bad], "«MissionEngineeringThread» without an outgoing «Implements»")


@check("activity_swimlanes")
def _activity_swimlanes(s: Scope, r: Rule) -> Outcome:
    pop = [a for a in s.kinds("Activity") if _children(s, a, "CallBehaviorAction", "OpaqueAction")]
    bad = [a for a in pop if not _children(s, a, "ActivityPartition")]
    return Outcome(len(pop), [s.qn(a) for a in bad], "activities with actions but no swimlane (ActivityPartition)")


@check("pins_typed")
def _pins_typed(s: Scope, r: Rule) -> Outcome:
    pop = s.kinds("InputPin", "OutputPin")
    bad = [p for p in pop if not (s.model.type_of(p) or p.refs.get("type"))]
    uaf = sum(1 for p in pop if (t := s.model.type_of(p)) and t.has_stereotype("OperationalInformation", "ResourceInformation"))
    return Outcome(
        len(pop), [s.qn(p) for p in bad], f"{len(pop) - len(bad)} pins typed, {uaf} of them by UAF Operational/ResourceInformation"
    )


@check("asset_country_property")
def _asset_country_property(s: Scope, r: Rule) -> Outcome:
    pop = s.stereotyped(*UAF_ASSET_STEREOTYPES)
    bad = [e for e in pop if not any(p.name.lower() == "country" for p in _children(s, e, "Property"))]
    return Outcome(len(pop), [s.qn(e) for e in bad], "UAF assets without a 'Country' property")


@check("oa_maps_to_capability")
def _oa_maps_to_capability(s: Scope, r: Rule) -> Outcome:
    pop = s.stereotyped("OperationalActivity")
    bad = [e for e in pop if not _outgoing(s, e, "MapsToCapability")]
    return Outcome(len(pop), [s.qn(e) for e in bad], "«OperationalActivity» without «MapsToCapability»")


@check("performer_is_capable")
def _performer_is_capable(s: Scope, r: Rule) -> Outcome:
    pop = s.stereotyped("OperationalPerformer")
    bad = [e for e in pop if not _outgoing(s, e, "IsCapableToPerform")]
    return Outcome(len(pop), [s.qn(e) for e in bad], "«OperationalPerformer» without «IsCapableToPerform»")


@check("resource_architecture_exists")
def _resource_architecture_exists(s: Scope, r: Rule) -> Outcome:
    n = len(s.stereotyped("ResourceArchitecture"))
    return Outcome(1, [] if n else ["delivery defines no «ResourceArchitecture»"], f"{n} «ResourceArchitecture» in delivery")


@check("required_views")
def _required_views(s: Scope, r: Rule) -> Outcome:
    types = {d.diagram_type for d in s.diagrams()}
    missing = [v for v in r.params.get("views", []) if not any(link.tokens(v) <= link.tokens(t) for t in types)]
    return Outcome(len(r.params.get("views", [])), missing, f"delivery diagram types: {', '.join(sorted(types))}")


@check("dependency_matrices")
def _dependency_matrices(s: Scope, r: Rule) -> Outcome:
    mats = [d for d in s.diagrams() if "Matrix" in d.diagram_type]
    missing = []
    for spec in r.params.get("matrices", []):
        dtype, name = spec.split("|", 1)
        generic = dtype == "Dependency Matrix"
        ok = any(
            (not generic and d.diagram_type == dtype)
            or (generic and len(link.tokens(name) & link.tokens(d.name)) * 2 >= len(link.tokens(name)))
            for d in mats
        )
        if not ok:
            missing.append(f"{name} ({dtype})")
    return Outcome(
        len(r.params.get("matrices", [])),
        missing,
        f"delivery has {len(mats)} matrix diagrams: {', '.join(sorted({d.diagram_type for d in mats}))}",
    )


@check("package_title_case")
def _package_title_case(s: Scope, r: Rule) -> Outcome:
    pop = s.top_packages()
    bad = [p for p in pop if not _is_title_case(p.name)]
    return Outcome(len(pop), [s.qn(p) for p in bad], "top-level packages not in Title Case")


@check("package_documentation")
def _package_documentation(s: Scope, r: Rule) -> Outcome:
    pop = s.top_packages()
    bad = [p for p in pop if not p.doc]
    return Outcome(len(pop), [s.qn(p) for p in bad], "top-level packages without documentation")


@check("diagram_classification")
def _diagram_classification(s: Scope, r: Rule) -> Outcome:
    pop = s.diagrams()
    bad = [d for d in pop if not _marking_tags(d) and not _has_metadata_comment(s, d)]
    return Outcome(len(pop), [f"{s.qn(d)} ({d.diagram_type})" for d in bad], "diagrams without a classification marking")


@check("classification_values")
def _classification_values(s: Scope, r: Rule) -> Outcome:
    allowed = {v.lower() for v in r.params.get("literals", [])} | {"u", "unclassified"}
    pop, bad = [], []
    for e in s.elements:
        for k, v in _marking_tags(e).items():
            if not re.search(r"classif", k, re.I):
                continue
            val = s.model.elements[v].name if v in s.model.elements else v
            pop.append(e)
            if val.strip("() ").lower() not in allowed:
                bad.append(f"{s.qn(e)}: {k}={val}")
    return Outcome(len(pop), bad, f"allowed values: {', '.join(r.params.get('literals', []))}")


@check("package_markings")
def _package_markings(s: Scope, r: Rule) -> Outcome:
    pop = s.top_packages()
    bad = [p for p in pop if not _marking_tags(p)]
    return Outcome(len(pop), [s.qn(p) for p in bad], "top-level packages without a marking stereotype/tag")


@check("root_marking_statement")
def _root_marking_statement(s: Scope, r: Rule) -> Outcome:
    docs = [e for e in s.kinds("Model") + s.top_packages() if e.doc and MARKING_RE.search(e.doc)]
    return Outcome(
        1,
        [] if docs else ["no model/top-level package documentation states a classification or distribution statement"],
        f"{len(docs)} elements carry a marking statement",
    )


@check("mission_profile_applied")
def _mission_profile_applied(s: Scope, r: Rule) -> Outcome:
    names = r.params.get("stereotypes", [])
    used = Counter(st for e in s.elements for st in e.stereotype_names() if st in names)
    return Outcome(
        1,
        [] if used else [f"delivery applies none of {', '.join(names[:8])}…"],
        "applied: " + (", ".join(f"{k} x{v}" for k, v in used.most_common()) or "none"),
    )


@check("stereotype_metaclass")
def _stereotype_metaclass(s: Scope, r: Rule) -> Outcome:
    st, meta = r.params["stereotype"][0], r.params["metaclass"][0]
    pop = s.stereotyped(st)
    allowed = METACLASS_KINDS.get(meta)
    bad = [e for e in pop if allowed is not None and e.kind not in allowed]
    return Outcome(len(pop), [f"{s.qn(e)} is a {e.kind}" for e in bad], f"«{st}» applied {len(pop)} times; expected metaclass {meta}")


def _dependency_ends(s: Scope, stereo: str, end: str, ok: Callable[[Element], bool], what: str) -> Outcome:
    pop = s.stereotyped(stereo)
    bad = [e for e in pop if not all(ok(s.model.elements[t]) for t in e.refs.get(end, []) if t in s.model.elements)]
    return Outcome(len(pop), [s.qn(e) for e in bad], f"«{stereo}».{end} must be {what}")


@check("defines_client")
def _defines_client(s: Scope, r: Rule) -> Outcome:
    return _dependency_ends(s, "Defines", "client", lambda e: e.kind == "Activity", "an Activity")


@check("defines_supplier")
def _defines_supplier(s: Scope, r: Rule) -> Outcome:
    ok = set(r.params.get("strategic", ["StrategicPhase"]))
    return _dependency_ends(s, "Defines", "supplier", lambda e: bool(set(e.stereotype_names()) & ok), "a StrategicPhase")


@check("opposes_client")
def _opposes_client(s: Scope, r: Rule) -> Outcome:
    ok = set(r.params.get("opposable", ["OpposableElement"]))
    return _dependency_ends(s, "Opposes", "client", lambda e: bool(set(e.stereotype_names()) & ok), "an OpposableElement")


@check("opposes_supplier")
def _opposes_supplier(s: Scope, r: Rule) -> Outcome:
    ok = set(r.params.get("opposable", ["OpposableElement"]))
    return _dependency_ends(s, "Opposes", "supplier", lambda e: bool(set(e.stereotype_names()) & ok), "an OpposableElement")


def _subject(r: Rule, default: str) -> str:
    return r.params["match"][0] if r.params.get("match") else default


def _invoked(s: Scope, act: Element) -> list[tuple[Element, Element]]:
    """(call action, invoked behavior) pairs for an activity."""
    out = []
    for cba in _children(s, act, "CallBehaviorAction"):
        for b in cba.refs.get("behavior", []):
            if b in s.model.elements:
                out.append((cba, s.model.elements[b]))
    return out


@check("utp_min_test_configuration")
def _utp_min_test_configuration(s: Scope, r: Rule) -> Outcome:
    pop = s.stereotyped("TestConfiguration")
    bad = [e for e in pop if not any(p.has_stereotype("TestItem") for p in _children(s, e, "Property"))]
    parts = sum(len(_children(s, e, "Property")) for e in pop)
    return Outcome(
        len(pop), [s.qn(e) for e in bad], f"{parts} parts across {len(pop)} TestConfiguration(s); offenders have no part with «TestItem»"
    )


@check("utp_verdict_return")
def _utp_verdict_return(s: Scope, r: Rule) -> Outcome:
    pop = s.stereotyped("TestCase")
    bad = []
    for e in pop:
        params = [p for p in _children(s, e, "Parameter") if p.attrs.get("direction") in ("out", "return", "inout")]
        if not any("verdict" in s.model.type_name_of(p).lower() for p in params):
            bad.append(e)
    return Outcome(len(pop), [s.qn(e) for e in bad], "TestCases without an out/return Parameter typed by Verdict")


@check("utp_no_owned_usecase")
def _utp_no_owned_usecase(s: Scope, r: Rule) -> Outcome:
    pop = s.stereotyped("TestCase")
    bad = [e for e in pop if any(u.has_stereotype("TestCase") for u in _children(s, e, "UseCase"))]
    return Outcome(len(pop), [s.qn(e) for e in bad], "TestCases owning «TestCase» UseCases")


def _at_most_one_ref(s: Scope, r: Rule, ref: str) -> Outcome:
    st = _subject(r, "TestCase")
    pop = s.stereotyped(st)
    bad = [e for e in pop if len(e.refs.get(ref, [])) > 1]
    return Outcome(len(pop), [s.qn(e) for e in bad], f"«{st}» with more than one {ref}")


@check("utp_at_most_one_precondition")
def _utp_at_most_one_precondition(s: Scope, r: Rule) -> Outcome:
    return _at_most_one_ref(s, r, "precondition")


@check("utp_at_most_one_postcondition")
def _utp_at_most_one_postcondition(s: Scope, r: Rule) -> Outcome:
    return _at_most_one_ref(s, r, "postcondition")


@check("utp_has_precondition")
def _utp_has_precondition(s: Scope, r: Rule) -> Outcome:
    st = _subject(r, "TestCase")
    pop = s.stereotyped(st)
    bad = [e for e in pop if not e.refs.get("precondition")]
    return Outcome(len(pop), [s.qn(e) for e in bad], f"«{st}» without a precondition")


@check("utp_no_nested_testcase")
def _utp_no_nested_testcase(s: Scope, r: Rule) -> Outcome:
    pop = [e for e in s.stereotyped("TestCase") if e.kind == "Activity"]
    bad = [e for e in pop if any(d.has_stereotype("TestCase") for d in s.model.descendants(e.id))]
    return Outcome(len(pop), [s.qn(e) for e in bad], "behaviour TestCases nesting another «TestCase»")


@check("utp_invocation_scheme")
def _utp_invocation_scheme(s: Scope, r: Rule) -> Outcome:
    st = _subject(r, "TestCase")
    forbidden = ("TestCase", "TestExecutionSchedule") if st == "TestCase" else ("TestCase",)
    pop = s.stereotyped(st)
    bad = [f"{s.qn(e)} invokes {b.name}" for e in pop for _, b in _invoked(s, e) if b.has_stereotype(*forbidden)]
    return Outcome(len(pop), bad, f"«{st}» must not invoke {'/'.join(forbidden)}")


@check("utp_main_procedure")
def _utp_main_procedure(s: Scope, r: Rule) -> Outcome:
    pop = s.stereotyped("TestCase")
    bad = []
    for e in pop:
        calls = [(c, b) for c, b in _invoked(s, e) if b.has_stereotype("TestProcedure")]
        if len(calls) > 1 and not any("main" in (c.tag("role") or "").lower() for c, _ in calls):
            bad.append(f"{s.qn(e)} invokes {len(calls)} TestProcedures, none marked «ProcedureInvocation» role=main")
    return Outcome(len(pop), bad, "TestCases invoking several TestProcedures need one main ProcedureInvocation")


@check("utp_at_most_one_arbitration")
def _utp_at_most_one_arbitration(s: Scope, r: Rule) -> Outcome:
    st = _subject(r, "TestCase")
    pop = s.stereotyped(st)
    bad = [e for e in pop if sum(1 for c in _children(s, e) if c.has_stereotype("ArbitrationSpecification")) > 1]
    return Outcome(len(pop), [s.qn(e) for e in bad], f"«{st}» owning more than one «ArbitrationSpecification»")


@check("utp_procedure_not_empty")
def _utp_procedure_not_empty(s: Scope, r: Rule) -> Outcome:
    pop = [e for e in s.stereotyped("TestProcedure") if e.kind == "Activity"]
    bad = [e for e in pop if not any(c.kind.endswith(("Action", "Node")) for c in _children(s, e))]
    return Outcome(len(pop), [s.qn(e) for e in bad], "TestProcedure activities without any action/node (empty procedure)")


@check("utp_procedure_on_configuration")
def _utp_procedure_on_configuration(s: Scope, r: Rule) -> Outcome:
    pop = s.stereotyped("TestProcedure")
    bad = []
    for e in pop:
        ctx = [o for o in s.model.owner_chain(e.id) if o.has_stereotype("TestContext")]
        cfgs = [c for o in ctx for c in _children(s, o) if c.has_stereotype("TestConfiguration")]
        if not any(p.has_stereotype("TestItem") for c in cfgs for p in _children(s, c, "Property")):
            why = (
                "no owning «TestContext»"
                if not ctx
                else ("no «TestConfiguration» in context" if not cfgs else "TestConfiguration has no «TestItem» part")
            )
            bad.append(f"{s.qn(e)}: {why}")
    return Outcome(len(pop), bad, "TestProcedures must run on a TestConfiguration with at least one TestItem")


@check("utp_procedure_invocation_role")
def _utp_procedure_invocation_role(s: Scope, r: Rule) -> Outcome:
    pop = s.stereotyped("TestProcedure")
    bad = [
        f"{s.qn(e)}: invocation role={c.tag('role')}"
        for e in pop
        for c, _ in _invoked(s, e)
        if c.has_stereotype("ProcedureInvocation") and c.tag("role")
    ]
    return Outcome(len(pop), bad, "ProcedureInvocations inside a TestProcedure must not set a role")


@check("utp_at_most_one_tag")
def _utp_at_most_one_tag(s: Scope, r: Rule) -> Outcome:
    tag = _subject(r, "TestLevel").lower().replace("test", "")
    pop = s.stereotyped("TestContext")
    bad = [
        e
        for e in pop
        if any(tag in k.lower() and len(re.split(r"[;\s]+", v.strip())) > 1 for st in e.stereotypes for k, v in st.tags.items())
    ]
    return Outcome(len(pop), [s.qn(e) for e in bad], f"TestContexts with more than one test{tag}")


@check("utp_applied_to")
def _utp_applied_to(s: Scope, r: Rule) -> Outcome:
    st = _subject(r, "TestObjective")
    pop = s.stereotyped(st)
    bad = [f"{s.qn(e)} is a {e.kind}" for e in pop if e.kind != "Class"]
    return Outcome(len(pop), bad, f"«{st}» must be applied to Class")


@check("utp_not_applied_to")
def _utp_not_applied_to(s: Scope, r: Rule) -> Outcome:
    st = _subject(r, "TestLogElement")
    pop = s.stereotyped(st)
    bad = [f"{s.qn(e)} is a {e.kind}" for e in pop if e.kind == UTP_NOT_APPLIED.get(st)]
    return Outcome(len(pop), bad, f"«{st}» must not be applied to {UTP_NOT_APPLIED.get(st)}")


@check("utp_activity_node_kind")
def _utp_activity_node_kind(s: Scope, r: Rule) -> Outcome:
    st = _subject(r, "Alternative")
    pop = [e for e in s.stereotyped(st) if e.kind != "CombinedFragment"]
    bad = [f"{s.qn(e)} is a {e.kind}" for e in pop if e.kind != UTP_NODE_KIND[st]]
    return Outcome(len(pop), bad, f"in activities «{st}» is only allowed on {UTP_NODE_KIND[st]}")


@check("utp_overrides_ends")
def _utp_overrides_ends(s: Scope, r: Rule) -> Outcome:
    pop = s.stereotyped("Overrides")
    bad = [
        s.qn(e)
        for e in pop
        if any(
            s.model.elements[t].kind != "InstanceSpecification"
            for k in ("client", "supplier")
            for t in e.refs.get(k, [])
            if t in s.model.elements
        )
    ]
    return Outcome(len(pop), bad, "«Overrides» ends must be InstanceSpecifications")


@check("utp_dataprovider_spec")
def _utp_dataprovider_spec(s: Scope, r: Rule) -> Outcome:
    pop = s.stereotyped("DataProvider")
    bad = []
    for e in pop:
        owns = any(c.has_stereotype("DataSpecification") for c in _children(s, e))
        refines = any(
            s.model.elements[t].has_stereotype("DataSpecification")
            for rel in _outgoing(s, e, "Refine")
            for t in rel.refs.get("supplier", [])
            if t in s.model.elements
        )
        if not (owns or refines):
            bad.append(s.qn(e))
    return Outcome(len(pop), bad, "«DataProvider» without an owned or refined «DataSpecification»")


def evaluate(scope: Scope, rules: Iterable[Rule]) -> list[RuleResult]:
    out = []
    for r in rules:
        fn = CHECKS.get(r.check)
        if fn is None:
            out.append(RuleResult(r, "not automatable", 0, 0, []))
            continue
        o = fn(scope, r)
        status = "n.a." if o.checked == 0 else ("fail" if o.offenders else "pass")
        out.append(RuleResult(r, status, o.checked, len(o.offenders), o.offenders[:EXAMPLE_LIMIT], o.detail))
    return out


# --------------------------------------------------------------------------- completeness
@dataclass
class Completeness:
    projects: dict[str, int]
    scope: list[str]
    missing_projects: list[str]
    dangling: list[str]
    dangling_count: int
    library_ref_count: int

    def as_dict(self) -> dict:
        return asdict(self)


def completeness(scope: Scope) -> Completeness:
    m = scope.model
    findings = queries.health_check(m)
    dangling = [f for f in findings if f.check == "dangling-ref"]
    lib = sum(1 for f in findings if f.check == "library-ref")
    ex = [f"{m.qualified_name(f.element.id) if f.element else '-'}: {f.detail}" for f in dangling[:EXAMPLE_LIMIT]]
    return Completeness(dict(m.projects), sorted(scope.projects), list(m.missing_projects), ex, len(dangling), lib)


# --------------------------------------------------------------------------- reports
def _short(text: str, n: int = 160) -> str:
    text = text.replace("|", "\\|").replace("\n", " ")
    return text if len(text) <= n else text[: n - 1] + "…"


def rules_markdown(rules: list[Rule]) -> str:
    lines = ["# Reference rules", ""]
    lines.append(
        f"{len(rules)} rules extracted; {sum(r.automatable for r in rules)} executable, "
        f"{sum(not r.automatable for r in rules)} not automatable."
    )
    lines.append(
        "Text is quoted from the reference model element named in *Source element*; "
        "lines marked `[observed in exemplar]` describe the exemplar's own structure."
    )
    for source in dict.fromkeys(r.source for r in rules):
        sub = [r for r in rules if r.source == source]
        lines += ["", f"## {source} ({len(sub)} rules, {sum(r.automatable for r in sub)} executable)", ""]
        lines.append("| Rule | Automatable | Severity | Family | Source element | Text |")
        lines.append("|---|---|---|---|---|---|")
        for r in sub:
            auto = f"yes (`{r.check}`)" if r.automatable else "no"
            lines.append(f"| {r.id} | {auto} | {r.severity} | {r.family} | `{_short(r.element, 90)}` | {_short(r.text, 600)} |")
    return "\n".join(lines) + "\n"


def rules_text(rules: list[Rule]) -> str:
    out = []
    for r in rules:
        flag = f"executable ({r.check})" if r.automatable else "not automatable"
        out.append(f"{r.id:8} [{r.severity:5}] {flag}\n         source: {r.source} :: {r.element}\n         {r.text}")
    out.append(f"\n{len(rules)} rules, {sum(r.automatable for r in rules)} executable")
    return "\n".join(out)


def conformance_report(model: Model, results: list[RuleResult], comp: Completeness, references: list[str]) -> dict:
    counts = Counter(r.status for r in results)
    return {
        "delivery": {"root": model.name, "elements": len(model.elements), "projects": comp.projects, "scope": comp.scope},
        "references": references,
        "summary": {
            "rules": len(results),
            "executable": sum(r.rule.automatable for r in results),
            "pass": counts.get("pass", 0),
            "fail": counts.get("fail", 0),
            "n.a.": counts.get("n.a.", 0),
            "not_automatable": counts.get("not automatable", 0),
            "fail_by_severity": dict(Counter(r.rule.severity for r in results if r.status == "fail")),
        },
        "completeness": comp.as_dict(),
        "results": [r.as_dict() for r in results],
    }


def conformance_markdown(rep: dict) -> str:
    s, c, d = rep["summary"], rep["completeness"], rep["delivery"]
    lines = [f"# Conformance of `{d['root']}` against the reference layer", ""]
    lines.append(f"Delivery scope: {', '.join(d['scope'])} ({d['elements']} elements loaded across {len(d['projects'])} projects).")
    lines.append(f"Reference models: {', '.join(rep['references'])}.")
    lines += ["", "## Summary", ""]
    lines.append(
        f"- {s['rules']} rules, {s['executable']} executable: **{s['pass']} pass**, **{s['fail']} fail**, "
        f"{s['n.a.']} n.a. (nothing in the delivery to check); {s['not_automatable']} not automatable"
    )
    if s["fail_by_severity"]:
        lines.append("- failures by severity: " + ", ".join(f"{k} {v}" for k, v in sorted(s["fail_by_severity"].items())))
    lines += ["", "## Delivery completeness", ""]
    lines.append("| Project | Elements | In scope |")
    lines.append("|---|---|---|")
    for p, n in c["projects"].items():
        lines.append(f"| {p} | {n} | {'yes' if p in c['scope'] else 'reference / mounted'} |")
    for miss in c["missing_projects"]:
        lines.append(f"| {miss} | — | **MISSING** (mounted but not on disk) |")
    lines.append("")
    lines.append(
        f"- **{c['dangling_count']} dangling references** (`health` dangling-ref: unresolved refs into unloaded/missing "
        "projects or broken ids) — counted as delivery-completeness warnings"
    )
    lines.append(
        f"- {c['library_ref_count']} references into Cameo-bundled profiles / OMG spec XMI (library-ref, informational, not counted)"
    )
    for ex in c["dangling"]:
        lines.append(f"  - {ex}")
    for status, title in (
        ("fail", "Failed rules"),
        ("pass", "Passed rules"),
        ("n.a.", "Not applicable (nothing in the delivery to check)"),
    ):
        rows = [r for r in rep["results"] if r["status"] == status]
        if not rows:
            continue
        lines += ["", f"## {title} ({len(rows)})", ""]
        lines.append("| Rule | Severity | Checked | Failed | Source | Text |")
        lines.append("|---|---|---|---|---|---|")
        for r in rows:
            lines.append(
                f"| {r['id']} | {r['severity']} | {r['checked']} | {r['failed']} | {_short(r['source'], 40)} | {_short(r['text'], 140)} |"
            )
        if status == "fail":
            lines.append("")
            for r in rows:
                lines.append(f"**{r['id']}** — {_short(r['text'], 200)}  ")
                lines.append(f"source: `{r['element']}`; {r['detail']}  ")
                for ex in r["examples"]:
                    lines.append(f"- {ex}")
                if r["failed"] > len(r["examples"]):
                    lines.append(f"- … {r['failed'] - len(r['examples'])} more")
                lines.append("")
    rows = [r for r in rep["results"] if r["status"] == "not automatable"]
    if rows:
        lines += [
            "",
            f"## Not automatable ({len(rows)})",
            "",
            "Listed with their text in `reference_rules.md`; ids: " + ", ".join(r["id"] for r in rows),
        ]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- cross-org linking
@dataclass
class Reference:
    name: str
    model: Model
    candidates: list[Element]


MISSION_STEREOTYPES = (
    "MissionEngineeringThread",
    "MissionThread",
    "Mission",
    "MissionTask",
    "MissionPhase",
    "OperationalActivity",
    "Function",
    "Capability",
    "MeasurementSet",
    "Measurement",
    "TestProcedure",
    "TestCase",
    "TestSet",
    "TestContext",
    "TestObjective",
    "OperationalPerformer",
    "ResourceInformation",
    "OperationalInformation",
)


def _view(model: Model, name: str, elems: Iterable[Element]) -> Model:
    """A Model exposing only `elems` as match candidates while keeping owners/children resolvable."""
    v = Model(name, model.source)
    elems = list(elems)
    for e in elems:
        v.add(e)
    for e in elems:
        for o in model.owner_chain(e.id):
            v.elements.setdefault(o.id, o)
        for c in e.children:
            if c in model.elements:
                v.elements.setdefault(c, model.elements[c])
    return v


def delivery_candidates(scope: Scope) -> list[Element]:
    """Mission-level content: top-level behaviours, use cases, UTP test artefacts, test-data items, shallow packages."""
    m = scope.model
    out: list[Element] = []
    for e in scope.elements:
        if not e.name or e.name.endswith("_shared"):
            continue
        owner = m.elements.get(e.owner or "")
        if e.kind == "Activity" and (owner is None or owner.kind != "Activity"):
            out.append(e)
        elif e.kind == "UseCase":
            out.append(e)
        elif e.kind == "Class" and e.has_stereotype(
            "ResourceInformation", "OperationalInformation", "TestObjective", "TestConfiguration", "TestContext"
        ):
            out.append(e)
        elif e.kind == "Package" and not e.has_stereotype(*NOISE) and sum(1 for o in m.owner_chain(e.id) if o.kind == "Package") <= 1:
            out.append(e)
    return out


def reference_candidates(m: Model, kind: str) -> list[Element]:
    if kind == "ujtl":
        pool = m.with_stereotype("OperationalActivity")
    elif kind == "mission-meta-model":
        pool = [e for e in m.of_type("Class", "Activity", "Stereotype", "DataType", "Enumeration") if not e.name.startswith("base_")]
    else:
        pool = m.with_stereotype(*MISSION_STEREOTYPES)
    return [e for e in pool if len(link.tokens(e.name)) >= 2]


def project_view(m: Model, project: str) -> Model:
    """A standalone Model for one project of a federation (shares Element objects, own incoming index)."""
    v = Model(project, m.source)
    for e in m.elements.values():
        if e.project == project:
            v.add(e)
    v.finalize()
    return v


HIGH, MEDIUM, MIN_CONFIDENCE = 0.55, 0.45, 0.35


def confidence_label(c: float) -> str:
    """link.match scores are a shared-term ratio (identical names ~1.0); across organisations most
    genuine correspondences share only part of their vocabulary, hence the lower bands."""
    return "high" if c >= HIGH else "medium" if c >= MEDIUM else "low"


def _ujtl_detail(m: Model, oa: Element) -> str:
    ident = oa.tag("identifier") or ""
    ms = m.elements.get(oa.tag("measurementSet") or "")
    measures = [p for p in (m.elements[c] for c in ms.children if c in m.elements) if p.kind == "Property"] if ms else []
    head = ", ".join(f"{p.name} ({m.type_name_of(p)}): {clean(p.doc)[:60]}" for p in measures[:3])
    return f"{ident}; {len(measures)} measures" + (f" e.g. {head}" if head else "")


def cross_link(
    scope: Scope, refs: list[Reference], min_confidence: float = MIN_CONFIDENCE, per_element: int = 3
) -> dict[str, list[link.Link]]:
    """Proposed links from delivery mission-level content to each reference, via link.match on filtered views."""
    a_cands = [e for e in delivery_candidates(scope) if len(link.tokens(e.name)) >= 2]
    va = _view(scope.model, scope.model.name, a_cands)
    out: dict[str, list[link.Link]] = {}
    for ref in refs:
        vb = _view(ref.model, ref.name, ref.candidates)
        kinds = tuple(sorted({e.kind for e in a_cands} | {e.kind for e in ref.candidates}))
        links = link.match(va, vb, min_confidence, kinds)
        kept: list[link.Link] = []
        seen: Counter[str] = Counter()
        pairs: set[tuple[str, str]] = set()
        for l in links:
            if (l.a.id, l.b.id) in pairs:
                continue
            pairs.add((l.a.id, l.b.id))
            if seen[l.a.id] < per_element:
                kept.append(l)
                seen[l.a.id] += 1
        out[ref.name] = kept
    return out


def links_report(scope: Scope, refs: list[Reference], links: dict[str, list[link.Link]], limit: int = 200) -> dict:
    m = scope.model
    rep: dict = {
        "delivery": m.name,
        "note": (
            "Heuristic proposals produced by link.match (name-token / synonym matching); not model facts. "
            f"Confidence is the shared-term ratio: high >= {HIGH}, medium >= {MEDIUM}, low >= {MIN_CONFIDENCE}."
        ),
        "references": {},
    }
    for ref in refs:
        ls = links.get(ref.name, [])
        rows = []
        for l in ls[:limit]:
            d = l.as_dict(m, ref.model)
            d["label"] = confidence_label(l.confidence)
            if ref.name.lower().startswith("ujtl") or l.b.tag("identifier"):
                d["b_detail"] = _ujtl_detail(ref.model, l.b)
            rows.append(d)
        rep["references"][ref.name] = {
            "candidates_a": len(delivery_candidates(scope)),
            "candidates_b": len(ref.candidates),
            "links": len(ls),
            "high": sum(1 for l in ls if l.confidence >= HIGH),
            "with_disagreements": sum(1 for l in ls if l.disagreements),
            "shown": len(rows),
            "proposals": rows,
        }
    return rep


def links_markdown(rep: dict, impact_text: list[str] | None = None, impact_file: str = "") -> str:
    lines = [f"# Proposed links: `{rep['delivery']}` ↔ reference layer", "", f"> {rep['note']}", ""]
    for name, r in rep["references"].items():
        lines += [f"## {name}", ""]
        lines.append(
            f"{r['candidates_a']} delivery candidates × {r['candidates_b']} reference candidates → {r['links']} proposals "
            f"({r['high']} high confidence, {r['with_disagreements']} with disagreements); top {r['shown']} shown."
        )
        if not r["proposals"]:
            lines += [
                "",
                "No delivery element shares enough of its name with this reference's vocabulary to clear the threshold: "
                "the delivery does not use these concepts by name (see the conformance report for whether it applies "
                "them as stereotypes).",
                "",
            ]
            continue
        lines += ["", "| Conf | Delivery element | Reference element | Rationale | Disagreements |", "|---|---|---|---|---|"]
        for p in r["proposals"]:
            extra = f" — {p['b_detail']}" if p.get("b_detail") else ""
            lines.append(
                f"| {p['confidence']:.2f} {p['label']} | `{_short(p['a'], 80)}` [{_short(p['a_kind'], 30)}] | "
                f"`{_short(p['b'], 80)}` [{_short(p['b_kind'], 30)}]{_short(extra, 160)} | "
                f"{_short('; '.join(p['rationale']), 120)} | {_short('; '.join(p['disagreements']), 160)} |"
            )
        lines.append("")
    if impact_text:
        lines += ["## Impact walk-through", "", f"Mermaid graph: `{impact_file}`" if impact_file else "", "```", *impact_text, "```", ""]
    return "\n".join(lines)


def _flip(links: list[link.Link]) -> list[link.Link]:
    return [link.Link(l.b, l.a, l.confidence, l.rationale, l.disagreements) for l in links]


def pick_impact_start(scope: Scope, ref: Reference, links: list[link.Link], depth: int = 3) -> Element | None:
    """Reference element to "change" for the impact graph: the measure / measure set whose impact crosses into the
    delivery with the best-supported links, preferring specific measures (small local blast radius) over hubs;
    failing that, the reference element best linked to a delivery test procedure."""
    procs = {e.id for e in scope.stereotyped("TestProcedure")}
    flipped = _flip(links)
    best: Element | None = None
    best_score = 0.0
    for ms in ref.model.with_stereotype("MeasurementSet", "Measurement"):
        if not ms.name:
            continue
        res = link.cross_impact(ref.model, scope.model, ms, flipped, depth)
        support = sum(l.confidence + (1.0 if l.b.id in procs else 0.0) for l in res["links"] if l.confidence >= MEDIUM)
        score = support / (1 + len(res["local"]) / 25)
        if score > best_score:
            best, best_score = ms, score
    if best is None:
        direct = [l for l in links if l.a.id in procs]
        best = max(direct, key=lambda l: l.confidence).b if direct else None
    return best


def impact_from_reference(scope: Scope, ref: Reference, links: list[link.Link], start: Element, depth: int = 3) -> dict:
    """What in the delivery is hit if `start` (a reference element) changes: link.cross_impact with links flipped."""
    return link.cross_impact(ref.model, scope.model, start, _flip(links), depth)


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
