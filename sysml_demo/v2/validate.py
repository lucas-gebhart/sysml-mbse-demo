"""Validate SysML v2 textual notation against the OMG pilot implementation.

Uses the `jupyter-sysml-kernel` (the pilot implementation's Jupyter kernel, which embeds
the reference parser + name resolver). Each call spins up one kernel and feeds it one or
more cells; the kernel reports parse errors and unresolved names as ERROR/WARNING lines.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_ENV = Path(os.environ.get("SYSML_ENV", str(Path.home() / "micromamba/envs/sysml")))
ERROR_RE = re.compile(r"^(ERROR|WARNING):(.*?)\s*\((\S+) line : (\d+) column : (\d+)\)\s*$", re.M)


@dataclass
class Diagnostic:
    level: str
    message: str
    line: int
    column: int
    cell: int = 1

    def __str__(self) -> str:
        return f"{self.level} cell {self.cell} line {self.line}:{self.column} {self.message}"


@dataclass
class ValidationResult:
    ok: bool
    diagnostics: list[Diagnostic] = field(default_factory=list)
    raw: str = ""
    published: list[str] = field(default_factory=list)

    @property
    def errors(self) -> list[Diagnostic]:
        return [d for d in self.diagnostics if d.level == "ERROR"]

    @property
    def warnings(self) -> list[Diagnostic]:
        return [d for d in self.diagnostics if d.level == "WARNING"]


def kernel_available(env: Path = DEFAULT_ENV) -> bool:
    return (env / "share/jupyter/kernels/sysml/kernel.json").exists() and shutil.which("java") is not None


def _env_for_kernel(env: Path) -> dict[str, str]:
    e = dict(os.environ)
    e["JUPYTER_PATH"] = str(env / "share/jupyter") + os.pathsep + e.get("JUPYTER_PATH", "")
    e["PATH"] = str(env / "bin") + os.pathsep + e.get("PATH", "")  # kernel.json calls the env's `java`
    return e


def validate(cells: list[str] | str, env: Path = DEFAULT_ENV, timeout: int = 300) -> ValidationResult:
    if isinstance(cells, str):
        cells = [cells]
    if not kernel_available(env):
        return ValidationResult(ok=False, raw="SysML v2 kernel not installed (see README: micromamba env 'sysml')")

    py = env / "bin/python"
    runner = Path(__file__).with_name("_kernel_runner.py")
    try:
        proc = subprocess.run(
            [str(py), str(runner)], input=json.dumps(cells), capture_output=True, text=True, env=_env_for_kernel(env), timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return ValidationResult(ok=False, raw=f"SysML v2 validation timed out after {timeout}s")
    if proc.returncode != 0 or "@@RESULT@@" not in proc.stdout:
        return ValidationResult(ok=False, raw=proc.stderr or proc.stdout)
    out = json.loads(proc.stdout.rsplit("@@RESULT@@", 1)[1])
    raw = "\n".join(out["outputs"])
    diags = [
        Diagnostic(m.group(1), m.group(2).strip(), int(m.group(4)), int(m.group(5)), _cell_index(m.group(3)))
        for m in ERROR_RE.finditer(raw)
    ]
    published = [ln for ln in raw.splitlines() if ln.startswith("Package ") or ln.startswith("Library ")]
    ok = not any(d.level == "ERROR" for d in diags) and not out.get("kernel_error")
    if out.get("kernel_error"):
        raw += "\n" + out["kernel_error"]
    return ValidationResult(ok=ok, diagnostics=diags, raw=raw, published=published)


def _cell_index(resource: str) -> int:
    m = re.match(r"(\d+)\.sysml", resource)
    return int(m.group(1)) if m else 1


def annotate(cells: list[str], result: ValidationResult, context: int = 1) -> str:
    """Return the offending lines with their diagnostics, for a human-readable report."""
    out = []
    for d in result.diagnostics:
        lines = cells[d.cell - 1].splitlines() if 0 < d.cell <= len(cells) else []
        lo, hi = max(0, d.line - 1 - context), min(len(lines), d.line + context)
        out.append(f"{d}")
        for i in range(lo, hi):
            marker = ">>" if i == d.line - 1 else "  "
            out.append(f"{marker} {i + 1:5d} | {lines[i]}")
        out.append("")
    return "\n".join(out)
