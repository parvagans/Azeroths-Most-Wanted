from pathlib import Path
import unittest


class AnalyticsRenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template_text = Path("render/dashboard_template.html").read_text(encoding="utf-8")
        cls.style_text = Path("render/style.css").read_text(encoding="utf-8")
        cls.analytics_css = Path("render/src/css/features/analytics/analytics.css").read_text(encoding="utf-8")
        cls.analytics_cards_text = Path("render/src/js/features/home_analytics/analytics_cards.js").read_text(encoding="utf-8")
        cls.script_text = Path("render/script.js").read_text(encoding="utf-8")
        cls.html_dashboard_text = Path("render/html_dashboard.py").read_text(encoding="utf-8")

    def test_analytics_route_markup_and_scope_copy(self):
        template = self.template_text

        self.assertIn('id="analytics-view"', template)
        self.assertIn('class="analytics-hero-section"', template)
        self.assertIn('id="analytics-snapshot-section"', template)
        self.assertIn('class="analytics-snapshot-grid"', template)
        self.assertIn('analytics-kpi-wrapper', template)
        self.assertIn('class="analytics-pressure-grid"', template)
        self.assertIn('class="analytics-readiness-grid"', template)
        self.assertIn('class="analytics-spotlight-grid"', template)
        self.assertIn('class="analytics-quick-routes"', template)
        self.assertIn('id="analyticsActivityChart"', template)
        self.assertIn('id="roleDonutChart"', template)
        self.assertIn('id="levelDistChart"', template)
        self.assertIn('Scope: raw roster totals, mains-only readiness, roster-known levels, and processed detail-eligible intelligence.', template)
        self.assertIn('What changed since the previous scan?', template)
        self.assertIn('Guild Roster', template)
        self.assertIn('Active Mains', template)
        self.assertIn('Raid-Ready Mains', template)
        self.assertIn('Avg Level 70 iLvl', template)
        self.assertIn('Analytics', template)
        self.assertIn('Open Analytics', template)
        self.assertNotIn('Advanced Analytics', template)
        self.assertNotIn('https://github.com/parvagans/Azeroths-Most-Wanted', template)
        self.assertNotIn('Recent Campaign Activity', template)
        self.assertNotIn('Campaign Chronicle', template)

    def test_analytics_css_is_owning_its_route_styles(self):
        html_dashboard = self.html_dashboard_text
        analytics_css = self.analytics_css
        style_css = self.style_text
        analytics_cards = self.analytics_cards_text
        script_text = self.script_text

        self.assertIn('os.path.join(base_dir, "src", "css", "features", "search", "autocomplete.css")', html_dashboard)
        self.assertIn('os.path.join(base_dir, "src", "css", "features", "war_effort", "war_effort.css")', html_dashboard)
        self.assertIn('os.path.join(base_dir, "src", "css", "features", "character", "dossier.css")', html_dashboard)
        self.assertIn('os.path.join(base_dir, "src", "css", "features", "analytics", "analytics.css")', html_dashboard)

        self.assertIn('.analytics-view-container', analytics_css)
        self.assertIn('.analytics-hero-section', analytics_css)
        self.assertIn('.analytics-hero-scope', analytics_css)
        self.assertIn('.analytics-snapshot-section', analytics_css)
        self.assertIn('.analytics-snapshot-grid', analytics_css)
        self.assertIn('.analytics-snapshot-card', analytics_css)
        self.assertIn('.analytics-snapshot-status', analytics_css)
        self.assertIn('.analytics-snapshot-scope', analytics_css)
        self.assertIn('.analytics-pressure-card', analytics_css)
        self.assertIn('.analytics-route-card', analytics_css)
        self.assertIn('.command-shell-analytics-role', analytics_css)
        self.assertIn('body[data-route-family="analytics"]::before', analytics_css)
        self.assertIn('renderAnalyticsSnapshotStrip', analytics_cards)
        self.assertIn('formatAnalyticsSnapshotDelta', analytics_cards)
        self.assertIn("const cardEl = document.getElementById(cardId);", analytics_cards)
        self.assertIn("if (!cardEl) return;", analytics_cards)
        self.assertIn("const analyticsTrends = dashboardConfig.global_trends || {};", script_text)
        self.assertIn("renderAnalyticsSnapshotStrip({", script_text)
        self.assertIn("analytics-snapshot-section", script_text)
        self.assertIn(".analytics-snapshot-section, .analytics-summary-section, .analytics-intel-section", script_text)

        self.assertNotIn('.analytics-view-container', style_css)
        self.assertNotIn('.analytics-snapshot-section', style_css)
        self.assertNotIn('.analytics-snapshot-grid', style_css)
        self.assertNotIn('.analytics-snapshot-card', style_css)
        self.assertNotIn('.analytics-snapshot-status', style_css)
        self.assertNotIn('.analytics-snapshot-scope', style_css)
        self.assertNotIn('.analytics-pressure-card', style_css)
        self.assertNotIn('.analytics-route-card', style_css)
        self.assertNotIn('.command-shell-analytics-role', style_css)
        self.assertNotIn('analytics-', style_css)


if __name__ == "__main__":
    unittest.main()
