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
        css_text = Path("render/style.css").read_text(encoding="utf-8")
        search_css_text = Path("render/src/css/features/search/autocomplete.css").read_text(encoding="utf-8")
        mobile_css_text = Path("render/src/css/features/mobile/mobile.css").read_text(encoding="utf-8")
        html_dashboard_text = Path("render/html_dashboard.py").read_text(encoding="utf-8")

        self.assertIn('class="home-roster-intelligence-section"', template_text)
        self.assertIn('class="home-scan-summary-shell"', template_text)
        self.assertIn('id="command-ribbon-container"', template_text)
        self.assertIn('id="recent-milestones-container"', template_text)
        self.assertIn('id="home-api-status-banner"', template_text)
        self.assertNotIn('id="weekly-reset-module"', template_text)
        self.assertNotIn('id="ribbon-countdown"', template_text)
        self.assertNotIn('id="countdown-timer-text"', template_text)
        self.assertIn('id="home-command-brief-reset"', template_text)
        self.assertIn('class="home-section-nav"', template_text)
        self.assertIn('class="home-pulse-grid"', template_text)
        self.assertIn('href="#homepage-status"', template_text)
        self.assertIn('href="#homepage-roster"', template_text)
        self.assertIn('href="#homepage-war-effort"', template_text)
        self.assertIn('href="#homepage-standouts"', template_text)
        self.assertIn('href="#homepage-councils"', template_text)
        self.assertIn('href="#homepage-analytics"', template_text)
        self.assertIn('homepage-section-nav-link', template_text)
        self.assertIn('class="home-section-nav-link homepage-section-nav-link">Status</a>', template_text)
        self.assertIn('class="home-section-nav-link homepage-section-nav-link">Roster</a>', template_text)
        self.assertIn('class="home-section-nav-link homepage-section-nav-link">War Effort</a>', template_text)
        self.assertIn('class="home-section-nav-link homepage-section-nav-link">Standouts</a>', template_text)
        self.assertIn('class="home-section-nav-link homepage-section-nav-link">Councils</a>', template_text)
        self.assertIn('class="home-section-nav-link homepage-section-nav-link">Analytics</a>', template_text)
        self.assertIn('id="homepage-status"', template_text)
        self.assertIn('id="homepage-roster"', template_text)
        self.assertIn('id="homepage-war-effort"', template_text)
        self.assertIn('id="homepage-standouts"', template_text)
        self.assertIn('id="homepage-councils"', template_text)
        self.assertIn('id="homepage-analytics"', template_text)
        self.assertIn('class="home-report-cluster"', template_text)
        self.assertIn('id="weekly-mvps-container"', template_text)
        self.assertIn('id="homepage-councils"', template_text)
        self.assertIn('id="homepage-analytics"', template_text)
        self.assertIn('class="home-roster-intelligence-cluster"', template_text)
        self.assertIn('class="home-movement-card"', template_text)
        self.assertIn('class="home-insights-row"', template_text)
        self.assertIn('id="home-roster-intelligence-sync"', template_text)
        self.assertNotIn('Dispatch Board', template_text)
        self.assertNotIn('home-command-section', template_text)
        self.assertIn('Roster Intelligence', template_text)
        self.assertIn('Detailed status from the latest scan', template_text)
        self.assertIn('Detailed cards for guild size, activity, readiness, and endgame strength.', template_text)
        self.assertIn('How these numbers are counted', template_text)
        self.assertIn('Metric Scope', template_text)
        self.assertIn('Guild Roster:</strong> raw guild roster total from the roster endpoint, including mains and alts.', template_text)
        self.assertIn('Roster Movement:</strong> guild membership snapshots used to detect joins, departures, and rejoins, so its baseline can differ from raw roster totals and detail-eligible processed counts.', template_text)
        self.assertIn('Progression Readiness', template_text)
        self.assertIn('Level Distribution', template_text)
        self.assertIn('Max Level iLvl Spread', template_text)
        self.assertNotIn('id="levelDistChart"', template_text)
        self.assertNotIn('id="ilvlDistChart"', template_text)
        self.assertIn('Movement, recent changes, and officer health from the latest guild snapshot.', template_text)
        self.assertIn('Dashboard built: {{ last_updated_display }}', template_text)
        self.assertIn('id="home-latest-changes-card"', template_text)
        self.assertIn('id="home-officer-brief-card"', template_text)
        self.assertIn('Recent activity, trend shifts, and notable roster signals worth noting.', template_text)
        self.assertIn('class="dashboard-footer"', template_text)
        self.assertIn('Dashboard Built', template_text)
        self.assertIn('Contact: <a href="mailto:nullbit5@protonmail.com">nullbit5@protonmail.com</a>', template_text)
        self.assertIn('href="#campaign-archive"', template_text)
        self.assertIn('View Campaign Archive', template_text)
        self.assertIn('Campaign Archive', template_text)
        self.assertIn("Warden's Standard", template_text)
        self.assertIn('id="guild-readiness-summary"', template_text)
        self.assertNotIn('https://github.com/parvagans/Azeroths-Most-Wanted', template_text)
        self.assertNotIn('class="nav-btn nav-btn-source"', template_text)
        self.assertNotIn('class="footer-source-info"', template_text)
        self.assertIn('id="backToTopBtn"', template_text)
        self.assertIn('last_updated_display=last_updated_display', html_dashboard_text)
        self.assertIn('os.path.join(base_dir, "src", "css", "features", "search", "autocomplete.css")', html_dashboard_text)
        self.assertIn('.home-roster-intelligence-section {', css_text)
        self.assertIn('.home-scan-summary-shell {', css_text)
        self.assertIn('display: flex;', css_text)
        self.assertIn('flex-direction: column;', css_text)
        self.assertIn('gap: 16px;', css_text)
        self.assertIn('margin: 0 auto 62px;', css_text)
        self.assertIn('.home-scan-summary-shell .command-ribbon-container,', css_text)
        self.assertIn('.home-scan-summary-shell .home-section-nav,', css_text)
        self.assertIn('.home-scan-summary-shell .home-pulse-section {', css_text)
        self.assertIn('.command-ribbon-container .milestone-banner {', css_text)
        self.assertIn('.command-ribbon-container .milestone-banner::after {', css_text)
        self.assertIn('.command-ribbon-container .milestone-icon {', css_text)
        self.assertIn('margin-top: 0;', css_text)
        self.assertIn('.home-roster-intelligence-cluster {', css_text)
        self.assertIn('grid-template-columns: minmax(0, 1.2fr) minmax(340px, 0.8fr);', css_text)
        self.assertIn('grid-template-areas: "movement side";', css_text)
        self.assertIn('.home-report-cluster {', css_text)
        self.assertIn('gap: 26px;', css_text)
        self.assertIn('border-radius: 26px;', css_text)
        self.assertIn('.home-report-cluster .weekly-mvps-wrapper,', css_text)
        self.assertIn('.home-report-cluster .home-ladders-section,', css_text)
        self.assertIn('.home-report-cluster .home-secondary-section {', css_text)
        self.assertIn('.home-report-cluster .mvp-cards-container,', css_text)
        self.assertIn('.home-report-cluster .leaderboards-wrapper,', css_text)
        self.assertIn('.home-report-cluster .home-secondary-grid {', css_text)
        self.assertIn('.home-movement-card {', css_text)
        self.assertIn('.home-insights-row {', css_text)
        self.assertIn('display: flex;', css_text)
        self.assertIn('flex-direction: column;', css_text)
        self.assertIn('scroll-margin-top: 112px;', css_text)
        self.assertIn('#homepage-status, #homepage-roster, #homepage-war-effort, #homepage-standouts, #homepage-councils, #homepage-analytics {', css_text)
        self.assertIn('#homepage-standouts {', css_text)
        self.assertIn('#homepage-standouts {\n  scroll-margin-top: 144px;\n}', css_text)
        self.assertIn('.home-section-nav {', css_text)
        self.assertIn('.home-roster-intelligence-cluster {', css_text)
        self.assertIn('.home-roster-intelligence-sync {', css_text)
        self.assertIn('.home-metric-scope {', css_text)
        self.assertIn('.home-metric-scope-summary {', css_text)
        self.assertIn('.home-metric-scope-summary:focus-visible {', css_text)
        self.assertIn('.home-metric-scope-panel {', css_text)
        self.assertNotIn('.search-box:has(input:focus-visible) {', css_text)
        self.assertNotIn('.hero-search-box:has(input:focus-visible) {', css_text)
        self.assertIn('.search-box:has(input:focus-visible) {', search_css_text)
        self.assertIn('.hero-search-box:has(input:focus-visible) {', search_css_text)
        self.assertIn('.hero-search-wrapper {', search_css_text)
        self.assertIn('.hero-text-col .hero-search-wrapper {\n  z-index: 1;', css_text)
        self.assertIn('.hero-ac-item {', search_css_text)
        self.assertNotIn('@media (max-width:', search_css_text)
        self.assertIn('@media (max-width: 1024px) {', mobile_css_text)
        self.assertIn('.controls-wrapper {', mobile_css_text)
        self.assertIn('.nav-utility-cluster {', mobile_css_text)
        self.assertIn('.hero-search-wrapper {', mobile_css_text)
        self.assertIn('.home-section-nav {', mobile_css_text)
        self.assertIn('.home-section-nav-link {', mobile_css_text)
        self.assertIn('.home-roster-intelligence-cluster {', mobile_css_text)
        self.assertIn('display: flex;', mobile_css_text)
        self.assertIn('flex-direction: column;', mobile_css_text)
        self.assertIn('.home-scan-summary-shell {', mobile_css_text)
        self.assertIn('padding: 14px 14px 16px;', mobile_css_text)
        self.assertIn('.home-scan-summary-shell .command-ribbon-container,', mobile_css_text)
        self.assertIn('.home-scan-summary-shell .command-ribbon-container {', mobile_css_text)
        self.assertIn('.command-ribbon-container .milestone-banner {', mobile_css_text)
        self.assertIn('.home-report-cluster {', mobile_css_text)
        self.assertIn('border-radius: 22px;', mobile_css_text)
        self.assertIn('.home-report-cluster .weekly-mvps-wrapper,', mobile_css_text)
        self.assertIn('.home-roster-intelligence-section {', mobile_css_text)
        self.assertIn('#homepage-status,', mobile_css_text)
        self.assertIn('#homepage-standouts {', mobile_css_text)
        self.assertIn('scroll-margin-top: 108px;', mobile_css_text)
        self.assertIn('body.nav-menu-open .navbar .search-container {', mobile_css_text)
        self.assertIn('.concise-view-header {', css_text)
        self.assertIn('.concise-view-context {', css_text)
        self.assertIn('.concise-back-btn {', css_text)
        self.assertIn('.concise-back-btn:focus-visible {', css_text)
        self.assertIn('.dashboard-footer {', css_text)
        self.assertIn('.footer-disclaimer {', css_text)
        self.assertNotIn('analytics-intel-section-chronicle', template_text)
        self.assertNotIn('Campaign Chronicle', template_text)
        self.assertNotIn('Recent Campaign Activity', template_text)
        self.assertNotIn('Campaign Chronicle', script_text)
        self.assertNotIn('Recent Campaign Activity', script_text)
        self.assertNotIn('analytics-chronicle', css_text)
        self.assertNotIn('search-autocomplete', css_text)
        self.assertNotIn('applyChronicleCard', cards_text)

    def test_navigation_context_and_return_controls_are_present(self):
        template_text = Path("render/dashboard_template.html").read_text(encoding="utf-8")
        script_text = Path("render/script.js").read_text(encoding="utf-8")
        shell_text = Path("render/src/js/features/command_hall/command_shell.js").read_text(encoding="utf-8")

        self.assertIn('id="concise-view-context"', template_text)
        self.assertIn('id="concise-back-btn"', template_text)
        self.assertIn('Back to overview', template_text)
        self.assertIn('No matching character found. Try a character name or a shorter search.', template_text)
        self.assertIn('Viewing: full roster. Filter: all scanned mains and alts.', shell_text)
        self.assertIn('Viewing: active roster. Filter: mains seen in the last 14 days.', shell_text)
        self.assertIn('Viewing: raid-ready roster. Filter: mains meeting the configured readiness threshold.', shell_text)
        self.assertIn('Character dossier •', script_text)

    def test_shared_leaderboard_system_contract_is_present(self):
        template_text = Path("render/dashboard_template.html").read_text(encoding="utf-8")
        script_text = Path("render/script.js").read_text(encoding="utf-8")
        css_text = Path("render/style.css").read_text(encoding="utf-8")
        mobile_css_text = Path("render/src/css/features/mobile/mobile.css").read_text(encoding="utf-8")

        self.assertIn('id="tpl-mvp-podium-block"', template_text)
        self.assertIn('id="tpl-home-leaderboard-podium"', template_text)
        self.assertIn('id="tpl-concise-podium"', template_text)
        self.assertIn('id="tpl-ladder-podium"', template_text)
        self.assertIn('class="amw-leaderboard-card tt-char"', template_text)
        self.assertIn('class="amw-leaderboard amw-leaderboard-list"', template_text)
        self.assertIn('class="amw-leaderboard-identity"', template_text)
        self.assertIn('class="amw-leaderboard-metric"', template_text)
        self.assertIn('class="amw-leaderboard-metric-value"', template_text)
        self.assertIn('class="amw-leaderboard-metric-label"', template_text)
        self.assertIn('.amw-leaderboard-list {', css_text)
        self.assertIn('.amw-leaderboard-card {', css_text)
        self.assertIn('.amw-leaderboard-featured {', css_text)
        self.assertIn('.amw-leaderboard-compact {', css_text)
        self.assertIn('grid-template-columns: repeat(3, minmax(0, 1fr));', css_text)
        self.assertIn('grid-template-columns: var(--leaderboard-card-columns);', css_text)
        self.assertIn('grid-template-areas:', css_text)
        self.assertIn('.amw-leaderboard-card-rank-1 {', css_text)
        self.assertIn('.amw-leaderboard-avatar {', css_text)
        self.assertIn('.amw-leaderboard-rank {', css_text)
        self.assertIn('.amw-leaderboard-theme-pve,', css_text)
        self.assertIn('.amw-leaderboard-theme-pvp,', css_text)
        self.assertIn('.amw-leaderboard-theme-ilvl,', css_text)
        self.assertIn('.amw-leaderboard-theme-hks {', css_text)
        self.assertIn('.amw-leaderboard-theme-readiness {', css_text)
        self.assertIn('.amw-leaderboard-theme-loot {', css_text)
        self.assertIn('.amw-leaderboard-theme-zenith {', css_text)
        self.assertNotIn('.amw-podium-grid {', css_text)
        self.assertNotIn('.podium-step-1 {', css_text)
        self.assertNotIn('.podium-step-2 {', css_text)
        self.assertNotIn('.podium-step-3 {', css_text)
        self.assertNotIn('.podium-1 {', css_text)
        self.assertNotIn('.podium-block {', css_text)
        self.assertNotIn('.amw-leaderboard-crown {', css_text)
        self.assertNotIn('.amw-leaderboard-list.ladder-podium-wrap', css_text)
        self.assertNotIn('ladder-podium-wrap stage', css_text)
        self.assertNotIn('ladder-podium-wrap floor', css_text)
        self.assertNotIn('.amw-leaderboard-list::before', css_text)
        self.assertNotIn('.amw-leaderboard-list::after', css_text)
        self.assertNotIn('stepClass = rank === 1 ? \'podium-step-1\'', script_text)
        self.assertNotIn('block.classList.add(stepClass);', script_text)
        self.assertNotIn('.podium-block', script_text)
        self.assertNotIn('podium-trend-text', script_text)
        self.assertIn('function getLeaderboardThemeClass(theme = \'\') {', script_text)
        self.assertIn("function decorateLeaderboardClone(clone, { rank = 0, theme = '', character = null } = {}) {", script_text)
        self.assertIn("theme: isPvp ? 'pvp' : 'pve'", script_text)
        self.assertIn("theme: 'pve'", script_text)
        self.assertIn("theme: 'pvp'", script_text)
        self.assertIn("theme: (() => {", script_text)
        self.assertIn("theme: hashUrl === 'ladder-pvp' ? 'pvp' : 'pve'", script_text)
        self.assertIn('.amw-leaderboard-list {', mobile_css_text)
        self.assertIn('.amw-leaderboard-card {', mobile_css_text)
        self.assertIn('--leaderboard-card-columns: 46px minmax(0, 1fr) auto;', mobile_css_text)
        self.assertIn('grid-template-columns: var(--leaderboard-card-columns);', mobile_css_text)
        self.assertIn('grid-template-areas:', mobile_css_text)
        self.assertIn('.amw-leaderboard-avatar {', mobile_css_text)
        self.assertIn('.amw-leaderboard-rank {', mobile_css_text)
        self.assertNotIn('.amw-leaderboard-grid', mobile_css_text)
        self.assertNotIn('.podium-step-1', mobile_css_text)
        self.assertNotIn('.podium-step-2', mobile_css_text)
        self.assertNotIn('.podium-step-3', mobile_css_text)
        self.assertNotIn('.podium-1', mobile_css_text)
        self.assertNotIn('.amw-leaderboard-list.ladder-podium-wrap', mobile_css_text)

    def test_homepage_standouts_use_featured_leaderboard_variant(self):
        script_text = Path("render/script.js").read_text(encoding="utf-8")
        mvp_start = script_text.index("window.renderMVPs = function()")
        mvp_end = script_text.index("function generateGloatingHtml", mvp_start)
        mvp_text = script_text[mvp_start:mvp_end]

        self.assertIn("const container = containerClone.querySelector('.amw-leaderboard-list');", mvp_text)
        self.assertIn("container.classList.add('amw-leaderboard-featured');", mvp_text)
        self.assertIn("setFeaturedLeaderboardCount(container, chars.length);", mvp_text)
        self.assertIn("decorateLeaderboardClone(clone, {", mvp_text)

    def test_homepage_previous_week_standout_banner_uses_metric_specific_copy(self):
        template_text = Path("render/dashboard_template.html").read_text(encoding="utf-8")
        script_text = Path("render/script.js").read_text(encoding="utf-8")
        css_text = Path("render/style.css").read_text(encoding="utf-8")
        mobile_css_text = Path("render/src/css/features/mobile/mobile.css").read_text(encoding="utf-8")

        placeholder_start = template_text.index('id="tpl-mvp-placeholder"')
        placeholder_end = template_text.index('id="tpl-mvp-gloat"', placeholder_start)
        placeholder_text = template_text[placeholder_start:placeholder_end]
        gloat_start = template_text.index('id="tpl-mvp-gloat"')
        gloat_end = template_text.index('id="tpl-mvp-empty"', gloat_start)
        gloat_text = template_text[gloat_start:gloat_end]
        mvp_start = script_text.index("function generateGloatingHtml(mvpData, isPvp) {")
        mvp_end = script_text.index("const prevMvps = config.prev_mvps || {};", mvp_start)
        gloat_runtime_text = script_text[mvp_start:mvp_end]

        self.assertNotIn("Reigning Champion", placeholder_text + gloat_text + gloat_runtime_text)
        self.assertIn("Awaiting previous week data", placeholder_text)
        self.assertIn("const label = isPvp ? 'HKs' : 'iLvl';", gloat_runtime_text)
        self.assertIn("const title = isPvp ? 'Previous HK Leader' : 'Previous Top Climber';", gloat_runtime_text)
        self.assertIn("clone.querySelector('.gloat-title').textContent = title;", gloat_runtime_text)
        self.assertIn("clone.querySelector('.gloat-score').textContent = `+${mvpData.score.toLocaleString()}`;", gloat_runtime_text)
        self.assertIn("clone.querySelector('.gloat-label').textContent = `${label} last week`;", gloat_runtime_text)
        self.assertNotIn("clone.querySelector('.mvp-placeholder-status').textContent = title;", gloat_runtime_text)
        self.assertNotIn("clone.querySelector('.mvp-placeholder-label').textContent = `${label} last week`;", gloat_runtime_text)
        self.assertIn(".mvp-gloat-card,", css_text)
        self.assertIn("grid-template-columns: 54px minmax(0, 1fr) auto;", css_text)
        self.assertIn(".gloat-score {", css_text)
        self.assertIn(".mvp-gloat-card,", mobile_css_text)

    def test_homepage_curated_ladder_intelligence_uses_featured_variant(self):
        script_text = Path("render/script.js").read_text(encoding="utf-8")
        pve_start = script_text.index("const pveContainer = document.getElementById('pve-leaderboard');")
        pvp_end = script_text.index("setupTooltips();", pve_start)
        homepage_ladder_text = script_text[pve_start:pvp_end]

        self.assertEqual(
            homepage_ladder_text.count(
                "podiumWrap.classList.add('amw-leaderboard-featured', "
                "'home-featured-grid', 'war-council-featured-grid');"
            ),
            2,
        )
        self.assertIn("setFeaturedLeaderboardCount(podiumWrap, topPve.length);", homepage_ladder_text)
        self.assertIn("setFeaturedLeaderboardCount(podiumWrap, topPvp.length);", homepage_ladder_text)
        self.assertIn("theme: 'pve'", homepage_ladder_text)
        self.assertIn("theme: 'pvp'", homepage_ladder_text)

    def test_homepage_report_layouts_have_deliberate_density_and_alignment(self):
        css_text = Path("render/style.css").read_text(encoding="utf-8")

        self.assertIn(".mvp-cards-container {\n  display: grid;", css_text)
        self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr));", css_text)
        self.assertIn(".mvp-card {\n  position: relative;\n  display: flex;\n  flex-direction: column;", css_text)
        self.assertIn(".mvp-empty-state {\n  display: flex;\n  flex: 1;", css_text)
        self.assertIn("min-height: 188px;", css_text)
        self.assertIn(".amw-leaderboard-featured.amw-leaderboard-count-1 {", css_text)
        self.assertIn(".amw-leaderboard-featured.amw-leaderboard-count-2 {", css_text)
        self.assertIn(".amw-leaderboard-featured .amw-leaderboard-card-rank-1 {", css_text)

    def test_homepage_council_rows_and_controls_use_shared_report_structure(self):
        template_text = Path("render/dashboard_template.html").read_text(encoding="utf-8")
        script_text = Path("render/script.js").read_text(encoding="utf-8")
        css_text = Path("render/style.css").read_text(encoding="utf-8")

        self.assertIn(".leaderboards-wrapper {\n  display: grid;", css_text)
        self.assertIn('class="leaderboard-row war-council-row tt-char"', template_text)
        self.assertIn('class="lb-trend"', template_text)
        self.assertIn(".leaderboard-panel .war-council-row {", css_text)
        self.assertIn('grid-template-areas: "rank avatar identity metric trend";', css_text)
        self.assertIn("var(--war-council-row-rank-width)", css_text)
        self.assertIn("var(--war-council-row-avatar-size)", css_text)
        self.assertIn("var(--war-council-row-metric-width)", css_text)
        self.assertIn("var(--war-council-row-trend-width)", css_text)
        self.assertIn(".leaderboard-panel .war-council-row .lb-score {", css_text)
        self.assertIn(".leaderboard-panel .war-council-row .lb-trend {", css_text)
        self.assertEqual(script_text.count("trendEl.appendChild(createTrendSpan(trend));"), 2)
        self.assertIn(".leaderboard-panel .expand-lb-btn {", css_text)
        self.assertIn(".leaderboard-panel > .view-all-btn {", css_text)
        self.assertIn("#pve-leaderboard-container {", css_text)
        self.assertIn("#pvp-leaderboard-container {", css_text)
        self.assertNotIn("pvp-row", template_text + css_text)

    def test_deeper_leaderboard_surfaces_use_compact_variant(self):
        script_text = Path("render/script.js").read_text(encoding="utf-8")
        concise_start = script_text.index("if (usePodium && podiumNodes.length > 0) {")
        concise_end = script_text.index("const conciseLoadMoreContainer", concise_start)
        concise_text = script_text[concise_start:concise_end]

        self.assertIn("podiumWrap.classList.add('amw-leaderboard-compact');", concise_text)
        self.assertNotIn("amw-leaderboard-featured", concise_text)

    def test_leaderboard_variants_share_base_component_classes(self):
        template_text = Path("render/dashboard_template.html").read_text(encoding="utf-8")
        css_text = Path("render/style.css").read_text(encoding="utf-8")

        for class_name in (
            "amw-leaderboard",
            "amw-leaderboard-list",
            "amw-leaderboard-card",
            "amw-leaderboard-rank",
            "amw-leaderboard-avatar",
            "amw-leaderboard-identity",
            "amw-leaderboard-name",
            "amw-leaderboard-subtitle",
            "amw-leaderboard-metric",
        ):
            self.assertIn(class_name, template_text + css_text)

        self.assertIn(".amw-leaderboard-featured {", css_text)
        self.assertIn(".amw-leaderboard-compact {", css_text)
        self.assertIn(".amw-leaderboard-card {", css_text)
        self.assertNotIn(".amw-leaderboard-compact .amw-leaderboard-card {", css_text)

    def test_featured_variant_increases_card_avatar_name_and_metric_sizing(self):
        css_text = Path("render/style.css").read_text(encoding="utf-8")

        self.assertIn("--leaderboard-avatar-size: 60px;", css_text)
        self.assertIn("--leaderboard-card-min-height: 118px;", css_text)
        self.assertIn("--leaderboard-name-size: 14px;", css_text)
        self.assertIn("--leaderboard-metric-size: 13px;", css_text)
        self.assertIn("--leaderboard-avatar-size: clamp(68px, 6vw, 84px);", css_text)
        self.assertIn("--leaderboard-card-min-height: 172px;", css_text)
        self.assertIn("--leaderboard-name-size: 17px;", css_text)
        self.assertIn("--leaderboard-metric-size: 15px;", css_text)
        self.assertIn("width: var(--leaderboard-avatar-size);", css_text)
        self.assertIn("min-height: var(--leaderboard-card-min-height);", css_text)
        self.assertIn("font-size: var(--leaderboard-name-size);", css_text)
        self.assertIn("font-size: var(--leaderboard-metric-size);", css_text)
        self.assertIn(".amw-leaderboard-featured .amw-leaderboard-subtitle {", css_text)
        self.assertIn(".amw-leaderboard-featured .amw-leaderboard-rank {", css_text)

    def test_featured_cards_use_vertical_showcase_layout_not_compact_horizontal_grid(self):
        css_text = Path("render/style.css").read_text(encoding="utf-8")
        featured_card_start = css_text.index(".amw-leaderboard-featured .amw-leaderboard-card {")
        featured_card_end = css_text.index("}", featured_card_start)
        featured_card_rule = css_text[featured_card_start:featured_card_end]

        self.assertIn("display: flex;", featured_card_rule)
        self.assertIn("flex-direction: column;", featured_card_rule)
        self.assertIn("align-items: center;", featured_card_rule)
        self.assertIn("text-align: center;", featured_card_rule)
        self.assertNotIn("grid-template-columns", featured_card_rule)
        self.assertNotIn("grid-template-areas", featured_card_rule)

    def test_homepage_featured_cards_use_shared_fixed_regions(self):
        template_text = Path("render/dashboard_template.html").read_text(encoding="utf-8")
        script_text = Path("render/script.js").read_text(encoding="utf-8")
        css_text = Path("render/style.css").read_text(encoding="utf-8")
        card_selector = ".home-featured-grid .home-featured-card {"
        card_start = css_text.index(card_selector)
        card_end = css_text.index("}", card_start)
        card_rule = css_text[card_start:card_end]

        self.assertIn("standout-featured-grid", template_text)
        self.assertIn("standout-featured-card", template_text)
        self.assertIn("war-council-featured-card", template_text)
        self.assertIn("'home-featured-grid', 'war-council-featured-grid'", script_text)
        self.assertIn("display: grid;", card_rule)
        self.assertIn("var(--leaderboard-avatar-size)", card_rule)
        self.assertIn("var(--home-featured-identity-height)", card_rule)
        self.assertIn("var(--home-featured-metric-height)", card_rule)
        self.assertIn('"avatar"', card_rule)
        self.assertIn('"identity"', card_rule)
        self.assertIn('"metric"', card_rule)
        self.assertIn(".home-featured-grid .home-featured-card .amw-leaderboard-avatar {\n  place-self: center;", css_text)
        self.assertIn(".home-featured-grid .home-featured-card .amw-leaderboard-metric {\n  place-self: center;", css_text)
        self.assertIn(".home-featured-grid .home-featured-card .amw-leaderboard-rank {\n  position: absolute;", css_text)
        self.assertNotIn("#pve-leaderboard .amw-leaderboard-card", css_text)
        self.assertNotIn("#pvp-leaderboard .amw-leaderboard-card", css_text)

    def test_current_ranking_names_keep_activity_before_name_in_one_identity_group(self):
        template_text = Path("render/dashboard_template.html").read_text(encoding="utf-8")
        script_text = Path("render/script.js").read_text(encoding="utf-8")
        css_text = Path("render/style.css").read_text(encoding="utf-8")

        compact_identity = (
            '<span class="lb-name-status-row character-status-name-grid">\n'
            '                    <span class="character-activity-slot" aria-hidden="true"></span>\n'
            '                    <span class="lb-name"></span>'
        )
        self.assertIn(compact_identity, template_text)
        self.assertIn('<span class="lb-spec"><span class="lb-spec-label"></span></span>', template_text)
        self.assertIn("if (identity && name) {", script_text)
        self.assertIn(
            "nameRow.className = 'character-name-status-row character-status-name-grid';",
            script_text,
        )
        self.assertLess(
            script_text.index("nameRow.appendChild(statusSlot);"),
            script_text.index("nameRow.appendChild(name);"),
        )
        self.assertIn("appendCharacterActivityIndicator(statusSlot, character);", script_text)
        self.assertIn("nameRow.classList.add('has-activity-indicator');", script_text)
        self.assertEqual(script_text.count("appendCharacterActivityIndicator(activitySlotEl, char);"), 2)
        self.assertIn("specLabelEl.textContent = displaySpecClass;", script_text)
        self.assertIn(".character-status-name-grid {", css_text)
        self.assertIn("var(--character-activity-slot-size, 18px)", css_text)
        self.assertIn("minmax(0, 1fr);", css_text)
        self.assertIn("width: fit-content;", css_text)
        self.assertIn(
            ".home-featured-grid .home-featured-card .character-status-name-grid::after {",
            css_text,
        )
        self.assertIn("-webkit-line-clamp: 2;", css_text)
        self.assertIn("overflow-wrap: break-word;", css_text)
        self.assertIn("text-wrap: balance;", css_text)
        self.assertIn(".leaderboard-panel .war-council-row .lb-info {", css_text)
        self.assertIn("grid-template-rows:", css_text)
        self.assertIn("grid-area: identity;", css_text)
        self.assertIn(
            "padding-inline-start: calc(var(--character-activity-slot-size) + var(--character-status-gap));",
            css_text,
        )
        self.assertIn(".leaderboard-panel .war-council-row .lb-spec-label {", css_text)

    def test_homepage_featured_names_reserve_two_lines_without_moving_metrics(self):
        css_text = Path("render/style.css").read_text(encoding="utf-8")

        self.assertIn("--home-featured-identity-height: 44px;", css_text)
        self.assertIn("--home-featured-metric-height: 31px;", css_text)
        self.assertIn("height: var(--home-featured-identity-height);", css_text)
        self.assertIn("min-height: var(--home-featured-identity-height);", css_text)
        self.assertIn("min-height: var(--home-featured-metric-height);", css_text)
        self.assertIn("-webkit-line-clamp: 2;", css_text)
        self.assertIn("overflow-wrap: break-word;", css_text)
        self.assertNotIn("word-break: break-all;", css_text)

    def test_featured_card_names_are_not_tiny_or_one_letter_clipped(self):
        css_text = Path("render/style.css").read_text(encoding="utf-8")
        featured_name_start = css_text.index(".amw-leaderboard-featured .amw-leaderboard-name {")
        featured_name_end = css_text.index("}", featured_name_start)
        featured_name_rule = css_text[featured_name_start:featured_name_end]

        self.assertIn("width: 100%;", featured_name_rule)
        self.assertIn("max-width: 100%;", featured_name_rule)
        self.assertIn("white-space: normal;", featured_name_rule)
        self.assertIn("overflow: visible;", featured_name_rule)
        self.assertIn("text-overflow: unset;", featured_name_rule)
        self.assertIn("text-align: center;", featured_name_rule)
        self.assertNotIn("width: auto;", featured_name_rule)
        self.assertNotIn("white-space: nowrap;", featured_name_rule)
        self.assertNotIn("overflow: hidden;", featured_name_rule)

    def test_homepage_featured_cards_do_not_emit_subtitle_identity_text(self):
        script_text = Path("render/script.js").read_text(encoding="utf-8")
        pve_start = script_text.index("const pveContainer = document.getElementById('pve-leaderboard');")
        pvp_end = script_text.index("setupTooltips();", pve_start)
        homepage_ladder_text = script_text[pve_start:pvp_end]
        mvp_start = script_text.index("window.renderMVPs = function()")
        mvp_end = script_text.index("function generateGloatingHtml", mvp_start)
        mvp_text = script_text[mvp_start:mvp_end]

        self.assertEqual(homepage_ladder_text.count("if (subtitleEl) subtitleEl.remove();"), 2)
        self.assertIn("if (subtitleDiv) subtitleDiv.remove();", mvp_text)
        self.assertNotIn("subtitleEl.textContent = displaySpecClass", homepage_ladder_text)
        self.assertNotIn("subtitleDiv.textContent", mvp_text)
        self.assertNotIn("subtitleText", mvp_text)
        self.assertIn("metricValue.textContent = trend.toLocaleString();", mvp_text)

    def test_compact_podiums_keep_subtitle_identity_text(self):
        script_text = Path("render/script.js").read_text(encoding="utf-8")
        concise_start = script_text.index("function buildConcisePodiumHtml({")
        ladder_end = script_text.index("// Variable to track current sort method", concise_start)
        compact_podium_text = script_text[concise_start:ladder_end]

        self.assertIn("const subtitleText = rivalryText || `${raceName} • ${displaySpecClass}`.trim();", compact_podium_text)
        self.assertIn("if (subtitleText) subtitleEl.textContent = subtitleText;", compact_podium_text)
        self.assertIn("if (displaySpecClass) subtitleEl.textContent = displaySpecClass;", compact_podium_text)

    def test_leaderboard_metrics_still_render_for_homepage_and_readiness(self):
        script_text = Path("render/script.js").read_text(encoding="utf-8")

        self.assertIn("statLabelEl.textContent = 'iLvl';", script_text)
        self.assertIn("statLabelEl.textContent = 'HKs';", script_text)
        self.assertIn("metricLabel.textContent = label;", script_text)
        self.assertIn("metricValueEl.textContent = `iLvl ${readinessIlvl.toLocaleString()}`;", script_text)

    def test_empty_leaderboard_metric_pill_is_not_emitted(self):
        script_text = Path("render/script.js").read_text(encoding="utf-8")

        self.assertIn("const metricPill = clone.querySelector('.amw-leaderboard-metric');", script_text)
        self.assertGreaterEqual(script_text.count("metricPill.remove();"), 2)
        self.assertNotIn("metricValueEl.textContent = '';", script_text)
        self.assertNotIn("metricLabelEl.textContent = '';", script_text)

    def test_search_autocomplete_helpers_are_present(self):
        script_text = Path("render/script.js").read_text(encoding="utf-8")

        self.assertIn('const CHARACTER_SEARCH_MIN_QUERY_LENGTH = 2;', script_text)
        self.assertIn('function normalizeCharacterSearchQuery(query)', script_text)
        self.assertIn('function getCharacterSearchRank(char, normalizedQuery)', script_text)
        self.assertIn('function clearCharacterSearchPanels({ clearInputs = false } = {})', script_text)
        self.assertIn('function renderCharacterSearchAutocomplete(targetEl, query, { limit = 6, forceObjectFitCover = false } = {})', script_text)
        self.assertIn('renderCharacterSearchAutocomplete(heroSearchAutoComplete, e.target.value, { limit: 6 });', script_text)
        self.assertIn('renderCharacterSearchAutocomplete(searchAutoComplete, e.target.value, { limit: 6, forceObjectFitCover: true });', script_text)
        self.assertIn('clearCharacterSearchPanels({ clearInputs: true });', script_text)
        self.assertIn('if (name === normalizedQuery) return 0;', script_text)
        self.assertIn('if (name.startsWith(normalizedQuery)) return 1;', script_text)
        self.assertIn('if (name.includes(normalizedQuery)) return 2;', script_text)

    def test_character_dossier_timeline_support_remains_intact(self):
        script_text = Path("render/script.js").read_text(encoding="utf-8")

        self.assertIn('timeline-character-dossier', script_text)
        self.assertIn("title: `📜 ${formattedName}'s Recent Activity`", script_text)
        self.assertIn("subtitle: 'Recent loot drops, level gains, and earned honors recorded for this hero.'", script_text)

    def test_homepage_section_nav_hashes_are_scrolled_by_the_router(self):
        script_text = Path("render/script.js").read_text(encoding="utf-8")

        self.assertIn("function bindHomepageSectionNav()", script_text)
        self.assertIn("document.querySelectorAll('.home-section-nav-link, .homepage-section-nav-link')", script_text)
        self.assertIn("event.preventDefault();", script_text)
        self.assertIn("history.pushState(null, '', `#${hash}`);", script_text)
        self.assertIn("history.replaceState(null, '', `#${hash}`);", script_text)
        self.assertIn("bindHomepageSectionNav();", script_text)
        self.assertIn("function isHomepageSectionHash(hash)", script_text)
        self.assertIn("const HOMEPAGE_SECTION_HASHES = new Set([", script_text)
        self.assertIn("'homepage-status'", script_text)
        self.assertIn("'homepage-roster'", script_text)
        self.assertIn("'homepage-war-effort'", script_text)
        self.assertIn("'homepage-standouts'", script_text)
        self.assertIn("'homepage-councils'", script_text)
        self.assertIn("'homepage-analytics'", script_text)
        self.assertIn("if (isHomepageSectionHash(hash)) return { route: 'home', family: 'home' };", script_text)
        self.assertIn("if (isHomepageSectionHash(hash)) {", script_text)
        self.assertIn("window.requestAnimationFrame(() => scrollToHomepageSection(hash));", script_text)
        self.assertIn("target.scrollIntoView({ behavior: 'smooth', block: 'start' });", script_text)
        self.assertIn("showHomeView();", script_text)
        self.assertIn("updateDropdownLabel('all');", script_text)
        self.assertIn("if (!hash || hash === '') {", script_text)
        self.assertIn("} else if (hash === 'analytics') {", script_text)
        self.assertIn("} else if (hash.startsWith('war-effort-')) {", script_text)
        self.assertIn("} else if (hash.startsWith('filter-role-')) {", script_text)

    def test_homepage_command_brief_uses_existing_status_sources(self):
        template_text = Path("render/dashboard_template.html").read_text(encoding="utf-8")
        js_text = Path("render/src/js/features/home_analytics/home_overview.js").read_text(encoding="utf-8")
        script_text = Path("render/script.js").read_text(encoding="utf-8")
        css_text = Path("render/style.css").read_text(encoding="utf-8")
        mobile_css_text = Path("render/src/css/features/mobile/mobile.css").read_text(encoding="utf-8")

        self.assertIn('id="home-command-brief"', template_text)
        self.assertIn('Command Brief', template_text)
        for label in ("Reset", "Roster", "War Effort", "Movement"):
            self.assertIn(f'class="home-command-brief-label">{label}</span>', template_text)
        self.assertIn('id="home-command-brief-reset"', template_text)
        self.assertIn('id="home-command-brief-roster"', template_text)
        self.assertIn('id="home-command-brief-war-effort"', template_text)
        self.assertIn('id="home-command-brief-movement"', template_text)
        self.assertIn('Awaiting scan', template_text)
        self.assertIn('Not available', template_text)

        self.assertIn("function renderHomeCommandBrief(dashboardConfig = {}, counts = {})", js_text)
        self.assertIn("const resetEl = document.getElementById('home-command-brief-reset');", js_text)
        self.assertIn("const snapshots = window.warEffortSnapshots || null;", js_text)
        self.assertIn("const movement = dashboardConfig.membership_movement || {};", js_text)
        self.assertIn("getNumericConfigValue(movement, 'joined', 0)", js_text)
        self.assertIn("getNumericConfigValue(movement, 'departed', 0)", js_text)
        self.assertIn("getNumericConfigValue(movement, 'rejoined', 0)", js_text)
        self.assertIn("getNumericConfigValue((dashboardConfig && dashboardConfig.global_trends) || {}, 'trend_total', 0)", js_text)
        self.assertIn("renderHomeCommandBrief(dashboardConfig, {", js_text)
        self.assertIn("totalAllCount,", js_text)
        self.assertIn("raidReadyMainCount", js_text)
        self.assertNotIn("command_brief", js_text)
        self.assertNotIn("home_command_brief", js_text)
        self.assertIn("const timerEl = document.getElementById('home-command-brief-reset');", script_text)
        self.assertNotIn("const timerEl = document.getElementById('countdown-timer-text');", script_text)

        self.assertIn(".home-command-brief {", css_text)
        self.assertIn("grid-template-columns: auto minmax(0, 1fr);", css_text)
        self.assertIn(".home-command-brief-grid {", css_text)
        self.assertIn("grid-template-columns: repeat(4, minmax(0, 1fr));", css_text)
        self.assertIn(".home-command-brief-value {", css_text)
        self.assertIn("overflow-wrap: anywhere;", css_text)

        self.assertIn(".home-command-brief {", mobile_css_text)
        self.assertIn("grid-template-columns: 1fr;", mobile_css_text)
        self.assertIn(".home-command-brief-grid {", mobile_css_text)
        self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr));", mobile_css_text)


if __name__ == "__main__":
    unittest.main()
