"""Activity 2: unvalidated exchange (no JSON Schema). Measures bytes, latency and overhead.

    python -m benchmarks.benchmark_activity2 --master http://<MASTER_IP>:5000 --runs 30
"""
import argparse
from node.client import load_channel, build_telemetry, post_exchange
from benchmarks.common import summarize, save_csv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", default="http://localhost:5000")
    ap.add_argument("--runs", type=int, default=30)
    ap.add_argument("--warmup", type=int, default=3, help="runs discarded before measuring")
    ap.add_argument("--out", default="benchmarks/results/activity2.csv")
    args = ap.parse_args()

    channel = load_channel()
    path = "/api/v2/activity2/telemetry"

    for i in range(args.warmup):
        post_exchange(args.master, path, build_telemetry(f"warm-{i}"), channel)

    rows = []
    for i in range(1, args.runs + 1):
        rid = f"req-telemetry-{i:04d}"
        response, metrics = post_exchange(args.master, path, build_telemetry(rid), channel)
        if response["request_id"] != rid:
            raise RuntimeError(f"Response for {rid} came back as {response['request_id']}")
        rows.append(metrics)

    summarize("ACTIVITY 2 (No Schema)", rows)
    save_csv(args.out, rows)


if __name__ == "__main__":
    main()
