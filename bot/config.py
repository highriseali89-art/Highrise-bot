import os
import json

HIGHRISE_TOKEN = os.environ.get("HIGHRISE_TOKEN", "")
HIGHRISE_ROOM_ID = os.environ.get("HIGHRISE_ROOM_ID", "6894bd39e3e4a405517cb530")

ADMINS_FILE = os.path.join(os.path.dirname(__file__), "admins.json")
TELEPORT_FILE = os.path.join(os.path.dirname(__file__), "teleport.json")
ZONES_FILE = os.path.join(os.path.dirname(__file__), "zones.json")
VIPS_FILE = os.path.join(os.path.dirname(__file__), "vips.json")


def load_admins() -> list[str]:
    if os.path.exists(ADMINS_FILE):
        with open(ADMINS_FILE, "r") as f:
            return json.load(f)
    return []


def save_admins(admins: list[str]) -> None:
    with open(ADMINS_FILE, "w") as f:
        json.dump(admins, f)


def load_teleport() -> dict | None:
    if os.path.exists(TELEPORT_FILE):
        with open(TELEPORT_FILE, "r") as f:
            return json.load(f)
    return None


def save_teleport(data: dict) -> None:
    with open(TELEPORT_FILE, "w") as f:
        json.dump(data, f)


def delete_teleport() -> None:
    if os.path.exists(TELEPORT_FILE):
        os.remove(TELEPORT_FILE)


def load_zones() -> list[dict]:
    if os.path.exists(ZONES_FILE):
        with open(ZONES_FILE, "r") as f:
            return json.load(f)
    return []


def save_zones(zones: list[dict]) -> None:
    with open(ZONES_FILE, "w") as f:
        json.dump(zones, f)


def delete_all_zones() -> None:
    if os.path.exists(ZONES_FILE):
        os.remove(ZONES_FILE)


def load_vips() -> list[str]:
    if os.path.exists(VIPS_FILE):
        with open(VIPS_FILE, "r") as f:
            return json.load(f)
    return []


def save_vips(vips: list[str]) -> None:
    with open(VIPS_FILE, "w") as f:
        json.dump(vips, f)
