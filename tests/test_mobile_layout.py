import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MobileLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = (ROOT / "render/dashboard_template.html").read_text(encoding="utf-8")
        cls.style = (ROOT / "render/style.css").read_text(encoding="utf-8")
        cls.mobile_css = (ROOT / "render/src/css/features/mobile/mobile.css").read_text(encoding="utf-8")
        cls.archive_css = (ROOT / "render/src/css/features/campaign/archive.css").read_text(encoding="utf-8")
        cls.analytics_css = (ROOT / "render/src/css/features/analytics/analytics.css").read_text(encoding="utf-8")
        cls.war_effort_css = (ROOT / "render/src/css/features/war_effort/war_effort.css").read_text(encoding="utf-8")
        cls.search_css = (ROOT / "render/src/css/features/search/autocomplete.css").read_text(encoding="utf-8")
        cls.dossier_css = (ROOT / "render/src/css/features/character/dossier.css").read_text(encoding="utf-8")
        cls.html_dashboard = (ROOT / "render/html_dashboard.py").read_text(encoding="utf-8")

    def test_mobile_foundation_stylesheet_is_loaded_last(self):
        html_dashboard = self.html_dashboard
        self.assertIn('"features", "mobile", "mobile.css"', html_dashboard)

        style_index = html_dashboard.index('os.path.join(base_dir, "style.css")')
        mobile_index = html_dashboard.index(
            'os.path.join(base_dir, "src", "css", "features", "mobile", "mobile.css")'
        )
        self.assertGreater(mobile_index, style_index)

    def test_mobile_nav_and_shell_rules_live_in_mobile_module(self):
        self.assertIn("mobile-menu-toggle", self.template)
        self.assertIn("nav-links-container", self.template)
        self.assertIn("nav-mobile-groups", self.template)

        self.assertIn("@media (max-width: 1024px) {", self.mobile_css)
        self.assertIn(".mobile-menu-toggle {\n    display: inline-flex;", self.mobile_css)
        self.assertIn(".nav-links-container {\n    position: fixed;", self.mobile_css)
        self.assertIn(".nav-links-container.open {\n    transform: translateX(0);", self.mobile_css)
        self.assertIn(".main-content {\n    padding-bottom: calc(24px + env(safe-area-inset-bottom, 0px));", self.mobile_css)

        self.assertNotIn(".mobile-menu-toggle {\n    display: inline-flex !important;", self.style)
        self.assertNotIn(".nav-links-container {\n    display: flex !important;", self.style)
        self.assertNotIn(".nav-mobile-groups {\n    display: flex !important;", self.style)

    def test_mobile_breakpoints_cover_small_phone_widths(self):
        for breakpoint in ("1024px", "920px", "760px", "640px", "430px", "412px", "390px", "360px"):
            self.assertIn(f"@media (max-width: {breakpoint})", self.mobile_css)

    def test_roster_and_metric_mobile_rules_are_readable(self):
        self.assertIn(".concise-row-inner {\n    display: grid;\n    grid-template-columns: 1fr;", self.mobile_css)
        self.assertIn(".c-main-info {\n    width: 100%;\n    grid-template-columns: 40px minmax(0, 1fr);", self.mobile_css)
        self.assertIn(".concise-row-stats-top {\n    width: 100%;\n    justify-content: flex-start;", self.mobile_css)
        self.assertIn(".stat-box-container {\n    display: grid;\n    grid-template-columns: repeat(2, minmax(0, 1fr));", self.mobile_css)
        self.assertIn(".stat-box-container {\n    grid-template-columns: 1fr;", self.mobile_css)
        self.assertIn(".command-shell-badges .command-info-band,", self.mobile_css)
        self.assertIn(".hall-stage-spotlight,\n  .hall-stage-wall {\n    grid-template-columns: 1fr;", self.mobile_css)

    def test_dossier_module_no_longer_owns_global_mobile_shell_rules(self):
        self.assertNotIn("@media (max-width: 1024px) {\n  .navbar {", self.dossier_css)
        self.assertNotIn(".mobile-menu-toggle {\n    display: inline-flex;", self.dossier_css)
        self.assertNotIn(".nav-links-container {\n    position: fixed;", self.dossier_css)
        self.assertNotIn(".concise-row-inner {\n    display: grid;", self.dossier_css)
        self.assertNotIn(".class-stat-container {\n    flex-wrap: nowrap !important;", self.dossier_css)

    def test_war_effort_and_archive_keep_route_specific_mobile_rules(self):
        self.assertIn(".war-effort-home-card-footer {\n    align-items: flex-start;\n    flex-direction: column;", self.war_effort_css)
        self.assertIn(".war-effort-home-track {\n    min-height: 48px;", self.war_effort_css)
        self.assertIn("@media (max-width: 412px) {", self.war_effort_css)
        self.assertIn(".campaign-archive-week-select {\n  min-width: 240px;", self.archive_css)
        self.assertIn(".campaign-archive-week-select {\n    width: 100%;", self.archive_css)
        self.assertIn(".campaign-archive-grid,\n  .campaign-archive-grid-war-effort,\n  .campaign-archive-grid-dual {\n    gap: 14px;\n    grid-template-columns: 1fr;", self.archive_css)

    def test_existing_module_ownership_and_public_cleanup_remain_intact(self):
        self.assertIn(".analytics-snapshot-section", self.analytics_css)
        self.assertNotIn(".analytics-snapshot-section", self.style)
        self.assertIn(".search-autocomplete", self.search_css)
        self.assertNotIn(".search-autocomplete", self.style)
        self.assertIn(".char-card-intelligence-shell", self.dossier_css)
        self.assertNotIn("github.com", self.template)
        self.assertNotIn("Source: GitHub", self.template)
        self.assertNotIn("Recent Campaign Activity", self.template)
        self.assertNotIn("Campaign Chronicle", self.template)
        self.assertNotIn("analytics-chronicle", self.style)


if __name__ == "__main__":
    unittest.main()
