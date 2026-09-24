"""In-memory index of a SysML v1 model loaded from MagicDraw/Cameo XMI."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field


@dataclass
class Stereotype:
    profile: str
    name: str
    tags: dict[str, str] = field(default_factory=dict)

    @property
    def qualified(self) -> str:
        return f"{self.profile}::{self.name}"


@dataclass
class Element:
    id: str
    xmi_type: str
    name: str = ""
    owner: str | None = None
    role: str = ""  # containment feature in the owner, e.g. packagedElement, ownedAttribute, lowerValue
    attrs: dict[str, str] = field(default_factory=dict)
    refs: dict[str, list[str]] = field(default_factory=dict)
    children: list[str] = field(default_factory=list)
    stereotypes: list[Stereotype] = field(default_factory=list)
    doc: str = ""
    diagram_type: str = ""
    project: str = ""  # stem of the .mdzip the element was read from (federated loads)

    @property
    def kind(self) -> str:
        return self.xmi_type.split(":")[-1]

    def has_stereotype(self, *names: str) -> bool:
        return any(s.name in names for s in self.stereotypes)

    def stereotype_names(self) -> list[str]:
        return [s.name for s in self.stereotypes]

    def tag(self, key: str) -> str | None:
        for s in self.stereotypes:
            if key in s.tags:
                return s.tags[key]
        return None


REQUIREMENT_STEREOTYPES = {
    "Requirement",
    "MissionRequirement",
    "SubsystemRequirement",
    "ComponentRequirement",
    "DeployerRequirement",
    "GroundSegmentRequirement",
    "SegmentRequirement",
    "CubeSatRequirement",
    "moeRequirement",
    "mopRequirement",
    "tpmRequirement",
    "kppRequirement",
    "performanceRequirement",
    "BusinessRequirement",
    "functionalRequirement",
    "interfaceRequirement",
    "physicalRequirement",
    "designConstraint",
    "extendedRequirement",
}
BLOCK_STEREOTYPES = {
    "Block",
    "Subsystem",
    "System",
    "Component",
    "Segment",
    "Facility",
    "Equipment",
    "CubeSat",
    "InterfaceBlock",
    "ConstraintBlock",
    "ValueType",
    "Stakeholder",
}
TRACE_STEREOTYPES = {"Satisfy", "Verify", "DeriveReqt", "Refine", "Trace", "Allocate", "Copy"}


class Model:
    def __init__(self, name: str, source: str):
        self.name = name
        self.source = source
        self.elements: dict[str, Element] = {}
        self.exporter: str = ""
        self.profiles: set[str] = set()
        self.external: dict[str, str] = {}  # id referenced via href -> human-readable referent path
        self.external_source: dict[str, str] = {}  # external id -> resource it lives in (file name or spec URL)
        self.projects: dict[str, int] = {}  # project stem -> element count (federated loads)
        self.missing_projects: list[str] = []  # used projects that could not be found next to the root
        self.bundled_files: set[str] = set()  # file names / PROJECT ids of used projects shipped with Cameo (never loaded)
        self._by_type: dict[str, list[str]] = defaultdict(list)
        self._by_stereo: dict[str, list[str]] = defaultdict(list)
        self._incoming: dict[str, list[tuple[str, str]]] = defaultdict(list)

    # -- construction -----------------------------------------------------
    def add(self, el: Element) -> None:
        self.elements[el.id] = el
        self._by_type[el.kind].append(el.id)

    def finalize(self) -> None:
        self._by_stereo.clear()
        self._incoming.clear()
        for id_ in [i for i in self.external if i in self.elements]:
            del self.external[id_]
            self.external_source.pop(id_, None)
        for el in self.elements.values():
            for s in el.stereotypes:
                self._by_stereo[s.name].append(el.id)
            for role, targets in el.refs.items():
                for t in targets:
                    if t in self.elements:
                        self._incoming[t].append((el.id, role))

    # -- lookup -----------------------------------------------------------
    def get(self, id_: str) -> Element | None:
        return self.elements.get(id_)

    def of_type(self, *kinds: str) -> list[Element]:
        return [self.elements[i] for k in kinds for i in self._by_type.get(k, [])]

    def external_name(self, id_: str) -> str:
        return self.external.get(id_, id_).rsplit("::", 1)[-1]

    def is_library_ref(self, id_: str) -> bool:
        """Reference into a resource that is never loaded here: OMG spec XMI or a Cameo-bundled profile/library."""
        src = self.external_source.get(id_, "")
        return src.startswith(("http://", "https://")) or src in self.bundled_files

    def with_stereotype(self, *names: str) -> list[Element]:
        seen: set[str] = set()
        out = []
        for n in names:
            for i in self._by_stereo.get(n, []):
                if i not in seen:
                    seen.add(i)
                    out.append(self.elements[i])
        return out

    def incoming(self, id_: str, role: str | None = None) -> list[Element]:
        return [self.elements[s] for s, r in self._incoming.get(id_, []) if role is None or r == role]

    def by_name(self, name: str, kind: str | None = None) -> list[Element]:
        n = name.lower()
        return [e for e in self.elements.values() if e.name.lower() == n and (kind is None or e.kind == kind)]

    def search(self, needle: str, kinds: Iterable[str] | None = None) -> list[Element]:
        n = needle.lower()
        ks = set(kinds) if kinds else None
        return [e for e in self.elements.values() if n in e.name.lower() and (ks is None or e.kind in ks)]

    def owner_chain(self, id_: str) -> list[Element]:
        chain = []
        cur = self.elements.get(id_)
        while cur is not None and cur.owner is not None:
            cur = self.elements.get(cur.owner)
            if cur is not None:
                chain.append(cur)
        return chain

    def qualified_name(self, id_: str) -> str:
        el = self.elements[id_]
        parts = [e.name for e in reversed(self.owner_chain(id_)) if e.name and e.kind != "Model"]
        return "::".join(parts + [el.name or f"<{el.kind}>"])

    def descendants(self, id_: str) -> Iterator[Element]:
        stack = list(self.elements[id_].children)
        while stack:
            c = stack.pop()
            el = self.elements.get(c)
            if el is None:
                continue
            yield el
            stack.extend(el.children)

    def package_of(self, id_: str) -> Element | None:
        for anc in self.owner_chain(id_):
            if anc.kind in ("Package", "Model", "Profile"):
                return anc
        return None

    # -- SysML-level helpers --------------------------------------------
    def requirements(self) -> list[Element]:
        return [e for e in self.of_type("Class") if e.has_stereotype(*REQUIREMENT_STEREOTYPES)]

    def blocks(self) -> list[Element]:
        return [e for e in self.of_type("Class") if e.has_stereotype(*BLOCK_STEREOTYPES)]

    def diagrams(self) -> list[Element]:
        return self.of_type("Diagram")

    def type_of(self, prop: Element) -> Element | None:
        t = prop.attrs.get("type") or (prop.refs.get("type") or [""])[0]
        return self.elements.get(t) if t else None

    def type_name_of(self, prop: Element) -> str:
        """Type name even when the type lives in another resource (e.g. SysML::Libraries::Real)."""
        t = self.type_of(prop)
        if t is not None:
            return t.name
        for ref in prop.refs.get("type", []):
            if ref in self.external:
                return self.external[ref].rsplit("::", 1)[-1]
        return ""

    def generals(self, el: Element) -> list[str]:
        """Names of direct generalizations (local or external)."""
        out = []
        for cid in el.children:
            g = self.elements.get(cid)
            if g is None or g.kind != "Generalization":
                continue
            for gid in g.refs.get("general", []):
                if gid in self.elements:
                    out.append(self.elements[gid].name)
                elif gid in self.external:
                    out.append(self.external[gid].rsplit("::", 1)[-1])
        return out

    def stereotype_summary(self) -> dict[str, dict[str, int]]:
        out: dict[str, dict[str, int]] = defaultdict(dict)
        for el in self.elements.values():
            for s in el.stereotypes:
                out[s.profile][s.name] = out[s.profile].get(s.name, 0) + 1
        return dict(out)

    def type_summary(self) -> dict[str, int]:
        return {k: len(v) for k, v in sorted(self._by_type.items(), key=lambda kv: -len(kv[1]))}
