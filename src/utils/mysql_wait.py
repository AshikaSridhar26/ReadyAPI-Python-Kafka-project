import time
from typing import Optional, Dict, Any
import mysql.connector

def wait_for_customer_row(
    host: str, port: int, database: str, user: str, password: str,
    customer_id: str,
    timeout_s: int = 30,
    poll_s: float = 1.0
) -> Dict[str, Any]:
    deadline = time.time() + timeout_s

    while time.time() < deadline:
        try:
            conn = mysql.connector.connect(
                host=host, port=port, database=database, user=user, password=password
            )
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT customer_id, customer_name, correlation_id FROM customers WHERE customer_id=%s",
                (customer_id,)
            )
            row = cur.fetchone()
            cur.close()
            conn.close()

            if row:
                return row
        except Exception:
            pass

        time.sleep(poll_s)

    raise TimeoutError(f"Customer row not found for customer_id={customer_id} within {timeout_s}s")
