import csv
import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from sysml_demo import thread
from sysml_demo.ingest import load

# requirement R-1 -> Satisfy <- activity "Check Systems" -> Allocate -> block "Controller"
#   <- Realization <- block "Allocated Controller" <- Realization <- block "Vendor Controller"
# test case "Launch Test" calls "Check Systems"; test procedure "Power Test" is allocated to "Controller";
# R-3 is already verified by "Launch Test"; R-2 has no relationships at all (status "none").
THREAD_XMI = """<?xml version='1.0' encoding='UTF-8'?>
<xmi:XMI xmlns:uml='http://www.omg.org/spec/UML/20131001' xmlns:xmi='http://www.omg.org/spec/XMI/20131001'
         xmlns:sysml='http://www.omg.org/spec/SysML/20181001/SysML' xmlns:UTP='http://www.omg.org/spec/UTP/2.1'>
  <xmi:Documentation><xmi:exporter>MagicDraw UML</xmi:exporter><xmi:exporterVersion>2024x</xmi:exporterVersion></xmi:Documentation>
  <uml:Model xmi:id='m' name='Thread'>
    <packagedElement xmi:type='uml:Package' xmi:id='reqs' name='Requirements'>
      <packagedElement xmi:type='uml:Class' xmi:id='r1' name='Final Systems Check'/>
      <packagedElement xmi:type='uml:Class' xmi:id='r2' name='Paint Colour'/>
      <packagedElement xmi:type='uml:Class' xmi:id='r3' name='Launch Time'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='sat1' client='act' supplier='r1'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='ver3' client='tc' supplier='r3'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='trc3' client='tp' supplier='r3'/>
    </packagedElement>
    <packagedElement xmi:type='uml:Package' xmi:id='fsa' name='Functional'>
      <packagedElement xmi:type='uml:Activity' xmi:id='act' name='Check Systems'/>
      <packagedElement xmi:type='uml:Activity' xmi:id='parent' name='Launch UAV'>
        <node xmi:type='uml:CallBehaviorAction' xmi:id='cba0' name='check' behavior='act'/>
      </packagedElement>
      <packagedElement xmi:type='uml:Class' xmi:id='ctl' name='Controller'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='alloc1' client='act' supplier='ctl'/>
    </packagedElement>
    <packagedElement xmi:type='uml:Package' xmi:id='abl' name='Allocated'>
      <packagedElement xmi:type='uml:Class' xmi:id='actl' name='Allocated Controller'/>
      <packagedElement xmi:type='uml:Realization' xmi:id='real1' client='actl' supplier='ctl'/>
    </packagedElement>
    <packagedElement xmi:type='uml:Package' xmi:id='pbl' name='Product'>
      <packagedElement xmi:type='uml:Class' xmi:id='pctl' name='Vendor Controller'/>
      <packagedElement xmi:type='uml:Realization' xmi:id='real2' client='pctl' supplier='actl'/>
    </packagedElement>
    <packagedElement xmi:type='uml:Package' xmi:id='tm' name='Tests'>
      <packagedElement xmi:type='uml:Activity' xmi:id='tc' name='Launch Test'>
        <ownedComment xmi:type='uml:Comment' xmi:id='cmt' body='&lt;p&gt;Confirms the systems check before launch (C-1.29).&lt;/p&gt;'/>
        <node xmi:type='uml:CallBehaviorAction' xmi:id='cba1' name='do check' behavior='act'/>
      </packagedElement>
      <packagedElement xmi:type='uml:Activity' xmi:id='tp' name='Power Test'/>
      <packagedElement xmi:type='uml:Activity' xmi:id='tp2' name='Paint Inspection'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='alloc2' client='tp' supplier='ctl'/>
    </packagedElement>
  </uml:Model>
  <sysml:Requirement xmi:id='s1' base_Class='r1' Id='C-1.29' Text='The vehicle shall perform a final systems check before launch.'/>
  <sysml:Requirement xmi:id='s2' base_Class='r2' Id='C-2' Text='The vehicle shall be painted grey.'/>
  <sysml:Requirement xmi:id='s3' base_Class='r3' Id='C-3' Text='The vehicle shall launch within 5 minutes.'/>
  <sysml:Block xmi:id='s4' base_Class='ctl'/>
  <sysml:Block xmi:id='s5' base_Class='actl'/>
  <sysml:Block xmi:id='s6' base_Class='pctl'/>
  <sysml:Satisfy xmi:id='s7' base_Abstraction='sat1'/>
  <sysml:Allocate xmi:id='s8' base_Abstraction='alloc1'/>
  <sysml:Allocate xmi:id='s9' base_Abstraction='alloc2'/>
  <sysml:Verify xmi:id='s10' base_Abstraction='ver3'/>
  <sysml:Trace xmi:id='s11' base_Abstraction='trc3'/>
  <UTP:TestCase xmi:id='s12' base_Activity='tc'/>
  <UTP:TestProcedure xmi:id='s13' base_Activity='tp'/>
  <UTP:TestProcedure xmi:id='s14' base_Activity='tp2'/>
</xmi:XMI>
"""


@pytest.fixture(scope="module")
def tm(tmp_path_factory):
    p = tmp_path_factory.mktemp("t") / "Thread.xmi"
    p.write_text(THREAD_XMI)
    return load(p)


@pytest.fixture(scope="module")
def result(tm, tmp_path_factory):
    out = tmp_path_factory.mktemp("out")
    return thread.run(tm, out, stem="t"), out


def _chain(res, name):
    return next(c for c in res.chains if c.requirement.name == name)


def test_chain_hops(tm, result):
    res, _ = result
    c = _chain(res, "Final Systems Check")
    assert [h.element.name for h in c.functions] == ["Check Systems"]
    assert c.functions[0].via == "Satisfy <-"
    assert [h.element.name for h in c.parents] == ["Launch UAV"]
    assert [h.element.name for h in c.blocks] == ["Controller"]
    assert [h.element.name for h in c.allocated] == ["Allocated Controller"]
    assert [h.element.name for h in c.product] == ["Vendor Controller"]
    assert not any(h.heuristic for h in c.blocks + c.allocated + c.product)
    assert c.status == "full"
    assert c.verified_by == []
    touches = {(t.test.name, t.role, t.edge) for t in c.tests}
    assert ("Launch Test", "function", "call") in touches
    assert ("Power Test", "block", "allocate") in touches


def test_chain_status_and_summary(result):
    res, _ = result
    assert _chain(res, "Paint Colour").status == "none"
    assert _chain(res, "Launch Time").status == "none"  # verified + traced, but no Satisfy/function hop
    assert [e.name for e in _chain(res, "Launch Time").verified_by] == ["Launch Test"]
    s = res.summary
    assert s["requirements"] == 3
    assert s["with_verify"] == 1 and s["without_verify"] == 2
    assert s["verify_relationships_in_model"] == 1
    assert s["status"] == {"full": 1, "partial": 0, "none": 2}
    assert s["by_package"]["Thread :: Requirements"]["total"] == 3


def test_candidate_ranking(result):
    res, _ = result
    by_req = {}
    for p in res.proposals:
        by_req.setdefault(p.requirement.name, []).append(p)
    assert "Launch Time" not in by_req  # already verified -> never proposed
    fsc = by_req["Final Systems Check"]
    assert [p.test.name for p in fsc][:2] == ["Launch Test", "Power Test"]
    assert fsc[0].confidence == "high" and fsc[0].score > fsc[1].score
    assert "HEURISTIC PROPOSAL" in fsc[0].rationale
    assert "calls Activity 'Check Systems'" in fsc[0].rationale
    assert "C-1.29" in fsc[0].rationale  # requirement Id found in the test documentation
    assert fsc[1].confidence in ("medium", "high")
    assert "Allocate -> Class 'Controller'" in fsc[1].rationale
    assert all(p.test.name != "Paint Inspection" or p.confidence == "low" for p in res.proposals)


def test_outputs_and_patch(tm, result):
    res, out = result
    names = {p.name for p in res.written}
    assert names == {
        "t_rvtm.md",
        "t_rvtm.csv",
        "t_rvtm.json",
        "t_proposed_verify.md",
        "t_proposed_verify.json",
        "t_proposed_verify.xmi",
        "t_proposed_verify.csv",
    }
    rvtm = json.loads((out / "t_rvtm.json").read_text())
    row = next(r for r in rvtm["rows"] if r["requirement"]["req_id"] == "C-1.29")
    assert row["product"][0]["name"] == "Vendor Controller"
    csv_rows = list(csv.DictReader((out / "t_rvtm.csv").open()))
    assert len(csv_rows) == 3
    none_row = next(r for r in csv_rows if r["Id"] == "C-2")
    assert none_row["Function (FSA)"].startswith("GAP:") and none_row["Verified by"] == "GAP: no Verify"
    md = (out / "t_rvtm.md").read_text()
    assert "| C-1.29 |" in md and "GAP:" in md

    with (out / "t_proposed_verify.csv").open(newline="") as f:
        patch = list(csv.reader(f))
    assert patch[0] == ["source id", "target id", "relationship"]
    assert ["tc", "r1", "Verify"] in patch[1:]
    assert all(r[2] == "Verify" for r in patch[1:])
    ids_in_patch = {(r[0], r[1]) for r in patch[1:]}
    assert all(tm.get(a) is not None and tm.get(b) is not None for a, b in ids_in_patch)

    root = ET.parse(out / "t_proposed_verify.xmi").getroot()
    ns = {
        "uml": "http://www.omg.org/spec/UML/20131001",
        "xmi": "http://www.omg.org/spec/XMI/20131001",
        "sysml": "http://www.omg.org/spec/SysML/20181001/SysML",
    }
    abstractions = [e for e in root.iter("packagedElement") if e.get(f"{{{ns['xmi']}}}type") == "uml:Abstraction"]
    verifies = root.findall("sysml:Verify", ns)
    assert len(abstractions) == len(verifies) == len(ids_in_patch) >= 1
    a = next(e for e in abstractions if e.find("client").get(f"{{{ns['xmi']}}}idref") == "tc")
    assert a.find("supplier").get(f"{{{ns['xmi']}}}idref") == "r1"
    assert {v.get("base_Abstraction") for v in verifies} == {e.get(f"{{{ns['xmi']}}}id") for e in abstractions}
    low_only = [p for p in res.proposals if p.confidence == "low"]
    assert all((p.test.id, p.requirement.id) not in ids_in_patch for p in low_only)


def test_min_confidence_filters_report(tm, tmp_path):
    res = thread.run(tm, tmp_path, stem="h", min_confidence="high")
    assert res.proposals and all(p.confidence == "high" for p in res.proposals)


def test_requirement_tree(tm, result):
    res, _ = result
    req = thread.find_requirement(tm, "C-1.29")
    assert req is not None and req.name == "Final Systems Check"
    c = _chain(res, "Final Systems Check")
    lines = thread.render_chain_tree(tm, c, res.proposals)
    text = "\n".join(lines)
    assert lines[0].startswith("C-1.29 Final Systems Check <<Requirement>>")
    assert "GAP: no Verify relationship" in text
    assert "[Satisfy <-] Check Systems <<Activity>>" in text
    assert "Vendor Controller <<Block>>" in text
    assert "HEURISTIC" in text and "[high] Launch Test" in text
    paint = thread.render_chain_tree(tm, _chain(res, "Paint Colour"), res.proposals)
    assert any(line.strip().startswith("GAP: no Satisfy") for line in paint)


# --------------------------------------------------------------------------- IGNITE-gated
IGNITE = os.environ.get("IGNITE_MODELS_DIR")


@pytest.fixture(scope="module")
def berserker():
    if not IGNITE or not Path(IGNITE).is_dir():
        pytest.skip("IGNITE_MODELS_DIR not set")
    d = Path(IGNITE)
    root = d / "Beserker System Level Test Model.mdzip"
    if not root.exists():
        pytest.skip(f"{root.name} not in IGNITE_MODELS_DIR")
    extra = [d / "Berserker Allocated Baseline Model.mdzip", d / "Berserker Product Baseline Library.mdzip"]
    return load(root, federate=True, extra=extra)


def test_ignite_federation(berserker):
    m = berserker
    for name in (
        "Beserker System Level Test Model",
        "MQ-99 Berserker Functional System Architecture",
        "Berserker Allocated Baseline Model",
        "Berserker Product Baseline Library",
        "(U) CapyBARA",
        "UML Test Profile v2_1",
    ):
        assert name in m.projects, name
    assert "MI Style Guide.mdzip" in m.missing_projects


def test_ignite_counts(berserker, tmp_path):
    import time

    t = time.time()
    res = thread.run(berserker, tmp_path, stem="b")
    assert time.time() - t < 30
    s = res.summary
    assert 250 <= s["requirements"] <= 290
    assert s["without_satisfy"] >= 230
    fsa = [c for c in res.chains if c.requirement.project == "MQ-99 Berserker Functional System Architecture"]
    assert len(fsa) == 233
    assert all(not c.verified_by for c in fsa), "FSA requirements have no Verify in the loaded data"
    assert s["status"]["full"] >= 1
    full = {thread.req_id(c.requirement) for c in res.chains if c.status == "full"}
    assert "C-1.29" in full
    c = next(c for c in res.chains if thread.req_id(c.requirement) == "C-1.29")
    assert {t.test.name for t in c.tests} >= {"Launch UAS Op Test Procedure"}
    assert any(p.confidence == "high" for p in res.proposals)
    assert all((tmp_path / f"b_{x}").stat().st_size > 0 for x in ("rvtm.md", "rvtm.csv", "rvtm.json", "proposed_verify.xmi"))
