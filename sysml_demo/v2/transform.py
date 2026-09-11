"""SysML v1 (Cameo XMI) -> SysML v2 textual notation.

Follows the mapping in the OMG SysML v2 release document
`2b-SysML_v1_to_v2_Transformation` where one exists, and records a MapRecord for every
source element so the gap report can say exactly what happened to each construct:

  clean        semantics preserved in the v2 text
  lossy        emitted, but some information dropped or approximated (recorded in note)
  decision     emitted with a placeholder / partial form; a human must choose the final v2 form
  unsupported  no v2 equivalent (or tool-specific); not emitted, listed in the report
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field

from ..ingest import strip_html
from ..model import Element, Model
from .profile import ProfileIndex

CLEAN, LOSSY, DECISION, UNSUPPORTED = "clean", "lossy", "decision", "unsupported"
SEVERITY = {CLEAN: 0, LOSSY: 1, DECISION: 2, UNSUPPORTED: 3}

V2_KEYWORDS = {
    "about",
    "abstract",
    "accept",
    "action",
    "actor",
    "after",
    "alias",
    "all",
    "allocate",
    "allocation",
    "analysis",
    "and",
    "as",
    "assert",
    "assign",
    "assume",
    "at",
    "attribute",
    "bind",
    "binding",
    "by",
    "calc",
    "case",
    "comment",
    "concern",
    "connect",
    "connection",
    "constraint",
    "decide",
    "def",
    "default",
    "defined",
    "dependency",
    "derived",
    "do",
    "doc",
    "else",
    "end",
    "entry",
    "enum",
    "event",
    "exhibit",
    "exit",
    "expose",
    "false",
    "filter",
    "first",
    "flow",
    "for",
    "fork",
    "frame",
    "from",
    "hastype",
    "if",
    "implies",
    "import",
    "in",
    "include",
    "individual",
    "inout",
    "interface",
    "istype",
    "item",
    "join",
    "language",
    "library",
    "locale",
    "loop",
    "merge",
    "message",
    "meta",
    "metadata",
    "nonunique",
    "not",
    "null",
    "objective",
    "occurrence",
    "of",
    "or",
    "ordered",
    "out",
    "package",
    "parallel",
    "part",
    "perform",
    "port",
    "private",
    "protected",
    "public",
    "readonly",
    "redefines",
    "ref",
    "references",
    "render",
    "rendering",
    "rep",
    "require",
    "requirement",
    "return",
    "satisfy",
    "send",
    "snapshot",
    "specializes",
    "stakeholder",
    "standard",
    "state",
    "subject",
    "subsets",
    "succession",
    "then",
    "timeslice",
    "to",
    "transition",
    "true",
    "until",
    "use",
    "variant",
    "variation",
    "verification",
    "verify",
    "via",
    "view",
    "viewpoint",
    "when",
    "while",
    "xor",
}
SIMPLE_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
SCALAR_TYPES = {
    "Real": "ScalarValues::Real",
    "Integer": "ScalarValues::Integer",
    "String": "ScalarValues::String",
    "Boolean": "ScalarValues::Boolean",
    "Number": "ScalarValues::Number",
    "Complex": "ScalarValues::Complex",
    "UnlimitedNatural": "ScalarValues::Natural",
    "Natural": "ScalarValues::Natural",
}
NOISE = {
    "HyperlinkOwner",
    "NumberOwner",
    "Customization",
    "auxiliaryResource",
    "CustomImageHolder",
    "Legend",
    "LegendItem",
    "propertyGroup",
    "derivedPropertySpecification",
    "derivedPropertiesSuite",
    "validationRule",
    "PartProperty",
    "ValueProperty",
    "ReferenceProperty",
    "SharedProperty",
    "ConstraintProperty",
}
TOOL_SPECIFIC_PACKAGES = {"Derived Properties", "CSRM Extentions", "Unit Imports"}
RELATIONSHIP_KINDS = {
    "Abstraction",
    "Dependency",
    "Realization",
    "Usage",
    "InformationFlow",
    "Connector",
    "Association",
    "Generalization",
    "ElementImport",
    "PackageImport",
    "ProfileApplication",
    "Extension",
    "ObjectFlow",
    "ControlFlow",
    "Transition",
}


@dataclass
class MapRecord:
    element_id: str
    element_name: str
    qualified_name: str
    v1_construct: str
    v2_construct: str
    status: str
    note: str = ""


@dataclass
class TransformResult:
    profile_text: str
    model_text: str
    records: list[MapRecord] = field(default_factory=list)
    metadata_defs: dict[str, list[str]] = field(default_factory=dict)  # stereotype -> tag names

    @property
    def cells(self) -> list[str]:
        return [self.profile_text, self.model_text]

    def by_construct(self) -> dict[str, Counter]:
        out: dict[str, Counter] = defaultdict(Counter)
        for r in self.records:
            out[r.v1_construct][r.status] += 1
        return out


def v2string(value: str) -> str:
    """KerML string literal."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\r", "").replace("\n", "\\n") + '"'


def v2name(name: str) -> str:
    name = name.strip()
    if not name:
        return "''"
    if SIMPLE_NAME.match(name) and name not in V2_KEYWORDS:
        return name
    return "'" + name.replace("\\", "\\\\").replace("'", "\\'") + "'"


def v2doc(text: str, indent: str) -> list[str]:
    text = strip_html(text).replace("*/", "* /")
    if not text:
        return []
    return [f"{indent}doc /* {text} */"]


class Transformer:
    def __init__(self, model: Model, profile: ProfileIndex | None = None, subset_root: str | None = None):
        self.m = model
        self.profile = profile or ProfileIndex()
        self.records: list[MapRecord] = []
        self.metadata_defs: dict[str, list[str]] = {}
        self.emitted: set[str] = set()
        self.subset_root = subset_root
        self._local_names: dict[str, dict[str, str]] = defaultdict(dict)  # owner -> name -> id
        self._v2_names: dict[str, str] = {}
        self._deferred: list[Element] = []
        self.scope: set[str] | None = None
        self.referenced: set[str] = set()
        self._by_id: dict[str, MapRecord] = {}
        self._tag_values: dict[str, list[tuple[str, dict[str, str]]]] = defaultdict(list)
        self._pending: dict[str, list[tuple[str, str]]] = defaultdict(list)  # element -> [(status, note)] before its record exists

    # ------------------------------------------------------------------ public
    def run(self) -> TransformResult:
        lines: list[str] = []
        if self.subset_root:
            self._run_subset(lines)
        else:
            for r in self._roots():
                self._emit_namespace(r, lines, "")
            self._emit_model_root_members(lines)
            self._emit_deferred_relationships(lines)
        self._record_unsupported_leftovers()
        for eid in list(self._tag_values):
            for name, values in self._tag_values.pop(eid):
                self.loss(self.m.elements[eid], LOSSY, f"<<{name}>> tag values {sorted(values)} dropped: v2 construct has no body")
        for eid in list(self._pending):
            losses = self._pending.pop(eid)
            el = self.m.elements[eid]
            self.rec(el, el.kind, "-", *losses[0])
            for status, note in losses[1:]:
                self.loss(el, status, note)
        profile_lines = self._profile_package()
        return TransformResult("\n".join(profile_lines), "\n".join(lines), self.records, self.metadata_defs)

    def _run_subset(self, lines: list[str]) -> None:
        """Emit one element (package or block) with its contents, wrapped in its owning package path,
        plus declaration-only stubs for everything outside the subset that it references."""
        root = self._find_subset_root()
        self.scope = {root.id} | {d.id for d in self.m.descendants(root.id)}
        body: list[str] = []
        self._emit_member(root, body, "")
        rel_lines: list[str] = []
        for rel in self._deferred:
            self._emit_relationship(rel, rel_lines, "")
        stubs = [self.m.elements[i] for i in sorted(self.referenced) if i not in self.scope and i in self.m.elements]
        tree: dict[str, dict] = {}
        self._tree_insert(tree, root, body)
        for s in stubs:
            self._tree_insert(tree, s, self._stub_lines(s))
        self._tree_emit(tree, lines, "", top=True)
        if rel_lines:
            lines.append(f"package {v2name(self.m.name + ' Relationships')} {{")
            lines.append(f"    private import {v2name(self.m.name + ' Profile')}::*;")
            lines.append("    private import RequirementDerivation::*;")
            lines.extend("    " + ln for ln in rel_lines)
            lines.append("}")

    def _find_subset_root(self) -> Element:
        hits = [e for e in self.m.by_name(self.subset_root or "") if e.kind in ("Package", "Class")]
        if not hits:
            hits = [e for e in self.m.search(self.subset_root or "", ("Package", "Class"))]
        if not hits:
            raise KeyError(f"no package or block named {self.subset_root!r}")
        hits.sort(key=lambda e: (e.kind != "Package", len(e.name)))
        return hits[0]

    def _tree_insert(self, tree: dict[str, dict], el: Element, body: list[str]) -> None:
        chain = [a for a in reversed(self.m.owner_chain(el.id)) if a.kind != "Model"]
        node = tree
        for a in chain:
            node = node.setdefault(a.id, {"el": a, "children": {}, "body": []})["children"]
        node.setdefault(el.id, {"el": el, "children": {}, "body": []})["body"] = body

    def _tree_emit(self, tree: dict[str, dict], lines: list[str], ind: str, top: bool = False) -> None:
        for node in tree.values():
            el, body, children = node["el"], node["body"], node["children"]
            if body and not children:
                lines.extend(ind + ln for ln in body)
                continue
            kw = "package" if el.kind in ("Package", "Profile") else "part def"
            lines.append(f"{ind}{kw} {v2name(self.unique_name(el))} {{")
            if top:
                lines.append(f"{ind}    private import {v2name(self.m.name + ' Profile')}::*;")
                lines.append(f"{ind}    private import RequirementDerivation::*;")
            if body:  # container that is itself in the subset: its body already includes the children
                lines.extend(ind + "    " + ln for ln in body)
            self._tree_emit(children, lines, ind + "    ")
            lines.append(f"{ind}}}")

    def _stub_lines(self, el: Element) -> list[str]:
        st, root = self.primary(el)
        kw = {
            "Requirement": "requirement",
            "ValueType": "attribute def",
            "InterfaceBlock": "port def",
            "FlowSpecification": "port def",
            "ConstraintBlock": "constraint def",
        }.get(root, "part def")
        if el.kind in ("DataType", "PrimitiveType", "Enumeration"):
            kw = "attribute def"
        elif el.kind == "Package":
            kw = "package"
        elif el.kind in ("Property", "Port"):
            kw = "ref"
        self.rec(el, st or el.kind, f"{kw} (stub)", CLEAN, "outside the requested subset; declaration-only stub so references resolve")
        return [f"{kw} {v2name(self.unique_name(el))};"]

    # ------------------------------------------------------------------ helpers
    def _roots(self) -> list[Element]:
        roots: list[Element] = []
        for mdl in self._model_roots():
            roots.extend(
                self.m.elements[c] for c in mdl.children if self.m.elements[c].kind in ("Package", "Profile") and self.m.elements[c].name
            )
        return roots

    def _model_roots(self) -> list[Element]:
        """Innermost uml:Model elements (MagicDraw sometimes wraps the model in a 'Data' model)."""
        return [mdl for mdl in self.m.of_type("Model") if not any(self.m.elements[c].kind == "Model" for c in mdl.children)]

    def _emit_model_root_members(self, lines: list[str]) -> None:
        """Elements owned directly by the uml:Model (use cases, comments, library imports)."""
        loose: list[str] = []
        for mdl in self._model_roots():
            for cid in mdl.children:
                el = self.m.elements[cid]
                if el.kind in ("Package", "Profile") and el.name:
                    continue
                self._emit_member(el, loose, "    ")
        if loose:
            lines.append(f"package {v2name(self.m.name + ' Root')} {{")
            lines.append(f"    private import {v2name(self.m.name + ' Profile')}::*;")
            lines.extend(loose)
            lines.append("}")

    def rec(self, el: Element, v1: str, v2: str, status: str, note: str = "") -> None:
        """One record per source element; losses noted earlier by helpers are folded in."""
        self.emitted.add(el.id)
        r = MapRecord(el.id, el.name, self.m.qualified_name(el.id), v1, v2, status, note)
        self.records.append(r)
        self._by_id[el.id] = r
        for s, n in self._pending.pop(el.id, []):
            self.loss(el, s, n)

    def loss(self, el: Element, status: str, note: str) -> None:
        """Attach a partial loss to the element's record, promoting its status to the worse of the two."""
        r = self._by_id.get(el.id)
        if r is None:
            self._pending[el.id].append((status, note))
            return
        if SEVERITY[status] > SEVERITY[r.status]:
            r.status = status
        r.note = f"{r.note}; {note}" if r.note else note

    def stereo(self, el: Element) -> list[str]:
        return [s.name for s in el.stereotypes if s.name not in NOISE]

    def primary(self, el: Element) -> tuple[str, str]:
        """(primary stereotype name, resolved SysML root) for a classifier."""
        names = self.stereo(el)
        for n in names:
            root = self.profile.root_of(n)
            if root:
                return n, root
        return (names[0], "") if names else ("", "")

    def custom(self, name: str) -> bool:
        """True if the stereotype is from a user profile (not SysML / MagicDraw built-in)."""
        info = self.profile.stereotypes.get(name)
        return info is not None

    def metadata_prefix(self, el: Element, skip: tuple[str, ...] = ()) -> str:
        """`#Stereotype` prefix for custom stereotypes. Applications that carry tag values cannot
        use the prefix form; they are parked for `metadata_body` (emitted as `@Stereotype { tag = ...; }`
        inside the element). `skip` names tags already carried by the v2 construct (e.g. requirement Id/Text)."""
        out = []
        for s in el.stereotypes:
            if s.name in NOISE or not self.custom(s.name):
                continue
            self.metadata_defs.setdefault(s.name, sorted(s.tags))
            values = {t: v for t, v in s.tags.items() if t not in skip and v}
            if values:
                self._tag_values[el.id].append((s.name, values))
            else:
                out.append(f"#{v2name(s.name)}")
        return (" ".join(out) + " ") if out else ""

    def metadata_body(self, el: Element, ind: str) -> list[str]:
        """`@Stereotype { tag = "value"; }` members for the applications parked by `metadata_prefix`."""
        out = []
        for name, values in self._tag_values.pop(el.id, []):
            body = " ".join(f"{v2name(t)} = {v2string(v)};" for t, v in sorted(values.items()))
            out.append(f"{ind}@{v2name(name)} {{ {body} }}")
        return out

    def _decl(self, el: Element, lines: list[str], ind: str, head: str, body: list[str] | None = None) -> None:
        """Emit `head;` or, when there is a body (features, docs, metadata values), `head { ... }`."""
        inner = ind + "    "
        body = (body or []) + self.metadata_body(el, inner)
        if body:
            lines.append(f"{ind}{head} {{")
            lines.extend(body)
            lines.append(f"{ind}}}")
        else:
            lines.append(f"{ind}{head};")

    def unique_name(self, el: Element) -> str:
        """v2 name unique among siblings (v1 allows same-named siblings via different metaclasses)."""
        if el.id in self._v2_names:
            return self._v2_names[el.id]
        owner = el.owner or ""
        base = el.name or f"{el.kind}_{len(self._local_names[owner]) + 1}"
        name, n = base, 2
        while name in self._local_names[owner] and self._local_names[owner][name] != el.id:
            name = f"{base}_{n}"
            n += 1
        if name != base:
            self.loss(el, LOSSY, f"sibling name clash; emitted as {name!r}")
        self._local_names[owner][name] = el.id
        self._v2_names[el.id] = name
        return name

    def qname(self, el: Element) -> str:
        parts = []
        cur: Element | None = el
        top = el
        while cur is not None and cur.kind != "Model":
            parts.append(v2name(self.unique_name(cur)))
            top = cur
            cur = self.m.elements.get(cur.owner) if cur.owner else None
        if not (top.kind in ("Package", "Profile") and top.name and parts):
            parts.append(v2name(self.m.name + " Root"))
        return "::".join(reversed(parts))

    def ref(self, target_id: str | None) -> str | None:
        if target_id is None:
            return None
        t = self.m.elements.get(target_id)
        if t is None:
            return None
        self.referenced.add(t.id)
        return self.qname(t)

    def mult(self, prop: Element) -> str:
        lo = hi = None
        for cid in prop.children:
            c = self.m.elements[cid]
            if c.role == "lowerValue":
                lo = c.attrs.get("value", "0")
            elif c.role == "upperValue":
                hi = c.attrs.get("value", "1")
        if lo is None and hi is None:
            return ""
        if not all(x is None or x.lstrip("-").isdigit() or x == "*" for x in (lo, hi)):
            self.loss(prop, LOSSY, f"multiplicity expression {lo!r}..{hi!r} dropped; use a v2 calc/constraint")
            return ""
        lo = lo or "0"
        hi = "*" if hi in ("*", "-1") else (hi or lo)
        return f"[{lo}]" if lo == hi else f"[{lo}..{hi}]"

    # ------------------------------------------------------------------ emitters
    def _emit_namespace(self, pkg: Element, lines: list[str], ind: str) -> None:
        if pkg.name in TOOL_SPECIFIC_PACKAGES:
            self.rec(
                pkg,
                "Package (tool customisation)",
                "-",
                UNSUPPORTED,
                "MagicDraw derived-property / DSL customisation / unit-import package: re-create with v2 libraries (ISQ, SI) or drop",
            )
            for d in self.m.descendants(pkg.id):
                self.emitted.add(d.id)
            return
        self.rec(pkg, pkg.kind, "package", CLEAN)
        lines.append(f"{ind}{self.metadata_prefix(pkg)}package {v2name(self.unique_name(pkg))} {{")
        inner = ind + "    "
        lines.extend(self.metadata_body(pkg, inner))
        if ind == "":
            lines.append(f"{inner}private import {v2name(self.m.name + ' Profile')}::*;")
            lines.append(f"{inner}private import RequirementDerivation::*;")
        lines.extend(v2doc(pkg.doc, inner))
        for cid in pkg.children:
            self._emit_member(self.m.elements[cid], lines, inner)
        lines.append(f"{ind}}}")

    def _emit_member(self, el: Element, lines: list[str], ind: str) -> None:
        k = el.kind
        if k in ("Package", "Profile"):
            self._emit_namespace(el, lines, ind)
        elif k == "Model":
            self.emitted.add(el.id)
        elif k == "Class":
            self._emit_class(el, lines, ind)
        elif k == "Comment":
            self._emit_comment(el, lines, ind)
        elif k == "Activity":
            self._emit_activity(el, lines, ind)
        elif k == "UseCase":
            self.rec(el, "UseCase", "use case def", CLEAN)
            self._decl(el, lines, ind, f"{self.metadata_prefix(el)}use case def {v2name(self.unique_name(el))}")
        elif k == "Actor":
            self.rec(el, "Actor", "part def (actor)", CLEAN, "v2 actors are parts; role assigned per use case")
            lines.append(f"{ind}part def {v2name(self.unique_name(el))};")
        elif k == "Enumeration":
            self._emit_enum(el, lines, ind)
        elif k in ("DataType", "PrimitiveType"):
            self._emit_datatype(el, lines, ind)
        elif k == "Interface":
            self.rec(
                el,
                "Interface (UML)",
                "port def",
                DECISION,
                "UML interface with operations: v2 has no operations; port def with flows, or action defs, must be chosen",
            )
            lines.append(f"{ind}port def {v2name(self.unique_name(el))};")
        elif k == "Signal":
            self.rec(el, "Signal", "item def", DECISION, "v2 messages carry items/attributes; confirm payload typing")
            lines.append(f"{ind}item def {v2name(self.unique_name(el))};")
        elif k == "StateMachine":
            self._emit_statemachine(el, lines, ind)
        elif k == "InstanceSpecification":
            self.rec(el, "InstanceSpecification", "-", DECISION, "v2 has no instances; use individuals/snapshots or attribute defaults")
        elif k == "Constraint":
            self._emit_constraint(el, lines, ind)
        elif k in ("Abstraction", "Dependency", "Realization", "Usage"):
            self._deferred.append(el)
        elif k == "Association":
            self._emit_association(el, lines, ind)
        elif k == "InformationFlow":
            self._deferred.append(el)
        elif k in ("ElementImport", "PackageImport"):
            self._emit_import(el, lines, ind)
        elif k == "Diagram":
            self.rec(
                el,
                f"Diagram: {el.diagram_type or 'unknown'}",
                "-",
                UNSUPPORTED,
                "v2 has no diagram-layout interchange; views/viewpoints must be re-authored in the target tool",
            )
            for d in self.m.descendants(el.id):
                self.emitted.add(d.id)
        elif k in ("ProfileApplication", "Extension", "Stereotype", "Image"):
            self.rec(el, k, "-", UNSUPPORTED if k != "Stereotype" else "metadata def", "profile mechanics; see profile cell")
        elif k in ("Property", "Port", "Operation", "Generalization"):
            pass  # handled by the owning classifier
        else:
            self.rec(el, k, "-", UNSUPPORTED, "no mapping implemented")

    def _emit_class(self, el: Element, lines: list[str], ind: str) -> None:
        st, root = self.primary(el)
        prefix = self.metadata_prefix(el, skip=("Id", "Text") if root == "Requirement" else ())
        name = v2name(self.unique_name(el))
        gens = [
            g
            for g in (
                self.ref(gid)
                for c in el.children
                for gid in self.m.elements[c].refs.get("general", [])
                if self.m.elements[c].kind == "Generalization"
            )
            if g
        ]
        ext_gens = [
            self.m.external_name(gid)
            for c in el.children
            if self.m.elements[c].kind == "Generalization"
            for gid in self.m.elements[c].refs.get("general", [])
            if gid not in self.m.elements
        ]
        spec = (" :> " + ", ".join(gens)) if gens else ""
        label = f"{st} ({'custom' if self.custom(st) else 'SysML'})" if st else "Class (unstereotyped)"

        if root == "Requirement":
            rid = el.tag("Id")
            short = f"<{v2name(rid)}> " if rid else ""
            self.rec(
                el,
                label,
                "requirement usage" + (" + metadata" if self.custom(st) else ""),
                CLEAN if not ext_gens else LOSSY,
                "; ".join(f"generalization to external {g} dropped" for g in ext_gens),
            )
            lines.append(f"{ind}{prefix}requirement {short}{name}{spec} {{")
            body = ind + "    "
            lines.extend(v2doc(el.tag("Text") or "", body))
            lines.extend(v2doc(el.doc, body) if not el.tag("Text") else [])
            lines.extend(self.metadata_body(el, body))
            self._emit_features(el, lines, body)
            lines.append(f"{ind}}}")
            return

        if root == "ValueType":
            base = SCALAR_TYPES.get(ext_gens[0], "") if ext_gens else ""
            self.rec(
                el,
                label,
                "attribute def",
                CLEAN if base or gens else LOSSY,
                "" if base or gens else "unit/quantity kind not mapped; use ISQ library",
            )
            spec2 = spec or (f" :> {base}" if base else "")
            self._decl(el, lines, ind, f"{prefix}attribute def {name}{spec2}")
            return
        if root == "ConstraintBlock":
            self.rec(el, label, "constraint def", LOSSY, "constraint expression language differs (v1 opaque text vs KerML expressions)")
            lines.append(f"{ind}{prefix}constraint def {name}{spec} {{")
            lines.extend(self.metadata_body(el, ind + "    "))
            self._emit_features(el, lines, ind + "    ")
            lines.append(f"{ind}}}")
            return
        if root in ("InterfaceBlock", "FlowSpecification"):
            self.rec(el, label, "port def", CLEAN)
            lines.append(f"{ind}{prefix}port def {name}{spec} {{")
            lines.extend(self.metadata_body(el, ind + "    "))
            self._emit_features(el, lines, ind + "    ", in_port_def=True)
            lines.append(f"{ind}}}")
            return
        if root in ("View", "Viewpoint"):
            self.rec(
                el,
                label,
                f"{root.lower()} def",
                DECISION,
                "v2 views are query-based renderings; v1 view contents/diagram must be re-expressed",
            )
            self._decl(el, lines, ind, f"{root.lower()} def {name}")
            return
        if root == "Stakeholder":
            self.rec(
                el,
                label,
                "part def (stakeholder)",
                LOSSY,
                "transformation doc maps Stakeholder to ItemDefinition; concerns must be re-attached",
            )
            self._decl(el, lines, ind, f"{prefix}part def {name}{spec}")
            return
        if root == "TestCase":
            self.rec(el, label, "verification case def", CLEAN)
            self._decl(el, lines, ind, f"{prefix}verification def {name}")
            return
        if root == "Behavior":
            self.rec(
                el,
                label,
                "action def + metadata",
                DECISION,
                "behaviour stereotype applied to a class (not an activity): emitted as action def; confirm intent",
            )
            self._decl(el, lines, ind, f"{prefix}action def {name}{spec}")
            return

        # Block, custom block subtypes, and plain classes
        status = CLEAN if root == "Block" else DECISION
        note = "" if root == "Block" else "plain UML class: treated as part def; confirm it is structural"
        if ext_gens:
            patterns = [g for g in ext_gens if "pattern" in g.lower() or "rollup" in g.lower()]
            if patterns:
                status, note = (
                    DECISION,
                    (
                        f"specialises MagicDraw analysis pattern {patterns[0]}: tool-specific; "
                        "re-create as a v2 calc (e.g. total mass = sum of parts) or drop"
                    ),
                )
            else:
                status, note = LOSSY, "; ".join(f"generalization to external {g} dropped" for g in ext_gens)
        self.rec(el, label, "part def" + (" + metadata" if self.custom(st) else ""), status, note)
        lines.append(f"{ind}{prefix}part def {name}{spec} {{")
        body = ind + "    "
        lines.extend(v2doc(el.doc, body))
        lines.extend(self.metadata_body(el, body))
        self._emit_features(el, lines, body)
        lines.append(f"{ind}}}")

    def _emit_features(self, cls: Element, lines: list[str], ind: str, in_port_def: bool = False) -> None:
        for cid in cls.children:
            c = self.m.elements[cid]
            if c.kind == "Property":
                self._emit_property(c, lines, ind, in_port_def)
            elif c.kind == "Port":
                self._emit_port(c, lines, ind)
            elif c.kind == "Operation":
                params = [self.m.elements[p] for p in c.children if self.m.elements[p].kind == "Parameter"]
                self.rec(
                    c, "Operation", "action (nested)", DECISION, "v2 has no operations; emitted as nested action, calls must be re-modelled"
                )
                ps = " ".join(
                    f"{p.attrs.get('direction', 'in').replace('return', 'out')} {v2name(p.name or 'result')};" for p in params if p.name
                )
                kw = "ref action" if in_port_def else "action"
                lines.append(f"{ind}{kw} {v2name(self.unique_name(c))}{' { ' + ps + ' }' if ps else ';'}")
            elif c.kind == "Class":
                self._emit_class(c, lines, ind)
            elif c.kind == "Comment":
                self._emit_comment(c, lines, ind)
            elif c.kind == "Constraint":
                self._emit_constraint(c, lines, ind)
            elif c.kind == "Connector":
                self._emit_connector(c, lines, ind)
            elif c.kind in (
                "Activity",
                "StateMachine",
                "Enumeration",
                "DataType",
                "UseCase",
                "Package",
                "InformationFlow",
                "Abstraction",
                "Dependency",
                "Association",
            ):
                self._emit_member(c, lines, ind)
            elif c.kind == "Generalization":
                self.emitted.add(c.id)
            elif c.kind == "Diagram":
                self._emit_member(c, lines, ind)

    def _emit_property(self, p: Element, lines: list[str], ind: str, in_port_def: bool) -> None:
        typ = self.m.type_of(p)
        tname = self.m.type_name_of(p)
        st = self.stereo(p) + [
            s.name
            for s in p.stereotypes
            if s.name in ("PartProperty", "ValueProperty", "ReferenceProperty", "SharedProperty", "ConstraintProperty")
        ]
        prefix = self.metadata_prefix(p)
        name = v2name(self.unique_name(p)) + self._redefines(p)
        mult = self.mult(p)
        aggr = p.attrs.get("aggregation", "none")
        if "FlowProperty" in st or in_port_def:
            d = p.tag("direction") or "inout"
            t = self._type_ref(typ, tname)
            kw = "item" if typ is not None and typ.kind == "Class" and self.primary(typ)[1] != "ValueType" else "attribute"
            self.rec(p, "FlowProperty", f"{d} {kw}", CLEAN if t else LOSSY, "" if t else f"type {tname!r} unresolved")
            lines.append(f"{ind}{d} {kw} {name}{(' : ' + t) if t else ''}{mult};")
            return
        if "ConstraintProperty" in st:
            t = self.ref(typ.id) if typ else None
            self.rec(p, "ConstraintProperty", "constraint usage", CLEAN if t else LOSSY)
            lines.append(f"{ind}constraint {name}{(' : ' + t) if t else ''};")
            return
        if (
            typ is not None
            and typ.kind == "Class"
            and self.primary(typ)[1] not in ("ValueType", "")
            or (typ is not None and typ.kind == "Class" and self.primary(typ)[1] == "" and aggr == "composite")
        ):
            t = self.ref(typ.id)
            if aggr == "composite":
                self.rec(p, "PartProperty" if "PartProperty" in st else "Property (composite)", "part usage", CLEAN)
                self._decl(p, lines, ind, f"{prefix}part {name} : {t}{mult}")
            elif aggr == "shared":
                self.rec(p, "SharedProperty", "ref part", LOSSY, "shared aggregation semantics approximated by reference")
                self._decl(p, lines, ind, f"{prefix}ref part {name} : {t}{mult}")
            else:
                self.rec(p, "ReferenceProperty" if "ReferenceProperty" in st else "Property (reference)", "ref part", CLEAN)
                self._decl(p, lines, ind, f"{prefix}ref part {name} : {t}{mult}")
            return
        t = self._type_ref(typ, tname)
        default = self._default(p)
        if "ValueProperty" in st or t or typ is None:
            status = CLEAN if t or not tname else LOSSY
            note = "" if status == CLEAN else f"type {tname!r} not mapped to a v2 attribute def (unit / quantity kind)"
            if not tname:
                note = "untyped in the source model"
                status = CLEAN
            self.rec(p, "ValueProperty" if "ValueProperty" in st else "Property (value)", "attribute usage", status, note)
            self._decl(p, lines, ind, f"{prefix}attribute {name}{(' : ' + t) if t else ''}{mult}{default}")
            return
        self.rec(p, "Property", "ref", DECISION, f"typed by {typ.kind if typ else '?'}; choose part/attribute/ref")
        lines.append(f"{ind}ref {name}{mult};")

    def _redefines(self, p: Element) -> str:
        redefined = [self.m.elements.get(r) for r in p.refs.get("redefinedProperty", []) + p.refs.get("redefinedPort", [])]
        names = []
        for r in redefined:
            if r is None:
                continue
            rt = self.m.type_of(r)
            plain_class = rt is not None and rt.kind == "Class" and self.primary(rt)[1] == ""
            if rt is None or r.attrs.get("aggregation", "none") != p.attrs.get("aggregation", "none") or plain_class:
                self.loss(p, LOSSY, f"redefinition of {r.name!r} dropped: redefined feature has a different v2 kind")
                continue
            names.append(v2name(self.unique_name(r)))
        return (" :>> " + ", ".join(names)) if names else ""

    def _type_ref(self, typ: Element | None, tname: str) -> str | None:
        if typ is not None:
            if typ.kind in ("Class", "DataType", "PrimitiveType", "Enumeration"):
                return self.ref(typ.id)
            return None
        if tname in SCALAR_TYPES:
            return SCALAR_TYPES[tname]
        return None

    def _default(self, p: Element) -> str:
        for cid in p.children:
            c = self.m.elements[cid]
            if c.role == "defaultValue" and "value" in c.attrs:
                v = c.attrs["value"]
                if c.kind == "LiteralString":
                    return f' = "{v}"'
                if c.kind in ("LiteralReal", "LiteralInteger", "LiteralBoolean"):
                    return f" = {v}"
        return ""

    def _emit_port(self, p: Element, lines: list[str], ind: str) -> None:
        typ = self.m.type_of(p)
        st = self.stereo(p)
        conj = "~" if p.attrs.get("isConjugated") == "true" else ""
        t = self.ref(typ.id) if typ else None
        name = v2name(self.unique_name(p)) + self._redefines(p)
        if typ is not None and self.primary(typ)[1] == "Block":
            self.rec(
                p,
                "FullPort" if "FullPort" in st else "Port (block-typed)",
                "port usage",
                DECISION,
                "port typed by a Block: v2 ports are typed by port defs; convert the block to a port def or nest a part",
            )
        elif "ProxyPort" in st or typ is not None:
            self.rec(
                p, "ProxyPort" if "ProxyPort" in st else "Port", "port usage", CLEAN if t else LOSSY, "" if t else "port type unresolved"
            )
        else:
            self.rec(p, "Port (untyped)", "port usage", LOSSY, "no type; interface cannot be checked")
        lines.append(f"{ind}port {name}{(' : ' + conj + t) if t else ''}{self.mult(p)};")

    def _emit_connector(self, c: Element, lines: list[str], ind: str) -> None:
        ends: list[str | None] = []
        for eid in c.children:
            e = self.m.elements[eid]
            if e.kind != "ConnectorEnd":
                continue
            role = self.m.elements.get((e.refs.get("role") or [""])[0])
            pwp = self.m.elements.get((e.refs.get("partWithPort") or [""])[0])
            if role is None:
                ends.append(None)
                continue
            path = v2name(self.unique_name(role))
            if pwp is not None:
                path = f"{v2name(self.unique_name(pwp))}.{path}"
            ends.append(path)
        st = self.stereo(c)
        if len(ends) == 2 and all(ends):
            if "BindingConnector" in st:
                self.rec(c, "BindingConnector", "bind", CLEAN)
                lines.append(f"{ind}bind {ends[0]} = {ends[1]};")
            else:
                self.rec(c, "Connector", "connect", CLEAN)
                lines.append(f"{ind}connect {ends[0]} to {ends[1]};")
        else:
            self.rec(c, "Connector", "-", LOSSY, "connector end role could not be resolved")

    def _emit_comment(self, c: Element, lines: list[str], ind: str) -> None:
        body = strip_html(c.attrs.get("body", ""))
        if not body:
            self.emitted.add(c.id)
            return
        st = self.stereo(c)
        targets = c.refs.get("annotatedElement", [])
        label = f"Comment <<{st[0]}>>" if st else "Comment"
        if c.owner in targets or not targets:
            self.emitted.add(c.id)  # already folded into the owner's doc
            self.records.append(MapRecord(c.id, "", self.m.qualified_name(c.id), label, "doc", CLEAN))
            return
        refs = [r for r in (self.ref(t) for t in targets) if r]
        if not refs:
            self.rec(c, label, "comment", LOSSY, "annotated element not in this file")
            lines.append(f"{ind}comment /* {body.replace('*/', '* /')} */")
            return
        self.rec(c, label, "comment about", CLEAN if not st else LOSSY, f"<<{st[0]}>> stereotype on comment becomes metadata" if st else "")
        lines.append(f"{ind}{self.metadata_prefix(c)}comment about {', '.join(refs)} /* {body.replace('*/', '* /')} */")

    def _emit_constraint(self, c: Element, lines: list[str], ind: str) -> None:
        spec = ""
        for cid in c.children:
            s = self.m.elements[cid]
            if s.kind == "OpaqueExpression":
                spec = s.attrs.get("body", "")
        self.rec(
            c, "Constraint (opaque)", "constraint { doc }", LOSSY, "expression kept as text; must be rewritten in KerML expression language"
        )
        lines.append(f"{ind}constraint {v2name(self.unique_name(c))} {{")
        lines.extend(v2doc(spec or c.doc, ind + "    "))
        lines.append(f"{ind}}}")

    def _emit_activity(self, a: Element, lines: list[str], ind: str) -> None:
        params = [self.m.elements[c] for c in a.children if self.m.elements[c].kind == "Parameter"]
        nodes = [
            self.m.elements[c]
            for c in a.children
            if self.m.elements[c].kind.endswith(("Action", "Node")) and self.m.elements[c].kind != "ActivityParameterNode"
        ]
        edges = [self.m.elements[c] for c in a.children if self.m.elements[c].kind in ("ObjectFlow", "ControlFlow")]
        for desc in self.m.descendants(a.id):
            self.emitted.add(desc.id)
        st = self.stereo(a)
        label = f"Activity <<{st[0]}>>" if st else "Activity"
        v2 = "action def"
        if "VerificationActivity" in st:
            v2 = "verification def"
        elif "ValidationActivity" in st:
            v2 = "verification def (validation)"
        status = CLEAN if not nodes and not edges else LOSSY
        note = (
            f"{len(nodes)} action nodes and {len(edges)} flows not migrated (activity internals require manual re-modelling)"
            if status == LOSSY
            else ""
        )
        self.rec(a, label, v2, status, note)
        ps = []
        for p in params:
            d = p.attrs.get("direction", "in").replace("return", "out")
            tref = self._type_ref(self.m.type_of(p), self.m.type_name_of(p))
            ps.append(f"{d} {v2name(p.name or 'p')}{(' : ' + tref) if tref else ''}")
        kw = "verification def" if v2.startswith("verification") else "action def"
        prefix = self.metadata_prefix(a)
        self._decl(a, lines, ind, f"{prefix}{kw} {v2name(self.unique_name(a))}", [f"{ind}    {x};" for x in ps])

    def _emit_statemachine(self, sm: Element, lines: list[str], ind: str) -> None:
        states, transitions, pseudo = [], [], []
        for d in self.m.descendants(sm.id):
            self.emitted.add(d.id)
            if d.kind == "State":
                states.append(d)
            elif d.kind == "Transition":
                transitions.append(d)
            elif d.kind == "Pseudostate":
                pseudo.append(d)
        self.rec(
            sm,
            "StateMachine",
            "state def",
            LOSSY,
            f"{len(states)} states / {len(transitions)} transitions emitted; "
            f"triggers, guards, effects and {len(pseudo)} pseudostates dropped",
        )
        lines.append(f"{ind}state def {v2name(self.unique_name(sm))} {{")
        for s in states:
            lines.append(f"{ind}    state {v2name(self.unique_name(s))};")
        for t in transitions:
            src = self.m.elements.get((t.refs.get("source") or [""])[0])
            tgt = self.m.elements.get((t.refs.get("target") or [""])[0])
            if src and tgt and src.kind == "State" and tgt.kind == "State":
                lines.append(f"{ind}    transition {v2name(self.unique_name(src))} then {v2name(self.unique_name(tgt))};")
        lines.append(f"{ind}}}")

    def _emit_enum(self, e: Element, lines: list[str], ind: str) -> None:
        lits = [self.m.elements[c] for c in e.children if self.m.elements[c].kind == "EnumerationLiteral"]
        for l in lits:
            self.emitted.add(l.id)
        self.rec(e, "Enumeration", "enum def", CLEAN)
        lines.append(f"{ind}enum def {v2name(self.unique_name(e))} {{ " + " ".join(v2name(l.name) + ";" for l in lits) + " }")

    def _emit_datatype(self, d: Element, lines: list[str], ind: str) -> None:
        st, root = self.primary(d)
        gens = self.m.generals(d)
        base = next((SCALAR_TYPES[g] for g in gens if g in SCALAR_TYPES), "")
        self.rec(
            d,
            f"{st or d.kind}",
            "attribute def",
            CLEAN if base or not gens else LOSSY,
            "" if base or not gens else f"specialises {gens}: map to ISQ/SI",
        )
        props = [self.m.elements[c] for c in d.children if self.m.elements[c].kind == "Property"]
        head = f"{self.metadata_prefix(d)}attribute def {v2name(self.unique_name(d))}{(' :> ' + base) if base else ''}"
        body: list[str] = []
        for p in props:
            self._emit_property(p, body, ind + "    ", False)
        self._decl(d, lines, ind, head, body)

    def _emit_association(self, a: Element, lines: list[str], ind: str) -> None:
        ends = [self.m.elements.get(e) for e in a.refs.get("memberEnd", [])]
        owned = [self.m.elements[c] for c in a.children if self.m.elements[c].kind == "Property"]
        for o in owned:
            self.emitted.add(o.id)
        # composite associations are already expressed by the part usage on the owning block
        if any(e is not None and e.attrs.get("aggregation") == "composite" for e in ends if e is not None):
            self.rec(a, "Association (composite)", "(part usage)", CLEAN, "expressed by the owning block's part usage")
            return
        maybe_types = [self.m.type_of(e) for e in ends if e is not None]
        types = [t for t in maybe_types if t is not None]
        if len(maybe_types) == 2 and len(types) == 2 and a.name:
            self.rec(a, "Association (named)", "connection def", CLEAN)
            lines.append(
                f"{ind}connection def {v2name(self.unique_name(a))} {{ end : {self.ref(types[0].id)}; end : {self.ref(types[1].id)}; }}"
            )
        elif len(maybe_types) == 2 and len(types) == 2:
            self.rec(a, "Association (reference)", "(ref part usage)", CLEAN, "expressed by the owning block's reference usage")
        else:
            self.rec(a, "Association", "-", LOSSY, "association end types unresolved (external or missing)")

    def _emit_import(self, imp: Element, lines: list[str], ind: str) -> None:
        tgt = (imp.refs.get("importedElement") or imp.refs.get("importedPackage") or [""])[0]
        if tgt and tgt in self.m.elements:
            self.rec(imp, imp.kind, "import", CLEAN)
            lines.append(f"{ind}private import {self.ref(tgt)}{'::*' if imp.kind == 'PackageImport' else ''};")
        else:
            name = self.m.external_name(tgt) if tgt else "?"
            self.rec(
                imp,
                f"{imp.kind} (external)",
                "import (v2 library)",
                DECISION,
                f"imports {name!r} from a v1 library/profile; map to the v2 standard library (ISQ, SI, ScalarValues)",
            )

    def _emit_deferred_relationships(self, lines: list[str]) -> None:
        lines.append("")
        lines.append(f"package {v2name(self.m.name + ' Relationships')} {{")
        lines.append(f"    private import {v2name(self.m.name + ' Profile')}::*;")
        lines.append("    private import RequirementDerivation::*;")
        for rel in self._deferred:
            self._emit_relationship(rel, lines, "    ")
        lines.append("}")

    def _emit_relationship(self, rel: Element, lines: list[str], ind: str) -> None:
        st = self.stereo(rel)
        kind = st[0] if st else rel.kind
        if rel.kind == "InformationFlow":
            ends = rel.refs.get("informationSource", []) + rel.refs.get("informationTarget", [])
            if any(a.kind in ("Activity", "StateMachine") for e in ends for a in self.m.owner_chain(e)):
                self.rec(rel, "ItemFlow / InformationFlow", "-", LOSSY, "flow between activity nodes; activity internals are not migrated")
                return
            src = [self.ref(s) for s in rel.refs.get("informationSource", [])]
            tgt = [self.ref(t) for t in rel.refs.get("informationTarget", [])]
            conv = [self.ref(c) for c in rel.refs.get("conveyed", [])]
            if src and tgt and src[0] and tgt[0]:
                self.rec(
                    rel,
                    "ItemFlow / InformationFlow",
                    "#ItemFlow dependency",
                    DECISION,
                    "v2 flows need a common part context (connect a.port to b.port inside an owner); "
                    "ends live in different definitions, so the flow is kept as a traced dependency"
                    + ("" if conv and conv[0] else "; conveyed item type unresolved"),
                )
                self.metadata_defs.setdefault("ItemFlow", ["conveyed"])
                of = f" /* conveys {conv[0]} */" if conv and conv[0] else ""
                lines.append(
                    f"{ind}#ItemFlow dependency {v2name(self.unique_name(rel)) if rel.name else ''} from {src[0]} to {tgt[0]};{of}"
                )
            else:
                self.rec(rel, "InformationFlow", "-", LOSSY, "flow ends unresolved")
            return
        clients = [self.ref(c) for c in rel.refs.get("client", [])]
        suppliers = [self.ref(s) for s in rel.refs.get("supplier", [])]
        if not clients or not suppliers or not clients[0] or not suppliers[0]:
            self.rec(rel, kind, "-", LOSSY, "relationship end not in this file")
            return
        c, s = clients[0], suppliers[0]
        c_el = self.m.elements.get(rel.refs["client"][0])
        s_el = self.m.elements.get(rel.refs["supplier"][0])
        both_req = (
            c_el is not None and s_el is not None and self.primary(c_el)[1] == "Requirement" and self.primary(s_el)[1] == "Requirement"
        )
        if kind == "DeriveReqt":
            if both_req:
                self.rec(rel, "DeriveReqt", "#derivation connection", CLEAN)
                lines.append(f"{ind}#derivation connection {{ end #original ::> {s}; end #derive ::> {c}; }}")
            else:
                self.rec(
                    rel, "DeriveReqt", "dependency", LOSSY, "one end is not a requirement; derivation connection needs requirement usages"
                )
                lines.append(f"{ind}#DeriveReqt dependency from {c} to {s};")
                self.metadata_defs.setdefault("DeriveReqt", [])
        elif kind == "Satisfy":
            self.rec(
                rel,
                "Satisfy",
                "satisfy ... by",
                DECISION,
                "v2 satisfy needs a part *usage*; emitted as dependency until the satisfying usage is chosen",
            )
            self.metadata_defs.setdefault("Satisfy", [])
            lines.append(f"{ind}#Satisfy dependency from {c} to {s};")
        elif kind in ("Verify", "Verification"):
            self.rec(
                rel,
                kind,
                "verification case / verify",
                DECISION,
                "v2 verifies requirements from a verification case's objective; needs restructuring",
            )
            self.metadata_defs.setdefault(kind, [])
            lines.append(f"{ind}#{v2name(kind)} dependency from {c} to {s};")
        elif kind in ("Refine", "Trace", "Validation", "ConcernOf", "Copy", "Allocate", "mount"):
            status = CLEAN if kind in ("Refine", "Trace") else (DECISION if kind == "Allocate" else LOSSY)
            note = {
                "Refine": "",
                "Trace": "",
                "Allocate": "v2 allocation is a connection between usages; dependency keeps the intent only",
                "Copy": "copy semantics (text sync) has no v2 equivalent",
            }.get(kind, "custom relationship stereotype kept as metadata on a dependency")
            self.rec(rel, kind, f"#{kind} dependency", status, note)
            self.metadata_defs.setdefault(kind, [])
            lines.append(f"{ind}#{v2name(kind)} dependency from {c} to {s};")
        else:
            self.rec(rel, rel.kind, "dependency", CLEAN)
            lines.append(f"{ind}dependency from {c} to {s};")

    def _profile_package(self) -> list[str]:
        lines = [
            f"package {v2name(self.m.name + ' Profile')} {{",
            "    doc /* Custom stereotypes from the v1 profile, carried over as SysML v2 metadata definitions.",
            "           Tag definitions become attributes; the tool-side behaviour (icons, validation rules,",
            "           derived properties, table customisations) is NOT carried and must be re-created. */",
        ]
        # pull in abstract ancestors (e.g. ExtRequirement) so specialisations resolve
        pending = list(self.metadata_defs)
        while pending:
            info = self.profile.stereotypes.get(pending.pop())
            for p in info.parents if info else []:
                if p in self.profile.stereotypes and p not in self.metadata_defs:
                    self.metadata_defs[p] = []
                    pending.append(p)

        def custom_parents(name: str) -> list[str]:
            info = self.profile.stereotypes.get(name)
            return [p for p in info.parents if p in self.profile.stereotypes] if info else []

        def declared_tags(name: str) -> list[str]:
            """Tags a metadata def must declare itself: its own profile tags, plus the SysML
            Requirement tags (Id/Text) on the root custom requirement stereotype."""
            info = self.profile.stereotypes.get(name)
            tags = list(info.tags) if info else []
            if info and info.root == "Requirement" and not custom_parents(name):
                tags = ["Id", "Text"] + tags
            observed = self.metadata_defs.get(name, [])
            inherited = set()
            stack = custom_parents(name)
            while stack:
                p = stack.pop()
                inherited.update(declared_tags(p))
                stack.extend(custom_parents(p))
            return sorted(set(tags) | (set(observed) - inherited))

        for name in sorted(self.metadata_defs):
            tags = declared_tags(name)
            parents = custom_parents(name)
            spec = (" :> " + ", ".join(v2name(p) for p in parents)) if parents else ""
            if tags:
                lines.append(
                    f"    metadata def {v2name(name)}{spec} {{ "
                    + " ".join(f"attribute {v2name(t)} : ScalarValues::String;" for t in tags)
                    + " }"
                )
            else:
                lines.append(f"    metadata def {v2name(name)}{spec};")
        lines.append("}")
        return lines

    def _record_unsupported_leftovers(self) -> None:
        for el in self.m.elements.values():
            if self.scope is not None and el.id not in self.scope:
                continue
            if el.id in self.emitted or el.kind in ("Model",) or el.kind.startswith("Literal"):
                continue
            if el.kind in ("Comment",) and not el.attrs.get("body"):
                continue
            if any(a.id in self.emitted and self.m.elements[a.id].kind in ("Activity", "StateMachine") for a in self.m.owner_chain(el.id)):
                continue
            if el.kind in (
                "Property",
                "Port",
                "Operation",
                "Parameter",
                "Generalization",
                "ConnectorEnd",
                "EnumerationLiteral",
                "OpaqueExpression",
                "InstanceValue",
            ):
                continue
            self.records.append(
                MapRecord(el.id, el.name, self.m.qualified_name(el.id), el.kind, "-", UNSUPPORTED, "not reached by the transformer")
            )


def transform(model: Model, profile: ProfileIndex | None = None, subset_root: str | None = None) -> TransformResult:
    return Transformer(model, profile, subset_root).run()
