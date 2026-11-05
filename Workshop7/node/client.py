"""Node component (client). Builds the JSON payloads, secures them, and calls the Master.

Quick end-to-end check from the project root:
    python -m node.client --master http://<MASTER_IP>:5000
"""
import argparse
import json
import time
import requests
from jsonschema import validate
from crypto.security import SecureChannel

KEYS_DIR = "crypto/keys"
JSON_HEADERS = {"Content-Type": "application/json"}


def load_channel() -> SecureChannel:
    return SecureChannel(
        private_key_path=f"{KEYS_DIR}/node_private.pem",
        peer_public_key_path=f"{KEYS_DIR}/master_public.pem",
    )


def load_schema(name: str) -> dict:
    with open(f"schemas/{name}") as f:
        return json.load(f)


def build_training_request(global_round: int, request_id: str) -> dict:
    return {
        "request_id": request_id,
        "global_round": global_round,
        "hyperparameters": {"learning_rate": 0.01, "batch_size": 32, "epochs": 3},
    }


def build_telemetry(request_id: str, node_id: str = "node-alpha-01") -> dict:
    # Activity 2 payload: no schema is defined for it on purpose
    return {"request_id": request_id, "node_id": node_id, "metrics_stream": [0.12, 0.45, 0.89, 0.33]}


def _ms(t0: float) -> float:
    return (time.perf_counter() - t0) * 1000


def post_exchange(master_url, path, payload, channel, request_schema=None, response_schema=None):
    """Sends one secured request and returns (decrypted_response, metrics).

    Metrics:
      bytes_sent / bytes_received / bytes_total : HTTP body sizes (JSON envelope), both directions
      rtt_ms                : full round trip seen by the client (network + server processing)
      server_processing_ms  : time the Master spent in decrypt/validate/encrypt (from header)
      network_ms_est        : rtt_ms - server_processing_ms (transfer time estimate)
      client_overhead_ms    : client-side validation + encryption + decryption
    """
    overhead_ms = 0.0

    if request_schema is not None:
        t0 = time.perf_counter()
        validate(instance=payload, schema=request_schema)
        overhead_ms += _ms(t0)

    t0 = time.perf_counter()
    envelope = channel.encrypt_and_sign(payload)
    overhead_ms += _ms(t0)

    body = json.dumps(envelope).encode("utf-8")

    t0 = time.perf_counter()
    resp = requests.post(master_url.rstrip("/") + path, data=body, headers=JSON_HEADERS, timeout=30)
    rtt_ms = _ms(t0)

    if resp.status_code != 200:
        raise RuntimeError(f"Master returned HTTP {resp.status_code}: {resp.text}")

    t0 = time.perf_counter()
    decrypted = channel.decrypt_and_verify(resp.json())
    overhead_ms += _ms(t0)

    if response_schema is not None:
        t0 = time.perf_counter()
        validate(instance=decrypted, schema=response_schema)
        overhead_ms += _ms(t0)

    server_ms = float(resp.headers.get("X-Server-Processing-ms", "nan"))
    metrics = {
        "bytes_sent": len(body),
        "bytes_received": len(resp.content),
        "bytes_total": len(body) + len(resp.content),
        "rtt_ms": round(rtt_ms, 3),
        "server_processing_ms": round(server_ms, 3),
        "network_ms_est": round(rtt_ms - server_ms, 3),
        "client_overhead_ms": round(overhead_ms, 3),
    }
    return decrypted, metrics


def main():
    ap = argparse.ArgumentParser(description="Single end-to-end check of both activities.")
    ap.add_argument("--master", default="http://localhost:5000")
    args = ap.parse_args()

    channel = load_channel()
    req_schema = load_schema("request_schema.json")
    res_schema = load_schema("response_schema.json")

    res, m = post_exchange(args.master, "/api/v1/activity1/train",
                           build_training_request(5, "req-fl-9901"), channel, req_schema, res_schema)
    print("Activity 1 response:", json.dumps(res, indent=2))
    print("Activity 1 metrics:", m)

    res, m = post_exchange(args.master, "/api/v2/activity2/telemetry",
                           build_telemetry("req-telemetry-001"), channel)
    print("Activity 2 response:", json.dumps(res, indent=2))
    print("Activity 2 metrics:", m)


if __name__ == "__main__":
    main()
