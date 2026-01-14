import json
import os
import time
from dataclasses import dataclass
from typing import Callable, Any
from confluent_kafka import Consumer, KafkaException
from pathlib import Path


@dataclass
class KafkaJsonCfg:
    bootstrap_servers: str
    topic: str
    group_id: str


def _write_ready_file():
    # Use env var so it works on Windows host AND in containers
    artifacts_dir = os.getenv("ARTIFACTS_DIR", r"C:\artifacts")
    ready_path = Path(artifacts_dir) / "consumer_ready.txt"

    ready_path.parent.mkdir(parents=True, exist_ok=True)
    ready_path.write_text("READY\n", encoding="utf-8")

    print(f"[READY] wrote: {ready_path.resolve()}")


def wait_for_json_event(
    cfg: KafkaJsonCfg,
    predicate: Callable[[dict[str, Any]], bool],
    timeout_s: int = 60,
    poll_s: float = 1.0,
    offset: str = "earliest",
) -> dict[str, Any]:
    consumer = Consumer({
        "bootstrap.servers": cfg.bootstrap_servers,
        "group.id": cfg.group_id,
        "auto.offset.reset": offset,
        "enable.auto.commit": False,
    })

    consumer.subscribe([cfg.topic])

    # Write READY after subscribe succeeds
    _write_ready_file()

    deadline = time.time() + timeout_s
    seen = 0

    try:
        while time.time() < deadline:
            msg = consumer.poll(poll_s)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            value = msg.value()
            if not value:
                continue

            try:
                event = json.loads(value.decode("utf-8"))
            except Exception:
                continue

            if seen < 5:
                print(f"[DEBUG] Kafka event: {event}")
                seen += 1

            if predicate(event):
                return event

        raise TimeoutError(f"No matching Kafka event found within {timeout_s}s")
    finally:
        consumer.close()
