"""Master component (server). Run from the project root:
    python -m master.server
"""
import json
import time
from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError
from crypto.security import SecureChannel

app = Flask(__name__)

# Master decrypts/verifies with its private key and encrypts/signs for the node
crypto_channel = SecureChannel(
    private_key_path="crypto/keys/master_private.pem",
    peer_public_key_path="crypto/keys/node_public.pem",
)

with open("schemas/request_schema.json") as f:
    REQUEST_SCHEMA = json.load(f)
with open("schemas/response_schema.json") as f:
    RESPONSE_SCHEMA = json.load(f)


def _secure_response(res_payload: dict, t_start: float):
    """Encrypts the response and reports the server-side processing time in a header,
    so the client can separate network time from server processing time."""
    encrypted = crypto_channel.encrypt_and_sign(res_payload)
    overhead_ms = (time.perf_counter() - t_start) * 1000
    print(f"[Master] Processing overhead: {overhead_ms:.3f} ms")

    resp = jsonify(encrypted)
    resp.headers["X-Server-Processing-ms"] = f"{overhead_ms:.3f}"
    return resp, 200


@app.route("/api/v1/activity1/train", methods=["POST"])
def activity1_service():
    """Activity 1: request and response are both validated against JSON Schemas."""
    t_start = time.perf_counter()
    envelope = request.get_json(silent=True) or {}

    try:
        req_payload = crypto_channel.decrypt_and_verify(envelope)
    except Exception as e:
        return jsonify({"error": f"Cryptographic verification failed: {type(e).__name__} {e}"}), 400

    try:
        validate(instance=req_payload, schema=REQUEST_SCHEMA)
    except ValidationError as e:
        return jsonify({"error": f"Request JSON Schema validation failed: {e.message}"}), 422

    print(f"[Master] Valid request {req_payload['request_id']} for round {req_payload['global_round']}")

    res_payload = {
        "request_id": req_payload["request_id"],
        "node_id": "node-alpha-01",
        "status": "SUCCESS",
        "metrics": {
            "loss": 0.2415,
            "accuracy": 0.9420,
            "samples_processed": 1200,
            "training_time_seconds": 1.45,
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    validate(instance=res_payload, schema=RESPONSE_SCHEMA)

    return _secure_response(res_payload, t_start)


@app.route("/api/v2/activity2/telemetry", methods=["POST"])
def activity2_service():
    """Activity 2: no schema validation. Crypto is kept so the comparison is fair."""
    t_start = time.perf_counter()
    envelope = request.get_json(silent=True) or {}

    try:
        req_payload = crypto_channel.decrypt_and_verify(envelope)
    except Exception as e:
        return jsonify({"error": f"Cryptographic verification failed: {type(e).__name__} {e}"}), 400

    res_payload = {
        "request_id": req_payload.get("request_id", "unknown"),
        "node_id": "node-alpha-01",
        "status": "OK",
        "raw_telemetry": {
            "cpu_usage_pct": 45.2,
            "ram_used_mb": 1024,
            "temp_c": 54.0,
        },
    }
    return _secure_response(res_payload, t_start)


if __name__ == "__main__":
    # 0.0.0.0 so the Node on another machine can reach it. Allow port 5000 in the firewall.
    app.run(host="0.0.0.0", port=5000)
