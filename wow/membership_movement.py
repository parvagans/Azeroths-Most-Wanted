"""Pure helpers for guild membership movement detection."""

from __future__ import annotations

from typing import Any, Iterable

EVENT_TYPE_PRIORITY = {
    "joined": 0,
    "rejoined": 1,
    "departed": 2,
}

KNOWN_STATUSES = {"active", "departed"}


def _normalize_name(value: Any) -> str | None:
    clean = str(value or "").strip()
    return clean.lower() or None


def _format_display_name(candidate: Any, normalized_name: str) -> str:
    clean = str(candidate or "").strip()
    if clean and clean != clean.lower() and clean != clean.upper():
        return clean
    return normalized_name.title()


def _extract_name_fields(row: Any) -> tuple[str | None, str | None]:
    if isinstance(row, dict):
        candidate = row.get("character_name") or row.get("name") or row.get("display_name")
        display_name = row.get("display_name") or row.get("character_name") or row.get("name")
        return _normalize_name(candidate), display_name

    return _normalize_name(row), row


def _normalize_status(value: Any) -> str | None:
    clean = str(value or "").strip().lower()
    return clean if clean in KNOWN_STATUSES else None


def _coerce_current_names(current_names: Iterable[Any]) -> dict[str, str]:
    current_map: dict[str, str] = {}

    for row in current_names or []:
        normalized_name, display_name = _extract_name_fields(row)
        if not normalized_name or normalized_name in current_map:
            continue

        current_map[normalized_name] = _format_display_name(display_name, normalized_name)

    return current_map


def _coerce_previous_status_rows(previous_status_rows: Iterable[Any]) -> dict[str, dict[str, Any]]:
    previous_map: dict[str, dict[str, Any]] = {}

    for row in previous_status_rows or []:
        if not isinstance(row, dict):
            continue

        normalized_name, display_name = _extract_name_fields(row)
        if not normalized_name or normalized_name in previous_map:
            continue

        status = _normalize_status(row.get("status") or row.get("current_status") or row.get("previous_status"))
        previous_map[normalized_name] = {
            "display_name": _format_display_name(display_name, normalized_name),
            "status": status,
        }

    return previous_map


def build_membership_movement_events(current_names, previous_status_rows, *, scan_id, detected_at):
    """Build deterministic join/leave movement events from plain roster/status rows.

    Current names may be strings or dict-like rows containing `character_name`,
    `name`, or `display_name`. Previous rows may additionally carry a `status`
    field with values of `active` or `departed`.

    The returned events are sorted by event type priority, then by character name.
    """
    current_map = _coerce_current_names(current_names or [])
    previous_map = _coerce_previous_status_rows(previous_status_rows or [])

    events = []

    for normalized_name, display_name in current_map.items():
        previous_row = previous_map.get(normalized_name)
        previous_status = previous_row["status"] if previous_row else None

        if previous_status == "departed":
            events.append({
                "scan_id": scan_id,
                "character_name": display_name,
                "event_type": "rejoined",
                "detected_at": detected_at,
                "previous_status": previous_status,
                "current_status": "active",
            })
        elif previous_status == "active":
            continue
        else:
            events.append({
                "scan_id": scan_id,
                "character_name": display_name,
                "event_type": "joined",
                "detected_at": detected_at,
                "previous_status": previous_status,
                "current_status": "active",
            })

    current_names_set = set(current_map)
    for normalized_name, previous_row in previous_map.items():
        if normalized_name in current_names_set:
            continue

        if previous_row["status"] != "active":
            continue

        events.append({
            "scan_id": scan_id,
            "character_name": previous_row["display_name"],
            "event_type": "departed",
            "detected_at": detected_at,
            "previous_status": "active",
            "current_status": "departed",
        })

    events.sort(key=lambda event: (
        EVENT_TYPE_PRIORITY.get(event["event_type"], 99),
        event["character_name"].lower(),
    ))

    return events
