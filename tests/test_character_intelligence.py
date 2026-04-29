import unittest
from unittest import mock

from wow.character_intelligence import build_character_intelligence


class CharacterIntelligenceTests(unittest.TestCase):
    def test_labels_raid_ready_character(self):
        summary = build_character_intelligence(
            {
                "profile": {
                    "name": "Alpha",
                    "level": 70,
                    "equipped_item_level": 116,
                    "last_login_timestamp": 0,
                }
            }
        )

        self.assertEqual(summary["readiness_label"], "Raid ready")
        self.assertEqual(summary["readiness_meta"], "116 equipped iLvl")

    def test_labels_staging_and_recently_active_character(self):
        with mock.patch("wow.character_intelligence._utc_now_ms", return_value=20 * 24 * 60 * 60 * 1000):
            summary = build_character_intelligence(
                {
                    "profile": {
                        "name": "Bravo",
                        "level": 70,
                        "equipped_item_level": 103,
                        "last_login_timestamp": 10 * 24 * 60 * 60 * 1000,
                    }
                }
            )

        self.assertEqual(summary["readiness_label"], "Staging for raid")
        self.assertEqual(summary["activity_label"], "Recently active")
        self.assertEqual(summary["activity_meta"], "Last seen 10d ago")

    def test_labels_quiet_and_inactive_conservatively(self):
        with mock.patch("wow.character_intelligence._utc_now_ms", return_value=50 * 24 * 60 * 60 * 1000):
            quiet = build_character_intelligence(
                {
                    "profile": {
                        "name": "Quiet",
                        "level": 69,
                        "equipped_item_level": 95,
                        "last_login_timestamp": 25 * 24 * 60 * 60 * 1000,
                    }
                }
            )
            inactive = build_character_intelligence(
                {
                    "profile": {
                        "name": "Inactive",
                        "level": 60,
                        "equipped_item_level": 70,
                        "last_login_timestamp": 10 * 24 * 60 * 60 * 1000,
                    }
                }
            )

        self.assertEqual(quiet["activity_label"], "Quiet lately")
        self.assertEqual(inactive["activity_label"], "Inactive lately")
        self.assertEqual(quiet["readiness_label"], "Still advancing")

    def test_groups_recent_timeline_and_growth_deterministically(self):
        summary = build_character_intelligence(
            {
                "profile": {
                    "name": "Charlie",
                    "level": 70,
                    "equipped_item_level": 100,
                }
            },
            timeline_events=[
                {"character_name": "charlie", "type": "badge"},
                {"character_name": "Charlie", "type": "item"},
                {"character_name": "CHARLIE", "type": "item"},
                {"character_name": "Charlie", "type": "level_up"},
                {"character_name": "Delta", "type": "item"},
            ],
            history_rows=[
                {"record_date": "2026-04-20", "ilvl": 97, "hks": 10},
                {"record_date": "2026-04-29", "ilvl": 100, "hks": 14},
            ],
        )

        self.assertEqual(
            [item["label"] for item in summary["recent"]],
            [
                "2 gear upgrades recorded",
                "1 level-up recorded",
                "1 award recorded",
                "+3 iLvl across recorded history",
                "+4 HKs across recorded history",
            ],
        )

    def test_surfaces_existing_recognition_and_last_movement(self):
        summary = build_character_intelligence(
            {
                "profile": {
                    "name": "Echo",
                    "level": 70,
                    "equipped_item_level": 112,
                    "vanguard_badges": ["XP", "Loot"],
                    "campaign_badges": ["XP"],
                    "pve_champ_count": 1,
                    "pvp_champ_count": 2,
                }
            },
            membership_events=[
                {"character_name": "Echo", "event_type": "joined", "detected_at": "2026-04-20T12:00:00Z"},
                {"character_name": "echo", "event_type": "rejoined", "detected_at": "2026-04-29T12:00:00Z"},
            ],
        )

        self.assertEqual(
            [item["label"] for item in summary["recognition"]],
            [
                "PvE MVP x1, PvP MVP x2",
                "2 vanguard marks",
                "1 campaign mark",
            ],
        )
        self.assertEqual(summary["last_movement"]["label"], "Last movement: rejoined the guild")

    def test_returns_calm_empty_state_when_no_extra_intelligence_exists(self):
        summary = build_character_intelligence(
            {
                "profile": {
                    "name": "Foxtrot",
                    "level": 12,
                    "equipped_item_level": 0,
                }
            }
        )

        self.assertTrue(summary["empty"])
        self.assertEqual(summary["recent"], [])
        self.assertEqual(summary["recognition"], [])
        self.assertIsNone(summary["last_movement"])


if __name__ == "__main__":
    unittest.main()
