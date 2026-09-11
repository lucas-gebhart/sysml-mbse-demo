from sysml_demo import link


def test_tokens_and_synonyms():
    assert link.tokens("L3.1.7_Power Subsystem") == link.tokens("Power Subsystems")
    assert link.tokens("Subsystems") == link.tokens("Component")  # domain synonyms collapse
    assert "subsystem" in link.raw_tokens("Subsystems")
    assert link.tokens("5 - Architecture") == {"architecture"}


def test_csrm_dels_links_are_explained(csrm, dels):
    links = link.match(csrm, dels)
    assert 5 <= len(links) <= 60
    names = {(l.a.name, l.b.name) for l in links}
    assert ("Facility", "Facility") in names
    for l in links:
        assert l.rationale
        assert 0 < l.confidence <= 1
    facility = next(l for l in links if l.a.name == "Facility" and l.b.name == "Facility")
    assert any(d.startswith("stereotype") for d in facility.disagreements)


def test_cross_impact(csrm, dels):
    links = link.match(csrm, dels)
    start = csrm.by_name("Power Subsystem", "Class")[0]
    res = link.cross_impact(csrm, dels, start, links)
    assert {n.element.name for n in res["local"]} >= {"CubeSat"}
    # Power Subsystem has no direct DELS match; it bridges through its owning package L3_Subsystems
    assert [l.a.name for l in res["links"]] == ["L3_Subsystems"]
    assert res["links"][0].a.id in res["via_owner"]
    txt = "\n".join(link.render_impact(csrm, dels, res))
    assert "Crosses into DELS via 1 link(s)" in txt and "(owning package)" in txt
    mm = link.mermaid(csrm, dels, res)
    assert mm.startswith("graph LR")
    assert "Subsystems" in mm.split("subgraph DELS", 1)[1].split("end", 1)[0]
