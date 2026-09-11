"""Load MagicDraw/Cameo models from .mdzip (project archive) or exported XMI.

Both formats carry the same XMI 2.5 structure: a ``uml:Model`` tree plus top-level
stereotype-application elements (``<sysml:Block base_Class="..."/>``) whose namespace
identifies the profile. The Teamwork Cloud REST API exposes the same EMF objects, so
the normalisation here is the piece that would be reused for live TWC ingest.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from .model import Element, Model, Stereotype

XMI_NS = {
    "http://www.omg.org/spec/XMI/20131001",
    "http://www.omg.org/XMI",
    "http://schema.omg.org/spec/XMI/2.1",
    "http://www.omg.org/spec/XMI/20110701",
}
MODEL_ENTRY_RE = re.compile(r"com\.nomagic\.magicdraw\.uml_model\.(shared_)?model$")
ID_RE = re.compile(r"^[A-Za-z_][\w\-$.]*$")


def _split(tag: str) -> tuple[str, str]:
    if tag.startswith("{"):
        ns, _, local = tag[1:].partition("}")
        return ns, local
    return "", tag


def profile_short_name(ns: str) -> str:
    """'https://www.omg.org/spec/CSRM/20220601/Concerns_and_Requirements_Profile.xmi' -> 'Concerns_and_Requirements_Profile'."""
    tail = ns.rstrip("/").rsplit("/", 1)[-1]
    tail = re.sub(r"\.xmi$", "", tail)
    if ns.startswith("http://www.magicdraw.com/spec/Customization/"):
        return f"MD_Customization_for_{tail}"
    return tail


def _read_xml(path: Path) -> list[tuple[str, bytes]]:
    if path.suffix.lower() == ".mdzip":
        with zipfile.ZipFile(path) as z:
            names = [n for n in z.namelist() if MODEL_ENTRY_RE.search(n)]
            if not names:
                raise ValueError(f"{path}: no uml_model entry in archive")
            return [(n, z.read(n)) for n in names]
    return [(path.name, path.read_bytes())]


def load(path: str | Path, name: str | None = None) -> Model:
    path = Path(path)
    model = Model(name or path.stem, str(path))
    for _entry, data in _read_xml(path):
        root = ET.fromstring(data)
        _ingest_root(model, root)
    model.finalize()
    return model


def _ingest_root(model: Model, root: ET.Element) -> None:
    stereo_apps: list[ET.Element] = []
    for child in root:
        ns, local = _split(child.tag)
        if ns in XMI_NS:
            if local == "Documentation":
                parts = {_split(c.tag)[1]: (c.text or "").strip() for c in child}
                exporter = child.get("exporter") or parts.get("exporter", "")
                version = child.get("exporterVersion") or parts.get("exporterVersion", "")
                model.exporter = f"{exporter} {version}".strip()
            continue
        if local in ("Model", "Package", "Profile") and ns.endswith(("UML/20131001", "UML/20110701", "UML/2.1")):
            _walk(model, child, owner=None)
        elif any(k.startswith("base_") for k in child.attrib):
            stereo_apps.append(child)
    _resolve_refs(model)
    _apply_stereotypes(model, stereo_apps)
    _attach_docs(model)


def _xmi_attr(node: ET.Element, name: str) -> str | None:
    for ns in XMI_NS:
        v = node.get(f"{{{ns}}}{name}")
        if v is not None:
            return v
    return None


def _walk(model: Model, node: ET.Element, owner: str | None) -> None:
    ns, local = _split(node.tag)
    if ns in XMI_NS and local == "Extension":
        return
    xid = _xmi_attr(node, "id")
    xtype = _xmi_attr(node, "type") or (f"uml:{local}" if ns.endswith("UML/20131001") else "")
    if xid is None or not xtype:
        return
    el = Element(id=xid, xmi_type=xtype, name=node.get("name", ""), owner=owner, role=local if owner else "")
    for k, v in node.attrib.items():
        kns, klocal = _split(k)
        if kns in XMI_NS:
            continue
        el.attrs[klocal] = v
    if el.kind == "Diagram":
        el.diagram_type = _diagram_type(node)
    model.add(el)
    if owner is not None and owner in model.elements:
        model.elements[owner].children.append(xid)
    for child in node:
        cns, clocal = _split(child.tag)
        if cns in XMI_NS:
            if clocal == "Extension":
                # MagicDraw keeps diagrams outside the UML tree: xmi:Extension/modelExtension/ownedDiagram
                for ext in child.iter():
                    if _split(ext.tag)[1] == "ownedDiagram":
                        _walk(model, ext, owner=xid)
            continue
        idref = _xmi_attr(child, "idref")
        if idref is not None and _xmi_attr(child, "id") is None:
            el.refs.setdefault(clocal, []).append(idref)
            continue
        href = child.get("href")
        if href is not None and _xmi_attr(child, "id") is None:
            # reference into another resource (SysML profile, UML metamodel, a used module)
            target = href.rsplit("#", 1)[-1]
            el.refs.setdefault(clocal, []).append(target)
            model.external[target] = _referent_path(child) or href
            continue
        if _xmi_attr(child, "id") is not None:
            _walk(model, child, owner=xid)
        elif child.text and child.text.strip() and clocal == "body":
            el.attrs["body"] = child.text.strip()


def _referent_path(node: ET.Element) -> str:
    for sub in node.iter():
        if _split(sub.tag)[1] == "referenceExtension":
            return sub.get("referentPath", "")
    return ""


def _diagram_type(node: ET.Element) -> str:
    for sub in node.iter():
        _, local = _split(sub.tag)
        if local == "DiagramRepresentationObject":
            return sub.get("type", "")
    return ""


def _resolve_refs(model: Model) -> None:
    """Promote attribute values that are element ids into typed references."""
    ids = model.elements
    for el in model.elements.values():
        for k, v in list(el.attrs.items()):
            if k in (
                "name",
                "body",
                "value",
                "visibility",
                "aggregation",
                "isAbstract",
                "isDerived",
                "direction",
                "isStatic",
                "isReadOnly",
                "isOrdered",
                "isUnique",
                "kind",
                "isLeaf",
                "isConjugated",
                "isService",
                "isBehavior",
                "isActive",
                "isReentrant",
                "concurrency",
                "isQuery",
                "effect",
                "isIndirectlyInstantiated",
                "symbol",
                "isSubstitutable",
            ):
                continue
            toks = v.split()
            if toks and all(t in ids for t in toks):
                el.refs.setdefault(k, []).extend(t for t in toks if t not in el.refs.get(k, []))


def _apply_stereotypes(model: Model, apps: list[ET.Element]) -> None:
    for app in apps:
        ns, local = _split(app.tag)
        profile = profile_short_name(ns)
        model.profiles.add(profile)
        base = next((v for k, v in app.attrib.items() if k.startswith("base_")), None)
        el = model.elements.get(base) if base else None
        if el is None:
            continue
        tags: dict[str, str] = {}
        for k, v in app.attrib.items():
            kns, klocal = _split(k)
            if kns in XMI_NS or klocal.startswith("base_"):
                continue
            tags[klocal] = v
        for child in app:
            _, clocal = _split(child.tag)
            val = _xmi_attr(child, "idref") or child.get("value") or (child.text or "").strip()
            if val:
                tags[clocal] = (tags[clocal] + "; " + val) if clocal in tags else val
        el.stereotypes.append(Stereotype(profile=profile, name=local, tags=tags))


def _attach_docs(model: Model) -> None:
    for c in model.of_type("Comment"):
        body = c.attrs.get("body", "")
        if not body or c.owner is None:
            continue
        targets = c.refs.get("annotatedElement", [])
        if c.owner in targets or not targets:
            owner = model.elements.get(c.owner)
            if owner is not None:
                owner.doc = (owner.doc + "\n" + body).strip() if owner.doc else body


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = (
        text.replace("&nbsp;", " ")
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
    )
    return re.sub(r"\s+", " ", text).strip()
