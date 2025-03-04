"""
    © Jürgen Schoenemeyer, 04.03.2025 16:59

    src/main.py

    .venv/Scripts/activate
    python src/main.py

    pytest -v
"""

from __future__ import annotations

import math
import sys

from datetime import datetime

from helper.circular_buffer import CircularBuffer
from utils.trace import Trace

def test01() -> None:
    buf = CircularBuffer(8)

    for i in range(15):
        if buf.full():
            Trace.error(f"full:  {buf}")
            break

        value = {
            "index": i,
            "value": i * math.pi,
            "timestamp": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        }
        buf.write(value)
        Trace.info(f"write: {buf} '{value["value"]}'")

    for _i in range(10):
        if buf.empty():
            Trace.error(f"empty: {buf}")
            break

        result = buf.read()
        Trace.info(f"read:  {buf} -> '{result["value"]}'")

def main() -> None:
    test01()

if __name__ == "__main__":
    Trace.set( debug_mode=True, timezone=False )
    Trace.action(f"Python version {sys.version}")
    main()
