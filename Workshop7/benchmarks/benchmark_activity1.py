"""Activity 1: validated request/response. Measures bytes, latency and overhead.

    python -m benchmarks.benchmark_activity1 --master http://<MASTER_IP>:5000 --runs 30
"""
import argparse
from node.client import load_channel, load_schema, build_training_request, post_exchange
from benchmarks.common import summarize, save_csv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", default="http://localhost:5000")
    ap.add_argument("--runs", type=int, default=30)
    ap.add_argument("--warmup", type=int, default=3, help="runs discarded before measuring")
    ap.add_argument("--out", default="benchmarks/results/activity1.csv")
    args = ap.parse_args()

    channel = load_channel()
    req_schema = load_schema("request_schema.json")
    res_schema = load_schema("response_schema.json")
    path = "/api/v1/activity1/train"

    for i in range(args.warmup):
        post_exchange(args.master, path, build_training_request(i + 1, f"warm-{i}"),
                      channel, req_schema, res_schema)

    rows = []
    for i in range(1, args.runs + 1):
        rid = f"req-fl-{i:04d}"
        response, metrics = post_exchange(args.master, path,
                                          build_training_request(i, rid),
                                          channel, req_schema, res_schema)
        if response["request_id"] != rid:
            raise RuntimeError(f"Response for {rid} came back as {response['request_id']}")
        rows.append(metrics)

    summarize("ACTIVITY 1 (Schema Validated)", rows)
    save_csv(args.out, rows)


if __name__ == "__main__":
    main()
