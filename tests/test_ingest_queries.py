from sysml_demo import queries


def test_tiny_ingest_basics(tiny):
    assert tiny.exporter == "MagicDraw UML 19.0"
    veh = tiny.by_name("Vehicle")[0]
    assert veh.kind == "Class"
    assert veh.has_stereotype("Block")
    assert veh.has_stereotype("Vehicle")
    assert [s.profile for s in veh.stereotypes if s.name == "Vehicle"] == ["Demo_Profile"]
    assert veh.tag("owner") == "ACME"
    assert tiny.qualified_name(veh.id) == "1 - Structure::Vehicle"
    eng = tiny.by_name("engine")[0]
    assert eng.role == "ownedAttribute"
    assert tiny.type_of(eng).name == "Engine"
    assert {tiny.elements[c].role for c in eng.children} == {"lowerValue", "upperValue"}


def test_requirements_and_satisfy(tiny):
    rows = {r["id"]: r for r in queries.requirements_table(tiny)}
    assert rows["R-1"]["satisfied_by"] == ["Vehicle"]
    assert rows["R-2"]["satisfied_by"] == []
    assert rows["R-1"]["text"].startswith("The vehicle shall")


def test_health_check_finds_planted_problems(tiny):
    findings = queries.health_check(tiny)
    by_check = {}
    for f in findings:
        by_check.setdefault(f.check, []).append(f)
    assert {f.element.name for f in by_check["requirement-text"]} == {"Range"}
    assert any(f.element.name == "Orphan" for f in by_check["orphan-block"])
    assert any(f.element.name == "Empty" for f in by_check["empty-package"])
    assert any("nowhere" in f.detail for f in by_check["dangling-ref"])
    assert any(f.element.name == "Range" for f in by_check["duplicate-name"])
    assert any(f.check == "requirement-unsatisfied" and f.element.tag("Id") == "R-2" for f in findings)


def test_structure_tree(tiny):
    veh = tiny.by_name("Vehicle")[0]
    tree = queries.structure_tree(tiny, veh)
    assert tree["name"] == "Vehicle"
    assert {p["role"] for p in tree["parts"]} == {"engine", "part"}


def test_csrm_loads_with_diagrams_and_profile(csrm):
    assert len(csrm.elements) > 1500
    assert len(csrm.diagrams()) > 200
    assert csrm.with_stereotype("Component")
    ov = queries.overview(csrm)
    assert ov["requirements"] > 50


def test_csrm_trace_reports_breaks(csrm):
    req = csrm.by_name("Subsystem Requirement Name")[0]
    root, breaks = queries.trace(csrm, req)
    assert root.children
    assert any("Satisfy" in b for b in breaks)
    assert any("Verify" in b for b in breaks)


def test_dels_interfaces(dels):
    q = dels.by_name("Queue", "Class")[0]
    r = dels.by_name("Router", "Class")[0]
    res = queries.interfaces_between(dels, q, r)
    assert res["connectors"]
    assert res["flows"]
    assert {p.name for p in res["ports_a"]} == {"inTask", "outTask"}
