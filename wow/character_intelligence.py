"""Pure helpers for compact character-level intelligence summaries."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any


RECENT_ACTIVITY_WINDOW_DAYS = 14
QUIET_ACTIVITY_WINDOW_DAYS = 30
RAID_READY_ILVL = 110
STAGING_ILVL = 100
TIMELINE_ITEM_ORDER = ("item", "level_up", "badge", "movement", "growth")


def _clean_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _normalize_name(value: Any) -> str:
    return str(value or "").strip().lower()


def _utc_now_ms() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)


def _parse_timestamp_ms(value: Any) -> int | None:
    try:
        raw = int(value)
    except (TypeError, ValueError):
        return None
    return raw if raw > 0 else None


def _build_activity_state(character: dict[str, Any]) -> tuple[str, str | None]:
    profile = character.get("profile") if isinstance(character.get("profile"), dict) else {}
    equipped = character.get("equipped") if isinstance(character.get("equipped"), dict) else {}

    last_seen_ms = (
        _parse_timestamp_ms(profile.get("last_login_timestamp"))
        or _parse_timestamp_ms(character.get("last_login_ms"))
        or _parse_timestamp_ms(equipped.get("last_login_ms"))
    )
    if not last_seen_ms:
        return "Activity unknown", None

    age_days = max(0, (_utc_now_ms() - last_seen_ms) // (24 * 60 * 60 * 1000))
    if age_days <= RECENT_ACTIVITY_WINDOW_DAYS:
        return "Recently active", f"Last seen {age_days}d ago"
    if age_days <= QUIET_ACTIVITY_WINDOW_DAYS:
        return "Quiet lately", f"Last seen {age_days}d ago"
    return "Inactive lately", f"Last seen {age_days}d ago"


def _build_readiness_state(character: dict[str, Any]) -> tuple[str, str | None]:
    profile = character.get("profile") if isinstance(character.get("profile"), dict) else {}
    level = _clean_int(profile.get("level") or character.get("level"), 0)
    ilvl = _clean_int(profile.get("equipped_item_level") or character.get("equipped_item_level"), 0)

    if level < 70:
        return "Still advancing", f"Level {level}"
    if ilvl >= RAID_READY_ILVL:
        return "Raid ready", f"{ilvl} equipped iLvl"
    if ilvl >= STAGING_ILVL:
        return "Staging for raid", f"{ilvl} equipped iLvl"
    return "Needs gear", f"{ilvl} equipped iLvl"


def _build_recent_items(character_name: str, timeline_events: Any) -> list[dict[str, Any]]:
    counts = Counter()

    for row in timeline_events or []:
        if not isinstance(row, dict):
            continue
        if _normalize_name(row.get("character_name") or row.get("character")) != character_name:
            continue

        event_type = str(row.get("type") or row.get("event_type") or "").strip().lower()
        if event_type in {"item", "level_up", "badge"}:
            counts[event_type] += 1

    items: list[dict[str, Any]] = []
    if counts["item"] > 0:
        count = counts["item"]
        items.append({
            "type": "item",
            "label": f"{count} gear upgrade{'s' if count != 1 else ''} recorded",
            "tone": "positive",
        })
    if counts["level_up"] > 0:
        count = counts["level_up"]
        items.append({
            "type": "level_up",
            "label": f"{count} level-up{'s' if count != 1 else ''} recorded",
            "tone": "positive",
        })
    if counts["badge"] > 0:
        count = counts["badge"]
        items.append({
            "type": "badge",
            "label": f"{count} award{'s' if count != 1 else ''} recorded",
            "tone": "neutral",
        })

    return items


def _build_growth_items(history_rows: Any) -> list[dict[str, Any]]:
    rows = [row for row in (history_rows or []) if isinstance(row, dict)]
    if len(rows) < 2:
        return []

    sorted_rows = sorted(rows, key=lambda row: str(row.get("record_date") or ""))
    start = sorted_rows[0]
    end = sorted_rows[-1]

    ilvl_delta = _clean_int(end.get("ilvl"), 0) - _clean_int(start.get("ilvl"), 0)
    hks_delta = _clean_int(end.get("hks"), 0) - _clean_int(start.get("hks"), 0)

    items: list[dict[str, Any]] = []
    if ilvl_delta > 0:
        items.append({
            "type": "growth",
            "label": f"+{ilvl_delta} iLvl across recorded history",
            "tone": "positive",
        })
    if hks_delta > 0:
        items.append({
            "type": "growth",
            "label": f"+{hks_delta} HKs across recorded history",
            "tone": "positive",
        })

    return items


def _build_recognition_items(character: dict[str, Any]) -> list[dict[str, Any]]:
    profile = character.get("profile") if isinstance(character.get("profile"), dict) else {}

    vanguard_badges = profile.get("vanguard_badges") or character.get("vanguard_badges") or []
    campaign_badges = profile.get("campaign_badges") or character.get("campaign_badges") or []
    pve_champ_count = _clean_int(profile.get("pve_champ_count") or character.get("pve_champ_count"), 0)
    pvp_champ_count = _clean_int(profile.get("pvp_champ_count") or character.get("pvp_champ_count"), 0)

    items: list[dict[str, Any]] = []
    if pve_champ_count > 0 or pvp_champ_count > 0:
        parts = []
        if pve_champ_count > 0:
            parts.append(f"PvE MVP x{pve_champ_count}")
        if pvp_champ_count > 0:
            parts.append(f"PvP MVP x{pvp_champ_count}")
        items.append({
            "type": "mvp",
            "label": ", ".join(parts),
            "tone": "honor",
        })
    if len(vanguard_badges) > 0:
        items.append({
            "type": "vanguard",
            "label": f"{len(vanguard_badges)} vanguard mark{'s' if len(vanguard_badges) != 1 else ''}",
            "tone": "honor",
        })
    if len(campaign_badges) > 0:
        items.append({
            "type": "campaign",
            "label": f"{len(campaign_badges)} campaign mark{'s' if len(campaign_badges) != 1 else ''}",
            "tone": "honor",
        })

    return items


def _build_last_movement_item(character_name: str, membership_events: Any) -> dict[str, Any] | None:
    latest = None

    for row in membership_events or []:
        if not isinstance(row, dict):
            continue
        if _normalize_name(row.get("character_name")) != character_name:
            continue

        candidate = {
            "event_type": str(row.get("event_type") or "").strip().lower(),
            "detected_at": str(row.get("detected_at") or "").strip(),
        }
        if candidate["event_type"] not in {"joined", "rejoined", "departed"} or not candidate["detected_at"]:
            continue
        if latest is None or candidate["detected_at"] > latest["detected_at"]:
            latest = candidate

    if not latest:
        return None

    label_map = {
        "joined": "Last movement: joined the guild",
        "rejoined": "Last movement: rejoined the guild",
        "departed": "Last movement: departed the guild",
    }
    return {
        "type": "movement",
        "label": label_map[latest["event_type"]],
        "tone": "neutral",
    }


def build_character_intelligence(character, *, timeline_events=None, membership_events=None, badge_data=None, history_rows=None):
    """Build a compact, deterministic intelligence summary for one character.

    The helper only derives labels from existing roster/timeline/history inputs.
    It does not invent activity, readiness, or growth beyond what the supplied
    data can actually support.
    """
    if not isinstance(character, dict):
        return {
            "name": "",
            "activity_label": "Activity unknown",
            "activity_meta": None,
            "readiness_label": "Unknown",
            "readiness_meta": None,
            "recent": [],
            "recognition": [],
            "last_movement": None,
            "empty": True,
        }

    profile = character.get("profile") if isinstance(character.get("profile"), dict) else {}
    name = str(profile.get("name") or character.get("name") or "").strip()
    normalized_name = _normalize_name(name)

    merged_character = dict(character)
    if isinstance(badge_data, dict):
        merged_character.update(badge_data)
        merged_profile = dict(profile)
        merged_profile.update({k: v for k, v in badge_data.items() if k not in {"profile", "equipped"}})
        merged_character["profile"] = merged_profile

    activity_label, activity_meta = _build_activity_state(merged_character)
    readiness_label, readiness_meta = _build_readiness_state(merged_character)

    recent_items = _build_recent_items(normalized_name, timeline_events)
    recent_items.extend(_build_growth_items(history_rows))
    recent_items.sort(key=lambda item: (TIMELINE_ITEM_ORDER.index(item["type"]), item["label"]))

    recognition_items = _build_recognition_items(merged_character)
    movement_item = _build_last_movement_item(normalized_name, membership_events)

    return {
        "name": name,
        "activity_label": activity_label,
        "activity_meta": activity_meta,
        "readiness_label": readiness_label,
        "readiness_meta": readiness_meta,
        "recent": recent_items,
        "recognition": recognition_items,
        "last_movement": movement_item,
        "empty": not recent_items and not recognition_items and movement_item is None,
    }
