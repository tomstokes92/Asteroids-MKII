import json
import os

DEFAULT_SETTINGS = {
    "volume": 50,
    "resolution": [1280, 720],
}

SETTINGS_PATH = "user_settings.json"

def load_settings(path: str = SETTINGS_PATH) -> dict:
    """Load settings from JSON; fall back to defaults if missing/broken."""
    if not os.path.exists(path):
        return DEFAULT_SETTINGS.copy()

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return DEFAULT_SETTINGS.copy()

    # Merge with defaults to support new keys later
    settings = DEFAULT_SETTINGS.copy()
    settings.update(data)

    # Basic validation / normalization
    settings["volume"] = int(max(0, min(100, settings.get("volume", 50))))

    res = settings.get("resolution", DEFAULT_SETTINGS["resolution"])
    if (
        isinstance(res, (list, tuple))
        and len(res) == 2
        and all(isinstance(x, int) for x in res)
        and res[0] > 0 and res[1] > 0
    ):
        settings["resolution"] = [res[0], res[1]]
    else:
        settings["resolution"] = DEFAULT_SETTINGS["resolution"][:]

    return settings


def save_settings(settings: dict, path: str = SETTINGS_PATH) -> None:
    """Save settings to JSON safely."""
    # Ensure JSON-friendly types
    data = dict(settings)
    if isinstance(data.get("resolution"), tuple):
        data["resolution"] = list(data["resolution"])

    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, path)