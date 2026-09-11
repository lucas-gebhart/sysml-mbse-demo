"""Runs inside the `sysml` micromamba env: feeds cells to the SysML v2 kernel, returns JSON.

stdin:  JSON list of cell strings
stdout: {"outputs": [str, ...], "kernel_error": str|null}
"""

import json
import subprocess
import sys

from jupyter_client import KernelManager


def main() -> None:
    cells = json.loads(sys.stdin.read())
    km = KernelManager(kernel_name="sysml")
    km.start_kernel(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    kc = km.client()
    kc.start_channels()
    outputs: list[str] = []
    kernel_error = None
    try:
        kc.wait_for_ready(timeout=180)
        for code in cells:
            mid = kc.execute(code)
            while True:
                msg = kc.get_iopub_msg(timeout=600)
                if msg["parent_header"].get("msg_id") != mid:
                    continue
                t, c = msg["msg_type"], msg["content"]
                if t == "stream":
                    outputs.append(c["text"])
                elif t in ("execute_result", "display_data"):
                    outputs.append(str(c["data"].get("text/plain", "")))
                elif t == "error":
                    outputs.append("\n".join(c.get("traceback", [])))
                elif t == "status" and c["execution_state"] == "idle":
                    break
    except Exception as exc:  # noqa: BLE001 - report anything to the caller
        kernel_error = f"{type(exc).__name__}: {exc}"
    finally:
        kc.stop_channels()
        km.shutdown_kernel(now=True)
    sys.stdout.write("\n@@RESULT@@" + json.dumps({"outputs": outputs, "kernel_error": kernel_error}))


if __name__ == "__main__":
    main()
