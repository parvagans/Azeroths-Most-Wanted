import unittest

from wow.character import select_character_portrait_url


class CharacterMediaTests(unittest.TestCase):
    def test_avatar_is_preferred_when_blizzard_returns_both_assets(self):
        media = {
            "assets": [
                {"key": "main-raw", "value": "https://example.invalid/character-main-raw.png"},
                {"key": "avatar", "value": "https://example.invalid/character-avatar.jpg"},
            ]
        }

        self.assertEqual(
            select_character_portrait_url(media),
            "https://example.invalid/character-avatar.jpg",
        )

    def test_main_raw_remains_a_safe_fallback_when_avatar_is_missing(self):
        media = {
            "assets": [
                {"key": "main-raw", "value": "https://example.invalid/character-main-raw.png"},
            ]
        }

        self.assertEqual(
            select_character_portrait_url(media),
            "https://example.invalid/character-main-raw.png",
        )

    def test_missing_or_malformed_media_has_no_selected_portrait(self):
        self.assertIsNone(select_character_portrait_url(None))
        self.assertIsNone(select_character_portrait_url({"assets": [{"key": "avatar"}]}))


if __name__ == "__main__":
    unittest.main()
