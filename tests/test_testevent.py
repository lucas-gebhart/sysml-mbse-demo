import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from sysml_demo import testevent
from sysml_demo.ingest import load

EVENT_XMI = """<?xml version='1.0' encoding='UTF-8'?>
<xmi:XMI xmlns:uml='http://www.omg.org/spec/UML/20131001' xmlns:xmi='http://www.omg.org/spec/XMI/20131001'
         xmlns:sysml='http://www.omg.org/spec/SysML/20181001/SysML' xmlns:UTP='http://www.omg.org/spec/UTP/2.1'>
  <xmi:Documentation><xmi:exporter>MagicDraw UML</xmi:exporter><xmi:exporterVersion>2024x</xmi:exporterVersion></xmi:Documentation>
  <uml:Model xmi:id='m' name='Event'>
    <packagedElement xmi:type='uml:Class' xmi:id='r1' name='Sensor Range'/>
    <packagedElement xmi:type='uml:Class' xmi:id='item' name='Scan Map'/>
    <packagedElement xmi:type='uml:Class' xmi:id='lead' name='Test Lead'/>
    <packagedElement xmi:type='uml:Activity' xmi:id='look' name='Look at Target'/>
    <packagedElement xmi:type='uml:Activity' xmi:id='tp' name='Range Test'>
      <group xmi:type='uml:ActivityPartition' xmi:id='lane' represents='lead' node='n1 n2'/>
      <node xmi:type='uml:InitialNode' xmi:id='n0' outgoing='f0'/>
      <node xmi:type='uml:CallBehaviorAction' xmi:id='n1' behavior='look' inPartition='lane'>
        <result xmi:type='uml:OutputPin' xmi:id='p1' type='item'/>
      </node>
      <node xmi:type='uml:CallBehaviorAction' xmi:id='n2' name='Log Result' inPartition='lane'>
        <argument xmi:type='uml:InputPin' xmi:id='p2' type='item'/>
      </node>
      <node xmi:type='uml:ActivityFinalNode' xmi:id='n3'/>
      <edge xmi:type='uml:ControlFlow' xmi:id='f0' source='n0' target='n1'/>
      <edge xmi:type='uml:ObjectFlow' xmi:id='f1' source='p1' target='p2'/>
      <edge xmi:type='uml:ControlFlow' xmi:id='f2' source='n2' target='n3'/>
    </packagedElement>
  </uml:Model>
  <sysml:Requirement xmi:id='s1' base_Class='r1' Id='R-1' Text='The sensor shall resolve a target at a range of at least 700 meters.'/>
  <UTP:TestProcedure xmi:id='s2' base_Activity='tp'/>
</xmi:XMI>
"""


@pytest.fixture(scope="module")
def model(tmp_path_factory) -> object:
    p = tmp_path_factory.mktemp("ev") / "event.xmi"
    p.write_text(EVENT_XMI)
    ET.parse(p)
    return load(str(p))


def test_parse_threshold():
    t = testevent.parse_threshold("at least 700 meters, ensuring clear identification")
    assert t is not None and (t.value, t.unit, t.direction) == (700.0, "m", ">=")
    t = testevent.parse_threshold("in no more than 60 minutes")
    assert t is not None and (t.value, t.unit, t.direction) == (60.0, "min", "<=")
    assert testevent.parse_threshold("shall be painted grey") is None


def test_read_procedure(model):
    act = testevent.find_procedure(model, "range test")
    assert act is not None
    proc = testevent.read_procedure(model, act)
    assert [s.kind for s in proc.steps] == ["start", "action", "action", "end"]
    assert proc.steps[1].name == "Look at Target" and proc.steps[1].lane == "Test Lead"
    assert proc.steps[1].outputs == ["Scan Map"] and proc.steps[2].inputs == ["Scan Map"]
    assert proc.information_items == {"Scan Map": 0}
    assert proc.log_steps == ["Log Result"]


def test_simulation_is_deterministic_and_bounded():
    s = testevent.SensorModel("t")
    a = testevent.simulate_passes(s, 80, 3)
    b = testevent.simulate_passes(s, 80, 3)
    assert [p.identified for p in a] == [p.identified for p in b]
    assert all(0 <= p.p_identify <= 1 for p in a)
    # closer targets are easier: P(ID) should be monotone in resolved cycles
    srt = sorted(a, key=lambda p: p.resolved_cycles)
    assert all(x.p_identify <= y.p_identify for x, y in zip(srt, srt[1:], strict=False))


def test_logistic_fit_recovers_r90():
    xs = [float(x) for x in range(300, 1300, 10)]
    ys = [x < 800 for x in xs]  # sharp cut-off: R90 should land just below 800
    f = testevent.fit_logistic(xs, ys)
    assert 740 < f.range_at(0.9) < 800
    thr = testevent.Threshold(700.0, "m", ">=", "at least 700 meters")
    passes = testevent.simulate_passes(testevent.SensorModel("t"), 240, 7)
    mop = testevent.evaluate_mop(passes, thr, seed=7, boot=40)
    conds = {m.condition for m in mop}
    assert "all conditions" in conds and len(conds) == 5
    for m in mop:
        assert m.r90_ci_m[0] <= m.r90_m <= m.r90_ci_m[1]
    assert testevent.verdict(mop, thr)[0] in {"pass", "fail", "inconclusive"}


def test_run_writes_outputs(model, tmp_path: Path):
    res = testevent.run(model, "R-1", "Range Test", tmp_path, stem="ev", passes=40, seed=1)
    assert res.threshold is not None and res.threshold.value == 700.0
    assert res.verdict in {"pass", "fail", "inconclusive"}
    assert {g["severity"] for g in res.gaps} <= {"error", "warn"}
    assert any("Verify" in g["gap"] for g in res.gaps)
    names = sorted(p.name for p in res.written)
    assert names == ["ev.json", "ev.md", "ev_runs.csv"]
    data = json.loads((tmp_path / "ev.json").read_text())
    assert data["test_log"]["verdict"] == res.verdict
    assert len(data["passes"]) == 40
    assert (tmp_path / "ev_runs.csv").read_text().count("\n") == 41


@pytest.mark.skipif(not os.environ.get("IGNITE_MODELS_DIR"), reason="needs the IGNITE archive")
def test_mr25_on_berserker():
    m = load(Path(os.environ["IGNITE_MODELS_DIR"]) / "Beserker System Level Test Model.mdzip", federate=True)
    res = testevent.run(m, "MR - 25", "Operational Target Damage Assessment Test", None)
    assert res.threshold is not None and res.threshold.value == 700.0
    assert len(res.procedure.steps) > 30 and "Test Lead" in res.procedure.lanes
