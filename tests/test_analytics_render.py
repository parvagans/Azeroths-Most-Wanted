from pathlib import Path
import unittest


class AnalyticsRenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template_text = Path("render/dashboard_template.html").read_text(encoding="utf-8")
        cls.style_text = Path("render/style.css").read_text(encoding="utf-8")
        cls.analytics_css = Path("render/src/css/features/analytics/analytics.css").read_text(encoding="utf-8")
        cls.html_dashboard_text = Path("render/html_dashboard.py").read_text(encoding="utf-8")

    def test_analytics_route_markup_and_scope_copy(self):
        template = self.template_text

        self.assertIn('id="analytics-view"', template)
        self.assertIn('class="analytics-hero-section"', template)
        self.assertIn('analytics-kpi-wrapper', template)
        self.assertIn('class="analytics-pressure-grid"', template)
        self.assertIn('class="analytics-readiness-grid"', template)
        self.assertIn('class="analytics-spotlight-grid"', template)
        self.assertIn('class="analytics-quick-routes"', template)
        self.assertIn('id="analyticsActivityChart"', template)
        self.assertIn('id="roleDonutChart"', template)
        self.assertIn('id="levelDistChart"', template)
        self.assertIn('Scope: raw roster totals, mains-only readiness, roster-known levels, and processed detail-eligible intelligence.', template)
        self.assertIn('📊 Analytics', template)
        self.assertIn('Open Analytics ➔', template)
        self.assertNotIn('Advanced Analytics', template)
        self.assertNotIn('https://github.com/parvagans/Azeroths-Most-Wanted', template)
        self.assertNotIn('Recent Campaign Activity', template)
        self.assertNotIn('Campaign Chronicle', template)

    def test_analytics_css_is_owning_its_route_styles(self):
        html_dashboard = self.html_dashboard_text
        analytics_css = self.analytics_css
        style_css = self.style_text

        self.assertIn('os.path.join(base_dir, "src", "css", "features", "search", "autocomplete.css")', html_dashboard)
        self.assertIn('os.path.join(base_dir, "src", "css", "features", "war_effort", "war_effort.css")', html_dashboard)
        self.assertIn('os.path.join(base_dir, "src", "css", "features", "character", "dossier.css")', html_dashboard)
        self.assertIn('os.path.join(base_dir, "src", "css", "features", "analytics", "analytics.css")', html_dashboard)

        self.assertIn('.analytics-view-container', analytics_css)
        self.assertIn('.analytics-hero-section', analytics_css)
        self.assertIn('.analytics-hero-scope', analytics_css)
        self.assertIn('.analytics-pressure-card', analytics_css)
        self.assertIn('.analytics-route-card', analytics_css)
        self.assertIn('.command-shell-analytics-role', analytics_css)
        self.assertIn('body[data-route-family="analytics"]::before', analytics_css)

        self.assertNotIn('.analytics-view-container', style_css)
        self.assertNotIn('.analytics-pressure-card', style_css)
        self.assertNotIn('.analytics-route-card', style_css)
        self.assertNotIn('.command-shell-analytics-role', style_css)
        self.assertNotIn('analytics-', style_css)


if __name__ == "__main__":
    unittest.main()
