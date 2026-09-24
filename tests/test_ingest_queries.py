from conftest import MODELS

from sysml_demo import queries
from sysml_demo.ingest import load, load_federation, used_projects


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
    # both usages typed by Engine expand; only a true ancestry cycle is cut
    for child in tree["parts"]:
        assert [g["role"] for g in child["parts"]] == ["piston"]


def test_structure_tree_cycle_guard(tiny):
    eng = tiny.elements["eng"]
    eng_veh = tiny.elements["eng_veh"]
    eng_veh.attrs["aggregation"] = "composite"
    try:
        tree = queries.structure_tree(tiny, eng, depth=5)
        veh = next(p for p in tree["parts"] if p["role"] == "vehicle")
        back = next(p for p in veh["parts"] if p["role"] == "engine")
        assert back["cycle"] is True and back["parts"] == []
    finally:
        del eng_veh.attrs["aggregation"]


def test_interfaces_closure_is_composite_only(tiny):
    veh, eng = tiny.elements["veh"], tiny.elements["eng"]
    res = queries.interfaces_between(tiny, eng, veh)
    # Engine.vehicle is a reference property: Vehicle (and its port) must not join Engine's subtree
    assert res["ports_a"] == []
    assert {p.name for p in res["ports_b"]} == {"power in"}


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


def test_used_projects_distinguish_bundled_from_sibling_modules():
    used = {u.filename: u for u in used_projects(MODELS / "CSRM.mdzip")}
    assert used["SysML Profile.mdzip"].bundled
    assert used["UML_Standard_Profile.mdzip"].project_id.startswith("PROJECT-")
    assert not used["CSRM-Profile.mdzip"].bundled


def test_federated_load_resolves_cross_project_refs(csrm):
    fed = load(MODELS / "CSRM.mdzip", federate=True)
    assert set(fed.projects) == {"CSRM", "CSRM-Profile"}
    assert fed.projects["CSRM"] == len(csrm.elements)
    assert "CSRM Reference Information.mdzip" in fed.missing_projects
    assert {fed.elements[i].project for i in fed.elements} == {"CSRM", "CSRM-Profile"}

    def dangling(m):
        return [f for f in queries.health_check(m) if f.check == "dangling-ref"]

    assert len(dangling(fed)) < len(dangling(csrm))
    lib = [f for f in queries.health_check(fed) if f.check == "library-ref"]
    assert lib and all("bundled" in f.detail for f in lib)
    assert load_federation([MODELS / "CSRM.mdzip", MODELS / "CSRM-Profile.mdzip"]).projects == fed.projects
