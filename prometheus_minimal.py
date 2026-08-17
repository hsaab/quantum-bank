"""Minimal Prometheus text exposition (no prometheus_client dependency).

OWASP Dependency Check often misattributes Prometheus *server* CVEs to the
Python prometheus_client package. This module keeps /metrics compatible with
simple tests while avoiding that third-party surface in SCA.
"""

from __future__ import annotations

import threading
from collections import defaultdict

_lock = threading.Lock()
_counters: dict[tuple[str, tuple[tuple[str, str], ...]], int] = defaultdict(int)
_histograms: dict[tuple[str, tuple[tuple[str, str], ...]], dict[str, float | int]] = (
    defaultdict(lambda: {"sum": 0.0, "count": 0})
)


def _label_key(
    labelnames: tuple[str, ...], values: tuple[str, ...]
) -> tuple[tuple[str, str], ...]:
    return tuple(zip(labelnames, values, strict=True))


def _fmt_labels(parts: tuple[tuple[str, str], ...]) -> str:
    out = []
    for k, v in parts:
        esc = str(v).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        out.append(f'{k}="{esc}"')
    return ",".join(out)


class _CounterChild:
    __slots__ = ("_metric", "_lk")

    def __init__(self, metric_name: str, label_key: tuple[tuple[str, str], ...]):
        self._metric = (metric_name, label_key)
        self._lk = _lock

    def inc(self, amount: int = 1) -> None:
        with self._lk:
            _counters[self._metric] += int(amount)


class Counter:
    __slots__ = ("_name", "_doc", "_labelnames")

    def __init__(self, name: str, documentation: str, labelnames: list[str]):
        self._name = name
        self._doc = documentation
        self._labelnames = tuple(labelnames)

    def labels(self, *values: str) -> _CounterChild:
        lk = _label_key(self._labelnames, values)
        return _CounterChild(self._name, lk)


class _HistogramChild:
    __slots__ = ("_metric", "_lk")

    def __init__(self, metric_name: str, label_key: tuple[tuple[str, str], ...]):
        self._metric = (metric_name, label_key)
        self._lk = _lock

    def observe(self, value: float) -> None:
        with self._lk:
            h = _histograms[self._metric]
            h["sum"] = float(h["sum"]) + float(value)
            h["count"] = int(h["count"]) + 1


class Histogram:
    __slots__ = ("_name", "_doc", "_labelnames")

    def __init__(self, name: str, documentation: str, labelnames: list[str]):
        self._name = name
        self._doc = documentation
        self._labelnames = tuple(labelnames)

    def labels(self, *values: str) -> _HistogramChild:
        lk = _label_key(self._labelnames, values)
        return _HistogramChild(self._name, lk)


def format_metrics() -> str:
    lines: list[str] = []
    with _lock:
        snap_c = sorted(_counters.items(), key=lambda i: (i[0][0], i[0][1]))
        snap_h = sorted(_histograms.items(), key=lambda i: (i[0][0], i[0][1]))

    lines.append("# HELP app_request_count Application Request Count")
    lines.append("# TYPE app_request_count counter")
    for (mname, lk), val in snap_c:
        lab = _fmt_labels(lk)
        lines.append(f"{mname}{{{lab}}} {val}")

    lines.append("# HELP app_request_latency_seconds Application Request Latency")
    lines.append("# TYPE app_request_latency_seconds histogram")
    for (mname, lk), data in snap_h:
        lab = _fmt_labels(lk)
        cnt = int(data["count"])
        s = float(data["sum"])
        lines.append(f'{mname}_bucket{{{lab},le="+Inf"}} {cnt}')
        lines.append(f"{mname}_sum{{{lab}}} {s}")
        lines.append(f"{mname}_count{{{lab}}} {cnt}")

    return "\n".join(lines) + "\n"
