# Workshop 7: Data-interchange using JSON (Secure FL System)

Distributed Systems, Yachay Tech. Master (server) and Node (client) exchange JSON over
hybrid RSA-2048 + AES-256-GCM with RSA-PSS signatures. Two activities are measured:
Activity 1 (JSON Schema validated) and Activity 2 (no schema).

## Setup (both machines)

```bash
pip install -r requirements.txt
```

All commands run from the project root.

## Keys

Generate the keys once, on the machine where you prepare the project:

```bash
python -m crypto.generate_keys
```

Then distribute them. Private keys never leave their machine:

| File | Master machine | Node machine |
|---|---|---|
| `master_private.pem` | yes | no |
| `master_public.pem` | yes | yes (copy it) |
| `node_private.pem` | no | yes |
| `node_public.pem` | yes (copy it) | yes |

## Run on two machines

1. **Master (Machine 1):** find its LAN IP (`ipconfig` on Windows, `hostname -I` on Linux), allow inbound TCP 5000 in the firewall, then:
   ```bash
   python -m master.server
   ```
2. **Node (Machine 2):** quick check, then the benchmarks:
   ```bash
   python -m node.client --master http://<MASTER_IP>:5000
   python -m benchmarks.benchmark_activity1 --master http://<MASTER_IP>:5000 --runs 30
   python -m benchmarks.benchmark_activity2 --master http://<MASTER_IP>:5000 --runs 30
   ```

Raw per-run data is written to `benchmarks/results/*.csv`. Use it for the report.

## What is measured

| Metric | Definition |
|---|---|
| `bytes_sent` / `bytes_received` | HTTP body size of the JSON envelope in each direction |
| `bytes_total` | Sum of both directions |
| `rtt_ms` | Client-side round trip (network + Master processing) |
| `server_processing_ms` | Master time for decrypt, validate and encrypt (from the `X-Server-Processing-ms` header) |
| `network_ms_est` | `rtt_ms - server_processing_ms`. The transfer-latency estimate |
| `client_overhead_ms` | Client validation + encryption + decryption |

All timings come from the Node's clock. Nothing compares clocks between the two machines.

## Deviations from the spec and known limitations

- **Crypto scheme.** This follows the workshop spec (RSA-2048 + AES-GCM). The Project 1 protocol
  (DH, ECDSA P-256, HKDF, AES-256-GCM) is different. Confirm with the professor which one is required.
- **No replay protection.** The envelope has a random nonce, but the Master does not track seen
  nonces or timestamps. A captured valid envelope can be resent. Mention this in the discussion.
- **Signature covers only the plaintext JSON.** It is not bound to the envelope metadata.
- **Schema direction.** The schema comments say "Master → Node", but the code sends the request
  Node → Master (the Master returns the metrics). The code is implemented as written.
- **Activity 1 metrics are fixed values** in `master/server.py`, as in the spec. Real training is
  not part of this workshop.
- **Table 5.2 of the spec** contains example numbers, not measured results. Do not copy them into the report.
- **Activity 2 is "without a predefined schema"**, which we interpret as: the Master accepts any
  JSON payload and performs no validation. Confirm the interpretation with the professor.
