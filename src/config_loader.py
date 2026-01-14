from pathlib import Path
import os
import yaml


def load_config():
    # points to src/
    base_dir = Path(__file__).resolve().parent  # <-- FIXED

    config_path = base_dir / "configs" / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"config.yaml not found at: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    cfg["api"]["base_url"] = os.getenv("API_BASE_URL", cfg["api"]["base_url"])

    cfg["db"]["host"] = os.getenv("MYSQL_HOST", cfg["db"]["host"])
    cfg["db"]["port"] = int(os.getenv("MYSQL_PORT", cfg["db"]["port"]))
    cfg["db"]["database"] = os.getenv("MYSQL_DB", cfg["db"]["database"])
    cfg["db"]["user"] = os.getenv("MYSQL_USER", cfg["db"]["user"])
    cfg["db"]["password"] = os.getenv("MYSQL_PASS", cfg["db"]["password"])

    cfg["elastic"]["url"] = os.getenv("ES_URL", cfg["elastic"]["url"])
    cfg["elastic"]["index"] = os.getenv("ES_INDEX", cfg["elastic"]["index"])

    cfg["kafka"]["bootstrap_servers"] = os.getenv("KAFKA_BOOTSTRAP", cfg["kafka"]["bootstrap_servers"])
    if "schema_registry_url" in cfg.get("kafka", {}):
        cfg["kafka"]["schema_registry_url"] = os.getenv("SCHEMA_REGISTRY_URL", cfg["kafka"]["schema_registry_url"])
    else:
        cfg["kafka"]["schema_registry_url"] = os.getenv("SCHEMA_REGISTRY_URL", "")

    cfg["kafka"]["topic"] = os.getenv("KAFKA_TOPIC", cfg["kafka"]["topic"])
    cfg["kafka"]["group_id"] = os.getenv("KAFKA_GROUP_ID", cfg["kafka"]["group_id"])

    return cfg
