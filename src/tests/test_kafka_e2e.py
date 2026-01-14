import os
from src.utils.kafka_json import wait_for_json_event


def _touch_ready():
    ready_file = os.getenv("READY_FILE")
    if ready_file:
        os.makedirs(os.path.dirname(ready_file), exist_ok=True)
        with open(ready_file, "w", encoding="utf-8") as f:
            f.write("READY")
        print(f"[READY] Python consumer ready file written at {ready_file}")


def test_kafka_event_received(kafka_cfg, test_ctx):
    # MUST be first line
    _touch_ready()

    correlation_id = test_ctx["correlationId"]
    expected_name = test_ctx["expected"]["customerName"]

    print("[DEBUG] Context correlationId:", correlation_id)

    event = wait_for_json_event(
        kafka_cfg,
        predicate=lambda e: e.get("correlationId") == correlation_id,
        timeout_s=45,
        offset="earliest",  #  FIX
    )

    assert event["eventType"] == "CUSTOMER_CREATED"
    assert event["customerName"] == expected_name