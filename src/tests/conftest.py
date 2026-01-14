import os
import json
import time
import pytest
from pathlib import Path

from src.config_loader import load_config
from src.utils.kafka_json import KafkaJsonCfg
import mysql.connector

from src.utils.addCustomer import add_customer


@pytest.fixture(scope="function")
def addcustomer(cfg, test_ctx):
    """
    Fixture that calls AddCustomer API using context data
    """
    base_url = cfg["api"]["base_url"]

    payload = {
        "customerId": test_ctx["customerId"],
        "customerName": test_ctx["expected"]["customerName"],
        "correlationId": test_ctx["correlationId"],
    }

    response = add_customer(base_url, payload)
    return response
@pytest.fixture(scope="session")
def cfg():
    return load_config()


@pytest.fixture(scope="session")
def test_ctx():
    ctx_path = os.getenv("TEST_CONTEXT_PATH", r"C:\artifacts\testContext.json")
    p = Path(ctx_path)
    if not p.exists():
        pytest.fail(f"TEST_CONTEXT_PATH not found: {ctx_path}")
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def kafka_cfg(cfg):
    bootstrap = os.getenv("KAFKA_BOOTSTRAP", cfg["kafka"]["bootstrap_servers"])
    topic = os.getenv("KAFKA_TOPIC", cfg["kafka"]["topic"])
    group_id = os.getenv("KAFKA_GROUP_ID", cfg["kafka"]["group_id"]) or ("qa-suite-" + str(int(time.time()*1000)))
    return KafkaJsonCfg(bootstrap_servers=bootstrap, topic=topic, group_id=group_id)


@pytest.fixture(scope="session")
def mysql_conn(cfg):
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", cfg["db"]["host"]),
        port=int(os.getenv("MYSQL_PORT", cfg["db"]["port"])),
        database=os.getenv("MYSQL_DB", cfg["db"]["database"]),
        user=os.getenv("MYSQL_USER", cfg["db"]["user"]),
        password=os.getenv("MYSQL_PASS", cfg["db"]["password"]),
    )
    yield conn
    conn.close()
@pytest.fixture(scope="function", autouse=True)
def db_rollback(mysql_conn, test_ctx):
    """
    Cleanup after each test: remove seeded customer row.
    Runs even if the test fails.
    """
    yield  # run the test first

    customer_id = test_ctx.get("customerId")
    if not customer_id:
        return

    try:
        cur = mysql_conn.cursor()
        cur.execute("DELETE FROM customers WHERE customer_id=%s", (customer_id,))
        mysql_conn.commit()
        cur.close()
    except Exception:
        # don't hide the real test failure because cleanup failed
        try:
            mysql_conn.rollback()
        except Exception:
            pass

