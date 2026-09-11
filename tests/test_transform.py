import pytest

from sysml_demo.v2 import validate
from sysml_demo.v2.report import build_report, render_json, render_markdown
from sysml_demo.v2.transform import CLEAN, DECISION, LOSSY, UNSUPPORTED, transform, v2name

needs_kernel = pytest.mark.skipif(not validate.kernel_available(), reason="SysML v2 pilot kernel not installed")


def test_v2name_quoting():
    assert v2name("Engine") == "Engine"
    assert v2name("power in") == "'power in'"
    assert v2name("part") == "'part'"
    assert v2name("1 - Structure") == "'1 - Structure'"
    assert v2name("it's") == "'it\\'s'"
    assert v2name("") == "''"


def test_tiny_transform_text(tiny):
    res = transform(tiny)
    text = res.model_text
    assert "part def Vehicle" in text
    assert "part engine : '1 - Structure'::Engine[1..2];" in text
    assert "attribute mass : '1 - Structure'::Real;" in text
    assert "port 'power in' : '1 - Structure'::PowerIF;" in text
    assert "port def PowerIF" in text
    assert "attribute def Real" in text
    assert "part 'part' : '1 - Structure'::Engine;" in text
    assert "requirement <'R-1'> Range" in text
    assert "Range_2" in text  # sibling name clash resolved
    assert "#Satisfy dependency from '1 - Structure'::Vehicle to '2 - Requirements'::Range;" in text
    statuses = {r.status for r in res.records}
    assert statuses <= {CLEAN, LOSSY, DECISION, UNSUPPORTED}
    by_id = {r.element_id: r for r in res.records if r.status != LOSSY}
    assert by_id["veh"].v2_construct.startswith("part def")
    assert by_id["r1"].v2_construct.startswith("requirement")
    assert by_id["sat"].status == DECISION  # satisfy needs a chosen part usage in v2
    assert by_id["orphan"].status == DECISION or by_id["orphan"].status == CLEAN


def test_csrm_full_transform_records(csrm, csrm_profile):
    res = transform(csrm, csrm_profile)
    assert "#Component" in res.model_text
    assert "metadata def Component" in res.profile_text
    counts = {}
    for r in res.records:
        counts[r.status] = counts.get(r.status, 0) + 1
    assert counts[CLEAN] > 900
    assert counts[UNSUPPORTED] > 200  # diagrams + tool customisations
    diagram_recs = [r for r in res.records if r.v1_construct.startswith("Diagram")]
    assert diagram_recs and all(r.status == UNSUPPORTED for r in diagram_recs)


def test_csrm_subset_has_stubs(csrm, csrm_profile):
    res = transform(csrm, csrm_profile, subset_root="Power Subsystem")
    assert "part def 'Power Subsystem'" in res.model_text
    assert res.model_text.count("\n") < 80


def test_dels_redefinition_is_lossy_or_redefines(dels):
    res = transform(dels)
    redef = [r for r in res.records if r.v1_construct == "Property (redefinition)"]
    assert redef and all(r.status == LOSSY for r in redef)
    assert ":>>" in res.model_text
    assert "[self." not in res.model_text


def test_report_rendering(tiny):
    res = transform(tiny)
    rep = build_report(tiny, res, None)
    md = render_markdown(rep)
    assert "migration gap report: Tiny" in md
    assert "| Status |" in md
    assert "not run" in md.lower() or "validation" in md.lower()
    js = render_json(rep)
    assert '"records"' in js


@needs_kernel
def test_tiny_validates(tiny):
    res = transform(tiny)
    v = validate.validate(res.cells)
    assert v.ok, v.raw
    assert v.errors == []


@needs_kernel
def test_csrm_subset_validates(csrm, csrm_profile):
    res = transform(csrm, csrm_profile, subset_root="Power Subsystem")
    v = validate.validate(res.cells)
    assert v.ok, v.raw
    assert v.errors == [] and v.warnings == []
