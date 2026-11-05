"""Shared helpers for the benchmarks: summary statistics and CSV export."""
import csv
import os
import statistics

NUMERIC_FIELDS = [
    "bytes_sent", "bytes_received", "bytes_total",
    "rtt_ms", "network_ms_est", "server_processing_ms", "client_overhead_ms",
]


def summarize(title: str, rows: list):
    print(f"\n--- {title} (n={len(rows)}) ---")
    for field in NUMERIC_FIELDS:
        values = [r[field] for r in rows if r[field] == r[field]]  # drop NaN
        if not values:
            continue
        mean = statistics.mean(values)
        stdev = statistics.stdev(values) if len(values) > 1 else 0.0
        print(f"{field:>22}: mean={mean:12.3f}  stdev={stdev:10.3f}")


def save_csv(path: str, rows: list):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["run"] + NUMERIC_FIELDS)
        writer.writeheader()
        for i, r in enumerate(rows, start=1):
            writer.writerow({"run": i, **{k: r[k] for k in NUMERIC_FIELDS}})
    print(f"[Bench] Raw results saved to {path}")
