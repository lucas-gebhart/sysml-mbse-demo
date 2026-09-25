"""Simulated test event: run a model-defined test procedure against a quantified requirement.

The model supplies *what* is tested (the requirement and its numeric threshold, the UTP
«TestProcedure» steps, their swimlanes and the information items they exchange); this module
supplies a notional physics/operator model to generate the data the procedure would have
logged, evaluates a Measure of Performance (MOP) against the threshold, and writes a
UTP-shaped TestLog with an arbitrated verdict. Every generated number is synthetic — the
value is in showing exactly which measurement definitions the model is missing.
"""

from __future__ import annotations

import csv
import json
import math
import random
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .ingest import strip_html
from .model import Element, Model
from .thread import find_requirement, req_id, req_text

# --------------------------------------------------------------------------- requirement side
_UNIT = r"(meters?|m|metres?|km|feet|ft|nmi?|knots?|kts?|hours?|hrs?|minutes?|min|seconds?|sec|s|percent|%|g|g’s|g's|pounds?|lbs?)"
_NUM = r"(\d[\d,]*(?:\.\d+)?)"
_THRESHOLD_RE = re.compile(
    rf"(at least|no (?:more|less) than|minimum|maximum|within|not exceed(?:ing)?|greater than|less than|of)\s+(?:of\s+)?(?:a\s+)?"
    rf"{_NUM}\s*{_UNIT}\b",
    re.IGNORECASE,
)
_DIRECTION = {
    "at least": ">=",
    "minimum": ">=",
    "greater than": ">=",
    "no less than": ">=",
    "no more than": "<=",
    "maximum": "<=",
    "within": "<=",
    "not exceed": "<=",
    "not exceeding": "<=",
    "less than": "<=",
    "of": ">=",
}
_UNIT_NORM = {
    "meter": "m", "meters": "m", "metre": "m", "metres": "m", "m": "m",
    "feet": "ft", "ft": "ft", "knot": "kt", "knots": "kt", "kts": "kt", "kt": "kt",
    "hour": "h", "hours": "h", "hr": "h", "hrs": "h", "minute": "min", "minutes": "min", "min": "min",
    "second": "s", "seconds": "s", "sec": "s", "s": "s", "percent": "%", "%": "%",
    "pound": "lb", "pounds": "lb", "lb": "lb", "lbs": "lb", "g": "g", "g’s": "g", "g's": "g", "km": "km", "nm": "nmi", "nmi": "nmi",
}  # fmt: skip


@dataclass
class Threshold:
    """A numeric acceptance threshold parsed out of requirement text."""

    value: float
    unit: str
    direction: str  # ">=" or "<="
    phrase: str

    def satisfied_by(self, measured: float) -> bool:
        return measured >= self.value if self.direction == ">=" else measured <= self.value

    def __str__(self) -> str:
        return f"{self.direction} {self.value:g} {self.unit}"


def parse_threshold(text: str) -> Threshold | None:
    for m in _THRESHOLD_RE.finditer(text):
        key, num, unit = m.group(1).lower(), m.group(2), m.group(3).lower()
        key = re.sub(r"\s+", " ", key)
        direction = _DIRECTION.get(key)
        if direction is None:
            continue
        return Threshold(float(num.replace(",", "")), _UNIT_NORM.get(unit, unit), direction, m.group(0))
    return None


# --------------------------------------------------------------------------- procedure side
@dataclass
class Step:
    order: int
    kind: str  # action | decision | merge | start | end | event
    name: str
    lane: str
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    guards: list[str] = field(default_factory=list)


@dataclass
class Procedure:
    id: str
    name: str
    qualified: str
    doc: str
    stereotypes: list[str]
    steps: list[Step]
    lanes: list[str]
    information_items: dict[str, int]  # item name -> number of attributes the model gives it
    log_steps: list[str]


_NODE_KINDS = {
    "CallBehaviorAction": "action",
    "OpaqueAction": "action",
    "DecisionNode": "decision",
    "MergeNode": "merge",
    "InitialNode": "start",
    "ActivityFinalNode": "end",
    "FlowFinalNode": "end",
    "AcceptEventAction": "event",
    "ForkNode": "fork",
    "JoinNode": "join",
}


def find_procedure(m: Model, needle: str) -> Element | None:
    n = needle.strip().lower()
    acts = [e for e in m.of_type("Activity") if e.has_stereotype("TestProcedure", "TestCase")]
    for e in acts:
        if e.id == needle or e.name.lower() == n:
            return e
    hits = sorted((e for e in acts if n in e.name.lower()), key=lambda e: len(e.name))
    return hits[0] if hits else None


def _pin_owner(m: Model, act: Element) -> dict[str, str]:
    owner: dict[str, str] = {}
    for cid in act.children:
        for pid in m.elements[cid].children:
            owner[pid] = cid
    return owner


def _lane_name(m: Model, partition: Element) -> str:
    for rid in partition.refs.get("represents", []):
        rep = m.elements.get(rid)
        if rep is not None:
            return rep.name or m.type_name_of(rep) or partition.name
    return partition.name


def read_procedure(m: Model, act: Element) -> Procedure:
    """Walk a UTP test procedure's activity graph in control-flow order."""
    kids = [m.elements[c] for c in act.children]
    lanes: dict[str, str] = {}
    for k in kids:
        if k.kind == "ActivityPartition":
            lanes[k.id] = _lane_name(m, k)
    pin_owner = _pin_owner(m, act)

    def own(x: str) -> str:
        return pin_owner.get(x, x)

    nodes: dict[str, Element] = {k.id: k for k in kids if k.kind in _NODE_KINDS}
    succ: dict[str, list[tuple[str, str]]] = {nid: [] for nid in nodes}
    for k in kids:
        if k.kind in ("ControlFlow", "ObjectFlow") and k.refs.get("source") and k.refs.get("target"):
            s, t = own(k.refs["source"][0]), own(k.refs["target"][0])
            guard = ""
            for gid in k.refs.get("guard", []):
                g = m.elements.get(gid)
                if g is not None:
                    guard = g.attrs.get("value") or g.attrs.get("body") or g.name
            if s in succ:
                succ[s].append((t, guard))

    def pins(node: Element, kind: str) -> list[str]:
        out = []
        for pid in node.children:
            p = m.elements[pid]
            if p.kind == kind:
                name = m.type_name_of(p) or p.name
                if name and name.lower() not in ("input", "output", "in", "out"):
                    out.append(name)
        return out

    starts = [nid for nid, n in nodes.items() if n.kind == "InitialNode"] or list(nodes)[:1]
    order: list[str] = []
    seen: set[str] = set()
    queue = list(starts)
    while queue:
        nid = queue.pop(0)
        if nid in seen or nid not in nodes:
            continue
        seen.add(nid)
        order.append(nid)
        queue.extend(t for t, _ in succ[nid])
    order += [nid for nid in nodes if nid not in seen]

    steps: list[Step] = []
    items: Counter[str] = Counter()
    for i, nid in enumerate(order):
        n = nodes[nid]
        beh = n.refs.get("behavior", [])
        name = m.elements[beh[0]].name if beh and beh[0] in m.elements else n.name
        lane = ""
        for pid in n.refs.get("inPartition", []):
            lane = lanes.get(pid, lane)
        ins, outs = pins(n, "InputPin"), pins(n, "OutputPin")
        items.update(x for x in ins + outs if x)
        steps.append(Step(i + 1, _NODE_KINDS[n.kind], name, lane, ins, outs, [g for _, g in succ[nid] if g]))

    info: dict[str, int] = {}
    for item in items:
        attrs = 0
        for e in m.by_name(item, "Class"):
            attrs = max(attrs, sum(1 for c in e.children if m.elements[c].kind == "Property"))
        info[item] = attrs
    return Procedure(
        id=act.id,
        name=act.name,
        qualified=m.qualified_name(act.id),
        doc=strip_html(act.doc).split("\n")[0].strip(),
        stereotypes=act.stereotype_names(),
        steps=steps,
        lanes=sorted({s.lane for s in steps if s.lane}),
        information_items=info,
        log_steps=[s.name for s in steps if s.kind == "action" and s.name.lower().startswith("log ")],
    )


# --------------------------------------------------------------------------- the notional event
@dataclass
class Condition:
    name: str
    illumination: str
    visibility_km: float
    atmospheric_factor: float  # multiplier on resolvable cycles (1.0 = clear day)


CONDITIONS = [
    Condition("day / clear", "day", 20.0, 1.00),
    Condition("day / haze", "day", 8.0, 0.90),
    Condition("night / clear", "night", 20.0, 0.93),
    Condition("night / haze", "night", 8.0, 0.80),
]


@dataclass
class SensorModel:
    """Notional EO/IR performance used to generate data. None of these values are in the model."""

    name: str
    ifov_mrad: float = 0.122  # instantaneous field of view per detector
    target_critical_dimension_m: float = 2.3  # vehicle-class target
    n50_identify: float = 6.4  # Johnson/TTP cycles for 50 % identification
    cycle_noise_sigma: float = 0.10  # lognormal scatter on resolved cycles (jitter, focus, operator)
    spoof_detection_probability: float = 0.83  # Cyber Sentinel catches an injected frame


@dataclass
class Pass:
    run: int
    condition: str
    slant_range_m: float
    resolved_cycles: float
    p_identify: float
    identified: bool
    time_to_identify_s: float | None
    cyber_branch: bool
    spoof_detected: bool | None


def _p_identify(cycles: float, n50: float) -> float:
    ratio = cycles / n50
    e = 2.7 + 0.7 * ratio
    x = ratio**e
    return x / (1 + x)


STATIONS_M = [400.0, 500.0, 600.0, 650.0, 700.0, 750.0, 800.0, 900.0, 1000.0, 1200.0]


def simulate_passes(
    sensor: SensorModel, passes: int, seed: int, stations: list[float] = STATIONS_M, cyber_share: float = 0.25
) -> list[Pass]:
    """Test matrix: every condition x every target station, repeated until `passes` presentations are logged."""
    rng = random.Random(seed)
    out: list[Pass] = []
    matrix = [(c, s) for c in CONDITIONS for s in stations]
    for i in range(passes):
        cond, station = matrix[i % len(matrix)]
        r = station + rng.gauss(0.0, 12.0)  # surveyed station +/- air-vehicle position error
        cycles = (sensor.target_critical_dimension_m / r) / (2 * sensor.ifov_mrad * 1e-3) * cond.atmospheric_factor
        cycles *= math.exp(rng.gauss(0.0, sensor.cycle_noise_sigma))
        p = _p_identify(cycles, sensor.n50_identify)
        ident = rng.random() < p
        tti = round(rng.lognormvariate(math.log(4.0 + 6.0 * (1 - p)), 0.35), 1) if ident else None
        cyber = rng.random() < cyber_share
        spoof = (rng.random() < sensor.spoof_detection_probability) if cyber else None
        out.append(Pass(i + 1, cond.name, round(r, 1), round(cycles, 2), round(p, 3), ident, tti, cyber, spoof))
    return out


# --------------------------------------------------------------------------- MOP evaluation
@dataclass
class LogisticFit:
    a: float
    b: float  # P(x) = 1 / (1 + exp(-(a + b x)))
    n: int

    def p(self, x: float) -> float:
        return _sigmoid(self.a + self.b * x)

    def range_at(self, p: float) -> float:
        if self.b == 0:
            return float("nan")
        return (math.log(p / (1 - p)) - self.a) / self.b


def _sigmoid(t: float) -> float:
    if t >= 0:
        return 1 / (1 + math.exp(-t))
    e = math.exp(t)
    return e / (1 + e)


def fit_logistic(xs: list[float], ys: list[bool], iters: int = 60, ridge: float = 1e-3) -> LogisticFit:
    """Two-parameter logistic regression (Newton-Raphson on standardised x, light ridge so separable
    bootstrap samples stay finite)."""
    n = len(xs)
    mu = sum(xs) / n
    sd = math.sqrt(sum((x - mu) ** 2 for x in xs) / n) or 1.0
    zs = [(x - mu) / sd for x in xs]
    a, b = 0.0, 0.0
    for _ in range(iters):
        ps = [_sigmoid(a + b * z) for z in zs]
        ga = sum(p - float(y) for p, y in zip(ps, ys, strict=True)) + ridge * a
        gb = sum((p - float(y)) * z for p, y, z in zip(ps, ys, zs, strict=True)) + ridge * b
        w = [p * (1 - p) for p in ps]
        haa = sum(w) + ridge
        hab = sum(wi * z for wi, z in zip(w, zs, strict=True))
        hbb = sum(wi * z * z for wi, z in zip(w, zs, strict=True)) + ridge
        det = haa * hbb - hab * hab
        if abs(det) < 1e-12:
            break
        da = (hbb * ga - hab * gb) / det
        db = (haa * gb - hab * ga) / det
        step = max(1.0, abs(da) / 2, abs(db) / 2)
        a, b = a - da / step, b - db / step
        if abs(da) + abs(db) < 1e-9:
            break
    return LogisticFit(a - b * mu / sd, b / sd, n)


@dataclass
class MopResult:
    condition: str
    passes: int
    identified: int
    r90_m: float
    r90_ci_m: tuple[float, float]
    fit: LogisticFit
    meets_threshold: bool


def fit_intercept(xs: list[float], ys: list[bool], b: float, iters: int = 60, ridge: float = 1e-3) -> float:
    """Intercept-only logistic fit with the slope held at the pooled value (1-D Newton)."""
    a = 0.0
    for _ in range(iters):
        ps = [_sigmoid(a + b * x) for x in xs]
        g = sum(p - float(y) for p, y in zip(ps, ys, strict=True)) + ridge * a
        h = sum(p * (1 - p) for p in ps) + ridge
        da = g / h
        a -= da / max(1.0, abs(da) / 2)
        if abs(da) < 1e-9:
            break
    return a


def _fits(passes: list[Pass]) -> dict[str, LogisticFit]:
    """Pooled slope (the sensor's resolution roll-off), one intercept per condition (its shift)."""
    xs = [p.slant_range_m for p in passes]
    ys = [p.identified for p in passes]
    pooled = fit_logistic(xs, ys)
    fits = {"all conditions": pooled}
    for cond in sorted({p.condition for p in passes}):
        cx = [p.slant_range_m for p in passes if p.condition == cond]
        cy = [p.identified for p in passes if p.condition == cond]
        fits[cond] = LogisticFit(fit_intercept(cx, cy, pooled.b), pooled.b, len(cx))
    return fits


def evaluate_mop(passes: list[Pass], threshold: Threshold, p_target: float = 0.9, seed: int = 1, boot: int = 300) -> list[MopResult]:
    rng = random.Random(seed)
    fits = _fits(passes)
    limit = 3 * max(p.slant_range_m for p in passes)
    samples: dict[str, list[float]] = {c: [] for c in fits}
    for _ in range(boot):
        resampled = [passes[rng.randrange(len(passes))] for _ in passes]
        for cond, f in _fits(resampled).items():
            v = f.range_at(p_target)
            if cond in samples and math.isfinite(v):
                samples[cond].append(min(max(v, 0.0), limit))
    out: list[MopResult] = []
    for cond, fit in fits.items():
        ps = passes if cond == "all conditions" else [p for p in passes if p.condition == cond]
        s = sorted(samples[cond])
        lo = s[int(0.05 * len(s))] if s else float("nan")
        hi = s[int(0.95 * len(s)) - 1] if s else float("nan")
        out.append(
            MopResult(
                cond,
                len(ps),
                sum(p.identified for p in ps),
                round(fit.range_at(p_target), 1),
                (round(lo, 1), round(hi, 1)),
                fit,
                threshold.satisfied_by(lo),
            )
        )
    return out


def observed_bins(passes: list[Pass], width: float = 100.0) -> list[dict]:
    bins: dict[float, list[Pass]] = {}
    for p in passes:
        bins.setdefault(math.floor(p.slant_range_m / width) * width, []).append(p)
    return [
        {
            "range_from_m": lo,
            "range_to_m": lo + width,
            "passes": len(ps),
            "identified": sum(p.identified for p in ps),
            "p_observed": round(sum(p.identified for p in ps) / len(ps), 3),
        }
        for lo, ps in sorted(bins.items())
    ]


# --------------------------------------------------------------------------- verdict + report
def verdict(results: list[MopResult], threshold: Threshold) -> tuple[str, str]:
    overall = next(r for r in results if r.condition == "all conditions")
    per_cond = [r for r in results if r.condition != "all conditions"]
    failing = [r for r in per_cond if not r.meets_threshold]
    if overall.meets_threshold and not failing:
        return "pass", "R90 lower confidence bound meets the threshold in every tested condition."
    if overall.meets_threshold and failing:
        point_ok = all(threshold.satisfied_by(r.r90_m) for r in failing)
        return "inconclusive", (
            f"Pooled data meets the threshold but the 90 % lower bound does not in {', '.join(r.condition for r in failing)}"
            + (" (point estimates do; the per-condition sample is too small to bound R90)" if point_ok else "")
            + "; the requirement does not state the conditions under which 'effective resolution' is to be achieved, "
            + "so the verdict cannot be arbitrated."
        )
    return "fail", "R90 lower confidence bound is below the threshold on pooled data."


def model_gaps(req: Element, threshold: Threshold | None, proc: Procedure, verified: bool) -> list[dict[str, str]]:
    gaps: list[dict[str, str]] = []
    if threshold is None:
        gaps.append(
            {
                "severity": "error",
                "gap": "requirement has no parsable numeric threshold",
                "change": "State the threshold value, unit and direction in the requirement text or as a «Requirement» value property.",
            }
        )
    else:
        gaps.append(
            {
                "severity": "error",
                "gap": f"threshold '{threshold.phrase}' has no Measure of Performance in the model",
                "change": "Add a MOP value property (e.g. 'effective identification range : m') to the verifying TestCase or a "
                "«TestObjective», with the measurement method (P(ID) ≥ 0.9 from per-pass identification outcomes) "
                f"and the acceptance criterion {threshold}.",
            }
        )
    empty = [k for k, n in proc.information_items.items() if n == 0]
    if empty:
        gaps.append(
            {
                "severity": "error",
                "gap": f"{len(empty)} of {len(proc.information_items)} information items exchanged by the procedure have no attributes "
                f"({', '.join(empty[:4])}{' …' if len(empty) > 4 else ''})",
                "change": "Give the «ResourceInformation» classes the fields the test actually records (slant range, condition, "
                "identification outcome, time to identify, spoof detected) so the log format is defined by the model, "
                "not by the test team on the day.",
            }
        )
    if proc.log_steps and "TestLog" not in proc.stereotypes:
        gaps.append(
            {
                "severity": "warn",
                "gap": f"{len(proc.log_steps)} 'Log …' steps but no UTP «TestLog» / «Verdict» elements anywhere in the test model",
                "change": "Add a «TestLog» per execution with «TestLogEntry»s produced by the Log steps and a Verdict typed by the "
                "UTP Verdict enumeration, so results are model elements the RVTM can read.",
            }
        )
    if not verified:
        gaps.append(
            {
                "severity": "error",
                "gap": f"{req_id(req)} is refined by the procedure's activities but has no «Verify» relationship",
                "change": f"Add Verify from '{proc.name}' (or its owning TestCase) to {req_id(req)} {req.name}.",
            }
        )
    gaps.append(
        {
            "severity": "warn",
            "gap": "requirement does not state test conditions (illumination, visibility, target class, aspect)",
            "change": "Add the conditions as constraint properties or a «TestObjective» so the verdict is arbitrable when day and night "
            "results disagree.",
        }
    )
    return gaps


@dataclass
class EventResult:
    requirement: dict
    threshold: Threshold | None
    procedure: Procedure
    sensor: SensorModel
    passes: list[Pass]
    bins: list[dict]
    mop: list[MopResult]
    verdict: str
    arbitration: str
    gaps: list[dict[str, str]]
    written: list[Path] = field(default_factory=list)


def _is_verified(m: Model, req: Element) -> bool:
    for e in m.elements.values():
        if e.kind == "Abstraction" and e.has_stereotype("Verify") and req.id in e.refs.get("supplier", []):
            return True
    return False


def run(
    m: Model,
    requirement: str,
    procedure: str,
    out: Path | None,
    stem: str = "testevent",
    passes: int = 240,
    seed: int = 7,
    sensor: SensorModel | None = None,
) -> EventResult:
    req = find_requirement(m, requirement)
    if req is None:
        raise SystemExit(f"no requirement matching {requirement!r}")
    act = find_procedure(m, procedure)
    if act is None:
        raise SystemExit(f"no «TestProcedure»/«TestCase» matching {procedure!r}")
    text = req_text(req)
    threshold = parse_threshold(text)
    proc = read_procedure(m, act)
    sensor = sensor or SensorModel(name="notional EO/IR (no performance properties in the product model)")
    runs = simulate_passes(sensor, passes, seed)
    thr = threshold or Threshold(0.0, "", ">=", "")
    mop = evaluate_mop(runs, thr, seed=seed)
    v, why = verdict(mop, threshold) if threshold else ("error", "no threshold to evaluate against")
    res = EventResult(
        requirement={
            "id": req.id,
            "req_id": req_id(req),
            "name": req.name,
            "text": text,
            "project": req.project,
            "qualified": m.qualified_name(req.id),
        },
        threshold=threshold,
        procedure=proc,
        sensor=sensor,
        passes=runs,
        bins=observed_bins(runs),
        mop=mop,
        verdict=v,
        arbitration=why,
        gaps=model_gaps(req, threshold, proc, _is_verified(m, req)),
    )
    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
        res.written = write_outputs(res, out, stem)
    return res


def to_json(res: EventResult) -> dict:
    return {
        "requirement": res.requirement,
        "threshold": asdict(res.threshold) if res.threshold else None,
        "procedure": {**asdict(res.procedure), "steps": [asdict(s) for s in res.procedure.steps]},
        "sensor_model": {**asdict(res.sensor), "note": "notional; synthetic data"},
        "conditions": [asdict(c) for c in CONDITIONS],
        "passes": [asdict(p) for p in res.passes],
        "observed_bins": res.bins,
        "mop": [
            {
                "condition": r.condition,
                "passes": r.passes,
                "identified": r.identified,
                "r90_m": r.r90_m,
                "r90_ci90_m": list(r.r90_ci_m),
                "fit": {"a": r.fit.a, "b": r.fit.b},
                "meets_threshold": r.meets_threshold,
            }
            for r in res.mop
        ],
        "test_log": {
            "testProcedure": res.procedure.qualified,
            "requirement": f"{res.requirement['req_id']} {res.requirement['name']}",
            "executions": len(res.passes),
            "verdict": res.verdict,
            "arbitration": res.arbitration,
            "entries": [f"{s}: {n} entries" for s, n in _log_entries(res).items()],
            "note": "UTP-shaped log built by the simulation; no TestLog element exists in the model.",
        },
        "model_gaps": res.gaps,
    }


def _log_entries(res: EventResult) -> dict[str, int]:
    out: dict[str, int] = {}
    for s in res.procedure.log_steps:
        low = s.lower()
        if "spoof" in low or "cyber" in low:
            out[s] = sum(1 for p in res.passes if p.cyber_branch)
        elif "damage" in low or "impact" in low or "video" in low or "assessment" in low:
            out[s] = len(res.passes)
        else:
            out[s] = 1
    return out


def render_markdown(res: EventResult) -> str:
    r = res.requirement
    L = [f"# Simulated test event: {r['req_id']} {r['name']}", ""]
    L += [f"> {r['text']}", ""]
    L += [
        f'- Threshold read from the requirement: **{res.threshold}** ("{res.threshold.phrase}")'
        if res.threshold
        else "- No numeric threshold found",
        "",
    ]
    L += [
        f"- Test procedure (from the model): **{res.procedure.name}** — {len(res.procedure.steps)} steps across swimlanes "
        f"{', '.join(res.procedure.lanes) or '—'}"
    ]
    L += [
        f"- Information items exchanged: {len(res.procedure.information_items)} "
        f"({sum(1 for n in res.procedure.information_items.values() if n == 0)} with no attributes)",
        "",
    ]
    L += ["## Procedure steps (model)", ""]
    L += ["| # | kind | step | lane | in | out |", "|---|---|---|---|---|---|"]
    for s in res.procedure.steps:
        L.append(f"| {s.order} | {s.kind} | {s.name} | {s.lane} | {', '.join(s.inputs)} | {', '.join(s.outputs)} |")
    L += ["", "## Measure of Performance", ""]
    L += [
        "Effective identification range R90: slant range at which P(identify) = 0.9 from a logistic fit of per-pass outcomes; "
        "90 % bootstrap CI.",
        "",
    ]
    L += ["| condition | passes | identified | R90 (m) | 90 % CI | meets threshold |", "|---|---|---|---|---|---|"]
    for mr in res.mop:
        L.append(
            f"| {mr.condition} | {mr.passes} | {mr.identified} | {mr.r90_m:.0f} | {mr.r90_ci_m[0]:.0f}–{mr.r90_ci_m[1]:.0f} | "
            f"{'yes' if mr.meets_threshold else 'no'} |"
        )
    L += ["", f"**Verdict: {res.verdict.upper()}** — {res.arbitration}", ""]
    L += ["## Observed P(ID) by range bin", "", "| range (m) | passes | identified | P(ID) |", "|---|---|---|---|"]
    for b in res.bins:
        L.append(f"| {b['range_from_m']:.0f}–{b['range_to_m']:.0f} | {b['passes']} | {b['identified']} | {b['p_observed']:.2f} |")
    L += ["", "## What the model is missing to make this a real verification", ""]
    for g in res.gaps:
        L.append(f"- **[{g['severity']}]** {g['gap']} → {g['change']}")
    L += [
        "",
        f"_Synthetic data: {len(res.passes)} passes generated with a notional sensor model ({res.sensor.name}); "
        "nothing here is a measured MQ-99 result._",
    ]
    return "\n".join(L)


def write_outputs(res: EventResult, out: Path, stem: str) -> list[Path]:
    j = out / f"{stem}.json"
    j.write_text(json.dumps(to_json(res), indent=2, default=str))
    c = out / f"{stem}_runs.csv"
    with c.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(res.passes[0])))
        w.writeheader()
        for p in res.passes:
            w.writerow(asdict(p))
    md = out / f"{stem}.md"
    md.write_text(render_markdown(res))
    return [j, c, md]
