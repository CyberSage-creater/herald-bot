# ===== Herald Symbol Cycle v3.0 =====
# Dual symbols per window: (Elemental, Natural) + ready-to-use joined tag.
HERALD_SYMBOLS = {
    "morning": {
        "elemental": "☀️",
        "natural": "🌱",
        "tag": "☀️🌱",
        "line": "The dawn returns. What you tend now will grow."
    },
    "afternoon": {
        "elemental": "⚡",
        "natural": "🌿",
        "tag": "⚡🌿",
        "line": "The day endures. The Grove learns through each spark."
    },
    "evening": {
        "elemental": "🌙",
        "natural": "💧",
        "tag": "🌙💧",
        "line": "The Grove listens. What was spoken in light, rests in water."
    },
}

# Optional: allow override via env (e.g., HERALD_TZ="America/Vancouver")
import os
from datetime import datetime
try:
    from zoneinfo import ZoneInfo  # Py3.9+
except Exception:
    ZoneInfo = None

HERALD_TZ = os.getenv("HERALD_TZ", "America/Vancouver")

def _now_local():
    if ZoneInfo:
        return datetime.now(ZoneInfo(HERALD_TZ))
    # Fallback to naive local time if zoneinfo unavailable
    return datetime.now()

def infer_period_from_now(dt=None):
    """
    Returns one of: 'morning', 'afternoon', 'evening'
    Morning: 05;
    """
