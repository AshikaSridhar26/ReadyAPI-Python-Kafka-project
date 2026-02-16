import os

import requests
from src.config_loader import load_config

from src.utils.context import load_test_context

def _touch_ready():
    ready_file = os.getenv("READY_FILE")
    if ready_file:
        os.makedirs(os.path.dirname(ready_file), exist_ok=True)
        with open(ready_file, "w", encoding="utf-8") as f:
            f.write("READY")
        print(f"[READY] Python consumer ready file written at {ready_file}")

def test_add_customer_readyapi_flow():
    cfg = load_config()
    ctx = load_test_context()

    # These come from ReadyAPI
    customer_id = ctx["customerId"]
    correlation_id = ctx["correlationId"]
    expected_name = ctx["expected"]["customerName"]

   
    #assert customer_id
    #assert correlation_id
    assert expected_name
