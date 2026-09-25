import json
import os
import re
from pathlib import Path

import pytest

from sysml_demo import cli, cyber
from sysml_demo.ingest import load
from sysml_demo.model import Element

# Two-level STPA-Sec chain (Loss <- Hazard <- Constraint / HCA <- Loss scenario <- Risk scenario), a 3-leaf
# probabilistic attack tree, one Trace to a cyber requirement, a 2-technique D3FEND slice and a 1-goal assurance case.
CYBER_XMI = """<?xml version='1.0' encoding='UTF-8'?>
<xmi:XMI xmlns:uml='http://www.omg.org/spec/UML/20131001' xmlns:xmi='http://www.omg.org/spec/XMI/20131001'
         xmlns:sysml='http://www.omg.org/spec/SysML/20181001/SysML'
         xmlns:STPA='https://example.org/STPA-Sec.xmi' xmlns:D3F='https://example.org/D3FEND.xmi'
         xmlns:AC='https://example.org/Assurance_Case.xmi'>
  <xmi:Documentation><xmi:exporter>MagicDraw UML</xmi:exporter><xmi:exporterVersion>19.0</xmi:exporterVersion></xmi:Documentation>
  <uml:Model xmi:id='m' name='TinyCyber'>
    <packagedElement xmi:type='uml:Package' xmi:id='stpa' name='STPA-Sec'>
      <packagedElement xmi:type='uml:Class' xmi:id='L1' name='Loss of the air vehicle'/>
      <packagedElement xmi:type='uml:Class' xmi:id='H1' name='AV flown to a location not chosen by the operator'/>
      <packagedElement xmi:type='uml:Class' xmi:id='SC1' name='AV shall only follow authenticated commands'/>
      <packagedElement xmi:type='uml:Class' xmi:id='C1' name='Ground Station Operator'/>
      <packagedElement xmi:type='uml:Class' xmi:id='HCA1' name='Operator provides waypoint that is not the planned one'/>
      <packagedElement xmi:type='uml:Class' xmi:id='LS1' name='Adversary breaks encryption to obtain the command link key'/>
      <packagedElement xmi:type='uml:Class' xmi:id='LS2' name='Adversary tampers with the navigation module during depot maintenance'/>
      <packagedElement xmi:type='uml:Class' xmi:id='RS1' name='Adversary flies AV to adversary selected location'/>
      <packagedElement xmi:type='uml:Class' xmi:id='RS2' name='Adversary prevents UAS operations'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='r1' client='LS1' supplier='RS1'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='r2' client='LS2' supplier='RS1'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='r3' client='LS1' supplier='HCA1'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='r4' client='HCA1' supplier='H1'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='r5' client='H1' supplier='L1'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='r6' client='SC1' supplier='H1'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='r7' client='HCA1' supplier='C1'/>
      <packagedElement xmi:type='uml:Dependency' xmi:id='r8' client='LS1' supplier='LF1'/>
      <packagedElement xmi:type='uml:Dependency' xmi:id='r9' client='LS2' supplier='LF3'/>
    </packagedElement>
    <packagedElement xmi:type='uml:Package' xmi:id='pat' name='Attack Trees'>
      <packagedElement xmi:type='uml:Class' xmi:id='RK1' name='R1 - Adversary flies AV to selected location'/>
      <packagedElement xmi:type='uml:Class' xmi:id='PAS1' name='R1 Probability of Attack Success'/>
      <packagedElement xmi:type='uml:Class' xmi:id='EML1' name='R1 Mission Impact'/>
      <packagedElement xmi:type='uml:Class' xmi:id='MID1' name='Adversary controls the command link'/>
      <packagedElement xmi:type='uml:Class' xmi:id='LF1' name='Adversary breaks encryption to determine the command link key'/>
      <packagedElement xmi:type='uml:Class' xmi:id='LF2' name='Adversary man-in-the-middle of the command link'/>
      <packagedElement xmi:type='uml:Class' xmi:id='LF3' name='Adversary physically replaces the navigation module'/>
      <packagedElement xmi:type='uml:Dependency' xmi:id='t0' client='RK1' supplier='RS1'/>
      <packagedElement xmi:type='uml:Dependency' xmi:id='t1' client='PAS1' supplier='RK1'/>
      <packagedElement xmi:type='uml:Dependency' xmi:id='t2' client='EML1' supplier='RK1'/>
      <packagedElement xmi:type='uml:Dependency' xmi:id='t3' client='MID1' supplier='PAS1'/>
      <packagedElement xmi:type='uml:Dependency' xmi:id='t4' client='LF3' supplier='PAS1'/>
      <packagedElement xmi:type='uml:Dependency' xmi:id='t5' client='LF1' supplier='MID1'/>
      <packagedElement xmi:type='uml:Dependency' xmi:id='t6' client='LF2' supplier='MID1'/>
    </packagedElement>
    <packagedElement xmi:type='uml:Package' xmi:id='reqs' name='Cyber Requirements'>
      <packagedElement xmi:type='uml:Class' xmi:id='RQ1' name='Command Link Encryption'/>
      <packagedElement xmi:type='uml:Class' xmi:id='RQ2' name='Ground Station MFA'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='tr1' client='RQ1' supplier='LF1'/>
    </packagedElement>
    <packagedElement xmi:type='uml:Package' xmi:id='ac' name='Assurance Case'>
      <packagedElement xmi:type='uml:Class' xmi:id='G1' name='Ground station access is controlled'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='g1s' client='G1' supplier='RQ2'/>
    </packagedElement>
    <packagedElement xmi:type='uml:Package' xmi:id='d3f' name='D3FEND'>
      <packagedElement xmi:type='uml:Class' xmi:id='OT1' name='Adversary-in-the-Middle:T1557'>
        <ownedComment xmi:type='uml:Comment' xmi:id='OT1c' annotatedElement='OT1'>
          <body>Adversaries position themselves between networked devices to intercept or modify command traffic and steal keys.</body>
        </ownedComment>
      </packagedElement>
      <packagedElement xmi:type='uml:Class' xmi:id='OT2' name='Data Obfuscation:T1001'/>
      <packagedElement xmi:type='uml:Class' xmi:id='DA1' name='Network Traffic'/>
      <packagedElement xmi:type='uml:Class' xmi:id='DT1' name='Message Encryption'/>
      <packagedElement xmi:type='uml:Class' xmi:id='DT2' name='Message Authentication'/>
      <packagedElement xmi:type='uml:Class' xmi:id='TAC1' name='Harden'/>
      <packagedElement xmi:type='uml:Association' xmi:id='A1' name='May Modify' memberEnd='A1a A1b'>
        <ownedEnd xmi:type='uml:Property' xmi:id='A1a' type='OT1'/>
        <ownedEnd xmi:type='uml:Property' xmi:id='A1b' type='DA1'/>
      </packagedElement>
      <packagedElement xmi:type='uml:Association' xmi:id='A2' name='Encrypts' memberEnd='A2a A2b'>
        <ownedEnd xmi:type='uml:Property' xmi:id='A2a' type='DT1'/>
        <ownedEnd xmi:type='uml:Property' xmi:id='A2b' type='DA1'/>
      </packagedElement>
      <packagedElement xmi:type='uml:Association' xmi:id='A3' name='May Counter' memberEnd='A3a A3b'>
        <ownedEnd xmi:type='uml:Property' xmi:id='A3a' type='DT2'/>
        <ownedEnd xmi:type='uml:Property' xmi:id='A3b' type='OT1'/>
      </packagedElement>
      <packagedElement xmi:type='uml:Association' xmi:id='A4' name='enables' memberEnd='A4a A4b'>
        <ownedEnd xmi:type='uml:Property' xmi:id='A4a' type='DT1'/>
        <ownedEnd xmi:type='uml:Property' xmi:id='A4b' type='TAC1'/>
      </packagedElement>
    </packagedElement>
  </uml:Model>
  <STPA:Loss xmi:id='s1' base_Class='L1' Id='L-1'/>
  <STPA:Hazard xmi:id='s2' base_Class='H1' Id='H-1'/>
  <STPA:Security_Constraint xmi:id='s3' base_Class='SC1' Id='SC-1'/>
  <STPA:Controller xmi:id='s4' base_Class='C1'/>
  <STPA:Hazardous_Control_Action xmi:id='s5' base_Class='HCA1' Id='HCA-1'/>
  <STPA:Loss_Scenario xmi:id='s6' base_Class='LS1' Id='LS-1'/>
  <STPA:Loss_Scenario xmi:id='s7' base_Class='LS2' Id='LS-2'/>
  <STPA:Risk_Scenario xmi:id='s8' base_Class='RS1' Id='RS-1'/>
  <STPA:Risk_Scenario xmi:id='s9' base_Class='RS2' Id='RS-2'/>
  <STPA:Roll_Up_To xmi:id='s10' base_Abstraction='r1'/>
  <STPA:Roll_Up_To xmi:id='s11' base_Abstraction='r2'/>
  <STPA:Leads_to xmi:id='s12' base_Abstraction='r3'/>
  <STPA:Causes xmi:id='s13' base_Abstraction='r4'/>
  <STPA:Causes xmi:id='s14' base_Abstraction='r5'/>
  <STPA:Mitigates xmi:id='s15' base_Abstraction='r6'/>
  <STPA:AssignedTo xmi:id='s16' base_Abstraction='r7'/>
  <STPA:Risk xmi:id='s20' base_Class='RK1'/>
  <STPA:Probability_of_Attack_Success xmi:id='s21' base_Class='PAS1'/>
  <STPA:Mission_Impact xmi:id='s22' base_Class='EML1' Impact='0.7'/>
  <STPA:PAT_Middle_Node xmi:id='s23' base_Class='MID1'/>
  <STPA:PAT_Leaf_Node xmi:id='s24' base_Class='LF1' _90CI_Low='0.001' _90CI_High='0.04'
                     TotalRiskSensitivity='0.02'/>
  <STPA:PAT_Leaf_Node xmi:id='s25' base_Class='LF2' _90CI_Low='0.1' _90CI_High='0.3'/>
  <STPA:PAT_Leaf_Node xmi:id='s26' base_Class='LF3' _90CI_Low='0.2' _90CI_High='0.5'/>
  <STPA:And xmi:id='s27' base_Dependency='t1'/>
  <STPA:And xmi:id='s28' base_Dependency='t2'/>
  <STPA:Or xmi:id='s29' base_Dependency='t3'/>
  <STPA:Or xmi:id='s30' base_Dependency='t4'/>
  <STPA:And xmi:id='s31' base_Dependency='t5'/>
  <STPA:And xmi:id='s32' base_Dependency='t6'/>
  <sysml:Requirement xmi:id='s40' base_Class='RQ1' Id='CR-1'
                     Text='The command link shall be encrypted with an approved cryptographic module.'/>
  <sysml:Requirement xmi:id='s41' base_Class='RQ2' Id='CR-2' Text='Ground station login shall use multi-factor authentication.'/>
  <sysml:Trace xmi:id='s42' base_Abstraction='tr1'/>
  <AC:Goal xmi:id='s50' base_Class='G1' Id='G-1'/>
  <sysml:Satisfy xmi:id='s51' base_Abstraction='g1s'/>
  <D3F:Offensive_Technique xmi:id='s60' base_Class='OT1' d3fClass='T1557'/>
  <D3F:Offensive_Technique xmi:id='s61' base_Class='OT2' d3fClass='T1001'/>
  <D3F:Digital_Artifact xmi:id='s62' base_Class='DA1'/>
  <D3F:Defensive_Technique xmi:id='s63' base_Class='DT1'/>
  <D3F:Defensive_Technique xmi:id='s64' base_Class='DT2'/>
  <D3F:Defensive_Tactic xmi:id='s65' base_Class='TAC1'/>
  <D3F:D3FEND_Association xmi:id='s66' base_Association='A1'/>
  <D3F:D3FEND_Association xmi:id='s67' base_Association='A2'/>
  <D3F:D3FEND_Association xmi:id='s68' base_Association='A3'/>
  <D3F:D3FEND_Association xmi:id='s69' base_Association='A4'/>
</xmi:XMI>
"""


@pytest.fixture(scope="module")
def tiny_cyber_path(tmp_path_factory) -> Path:
    p = tmp_path_factory.mktemp("cyber") / "TinyCyber.xmi"
    p.write_text(CYBER_XMI)
    return p


@pytest.fixture(scope="module")
def tiny_cyber(tiny_cyber_path):
    return load(tiny_cyber_path)


@pytest.fixture(scope="module")
def analysed(tiny_cyber):
    return cyber.analyse(tiny_cyber, cyber.find_scenario(tiny_cyber, None))


def test_scenario_listing_and_selection(tiny_cyber):
    scen = cyber.risk_scenarios(tiny_cyber)
    assert [cyber._id(s) for s in scen] == ["RS-1", "RS-2"]
    assert cyber._id(cyber.find_scenario(tiny_cyber, None)) == "RS-1"  # default = adversary-selected-location
    assert cyber._id(cyber.find_scenario(tiny_cyber, "rs-2")) == "RS-2"
    assert cyber._id(cyber.find_scenario(tiny_cyber, "prevents")) == "RS-2"
    with pytest.raises(SystemExit):
        cyber.find_scenario(tiny_cyber, "no such scenario")


def test_walker_follows_the_chain_and_the_tree(tiny_cyber):
    sc = cyber.walk(tiny_cyber, cyber.find_scenario(tiny_cyber, None))
    assert [cyber._id(x) for x in sc.loss_scenarios] == ["LS-1", "LS-2"]
    assert [cyber._id(x) for x in sc.hcas] == ["HCA-1"]
    assert [cyber._id(x) for x in sc.hazards] == ["H-1"]
    assert [cyber._id(x) for x in sc.losses] == ["L-1"]
    assert [cyber._id(x) for x in sc.constraints] == ["SC-1"]
    assert [x.name for x in sc.controllers] == ["Ground Station Operator"]
    assert sc.risk is not None and sc.eml == {"Impact": "0.7"}
    assert len(sc.roots) == 1 and sc.roots[0].gate == "And"
    assert {lf.element.id for lf in sc.leaves} == {"LF1", "LF2", "LF3"}
    assert all(lf.in_tree for lf in sc.leaves)
    lf1 = next(lf for lf in sc.leaves if lf.element.id == "LF1")
    assert lf1.p_low == 0.001 and lf1.p_high == 0.04 and lf1.p_text == "P=0.001–0.04"
    assert lf1.gate_path == ["Or Adversary controls the command link"]
    assert [cyber._id(x) for x in lf1.loss_scenarios] == ["LS-1"]
    assert [cyber._id(x) for x in lf1.hazards] == ["H-1"]
    lf2 = next(lf for lf in sc.leaves if lf.element.id == "LF2")
    assert lf2.loss_scenarios == [] and lf2.hazards == []


def test_requirement_coverage_uses_model_links_only(analysed):
    by_id = {lf.element.id: lf for lf in analysed.leaves}
    direct = by_id["LF1"].requirements
    assert [(r.kind, r.confidence) for r in direct] == [("direct", "high")]
    assert direct[0].label == "CR-1 Command Link Encryption"
    assert "Trace" in direct[0].rationale and "model relationship" in direct[0].rationale
    # LF2 has no model link; the lexical proposal must be labelled as such and stay below the threshold
    assert all(r.kind == "lexical" and r.confidence == "low" for r in by_id["LF2"].requirements)
    assert by_id["LF2"].covered_requirements("medium") == []
    assert by_id["LF3"].covered_requirements("medium") == []


def test_attack_and_d3fend_mapping_are_heuristic_and_explained(analysed):
    by_id = {lf.element.id: lf for lf in analysed.leaves}
    lf2 = by_id["LF2"]
    tids = {a.tid: a for a in lf2.attack}
    assert "T1557" in tids and tids["T1557"].confidence in ("high", "medium") and tids["T1557"].rationale
    assert "T1001" not in tids
    cms = {c.label: c for c in lf2.countermeasures}
    assert cms["Message Authentication"].via == "direct" and "May Counter" in cms["Message Authentication"].rationale
    assert cms["Message Encryption"].via == "artifact" and "Network Traffic" in cms["Message Encryption"].rationale
    assert cms["Message Encryption"].tactic == "Harden"
    assert cyber.CONF[cms["Message Encryption"].confidence] < cyber.CONF[cms["Message Authentication"].confidence]
    for cm in lf2.countermeasures:
        assert cm.confidence in cyber.CONF and cm.rationale.startswith("D3FEND:")
    assert analysed.d3fend_applied == {}  # no D3FEND stereotype leaks onto the system model


def test_gap_table_ranking_and_statuses(analysed):
    ranked = analysed.ranked()
    assert [lf.element.id for lf in ranked] == ["LF3", "LF2", "LF1"]
    status = {lf.element.id: lf.status("medium") for lf in ranked}
    assert status["LF1"] == "both"
    assert status["LF2"] == "countermeasure-only"
    assert status["LF3"] == "GAP"
    lf3 = ranked[0]
    assert lf3.gap_score("medium") == pytest.approx(lf3.p_mid) and lf3.p_mid == pytest.approx(0.35)
    assert ranked[1].gap_score("medium") == 0
    cov = analysed.coverage()
    assert cov == {
        "leaves": 3,
        "in_tree": 3,
        "requirement": 1,
        "requirement_model_link": 1,
        "countermeasure": 2,
        "both": 1,
        "requirement_only": 0,
        "countermeasure_only": 1,
        "neither": 1,
    }


def test_assurance_case_check(analysed):
    rows = {a["requirement"]: a for a in analysed.assurance}
    assert rows["CR-1 Command Link Encryption"]["supported"] is False
    assert "CR-2" in " ".join(analysed.assurance_referenced) and "G-1" in " ".join(analysed.assurance_referenced)


def test_nist_lookup_levels():
    table = cyber.load_nist_table()
    assert table["_meta"]["status"].startswith("STARTING POINT FOR REVIEW")
    assert 40 <= len(table["entries"]) <= 120
    for e in table["entries"]:
        assert e["nist"] and e["rationale"] and e["level"] in ("technique", "family", "tactic")

    def cm(name: str) -> cyber.Countermeasure:
        return cyber.Countermeasure(Element(name, "uml:Class", name), "Harden", "direct", "medium", "why", ["T1557"])

    exact = cyber.nist_candidates([cm("Message Encryption")], None, table)
    assert {n.control for n in exact} >= {"SC-8(1)", "SC-13"}
    assert all(n.level == "technique" and n.confidence == "medium" for n in exact)
    fallback = cyber.nist_candidates([cm("Some Brand New Hardening Technique")], None, table)
    assert fallback and all(n.level == "tactic" and n.confidence == "low" and n.matched == "Harden" for n in fallback)


def test_renderers_and_outputs(analysed, tiny_cyber, tmp_path):
    ascii_out = "\n".join(cyber.render_ascii(analysed))
    assert ascii_out.startswith("RS-1  Adversary flies AV to adversary selected location")
    assert "P=0.001–0.04" in ascii_out and "coverage @≥medium: 3 leaves" in ascii_out
    mm = cyber.render_mermaid(analysed)
    assert mm.startswith("graph") and "Command Link Encryption" in mm and ":::gap" in mm
    files = cyber.write_outputs(analysed, tiny_cyber, tmp_path, "python -m sysml_demo cyber tiny.xmi")
    names = {f.name for f in files}
    assert names == {
        "cyber_RS-1.md",
        "cyber_RS-1.mmd",
        "cyber_gaps.md",
        "cyber_gaps.json",
        "cyber_candidate_nist_controls.md",
        "cyber_candidate_nist_controls.csv",
        "nist_controls_candidate.xmi",
    }
    gaps = json.loads((tmp_path / "cyber_gaps.json").read_text())
    assert gaps["coverage"]["neither"] == 1 and gaps["leaves"][0]["status"] == "GAP"
    for lf in gaps["leaves"]:
        for k in ("requirements", "requirements_below_threshold", "attack_techniques", "d3fend_countermeasures"):
            for row in lf[k]:
                assert row["confidence"] in cyber.CONF and row["rationale"]
        for line in lf["nist_candidates"]:
            assert re.search(r"\[(high|medium|low)\]", line) and " via " in line
    md = (tmp_path / "cyber_gaps.md").read_text()
    assert "**GAP**" in md and "not model facts" in md
    # the XMI stub round-trips through our own loader as Requirement-stereotyped classes with Id + Text
    stub = load(tmp_path / "nist_controls_candidate.xmi")
    reqs = stub.requirements()
    assert reqs and all(r.tag("Id") and "CANDIDATE" in (r.tag("Text") or "") for r in reqs)
    csv_text = (tmp_path / "cyber_candidate_nist_controls.csv").read_text()
    assert csv_text.splitlines()[0].startswith("scenario,control,")


def test_cli_list_and_run(tiny_cyber_path, tmp_path, capsys):
    cli.main(["cyber", str(tiny_cyber_path), "--list"])
    out = capsys.readouterr().out
    assert "2 risk scenarios" in out and "RS-1" in out and "RS-2" in out
    cli.main(["cyber", str(tiny_cyber_path), "--scenario", "RS-1", "--out", str(tmp_path), "--mermaid", str(tmp_path / "g.mmd")])
    out = capsys.readouterr().out
    assert "coverage @≥medium" in out and (tmp_path / "g.mmd").exists()


# --------------------------------------------------------------------------- IGNITE-gated (real Berserker federation)
def _ignite_cyber() -> Path:
    d = os.environ.get("IGNITE_MODELS_DIR")
    if not d:
        pytest.skip("IGNITE_MODELS_DIR not set")
    p = Path(d).expanduser() / "Berserker Cyber Res. Model.mdzip"
    if not p.exists():
        pytest.skip(f"{p} not found")
    return p


@pytest.fixture(scope="module")
def ignite_cyber():
    return load(_ignite_cyber(), federate=True)


def test_ignite_federation_and_scenarios(ignite_cyber):
    assert len(ignite_cyber.projects) == 9
    assert ignite_cyber.missing_projects == ["MI Style Guide.mdzip"]
    scen = cyber.risk_scenarios(ignite_cyber)
    assert len(scen) == 8
    assert [cyber._id(s) for s in scen] == [f"RS-{i}" for i in range(1, 9)]
    rs2 = cyber.find_scenario(ignite_cyber, None)
    assert cyber._id(rs2) == "RS-2" and "adversary selected location" in rs2.name.lower()


def test_ignite_rs2_chain_and_d3fend(ignite_cyber):
    sc = cyber.analyse(ignite_cyber, cyber.find_scenario(ignite_cyber, None))
    assert len(sc.loss_scenarios) == 12
    cov = sc.coverage()
    assert cov["in_tree"] == 11 and cov["leaves"] >= cov["in_tree"]
    assert cov["requirement_model_link"] == 0  # nothing in the model ties a requirement to a leaf directly
    assert cov["countermeasure"] >= cov["leaves"] - 2
    assert sc.d3fend_applied == {}
    assert all(lf.p_low is not None for lf in sc.leaves if lf.in_tree)
    for lf in sc.leaves:
        for a in lf.attack:
            assert a.tid and a.rationale
