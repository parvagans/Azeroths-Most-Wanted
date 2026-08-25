import json
import subprocess
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from wow.character_intelligence import CHARACTER_INACTIVITY_DAYS
from wow.character_intelligence import RECENT_ACTIVITY_WINDOW_DAYS
from wow.character_intelligence import get_character_activity_state


class CharacterActivityTests(unittest.TestCase):
    def setUp(self):
        self.reference_time = datetime(2026, 8, 25, 12, 0, tzinfo=timezone.utc)

    def _status_at_age(self, age):
        return get_character_activity_state(
            {"profile": {"last_login_timestamp": self.reference_time - age}},
            reference_time=self.reference_time,
        )[0]

    def test_canonical_activity_boundaries(self):
        self.assertEqual(RECENT_ACTIVITY_WINDOW_DAYS, 14)
        self.assertEqual(CHARACTER_INACTIVITY_DAYS, 60)
        self.assertEqual(self._status_at_age(timedelta(days=14)), "active")
        self.assertEqual(self._status_at_age(timedelta(days=15)), "quiet")
        self.assertEqual(self._status_at_age(timedelta(days=59)), "quiet")
        self.assertEqual(self._status_at_age(timedelta(days=60)), "inactive")
        self.assertEqual(self._status_at_age(timedelta(days=61)), "inactive")

    def test_timezone_aware_comparison_handles_dst_by_elapsed_time(self):
        berlin = ZoneInfo("Europe/Berlin")
        reference_time = datetime(2026, 4, 30, 12, 0, tzinfo=berlin)
        last_seen = datetime(2026, 3, 1, 12, 0, tzinfo=berlin)

        status, age = get_character_activity_state(
            {"profile": {"last_login_timestamp": last_seen}},
            reference_time=reference_time,
        )

        self.assertEqual(age, timedelta(days=59, hours=23))
        self.assertEqual(status, "quiet")

    def test_missing_or_naive_last_seen_remains_unknown(self):
        self.assertEqual(
            get_character_activity_state({"profile": {}}, reference_time=self.reference_time)[0],
            "unknown",
        )
        self.assertEqual(
            get_character_activity_state(
                {"profile": {"last_login_timestamp": datetime(2026, 8, 1, 12, 0)}},
                reference_time=self.reference_time,
            )[0],
            "unknown",
        )
        self.assertEqual(
            get_character_activity_state(
                {"profile": {"last_login_timestamp": "not-a-timestamp"}},
                reference_time=self.reference_time,
            )[0],
            "unknown",
        )


class CurrentLeaderboardActivityTests(unittest.TestCase):
    def test_shared_js_ranking_uses_activity_priority_for_pve_and_pvp(self):
        data_js = Path("render/src/js/core/data.js").resolve()
        now_ms = int(datetime(2026, 8, 25, 12, 0, tzinfo=timezone.utc).timestamp() * 1000)
        day_ms = 24 * 60 * 60 * 1000
        characters = [
            {"profile": {"name": "Inactive A", "equipped_item_level": 125, "honorable_kills": 12000, "last_login_timestamp": now_ms - 61 * day_ms}},
            {"profile": {"name": "Quiet B", "equipped_item_level": 115, "honorable_kills": 4500, "last_login_timestamp": now_ms - 59 * day_ms}},
            {"profile": {"name": "Inactive D", "equipped_item_level": 120, "honorable_kills": 7000, "last_login_timestamp": now_ms - 60 * day_ms}},
            {"profile": {"name": "Quiet C", "equipped_item_level": 114, "honorable_kills": 5000, "last_login_timestamp": now_ms - 15 * day_ms}},
            {"profile": {"name": "Active E", "equipped_item_level": 113, "honorable_kills": 3000, "last_login_timestamp": now_ms - day_ms}},
            {"profile": {"name": "Active F", "equipped_item_level": 112, "honorable_kills": 3500, "last_login_timestamp": now_ms - 14 * day_ms}},
            {"profile": {"name": "Active G", "equipped_item_level": 111, "honorable_kills": 2500, "last_login_timestamp": now_ms}},
            {"profile": {"name": "Unknown U", "equipped_item_level": 130, "honorable_kills": 20000}},
        ]
        node_script = f"""
const fs = require('fs');
const vm = require('vm');
const context = {{ window: {{
  CHARACTER_INACTIVITY_THRESHOLD_DAYS: 60,
  CHARACTER_RECENT_ACTIVITY_WINDOW_DAYS: 14
}} }};
vm.createContext(context);
vm.runInContext(fs.readFileSync({json.dumps(str(data_js))}, 'utf8'), context);
context.characters = {json.dumps(characters)};
context.nowMs = {now_ms};
const pve = vm.runInContext(
  "rankCurrentLeaderboardCharacters(characters, c => c.profile.equipped_item_level, nowMs).map(c => c.profile.name)",
  context
);
const pvp = vm.runInContext(
  "rankCurrentLeaderboardCharacters(characters, c => c.profile.honorable_kills, nowMs).map(c => c.profile.name)",
  context
);
const boundaryStates = [14, 15, 59, 60, 61].map(days => vm.runInContext(
  `getCharacterActivityState({{ profile: {{ last_login_timestamp: nowMs - ${{days}} * 86400000 }} }}, nowMs).status`,
  context
));
process.stdout.write(JSON.stringify({{ pve, pvp, boundaryStates }}));
"""
        completed = subprocess.run(
            ["node", "-e", node_script],
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(completed.stdout)

        self.assertEqual(
            result["pve"],
            ["Active E", "Active F", "Active G", "Quiet B", "Quiet C", "Inactive A", "Inactive D", "Unknown U"],
        )
        self.assertEqual(
            result["pvp"],
            ["Active F", "Active E", "Active G", "Quiet C", "Quiet B", "Inactive A", "Inactive D", "Unknown U"],
        )
        self.assertEqual(result["boundaryStates"], ["active", "quiet", "quiet", "inactive", "inactive"])
        self.assertEqual(list(enumerate(result["pve"][:3], start=1)), [(1, "Active E"), (2, "Active F"), (3, "Active G")])

    def test_current_ranking_surfaces_use_shared_helper_and_recalculate_ranks(self):
        script = Path("render/script.js").read_text(encoding="utf-8")
        selectors = Path("render/src/js/features/home_analytics/analytics_selectors.js").read_text(encoding="utf-8")
        analytics = Path("render/src/js/features/home_analytics/analytics_cards.js").read_text(encoding="utf-8")
        ladder = Path("render/src/js/features/ladder/ladder_shell.js").read_text(encoding="utf-8")

        self.assertGreaterEqual(script.count("rankCurrentLeaderboardCharacters("), 7)
        self.assertGreaterEqual(selectors.count("rankCurrentLeaderboardCharacters("), 2)
        self.assertIn("const hkEntries = rankCurrentLeaderboardCharacters(", analytics)
        self.assertIn("const biggestMover = rankCurrentLeaderboardCharacters(", ladder)
        self.assertIn("const rank = index + 1;", script)
        self.assertIn("rankNumber = index + 1;", script)


if __name__ == "__main__":
    unittest.main()
