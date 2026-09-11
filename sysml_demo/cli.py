"""`python -m sysml_demo <command>` — the live-demo entry points."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from . import link, queries
from .ingest import load, strip_html
from .model import Element, Model
from .v2.profile import index_profile
from .v2.report import build_report, render_json, render_markdown
from .v2.transform import transform
from .v2.validate import annotate, kernel_available, validate


def _load(path: str, name: str | None = None) -> Model:
    t = time.time()
    m = load(path, name)
    print(f"[loaded {m.name}: {len(m.elements)} elements from {Path(path).name} in {time.time() - t:.1f}s]", file=sys.stderr)
    return m


def _find(m: Model, needle: str, kinds: tuple[str, ...] = ("Class", "Package")) -> Element:
    hits = [e for e in m.by_name(needle) if e.kind in kinds] or m.search(needle, kinds)
    if not hits:
        sys.exit(f"no element matching {needle!r}")
    hits.sort(key=lambda e: (e.kind != "Class", len(e.name)))
    if len(hits) > 1:
        print(f"[{len(hits)} matches for {needle!r}; using {m.qualified_name(hits[0].id)}]", file=sys.stderr)
    return hits[0]


def _table(rows: list[list[str]], header: list[str]) -> None:
    widths = [max(len(str(r[i])) for r in [header] + rows) for i in range(len(header))]
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print(fmt.format(*header))
    print(fmt.format(*["-" * w for w in widths]))
    for r in rows:
        print(fmt.format(*[str(c) for c in r]))


# --------------------------------------------------------------------------- commands
def cmd_overview(a: argparse.Namespace) -> None:
    m = _load(a.model)
    o = queries.overview(m)
    print(
        f"{o['name']}  ({o['exporter'] or 'XMI'}; {o['elements']} elements, {o['blocks']} blocks, "
        f"{o['requirements']} requirements, {sum(o['diagrams'].values())} diagrams)"
    )
    print("\nTop-level packages:")
    for name, n in o["top_level_packages"]:
        print(f"  {name:55} {n:>6} elements")
    print("\nElement kinds:", ", ".join(f"{k} {v}" for k, v in list(o["types"].items())[:12]))
    if o["diagrams"]:
        print("Diagrams:", ", ".join(f"{k} {v}" for k, v in o["diagrams"].items()))
    for prof, st in o["profiles"].items():
        print(f"Profile {prof}: " + ", ".join(f"{k} {v}" for k, v in list(st.items())[:12]))


def cmd_requirements(a: argparse.Namespace) -> None:
    m = _load(a.model)
    rows = queries.requirements_table(m)
    if a.unsatisfied:
        rows = [r for r in rows if not r["satisfied_by"]]
    if a.filter:
        rows = [r for r in rows if a.filter.lower() in (r["name"] + r["package"] + r["stereotype"]).lower()]
    _table(
        [
            [
                r["id"],
                r["stereotype"],
                r["name"][:45],
                r["package"][:30],
                ", ".join(r["satisfied_by"])[:40],
                ", ".join(r["verified_by"])[:30],
            ]
            for r in rows
        ],
        ["Id", "Type", "Requirement", "Package", "Satisfied by", "Verified by"],
    )
    total = len(queries.requirements_table(m))
    print(
        f"\n{len(rows)} shown of {total}; {sum(1 for r in rows if not r['satisfied_by'])} without Satisfy, "
        f"{sum(1 for r in rows if not r['verified_by'])} without Verify"
    )


def cmd_trace(a: argparse.Namespace) -> None:
    m = _load(a.model)
    reqs = [r for r in m.requirements() if a.element.lower() in (r.name.lower(), (r.tag("Id") or "").lower())]
    el = reqs[0] if reqs else _find(m, a.element, ("Class",))
    if len(reqs) > 1:
        print(f"[{len(reqs)} requirements match {a.element!r}; using {m.qualified_name(el.id)}]", file=sys.stderr)
    root, breaks = queries.trace(m, el)
    print(f"{m.qualified_name(el.id)}\n  Text: {strip_html(el.tag('Text') or '')[:200]}\n")
    print("\n".join(queries.render_trace(m, root)))
    print("\nWhere the trace breaks:")
    for b in breaks or ["(no breaks found)"]:
        print(f"  - {b}")


def cmd_structure(a: argparse.Namespace) -> None:
    m = _load(a.model)
    el = _find(m, a.element, ("Class",))

    def walk(node: dict, ind: str = "") -> None:
        role = f"{node.get('role')} : " if node.get("role") else ""
        print(f"{ind}{role}{node['name']} <<{','.join(node['stereotypes'])}>>")
        for c in node["parts"]:
            walk(c, ind + "  ")

    walk(queries.structure_tree(m, el, a.depth))


def cmd_interfaces(a: argparse.Namespace) -> None:
    m = _load(a.model)
    ea, eb = _find(m, a.a, ("Class",)), _find(m, a.b, ("Class",))
    r = queries.interfaces_between(m, ea, eb)
    print(f"{r['a']}  <->  {r['b']}")
    print(f"  ports on {r['a']}: {[p.name for p in r['ports_a']] or 'none'}")
    print(f"  ports on {r['b']}: {[p.name for p in r['ports_b']] or 'none'}")
    print(f"  connectors crossing: {len(r['connectors'])}   item flows crossing: {len(r['flows'])}")
    for f in r["flows"]:
        conveyed = ", ".join(m.elements[c].name for c in f.refs.get("conveyed", []) if c in m.elements)
        print(f"    flow {f.name or '?'} conveys {conveyed or '?'}")
    print(f"  associations crossing: {len(r['associations'])}")
    for assoc in r["associations"] if not (r["connectors"] or r["flows"]) else []:
        ends = [m.elements[e] for e in assoc.refs.get("memberEnd", []) if e in m.elements]
        print("    " + " -- ".join(f"{(m.type_of(e) or Element('', '', '?')).name}.{e.name}" for e in ends))
    if not r["ports_a"] and not r["ports_b"]:
        print(
            "\n  note: no ports/connectors between these two — the model defines the interface at the "
            "association/dependency level only (a finding in its own right)."
        )


def cmd_profile(a: argparse.Namespace) -> None:
    m = _load(a.model)
    prof = _load(a.profile) if a.profile else None
    usage = queries.profile_usage(m)
    if prof is not None:
        idx = index_profile(prof)
        print(f"Profile defines {len(idx.stereotypes)} stereotypes:")
        for name, info in sorted(idx.stereotypes.items(), key=lambda kv: kv[1].root):
            print(f"  <<{name}>> extends {', '.join(info.parents) or '-'} -> SysML {info.root or '?'}; tags {info.tags or '-'}")
        print()
    for p, rows in usage.items():
        print(f"Applied from {p}:")
        for r in rows:
            where = ", ".join(f"{pkg} ({n})" for pkg, n in r["top_packages"])
            print(f"  <<{r['stereotype']}>> x{r['count']} on {', '.join(r['applies_to'])}; mostly in {where}")


def cmd_health(a: argparse.Namespace) -> None:
    m = _load(a.model)
    prof = _load(a.profile) if a.profile else None
    findings = queries.health_check(m, prof)
    print("Summary:")
    for check, sev, n in queries.health_summary(findings):
        print(f"  {sev:5} {check:28} {n}")
    if a.verbose:
        print()
        for f in findings:
            if a.check and f.check != a.check:
                continue
            where = m.qualified_name(f.element.id) if f.element else "-"
            print(f"  [{f.severity}] {f.check}: {where}: {f.detail}")


def cmd_migrate(a: argparse.Namespace) -> None:
    m = _load(a.model)
    idx = index_profile(_load(a.profile)) if a.profile else None
    t = time.time()
    res = transform(m, idx, a.subset)
    print(
        f"[transformed: {sum(len(c.splitlines()) for c in res.cells)} lines of SysML v2, {len(res.records)} mapping records "
        f"in {time.time() - t:.1f}s]",
        file=sys.stderr,
    )
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    stem = m.name + (f"-{a.subset}" if a.subset else "")
    stem = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in stem)
    (out / f"{stem}.profile.sysml").write_text(res.profile_text)
    (out / f"{stem}.sysml").write_text(res.model_text)
    v = None
    if not a.no_validate:
        if not kernel_available():
            print("[pilot-implementation kernel not found; skipping validation]", file=sys.stderr)
        else:
            t = time.time()
            v = validate(res.cells)
            verdict = "FAILED" if not v.ok else ("PASSED WITH WARNINGS" if v.warnings else "PASSED")
            print(
                f"[pilot validation {verdict} in {time.time() - t:.1f}s: {len(v.errors)} errors, {len(v.warnings)} warnings]",
                file=sys.stderr,
            )
            if v.errors or a.show_warnings:
                print(annotate(res.cells, v))
    rep = build_report(m, res, v, idx, a.subset)
    (out / f"{stem}.migration.md").write_text(render_markdown(rep))
    (out / f"{stem}.migration.json").write_text(render_json(rep))
    md = render_markdown(rep)
    print(md.split("## Custom profile")[0] if a.brief else md)
    print(
        f"\nWritten: {out / (stem + '.sysml')}, {out / (stem + '.profile.sysml')}, {out / (stem + '.migration.md')}, "
        f"{out / (stem + '.migration.json')}"
    )


def cmd_show_v2(a: argparse.Namespace) -> None:
    m = _load(a.model)
    idx = index_profile(_load(a.profile)) if a.profile else None
    res = transform(m, idx, a.subset)
    print(res.model_text)


def cmd_link(a: argparse.Namespace) -> None:
    ma, mb = _load(a.model_a, a.name_a), _load(a.model_b, a.name_b)
    links = link.match(ma, mb, a.min_confidence)
    if a.json:
        print(json.dumps([l.as_dict(ma, mb) for l in links], indent=2))
        return
    print(f"{len(links)} candidate links between {ma.name} and {mb.name} (confidence >= {a.min_confidence}):\n")
    for l in links:
        print(f"{l.confidence:.2f}  {ma.qualified_name(l.a.id)}  [{link._kind_label(l.a)}]")
        print(f"      <->  {mb.qualified_name(l.b.id)}  [{link._kind_label(l.b)}]")
        print(f"      because: {'; '.join(l.rationale)}")
        for d in l.disagreements:
            print(f"      disagree: {d}")
    agreed = sum(1 for l in links if not l.disagreements)
    print(f"\n{agreed} links with no disagreements; {len(links) - agreed} flag a term/kind/interface/ownership mismatch.")


def cmd_impact(a: argparse.Namespace) -> None:
    ma, mb = _load(a.model_a, a.name_a), _load(a.model_b, a.name_b)
    start = _find(ma, a.element, ("Class", "Port", "Property", "Package"))
    links = link.match(ma, mb, a.min_confidence)
    res = link.cross_impact(ma, mb, start, links, a.depth)
    print("\n".join(link.render_impact(ma, mb, res)))
    if a.mermaid:
        Path(a.mermaid).write_text(link.mermaid(ma, mb, res))
        print(f"\n[mermaid graph written to {a.mermaid}]")


# --------------------------------------------------------------------------- parser
def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="sysml_demo", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name: str, fn, help_: str) -> argparse.ArgumentParser:
        sp = sub.add_parser(name, help=help_)
        sp.set_defaults(fn=fn)
        return sp

    s = add("overview", cmd_overview, "what is this model, how is it organised")
    s.add_argument("model")
    s = add("requirements", cmd_requirements, "requirement table with satisfy / verify coverage")
    s.add_argument("model")
    s.add_argument("--unsatisfied", action="store_true")
    s.add_argument("--filter")
    s = add("trace", cmd_trace, "walk every trace relationship from a requirement and report breaks")
    s.add_argument("model")
    s.add_argument("element")
    s = add("structure", cmd_structure, "composition tree of a block")
    s.add_argument("model")
    s.add_argument("element")
    s.add_argument("--depth", type=int, default=3)
    s = add("interfaces", cmd_interfaces, "ports / connectors / flows / associations between two blocks")
    s.add_argument("model")
    s.add_argument("a")
    s.add_argument("b")
    s = add("profile", cmd_profile, "what the custom profile adds and where it is applied")
    s.add_argument("model")
    s.add_argument("--profile")
    s = add("health", cmd_health, "model health check")
    s.add_argument("model")
    s.add_argument("--profile")
    s.add_argument("-v", "--verbose", action="store_true")
    s.add_argument("--check")
    s = add("migrate", cmd_migrate, "SysML v1 -> v2 textual notation + pilot validation + gap report")
    s.add_argument("model")
    s.add_argument("--profile")
    s.add_argument("--subset", help="package or block name to migrate on its own")
    s.add_argument("--out", default="out")
    s.add_argument("--no-validate", action="store_true")
    s.add_argument("--show-warnings", action="store_true")
    s.add_argument("--brief", action="store_true")
    s = add("show-v2", cmd_show_v2, "print the generated SysML v2 for a subset")
    s.add_argument("model")
    s.add_argument("--profile")
    s.add_argument("--subset")
    for name, fn, help_ in (
        ("link", cmd_link, "match concepts across two models and list disagreements"),
        ("impact", cmd_impact, "what is affected across both models if an element changes"),
    ):
        s = add(name, fn, help_)
        s.add_argument("model_a")
        s.add_argument("model_b")
        s.add_argument("--name-a")
        s.add_argument("--name-b")
        s.add_argument("--min-confidence", type=float, default=0.5)
        if name == "link":
            s.add_argument("--json", action="store_true")
        else:
            s.add_argument("element")
            s.add_argument("--depth", type=int, default=3)
            s.add_argument("--mermaid", help="write a Mermaid graph to this file")
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
