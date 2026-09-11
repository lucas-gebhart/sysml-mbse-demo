"""Resolve custom-profile stereotypes to the SysML v1 concept they specialise.

A Cameo profile (CSRM-Profile.mdzip) defines stereotypes that either extend a UML
metaclass directly or specialise a SysML stereotype (``Component :> SysML::Block``).
Knowing the SysML root of each custom stereotype tells the transformer which v2
construct to emit; the custom stereotype itself becomes v2 metadata.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..model import Model

# SysML v1 stereotypes we know how to place, and MagicDraw's built-ins, keyed by name.
SYSML_ROOTS = {
    "Block",
    "Requirement",
    "ValueType",
    "ConstraintBlock",
    "InterfaceBlock",
    "FlowSpecification",
    "TestCase",
    "Stakeholder",
    "View",
    "Viewpoint",
    "Allocated",
    "Rationale",
    "Problem",
    "ProxyPort",
    "FullPort",
    "FlowProperty",
    "ItemFlow",
    "Satisfy",
    "Verify",
    "DeriveReqt",
    "Refine",
    "Trace",
    "Copy",
    "Allocate",
    "Conform",
    "Expose",
    "ElementGroup",
    "BindingConnector",
    "NestedConnectorEnd",
    "PartProperty",
    "ValueProperty",
    "ReferenceProperty",
    "SharedProperty",
    "ConstraintProperty",
    "ControlOperator",
    "Optional",
    "Rate",
    "Continuous",
    "Discrete",
    "Probability",
    "NoBuffer",
    "Overwrite",
    "Subsystem",
    "System",
    "SystemContext",
    "Domain",
    "performanceRequirement",
    "functionalRequirement",
    "interfaceRequirement",
    "physicalRequirement",
    "designConstraint",
    "extendedRequirement",
    "businessRequirement",
    "usabilityRequirement",
}
# MagicDraw SysML customisation: non-normative requirement/block flavours and their normative root.
BUILTIN_PARENT = {
    "Subsystem": "Block",
    "System": "Block",
    "SystemContext": "Block",
    "Domain": "Block",
    "performanceRequirement": "Requirement",
    "functionalRequirement": "Requirement",
    "interfaceRequirement": "Requirement",
    "physicalRequirement": "Requirement",
    "designConstraint": "Requirement",
    "extendedRequirement": "Requirement",
    "businessRequirement": "Requirement",
    "usabilityRequirement": "Requirement",
    "PartProperty": "Property",
    "ValueProperty": "Property",
    "ReferenceProperty": "Property",
    "SharedProperty": "Property",
    "ConstraintProperty": "Property",
}


@dataclass
class StereotypeInfo:
    name: str
    profile_package: str
    parents: list[str]
    metaclasses: list[str]
    tags: list[str]
    doc: str = ""
    root: str = ""  # resolved SysML/UML concept, e.g. "Requirement", "Block", "Comment"


@dataclass
class ProfileIndex:
    stereotypes: dict[str, StereotypeInfo] = field(default_factory=dict)

    def root_of(self, name: str) -> str:
        if name in self.stereotypes:
            return self.stereotypes[name].root
        return BUILTIN_PARENT.get(name, name if name in SYSML_ROOTS else "")


def index_profile(profile: Model) -> ProfileIndex:
    idx = ProfileIndex()
    for s in profile.of_type("Stereotype"):
        parents = profile.generals(s)
        metaclasses = []
        tags = []
        for cid in s.children:
            c = profile.get(cid)
            if c is None or c.kind != "Property":
                continue
            if c.name.startswith("base_"):
                metaclasses.append(c.name[5:])
            else:
                tags.append(c.name)
        pkg = profile.package_of(s.id)
        idx.stereotypes[s.name] = StereotypeInfo(s.name, pkg.name if pkg else "", parents, metaclasses, tags, s.doc)
    for info in idx.stereotypes.values():
        info.root = _resolve_root(idx, info, set())
    return idx


def _resolve_root(idx: ProfileIndex, info: StereotypeInfo, seen: set[str]) -> str:
    seen.add(info.name)
    for p in info.parents:
        if p in BUILTIN_PARENT:
            return BUILTIN_PARENT[p]
        if p in SYSML_ROOTS:
            return p
        if p in idx.stereotypes and p not in seen:
            r = _resolve_root(idx, idx.stereotypes[p], seen)
            if r:
                return r
    if info.metaclasses:
        return info.metaclasses[0]  # extends a UML metaclass directly (Class, Comment, Behavior, ...)
    return ""
