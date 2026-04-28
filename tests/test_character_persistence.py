import unittest

from wow.character_persistence import build_character_row_lookup, build_character_write_batch


class CharacterPersistenceTests(unittest.TestCase):
    def test_build_character_row_lookup_lowercases_names_and_keeps_latest_duplicate(self):
        rows = [
            {"name": "Alpha", "level": 60, "equipped_item_level": 100},
            {"name": "alpha", "level": 61, "equipped_item_level": 110},
            {"name": "Bravo", "level": 55, "equipped_item_level": 90},
        ]

        lookup = build_character_row_lookup(rows)

        self.assertEqual(sorted(lookup.keys()), ["alpha", "bravo"])
        self.assertEqual(lookup["alpha"]["level"], 61)
        self.assertEqual(lookup["alpha"]["equipped_item_level"], 110)
        self.assertEqual(lookup["bravo"]["level"], 55)

    def test_build_character_write_batch_returns_empty_when_state_is_unchanged(self):
        history_data = {
            "alpha": {
                "level": 60,
                "equipped_item_level": 100,
                "last_login_ms": 123,
                "honorable_kills": 5,
                "active_spec": "Frost",
            }
        }
        orig_chars = {
            "alpha": {
                "level": 60,
                "equipped_item_level": 100,
                "last_login_ms": 123,
                "honorable_kills": 5,
                "active_spec": "Frost",
                "vanguard_badges": "[]",
                "campaign_badges": "[]",
                "pve_champ_count": 0,
                "pvp_champ_count": 0,
            }
        }

        batch = build_character_write_batch(
            history_data,
            orig_chars,
            vanguard_tallies={},
            campaign_tallies={},
            pve_champs={},
            pvp_champs={},
        )

        self.assertEqual(batch, [])

    def test_build_character_write_batch_includes_updated_character_payload(self):
        history_data = {
            "alpha": {
                "level": 61,
                "class": "Mage",
                "race": "Human",
                "faction": "Alliance",
                "equipped_item_level": 111,
                "last_login_ms": 456,
                "portrait_url": "https://example.invalid/portrait.jpg",
                "active_spec": "Frost",
                "honorable_kills": 12,
                "health": 1000,
                "power": 500,
                "power_type": "MANA",
            }
        }
        orig_chars = {}

        batch = build_character_write_batch(
            history_data,
            orig_chars,
            vanguard_tallies={"alpha": ["Heroic"]},
            campaign_tallies={"alpha": ["Campaign"]},
            pve_champs={"alpha": 2},
            pvp_champs={"alpha": 1},
        )

        self.assertEqual(len(batch), 1)
        statement = batch[0]

        self.assertIn("INSERT OR REPLACE INTO characters", statement["q"])
        self.assertEqual(statement["params"][0], "alpha")
        self.assertEqual(statement["params"][1], 61)
        self.assertEqual(statement["params"][2], "Mage")
        self.assertEqual(statement["params"][3], "Human")
        self.assertEqual(statement["params"][4], "Alliance")
        self.assertEqual(statement["params"][-4], '["Heroic"]')
        self.assertEqual(statement["params"][-3], '["Campaign"]')
        self.assertEqual(statement["params"][-2], 2)
        self.assertEqual(statement["params"][-1], 1)


if __name__ == "__main__":
    unittest.main()
