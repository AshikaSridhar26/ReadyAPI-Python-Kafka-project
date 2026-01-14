import requests
from typing import Dict, Any

def add_customer(base_url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calls AddCustomer API and returns JSON response
    """
    url = f"{base_url}/addCustomer"

    resp = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=10,
    )

    resp.raise_for_status()
    return resp.json()
