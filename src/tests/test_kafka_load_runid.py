import json
import os
import time
from confluent_kafka import Consumer
def _touch_ready():
    ready_file = os.getenv("READY_FILE")
    if ready_file:
        os.makedirs(os.path.dirname(ready_file), exist_ok=True)
        with open(ready_file, "w", encoding="utf-8") as f:
            f.write("READY")
        print(f"[READY] Python consumer ready file written at {ready_file}")

def test_kafka_load_by_runid():
    _touch_ready()
    run_id = os.getenv("RUN_ID")
    assert run_id, "RUN_ID env is required"

    expected = int(os.getenv("EXPECTED_EVENTS", "100"))
    topic = os.getenv("KAFKA_TOPIC", "customer.events")
    bootstrap = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")

    group_id = "qa-load-" + str(int(time.time()*1000))

    consumer = Consumer({
        "bootstrap.servers": bootstrap,
        "group.id": group_id,
        "auto.offset.reset": "latest",
        "enable.auto.commit": False,
    })
    consumer.subscribe([topic])

    deadline = time.time() + 90
    seen = 0

    try:
        while time.time() < deadline and seen < expected:
            msg = consumer.poll(1.0)
            if msg is None or msg.error():
                continue
            try:
                e = json.loads(msg.value().decode("utf-8"))
            except Exception:
                continue

            # Accept events only for this run_id
            if e.get("runId") == run_id or str(e.get("correlationId","")).startswith(run_id):
                seen += 1
    finally:
        consumer.close()

    assert seen >= expected, f"Expected {expected} events for run_id={run_id}, got {seen}"
