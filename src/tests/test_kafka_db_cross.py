import os
import time
from src.utils.kafka_json import wait_for_json_event
from src.utils.mysql_wait import wait_for_customer_row


def _touch_ready():
    ready_file = os.getenv("READY_FILE")
    if ready_file:
        os.makedirs(os.path.dirname(ready_file), exist_ok=True)
        with open(ready_file, "w", encoding="utf-8") as f:
            f.write("READY")
        print(f"[READY] Python consumer ready file written at {ready_file}")


def test_kafka_db_cross(kafka_cfg, mysql_conn, test_ctx, cfg):
    _touch_ready()

    expected_customer_id = test_ctx["customerId"]
    expected_name = test_ctx["expected"]["customerName"]
    expected_correlation = test_ctx["correlationId"]

    print("[DEBUG] correlationId:", expected_correlation)

    # 1) Wait for Kafka event that matches correlationId
    event = wait_for_json_event(
        kafka_cfg,
        predicate=lambda e: e.get("correlationId") == expected_correlation,
        timeout_s=45,
        offset="latest",
    )

    assert event.get("eventType") == "CUSTOMER_CREATED"
    assert event.get("customerId") == expected_customer_id
    assert event.get("customerName") == expected_name

    # 2) Wait for DB row (eventual consistency)
 
    row = wait_for_customer_row(
        host=os.getenv("MYSQL_HOST", cfg["db"]["host"]),
        port=int(os.getenv("MYSQL_PORT", cfg["db"]["port"])),
        database=os.getenv("MYSQL_DB", cfg["db"]["database"]),
        user=os.getenv("MYSQL_USER", cfg["db"]["user"]),
        password=os.getenv("MYSQL_PASS", cfg["db"]["password"]),
        customer_id=expected_customer_id,
        timeout_s=45,
        poll_s=1.0,
    )

    assert row["customer_id"] == expected_customer_id
    assert row["customer_name"] == expected_name
    assert row["correlation_id"] == expected_correlation
