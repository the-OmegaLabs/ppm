import json
import os


def open_config(config_path: str) -> list:
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.loads(f.read())

    else:
        with open(config_path, "w", encoding="utf-8") as f:
            f.write("{}")
            config = {}

    return [config_path, config]


def save_config(config: list) -> None:
    with open(config[0], "w", encoding="utf-8") as f:
        f.write(json.dumps(config[1], ensure_ascii=False))


def set(config: list, key: str, content) -> list:
    config[1][key] = content
    return config


def get(config: list, key: str, fallback=None):
    content = config[1].get(key, fallback)

    return content
