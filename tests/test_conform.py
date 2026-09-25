import json
import os
from pathlib import Path

import pytest

from sysml_demo import conform
from sysml_demo.ingest import load

XMI_HEAD = """<?xml version='1.0' encoding='UTF-8'?>
<xmi:XMI xmlns:uml='http://www.omg.org/spec/UML/20131001' xmlns:xmi='http://www.omg.org/spec/XMI/20131001'
         xmlns:Guide='https://example.org/Guide.xmi' xmlns:MP='https://example.org/Mission_Profile.xmi'
         xmlns:UTP='https://example.org/UTP.xmi' xmlns:UAF='https://example.org/UAF.xmi'>
  <xmi:Documentation><xmi:exporter>MagicDraw UML</xmi:exporter><xmi:exporterVersion>2024x</xmi:exporterVersion></xmi:Documentation>
"""


def _comment(cid: str, target: str, body: str) -> str:
    return f"<ownedComment xmi:type='uml:Comment' xmi:id='{cid}'><body>{body}</body><annotatedElement xmi:idref='{target}'/></ownedComment>"


def _diagram(did: str, name: str, dtype: str) -> str:
    return f"""<xmi:Extension extender='MagicDraw UML 2024x'><modelExtension>
      <ownedDiagram xmi:type='uml:Diagram' xmi:id='{did}' name='{name}'>
        <xmi:Extension extender='MagicDraw UML 2024x'><diagramRepresentation>
          <DiagramRepresentationObject type='{dtype}'/></diagramRepresentation></xmi:Extension>
      </ownedDiagram></modelExtension></xmi:Extension>"""


GUIDE_TEXT_1 = (
    "Diagrams should follow the following naming schema: [diagram type - MET for activity flow, E2E for connectivity, "
    "SEQ for sequence] [short view name]. Diagram Titles should be kept short; keep titles shorter than 30 characters. "
    "Reviewers should read the whole guide before modelling anything."
)
GUIDE_TEXT_2 = (
    "Diagrams should use a Comment to capture the following information: Diagram Classification and Author. "
    "All assets should have a Property added named Country. "
    "A collection of resources should be captured as a Resource Architecture. "
    "The containment browser should be organized as shown in the Package diagram. "
    "Mission Engineering Threads should be linked using the Implements relationship to the Mission Thread they realize. "
    "Operational Activities should relate to Capabilities using the MapsToCapability relationship. "
    "Horizontal swimlanes are to be used to indicate which ResourcePerformer performs each activity. "
    "The pins on each end should be typed using OperationalInformation."
)

STYLE_GUIDE_XMI = (
    XMI_HEAD
    + f"""
  <uml:Model xmi:id='g' name='Style Guide'>
    {_comment("gc0", "g", "UNCLASSIFIED // Distribution A. Approved for public release.")}
    <packagedElement xmi:type='uml:Package' xmi:id='g_op' name='Operational'>
      {_comment("gc1", "g_op", GUIDE_TEXT_1)}
      <packagedElement xmi:type='uml:Package' xmi:id='g_op_proc' name='Operational Processes'/>
      {_diagram("gd1", "Basic Unit Categories", "Dependency Matrix")}
    </packagedElement>
    <packagedElement xmi:type='uml:Package' xmi:id='g_res' name='Resources'>
      {_comment("gc2", "g_res", GUIDE_TEXT_2)}
    </packagedElement>
    <packagedElement xmi:type='uml:Package' xmi:id='g_strat' name='Strategy'>
      <packagedElement xmi:type='uml:Package' xmi:id='g_roadmap' name='Strategic Roadmap'/>
    </packagedElement>
    <packagedElement xmi:type='uml:Package' xmi:id='g_views' name='ME Study Views'>
      <ownedRule xmi:type='uml:Constraint' xmi:id='g_req' name='Required'><constrainedElement xmi:idref='g_op_proc'/></ownedRule>
      <ownedRule xmi:type='uml:Constraint' xmi:id='g_rec' name='Recommended'><constrainedElement xmi:idref='g_roadmap'/></ownedRule>
    </packagedElement>
    <packagedElement xmi:type='uml:Profile' xmi:id='g_prof' name='Guide'>
      <packagedElement xmi:type='uml:Stereotype' xmi:id='g_di' name='Diagram Info'>
        <ownedAttribute xmi:type='uml:Property' xmi:id='g_di_b' name='base_Diagram'/>
        <ownedAttribute xmi:type='uml:Property' xmi:id='g_di_c' name='Classification'/>
        <ownedAttribute xmi:type='uml:Property' xmi:id='g_di_a' name='Author'/>
      </packagedElement>
    </packagedElement>
  </uml:Model>
  <Guide:OperationalView xmi:id='ga1' base_Package='g_op'/>
  <Guide:ResourcesView xmi:id='ga2' base_Package='g_res'/>
  <Guide:Diagram_Info xmi:id='ga3' base_Diagram='gd1' Classification='UNCLASSIFIED'/>
</xmi:XMI>
"""
)

MMM_XMI = (
    XMI_HEAD
    + """
  <uml:Model xmi:id='mm' name='Mission Meta Model'>
    <packagedElement xmi:type='uml:Profile' xmi:id='mm_prof' name='Mission Profile'>
      <packagedElement xmi:type='uml:PrimitiveType' xmi:id='mm_str' name='String'/>
      <packagedElement xmi:type='uml:Stereotype' xmi:id='mm_mission' name='Mission'>
        <ownedComment xmi:type='uml:Comment' xmi:id='mm_mc'><body>A Mission is an operation with a purpose.</body></ownedComment>
        <ownedAttribute xmi:type='uml:Property' xmi:id='mm_mission_b' name='base_Class'/>
      </packagedElement>
      <packagedElement xmi:type='uml:Stereotype' xmi:id='mm_mt' name='MissionThread'>
        <ownedAttribute xmi:type='uml:Property' xmi:id='mm_mt_b' name='base_Activity'/>
      </packagedElement>
      <packagedElement xmi:type='uml:Stereotype' xmi:id='mm_met' name='MissionEngineeringThread'>
        <generalization xmi:type='uml:Generalization' xmi:id='mm_met_g' general='mm_mt'/>
        <ownedAttribute xmi:type='uml:Property' xmi:id='mm_met_b' name='base_Activity'/>
        <ownedAttribute xmi:type='uml:Property' xmi:id='mm_met_p' name='priority' type='mm_str'/>
      </packagedElement>
      <packagedElement xmi:type='uml:Stereotype' xmi:id='mm_def' name='Defines'>
        <ownedAttribute xmi:type='uml:Property' xmi:id='mm_def_b' name='base_Dependency'/>
      </packagedElement>
      <packagedElement xmi:type='uml:Stereotype' xmi:id='mm_sp' name='StrategicPhase'>
        <ownedAttribute xmi:type='uml:Property' xmi:id='mm_sp_b' name='base_Class'/>
      </packagedElement>
      <ownedRule xmi:type='uml:Constraint' xmi:id='mm_r1' name='Client is incorrect for Defines'>
        <constrainedElement xmi:idref='mm_def'/>
        <specification xmi:type='uml:OpaqueExpression' xmi:id='mm_r1_s'>
          <body>self.client->forAll(c | c.oclIsKindOf(Activity))</body></specification>
      </ownedRule>
      <ownedRule xmi:type='uml:Constraint' xmi:id='mm_r2' name='Supplier is Incorrect for Defines'>
        <constrainedElement xmi:idref='mm_def'/>
        <specification xmi:type='uml:OpaqueExpression' xmi:id='mm_r2_s'>
          <body>self.supplier->forAll(s | s.isStereotyped('StrategicPhase'))</body></specification>
      </ownedRule>
    </packagedElement>
  </uml:Model>
</xmi:XMI>
"""
)

UTP_XMI = (
    XMI_HEAD
    + """
  <uml:Model xmi:id='u' name='UML Test Profile'>
    <packagedElement xmi:type='uml:Profile' xmi:id='u_prof' name='UTP'>
      <packagedElement xmi:type='uml:Stereotype' xmi:id='u_tc' name='TestCase'/>
      <packagedElement xmi:type='uml:Stereotype' xmi:id='u_tconf' name='TestConfiguration'/>
      <packagedElement xmi:type='uml:Stereotype' xmi:id='u_tp' name='TestProcedure'/>
      <packagedElement xmi:type='uml:Stereotype' xmi:id='u_mark' name='DataMarking'>
        <ownedAttribute xmi:type='uml:Property' xmi:id='u_mark_b' name='base_Package'/>
        <ownedAttribute xmi:type='uml:Property' xmi:id='u_mark_d' name='distribution'/>
      </packagedElement>
      <ownedRule xmi:type='uml:Constraint' xmi:id='u_r1' name='Minimal TestConfiguration'>
        <constrainedElement xmi:idref='u_tconf'/>
        <ownedComment xmi:type='uml:Comment' xmi:id='u_r1_c'>
          <body>A StructuredClassifier with TestConfiguration applied must at least specify one part having TestItem applied.</body>
        </ownedComment>
        <specification xmi:type='uml:OpaqueExpression' xmi:id='u_r1_s'><body>true</body></specification>
      </ownedRule>
      <ownedRule xmi:type='uml:Constraint' xmi:id='u_r2' name='Each TestCase returns a Verdict statement'>
        <constrainedElement xmi:idref='u_tc'/>
        <specification xmi:type='uml:OpaqueExpression' xmi:id='u_r2_s'>
          <body>self.ownedParameter->exists(p | p.type.name = 'Verdict')</body></specification>
      </ownedRule>
      <ownedRule xmi:type='uml:Constraint' xmi:id='u_r3'
                 name='TestProcedure must prescribe the execution order of AT LEAST one AtomicProceduralElement'>
        <constrainedElement xmi:idref='u_tp'/>
      </ownedRule>
      <ownedRule xmi:type='uml:Constraint' xmi:id='u_r4' name='TestCase requires AT MOST ONE precondition'>
        <constrainedElement xmi:idref='u_tc'/>
      </ownedRule>
      <ownedRule xmi:type='uml:Constraint' xmi:id='u_r5' name='Arbitration outcome must be deterministic'>
        <constrainedElement xmi:idref='u_tc'/>
        <ownedComment xmi:type='uml:Comment' xmi:id='u_r5_c'>
          <body>The arbitration of a TestCase must yield the same verdict for identical logs.</body></ownedComment>
      </ownedRule>
    </packagedElement>
    <packagedElement xmi:type='uml:Package' xmi:id='u_ex' name='Examples'/>
  </uml:Model>
  <UTP:validationRule xmi:id='ua1' base_Constraint='u_r1' severity='error'/>
  <UTP:validationRule xmi:id='ua2' base_Constraint='u_r2' severity='error'/>
  <UTP:validationRule xmi:id='ua3' base_Constraint='u_r3' severity='warning'/>
  <UTP:validationRule xmi:id='ua4' base_Constraint='u_r4' severity='error'/>
  <UTP:validationRule xmi:id='ua5' base_Constraint='u_r5' severity='error'/>
  <UTP:DataMarking xmi:id='ua6' base_Package='u_ex' distribution='A'/>
</xmi:XMI>
"""
)

CLASSIFICATION_XMI = (
    XMI_HEAD
    + """
  <uml:Model xmi:id='c' name='Classification Profile'>
    <packagedElement xmi:type='uml:Enumeration' xmi:id='c_lvl' name='ClassificationLevel'>
      <ownedComment xmi:type='uml:Comment' xmi:id='c_lvl_c'><body>Overall classification of an element.</body></ownedComment>
      <ownedLiteral xmi:type='uml:EnumerationLiteral' xmi:id='c_u' name='UNCLASSIFIED'/>
      <ownedLiteral xmi:type='uml:EnumerationLiteral' xmi:id='c_cui' name='CUI'/>
      <ownedLiteral xmi:type='uml:EnumerationLiteral' xmi:id='c_s' name='SECRET'/>
    </packagedElement>
    <packagedElement xmi:type='uml:Enumeration' xmi:id='c_unit' name='Units'>
      <ownedLiteral xmi:type='uml:EnumerationLiteral' xmi:id='c_m' name='metre'/>
    </packagedElement>
  </uml:Model>
</xmi:XMI>
"""
)

DELIVERY_XMI = (
    XMI_HEAD
    + f"""
  <uml:Model xmi:id='d' name='Delivery'>
    {_comment("dc0", "d", "UNCLASSIFIED // Distribution A. Notional demonstration data.")}
    <packagedElement xmi:type='uml:Package' xmi:id='d_op' name='Operational'>
      {_comment("dc1", "d_op", "Operational content of the delivery.")}
      <packagedElement xmi:type='uml:Package' xmi:id='d_mission' name='Strike Mission'/>
      <packagedElement xmi:type='uml:Activity' xmi:id='d_launch' name='Launch Mission Thread'>
        <group xmi:type='uml:ActivityPartition' xmi:id='d_lane' name='Pilot'/>
        <node xmi:type='uml:OpaqueAction' xmi:id='d_ignite' name='Ignite'>
          <output xmi:type='uml:OutputPin' xmi:id='d_pin' name='telemetry'/>
        </node>
      </packagedElement>
      <packagedElement xmi:type='uml:Activity' xmi:id='d_strike' name='Strike Engineering Thread'/>
      <packagedElement xmi:type='uml:Activity' xmi:id='d_find' name='Find Target'/>
      <packagedElement xmi:type='uml:Class' xmi:id='d_phase' name='Phase One'/>
      <packagedElement xmi:type='uml:Abstraction' xmi:id='d_impl' client='d_strike' supplier='d_launch'/>
      <packagedElement xmi:type='uml:Dependency' xmi:id='d_def' client='d_launch' supplier='d_phase'/>
      {_diagram("dd1", "MET Launch", "SysML Activity Diagram")}
      {_diagram("dd2", "Launch Flow", "SysML Activity Diagram")}
      {_diagram("dd3", "Ops Processes", "Operational Processes Diagram")}
      {_diagram("dd4", "Unit Categories", "Dependency Matrix")}
    </packagedElement>
    <packagedElement xmi:type='uml:Package' xmi:id='d_str' name='Structure'>
      {_comment("dc2", "d_str", "Resource structure of the delivery.")}
      <packagedElement xmi:type='uml:Class' xmi:id='d_launcher' name='Launcher'>
        <ownedAttribute xmi:type='uml:Property' xmi:id='d_country' name='Country'/>
      </packagedElement>
      <packagedElement xmi:type='uml:Class' xmi:id='d_arch' name='Strike Package'>
        <ownedAttribute xmi:type='uml:Property' xmi:id='d_country2' name='country'/>
      </packagedElement>
    </packagedElement>
    <packagedElement xmi:type='uml:Package' xmi:id='d_test' name='Test'>
      {_comment("dc3", "d_test", "System level test set.")}
      <packagedElement xmi:type='uml:Class' xmi:id='d_cfg' name='Test Configuration'>
        <ownedAttribute xmi:type='uml:Property' xmi:id='d_sut' name='sut' type='d_launcher'/>
      </packagedElement>
      <packagedElement xmi:type='uml:Activity' xmi:id='d_proc' name='Launch Test Procedure'>
        <group xmi:type='uml:ActivityPartition' xmi:id='d_lane2' name='Test Conductor'/>
        <node xmi:type='uml:OpaqueAction' xmi:id='d_step' name='Arm'/>
      </packagedElement>
      <packagedElement xmi:type='uml:Activity' xmi:id='d_case' name='Launch Test Case'>
        <ownedParameter xmi:type='uml:Parameter' xmi:id='d_case_p' name='result' direction='return' type='d_launcher'/>
      </packagedElement>
    </packagedElement>
  </uml:Model>
  <MP:Mission xmi:id='da1' base_Package='d_mission'/>
  <MP:MissionThread xmi:id='da2' base_Activity='d_launch'/>
  <MP:MissionEngineeringThread xmi:id='da3' base_Activity='d_strike'/>
  <MP:Implements xmi:id='da4' base_Abstraction='d_impl'/>
  <MP:Defines xmi:id='da5' base_Dependency='d_def'/>
  <MP:StrategicPhase xmi:id='da6' base_Class='d_phase'/>
  <UAF:OperationalActivity xmi:id='da7' base_Activity='d_find'/>
  <UAF:ResourceArtifact xmi:id='da8' base_Class='d_launcher'/>
  <UAF:ResourceArchitecture xmi:id='da9' base_Class='d_arch'/>
  <UTP:TestContext xmi:id='da10' base_Package='d_test'/>
  <UTP:TestConfiguration xmi:id='da11' base_Class='d_cfg'/>
  <UTP:TestItem xmi:id='da12' base_Property='d_sut'/>
  <UTP:TestProcedure xmi:id='da13' base_Activity='d_proc'/>
  <UTP:TestCase xmi:id='da14' base_Activity='d_case'/>
  <Guide:Diagram_Info xmi:id='da15' base_Diagram='dd1' Classification='UNCLASSIFIED'/>
</xmi:XMI>
"""
)


def _load_xmi(tmp_path_factory, name: str, text: str):
    p = tmp_path_factory.mktemp("conform") / f"{name}.xmi"
    p.write_text(text)
    return load(p)


@pytest.fixture(scope="module")
def references(tmp_path_factory):
    return [
        _load_xmi(tmp_path_factory, "StyleGuide", STYLE_GUIDE_XMI),
        _load_xmi(tmp_path_factory, "MissionMetaModel", MMM_XMI),
        _load_xmi(tmp_path_factory, "UTP", UTP_XMI),
        _load_xmi(tmp_path_factory, "Classification", CLASSIFICATION_XMI),
    ]


@pytest.fixture(scope="module")
def rules(references):
    return conform.extract_rules(references)


@pytest.fixture(scope="module")
def delivery(tmp_path_factory):
    return _load_xmi(tmp_path_factory, "Delivery", DELIVERY_XMI)


@pytest.fixture(scope="module")
def results(delivery, rules):
    return {r.rule.id: r for r in conform.evaluate(conform.Scope(delivery), rules)}


def _by_check(results, check):
    return [r for r in results.values() if r.rule.check == check]


def test_reference_kinds_detected(references):
    assert [conform.detect_reference_kind(m) for m in references] == ["style-guide", "mission-meta-model", "utp", "classification"]


def test_style_guide_rules_quote_prose_with_source(rules):
    sg = [r for r in rules if r.id.startswith("SG-")]
    naming = next(r for r in sg if r.check == "diagram_naming")
    assert naming.element == "Operational" and naming.source == "StyleGuide"
    assert naming.text.startswith("Diagrams should follow the following naming schema")
    assert naming.params["prefixes"] == ["E2E", "MET", "SEQ"]
    title = next(r for r in sg if r.check == "diagram_title_length")
    assert title.params["match"] == ["30"]
    guidance = [r for r in sg if not r.automatable]
    assert any("Reviewers should read the whole guide" in r.text for r in guidance)
    legend = [r for r in sg if r.check == "required_views"]
    assert {r.severity for r in legend} == {"error", "info"}
    assert next(r for r in sg if r.check == "dependency_matrices").params["matrices"] == ["Dependency Matrix|Basic Unit Categories"]
    assert next(r for r in sg if r.check == "viewpoint_packages").params["expected"] == [
        "Operational<<OperationalView>>",
        "Resources<<ResourcesView>>",
    ]


def test_utp_extractor_reads_validation_rules(references):
    utp = conform.extract_utp(references[2])
    by_name = {r.text.split(":")[0]: r for r in utp if r.id == "UTP"}
    assert len(by_name) == 5
    assert by_name["Minimal TestConfiguration"].check == "utp_min_test_configuration"
    assert "must at least specify one part" in by_name["Minimal TestConfiguration"].text
    assert "true" not in by_name["Minimal TestConfiguration"].text.split(": ", 1)[1]
    assert "OCL: self.ownedParameter" in by_name["Each TestCase returns a Verdict statement"].text
    assert by_name["Each TestCase returns a Verdict statement"].element == "UTP::TestCase"
    assert by_name["TestProcedure must prescribe the execution order of AT LEAST one AtomicProceduralElement"].severity == "warn"
    assert not by_name["Arbitration outcome must be deterministic"].automatable
    assert "same verdict for identical logs" in by_name["Arbitration outcome must be deterministic"].text
    marking = [r for r in utp if r.check == "package_markings"]
    assert len(marking) == 1 and "distribution" in marking[0].text


def test_mission_meta_model_rules(rules):
    mmm = [r for r in rules if r.id.startswith("MMM-")]
    vocab = next(r for r in mmm if r.check == "mission_profile_applied")
    assert set(vocab.params["stereotypes"]) == {"Mission", "MissionThread", "MissionEngineeringThread", "Defines", "StrategicPhase"}
    met = next(r for r in mmm if r.params.get("stereotype") == ["MissionEngineeringThread"])
    assert "extends metaclass Activity" in met.text and "specializes «MissionThread»" in met.text and "priority: String" in met.text
    mission = next(r for r in mmm if r.params.get("stereotype") == ["Mission"])
    assert "A Mission is an operation with a purpose." in mission.text
    assert {r.check for r in mmm if r.family == "relationship"} == {"defines_client", "defines_supplier"}


def test_classification_rules(rules):
    cls = [r for r in rules if r.check == "classification_values"]
    assert len(cls) == 1 and cls[0].params["literals"] == ["UNCLASSIFIED", "CUI", "SECRET"]
    assert {r.check for r in rules if r.id.startswith("CLS-")} >= {"diagram_classification", "root_marking_statement", "package_markings"}


def test_rule_ids_unique_and_at_least_ten_executable(rules):
    ids = [r.id for r in rules]
    assert len(ids) == len(set(ids))
    assert sum(r.automatable for r in rules) >= 10
    assert all(r.check in conform.CHECKS for r in rules if r.automatable)


def test_every_family_has_a_pass_and_a_fail(results, rules, tiny):
    tiny_results = conform.evaluate(conform.Scope(tiny), rules)
    statuses: dict[str, set[str]] = {}
    for r in list(results.values()) + tiny_results:
        if r.rule.automatable:
            statuses.setdefault(r.rule.family, set()).add(r.status)
    assert statuses
    for family, seen in statuses.items():
        assert {"pass", "fail"} <= seen, f"{family}: {seen}"


def test_style_checks_name_offenders(results):
    naming = _by_check(results, "diagram_naming")[0]
    assert naming.status == "fail" and naming.checked == 2 and naming.failed == 1
    assert naming.examples == ["Operational::Launch Flow (SysML Activity Diagram)"]
    assert _by_check(results, "diagram_title_length")[0].status == "pass"
    metadata = _by_check(results, "diagram_metadata_comment")[0]
    assert metadata.failed == 3 and "Operational::Launch Flow" in metadata.examples[0]
    views = {r.rule.severity: r.status for r in _by_check(results, "required_views")}
    assert views == {"error": "pass", "info": "fail"}
    assert _by_check(results, "dependency_matrices")[0].status == "pass"
    structure = _by_check(results, "viewpoint_packages")[0]
    assert structure.status == "fail" and structure.examples == ["Resources<<ResourcesView>>"]
    assert _by_check(results, "asset_country_property")[0].status == "pass"
    assert _by_check(results, "met_implements_mt")[0].status == "pass"
    assert _by_check(results, "oa_maps_to_capability")[0].examples == ["Operational::Find Target"]
    assert _by_check(results, "activity_swimlanes")[0].status == "pass"
    pins = _by_check(results, "pins_typed")[0]
    assert pins.status == "fail" and pins.examples == ["Operational::Launch Mission Thread::Ignite::telemetry"]


def test_mission_and_utp_checks(results):
    assert _by_check(results, "mission_profile_applied")[0].status == "pass"
    by_st = {r.rule.params["stereotype"][0]: r for r in _by_check(results, "stereotype_metaclass")}
    assert by_st["Mission"].status == "fail" and by_st["Mission"].examples == ["Operational::Strike Mission is a Package"]
    assert by_st["MissionThread"].status == "pass"
    assert _by_check(results, "defines_client")[0].status == "pass"
    assert _by_check(results, "defines_supplier")[0].status == "pass"
    assert _by_check(results, "utp_min_test_configuration")[0].status == "pass"
    verdict = _by_check(results, "utp_verdict_return")[0]
    assert verdict.status == "fail" and verdict.examples == ["Test::Launch Test Case"]
    assert _by_check(results, "utp_procedure_not_empty")[0].status == "pass"
    assert _by_check(results, "utp_at_most_one_precondition")[0].status == "pass"


def test_classification_checks(results):
    assert _by_check(results, "classification_values")[0].status == "pass"
    marks = _by_check(results, "diagram_classification")[0]
    assert marks.status == "fail" and marks.checked == 4 and marks.failed == 3
    assert _by_check(results, "root_marking_statement")[0].status == "pass"
    assert _by_check(results, "package_markings")[0].status == "fail"


def test_reports_and_completeness(tiny, rules, tmp_path):
    scope = conform.Scope(tiny)
    comp = conform.completeness(scope)
    assert comp.dangling_count == 1 and comp.dangling[0].startswith("2 - Requirements")
    rep = conform.conformance_report(tiny, conform.evaluate(scope, rules), comp, ["Style Guide"])
    md = conform.conformance_markdown(rep)
    assert "1 dangling references" in md and "## Failed rules" in md
    conform.write_json(tmp_path / "c.json", rep)
    data = json.loads((tmp_path / "c.json").read_text())
    assert data["summary"]["rules"] == len(rules) and data["completeness"]["dangling_count"] == 1
    text = conform.rules_text(rules)
    assert "executable (diagram_naming)" in text and "StyleGuide :: Operational" in text
    assert "| SG-01 |" in conform.rules_markdown(rules)


def test_cross_link_uses_link_matcher_and_labels_proposals(delivery, references):
    scope = conform.Scope(delivery)
    mmm = references[1]
    ref = conform.Reference(mmm.name, mmm, conform.reference_candidates(mmm, "mission-meta-model"))
    assert {e.name for e in ref.candidates} == {"MissionThread", "MissionEngineeringThread", "StrategicPhase"}
    links = conform.cross_link(scope, [ref], min_confidence=0.2)
    assert links[mmm.name], "expected at least one Launch Mission Thread ~ MissionThread proposal"
    best = links[mmm.name][0]
    assert best.a.name == "Launch Mission Thread" and best.b.name == "MissionThread" and "thread" in " ".join(best.rationale)
    assert len({(l.a.id, l.b.id) for l in links[mmm.name]}) == len(links[mmm.name])
    rep = conform.links_report(scope, [ref], links)
    assert rep["references"][mmm.name]["links"] == len(links[mmm.name])
    md = conform.links_markdown(rep)
    assert "not model facts" in md and "MissionThread" in md


# --------------------------------------------------------------------------- IGNITE-gated
IGNITE = Path(os.environ.get("IGNITE_MODELS_DIR", ""))


@pytest.fixture(scope="module")
def ignite():
    if not os.environ.get("IGNITE_MODELS_DIR") or not (IGNITE / "Beserker System Level Test Model.mdzip").exists():
        pytest.skip("IGNITE_MODELS_DIR not set or models absent")
    return IGNITE


@pytest.fixture(scope="module")
def ignite_rules(ignite):
    refs = [
        load(ignite / "MissionArchitectureStyleGuide_Model_Version_1.0.mdzip"),
        load(ignite / "Mission Meta Model.mdzip"),
        load(ignite / "UML Test Profile v2_1.mdzip"),
        load(ignite / "ClassificationProfileDistA.mdzip"),
    ]
    return refs, conform.extract_rules(refs)


def test_ignite_rule_extraction(ignite_rules):
    refs, rules = ignite_rules
    assert [conform.detect_reference_kind(m) for m in refs] == ["style-guide", "mission-meta-model", "utp", "classification"]
    assert sum(r.automatable for r in rules) >= 10
    utp = [r for r in rules if r.id.startswith("UTP-")]
    assert len(utp) == 68
    assert any("TestCase must invoke AT LEAST ONE main TestProcedure" in r.text for r in utp)
    assert any(r.check == "diagram_naming" and "MET" in r.params["prefixes"] for r in rules)


def test_ignite_berserker_conformance_has_passes_and_failures(ignite, ignite_rules):
    refs, rules = ignite_rules
    m = load(
        ignite / "Beserker System Level Test Model.mdzip",
        federate=True,
        extra=[ignite / "Berserker Allocated Baseline Model.mdzip", ignite / "Berserker Product Baseline Library.mdzip"],
    )
    assert "MI Style Guide.mdzip" in m.missing_projects
    roots = ["Beserker System Level Test Model", "Berserker Allocated Baseline Model", "Berserker Product Baseline Library"]
    scope = conform.Scope(m, conform.delivery_projects(m, roots, [r.name for r in refs]))
    assert "MQ-99 Berserker Functional System Architecture" in scope.projects and "(U) CapyBARA" not in scope.projects
    statuses = {r.status for r in conform.evaluate(scope, rules)}
    assert {"pass", "fail"} <= statuses
    comp = conform.completeness(scope)
    assert comp.dangling_count > 0 and comp.missing_projects == ["MI Style Guide.mdzip"]
