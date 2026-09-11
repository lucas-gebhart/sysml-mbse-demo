import subprocess
from collections import Counter

import pytest

from sysml_demo.v2 import validate
from sysml_demo.v2.report import build_report, render_json, render_markdown
from sysml_demo.v2.transform import CLEAN, DECISION, LOSSY, UNSUPPORTED, transform, v2name, v2string

needs_kernel = pytest.mark.skipif(not validate.kernel_available(), reason="SysML v2 pilot kernel not installed")


def test_v2name_quoting():
    assert v2name("Engine") == "Engine"
    assert v2name("power in") == "'power in'"
    assert v2name("part") == "'part'"
    assert v2name("1 - Structure") == "'1 - Structure'"
    assert v2name("it's") == "'it\\'s'"
    assert v2name("") == "''"


def test_v2string_escaping():
    assert v2string('say "hi"\nnow') == '"say \\"hi\\"\\nnow"'
    assert v2string("a\\b") == '"a\\\\b"'


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
    assert max(Counter(r.element_id for r in res.records).values()) == 1  # one record per source element
    by_id = {r.element_id: r for r in res.records}
    assert by_id["veh"].v2_construct.startswith("part def")
    assert by_id["r1"].v2_construct.startswith("requirement")
    assert by_id["r2"].status == LOSSY and "Range_2" in by_id["r2"].note  # rename folded into the element's record
    assert by_id["sat"].status == DECISION  # satisfy needs a chosen part usage in v2
    assert by_id["orphan"].status == DECISION or by_id["orphan"].status == CLEAN


def test_csrm_full_transform_records(csrm, csrm_profile):
    res = transform(csrm, csrm_profile)
    assert "#Component" in res.model_text
    assert "metadata def Component" in res.profile_text
    assert '@moeSpecification { summary = "' in res.model_text  # custom tag values survive
    assert max(Counter(r.element_id for r in res.records).values()) == 1
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
    redef = [r for r in res.records if "redefinition of" in r.note]
    assert redef and all(r.status == LOSSY and r.v2_construct != "-" for r in redef)
    assert max(Counter(r.element_id for r in res.records).values()) == 1
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


def test_validate_timeout_is_a_failed_result(monkeypatch, tmp_path):
    def boom(*_a, **_k):
        raise subprocess.TimeoutExpired("kernel", 1)

    monkeypatch.setattr(validate, "kernel_available", lambda env: True)
    monkeypatch.setattr(validate.subprocess, "run", boom)
    v = validate.validate("package P;", env=tmp_path, timeout=1)
    assert not v.ok and "timed out" in v.raw


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
