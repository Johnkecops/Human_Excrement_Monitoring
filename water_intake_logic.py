#!/usr/bin/env python3
"""
Module: Water Intake Logic
Purpose: Core hydration assessment engine based on urine color and Bristol stool type
Author: Dr. Arli Aditya Parikesit (i3L University)
Date: 2026
References:
    Swastika N. et al. (2021). Water Intake Applet Based on Human Excrement.
    Jurnal Riset Informatika, 3(2), 109-118. DOI: 10.34288/jri.v3i2.56
"""

from __future__ import annotations

import os
from datetime import datetime

# ── Urine color palette ────────────────────────────────────────────────────────
# Indices 0-2 → Result 1 (Hydrated)
# Index 3     → Result 2 (Acceptable / mild dehydration)
# Index 4     → Result 3 (Dehydrated)
# Index 5     → Result 4 (Severely dehydrated)

URINE_COLORS: list[dict] = [
    {"id": 0, "hex": "#FEFCE8", "label": "Very pale yellow"},
    {"id": 1, "hex": "#FEF9C3", "label": "Pale yellow"},
    {"id": 2, "hex": "#FEF08A", "label": "Light yellow"},
    {"id": 3, "hex": "#FCD34D", "label": "Dark yellow"},
    {"id": 4, "hex": "#D97706", "label": "Amber"},
    {"id": 5, "hex": "#92400E", "label": "Dark brown"},
]

# ── Bristol stool type definitions ────────────────────────────────────────────
# Types 1,7 → Result 4 (Severe abnormalities)
# Types 2,6 → Result 3 (Mild abnormalities)
# Types 3,4 → Result 1 (Normal)
# Type 5    → Result 2 (Lack of fiber)

STOOL_TYPES: list[dict] = [
    {"type": 1, "label": "Separate hard lumps (like nuts)",          "severity": 4},
    {"type": 2, "label": "Sausage-shaped but lumpy",                 "severity": 3},
    {"type": 3, "label": "Sausage with surface cracks — Normal ✓",  "severity": 1},
    {"type": 4, "label": "Smooth, soft sausage or snake — Normal ✓","severity": 1},
    {"type": 5, "label": "Soft blobs with clear-cut edges",          "severity": 2},
    {"type": 6, "label": "Fluffy pieces with ragged edges (mushy)",  "severity": 3},
    {"type": 7, "label": "Liquid consistency, no solid pieces",      "severity": 4},
]

# ── Result definitions ─────────────────────────────────────────────────────────

_URINE_RESULTS: dict[int, dict] = {
    1: {
        "level": 1,
        "status": "Hydrated",
        "message": "You are hydrated.",
        "advice": "Keep up the good work!",
        "log_label": "Hydrated",
        "color": "#d4edda",
        "emoji": "💧",
    },
    2: {
        "level": 2,
        "status": "Acceptable",
        "message": "Healthy.",
        "advice": "But drink water soon~",
        "log_label": "Acceptable",
        "color": "#fff3cd",
        "emoji": "🟡",
    },
    3: {
        "level": 3,
        "status": "Dehydrated",
        "message": "You seem to be dehydrated.",
        "advice": "Please drink more water!",
        "log_label": "Dehydrated",
        "color": "#ffe0b2",
        "emoji": "⚠️",
    },
    4: {
        "level": 4,
        "status": "Severely Dehydrated",
        "message": "Oh no! You are severely dehydrated.",
        "advice": "Please drink water and consult a doctor.",
        "log_label": "Severely dehydrated",
        "color": "#f8d7da",
        "emoji": "🚨",
    },
}

_STOOL_RESULTS: dict[int, dict] = {
    1: {
        "level": 1,
        "status": "Normal",
        "message": "Your stool is normal.",
        "advice": "Keep up the good work!",
        "log_label": "Normal",
        "color": "#d4edda",
        "emoji": "✅",
    },
    2: {
        "level": 2,
        "status": "Lack of Fiber",
        "message": "You lack fiber.",
        "advice": "Try to eat some more fiber.",
        "log_label": "Lack of Fiber",
        "color": "#fff3cd",
        "emoji": "🟡",
    },
    3: {
        "level": 3,
        "status": "Mild Abnormality",
        "message": "Your stool is normal.",
        "advice": "But if it persists, please consult a doctor.",
        "log_label": "Mild Abnormalities",
        "color": "#ffe0b2",
        "emoji": "⚠️",
    },
    4: {
        "level": 4,
        "status": "Abnormal",
        "message": "Your stool is abnormal.",
        "advice": "Please seek medical attention.",
        "log_label": "Severe Abnormalities",
        "color": "#f8d7da",
        "emoji": "🚨",
    },
}


def get_urine_result(color_index: int) -> dict:
    """Map urine color button index (0–5) to a hydration result dict."""
    if color_index in (0, 1, 2):
        return _URINE_RESULTS[1]
    elif color_index == 3:
        return _URINE_RESULTS[2]
    elif color_index == 4:
        return _URINE_RESULTS[3]
    else:
        return _URINE_RESULTS[4]


def get_stool_result(stool_type: int) -> dict:
    """Map Bristol stool type (1–7) to a result dict."""
    severity_map = {1: 4, 2: 3, 3: 1, 4: 1, 5: 2, 6: 3, 7: 4}
    return _STOOL_RESULTS[severity_map[stool_type]]


# ── History log ───────────────────────────────────────────────────────────────

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.log")


def append_to_history(entry_type: str, label: str) -> None:
    """Append a timestamped entry to the flat-text history log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} - {entry_type} = {label}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as fh:
        fh.write(line)


def read_history() -> list[str]:
    """Return history log lines, newest entry first."""
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as fh:
        lines = [ln.strip() for ln in fh.readlines() if ln.strip()]
    return list(reversed(lines))


def clear_history() -> None:
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
