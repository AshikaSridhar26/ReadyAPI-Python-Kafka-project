import time
from utils.kafka_json import KafkaJsonCfg, wait_for_json_event

def test_missing_correlation_id_not_matched():
    kcfg = KafkaJsonCfg(
        bootstrap_servers="localhost:9092",
        topic="customer.events",
        group_id="qa-neg-" + str(int(time.time()*1000)),
    )

    target = "SHOULD-NOT-EXIST"

    try:
        wait_for_json_event(
            kcfg,
            predicate=lambda e: e.get("correlationId") == target,
            timeout_s=10,
            offset="latest",
        )
        assert False, "Unexpectedly matched an event"
    except TimeoutError:
        assert True
