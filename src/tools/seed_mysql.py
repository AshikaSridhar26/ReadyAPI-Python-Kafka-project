import os
import mysql.connector
import json
from pathlib import Path

ctx_path = Path(os.environ["TEST_CONTEXT_PATH"])
ctx = json.loads(ctx_path.read_text(encoding="utf-8"))

conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST","localhost"),
    port=int(os.getenv("MYSQL_PORT","3306")),
    database=os.getenv("MYSQL_DB","social_security"),
    user=os.getenv("MYSQL_USER","qa_user"),
    password=os.getenv("MYSQL_PASS","qa_pass")
)

cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS customers (
  customer_id VARCHAR(64) PRIMARY KEY,
  customer_name VARCHAR(255),
  correlation_id VARCHAR(64)
)
""")

cur.execute("""
INSERT INTO customers (customer_id, customer_name, correlation_id)
VALUES (%s, %s, %s)
ON DUPLICATE KEY UPDATE
customer_name=VALUES(customer_name),
correlation_id=VALUES(correlation_id)
""", (ctx["customerId"], ctx["expected"]["customerName"], ctx["correlationId"]))

conn.commit()
cur.close()
conn.close()

print("Seeded customer into MySQL")
