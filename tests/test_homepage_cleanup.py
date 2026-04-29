import unittest
from pathlib import Path


class HomepageCleanupTests(unittest.TestCase):
    def test_hero_logo_markup_and_styles_are_still_present(self):
        template_text = Path("render/dashboard_template.html").read_text(encoding="utf-8")
        css_text = Path("render/style.css").read_text(encoding="utf-8")

        self.assertIn('class="hero-logo-col"', template_text)
        self.assertIn('src="asset/amw.webp"', template_text)
        self.assertIn('.hero-logo-col .main-logo', css_text)

    def test_homepage_campaign_chronicle_surface_was_removed(self):
        template_text = Path("render/dashboard_template.html").read_text(encoding="utf-8")
        script_text = Path("render/script.js").read_text(encoding="utf-8")
        cards_text = Path("render/src/js/features/home_analytics/analytics_cards.js").read_text(encoding="utf-8")

        self.assertNotIn('analytics-intel-section-chronicle', template_text)
        self.assertNotIn('Campaign Chronicle', template_text)
        self.assertNotIn('Recent Campaign Activity', template_text)
        self.assertNotIn('Campaign Chronicle', script_text)
        self.assertNotIn('Recent Campaign Activity', script_text)
        self.assertNotIn('applyChronicleCard', cards_text)

    def test_character_dossier_timeline_support_remains_intact(self):
        script_text = Path("render/script.js").read_text(encoding="utf-8")

        self.assertIn('timeline-character-dossier', script_text)
        self.assertIn("title: `📜 ${formattedName}'s Recent Activity`", script_text)
        self.assertIn("subtitle: 'Recent loot drops, level gains, and earned honors recorded for this hero.'", script_text)


if __name__ == "__main__":
    unittest.main()
