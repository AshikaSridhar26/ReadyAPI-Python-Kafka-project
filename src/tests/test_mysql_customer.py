import os
from src.config_loader import load_config
from src.utils.context import load_test_context
from src.utils.mysql_wait import wait_for_customer_row

def test_customer_in_mysql(mysql_conn, test_ctx):
    cfg = load_config()
    ctx = load_test_context()

    customer_id = ctx["customerId"]
    expected_name = ctx["expected"]["customerName"]
    correlation_id = ctx["correlationId"]

    row = wait_for_customer_row(
        host=os.getenv("MYSQL_HOST", cfg["db"]["host"]),
        port=int(os.getenv("MYSQL_PORT", cfg["db"]["port"])),
        database=os.getenv("MYSQL_DB", cfg["db"]["database"]),
        user=os.getenv("MYSQL_USER", cfg["db"]["user"]),
        password=os.getenv("MYSQL_PASS", cfg["db"]["password"]),
        customer_id=customer_id,
        timeout_s=45,
        poll_s=1.0
    )

    assert row["customer_name"] == expected_name
    assert row["correlation_id"] == correlation_id
