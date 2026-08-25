import json
import subprocess
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


class CharacterActivityIndicatorTests(unittest.TestCase):
    def test_shared_indicator_only_renders_for_active_and_inactive_states(self):
        data_js = Path("render/src/js/core/data.js").resolve()
        dom_js = Path("render/src/js/core/dom.js").resolve()
        now = datetime(2026, 8, 25, 12, 0, tzinfo=timezone.utc)

        characters = {
            "active": {"profile": {"last_login_timestamp": int((now - timedelta(days=1)).timestamp() * 1000)}},
            "quiet": {"profile": {"last_login_timestamp": int((now - timedelta(days=20)).timestamp() * 1000)}},
            "inactive": {"profile": {"last_login_timestamp": int((now - timedelta(days=61)).timestamp() * 1000)}},
            "unknown": {"profile": {}},
        }
        node_script = f"""
const fs = require('fs');
const vm = require('vm');
const makeElement = tagName => ({{
  tagName,
  className: '',
  attributes: {{}},
  children: [],
  hidden: false,
  setAttribute(name, value) {{ this.attributes[name] = String(value); }},
  appendChild(child) {{ this.children.push(child); return child; }}
}});
const context = {{
  window: {{
    CHARACTER_INACTIVITY_THRESHOLD_DAYS: 60,
    CHARACTER_RECENT_ACTIVITY_WINDOW_DAYS: 14
  }},
  document: {{ createElement: makeElement }},
  Date
}};
vm.createContext(context);
vm.runInContext(fs.readFileSync({json.dumps(str(data_js))}, 'utf8'), context);
vm.runInContext(fs.readFileSync({json.dumps(str(dom_js))}, 'utf8'), context);
context.characters = {json.dumps(characters)};
context.referenceTime = {int(now.timestamp() * 1000)};
const result = vm.runInContext(`Object.fromEntries(Object.entries(characters).map(([key, character]) => {{
  const originalNow = Date.now;
  Date.now = () => referenceTime;
  const indicator = buildCharacterActivityIndicator(character);
  Date.now = originalNow;
  return [key, indicator ? {{
    className: indicator.className,
    status: indicator.attributes['data-activity-status'],
    ariaLabel: indicator.attributes['aria-label'],
    role: indicator.attributes.role,
    text: indicator.textContent
  }} : null];
}}))`, context);
process.stdout.write(JSON.stringify(result));
"""
        completed = subprocess.run(
            ["node", "-e", node_script],
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(completed.stdout)

        self.assertEqual(result["active"]["status"], "active")
        self.assertIn("is-active", result["active"]["className"])
        self.assertEqual(result["active"]["ariaLabel"], "Active character")
        self.assertEqual(result["inactive"]["status"], "inactive")
        self.assertIn("is-inactive", result["inactive"]["className"])
        self.assertEqual(result["inactive"]["ariaLabel"], "Inactive character")
        self.assertEqual(result["inactive"]["role"], "img")
        self.assertEqual(result["inactive"]["text"], "!")
        self.assertIsNone(result["quiet"])
        self.assertIsNone(result["unknown"])

    def test_dossier_and_shared_current_character_cards_use_the_indicator(self):
        script = Path("render/script.js").read_text(encoding="utf-8")
        css = Path("render/style.css").read_text(encoding="utf-8")
        dossier_css = Path("render/src/css/features/character/dossier.css").read_text(encoding="utf-8")

        self.assertIn("appendCharacterActivityIndicator(nameEl, char);", script)
        self.assertIn("character: deepChar", script)
        self.assertIn("appendCharacterActivityIndicator(nameEl, character);", script)
        self.assertIn("character-name-status-row", script)
        self.assertIn(".character-activity-indicator.is-active", css)
        self.assertIn(".character-activity-indicator.is-inactive", css)
        self.assertIn(".char-card-name .character-activity-indicator", dossier_css)


class ConcisePaginationControlsTests(unittest.TestCase):
    def test_load_more_and_show_all_share_count_state_without_reordering(self):
        dom_js = Path("render/src/js/core/dom.js").resolve()
        node_script = f"""
const fs = require('fs');
const vm = require('vm');
const context = {{}};
vm.createContext(context);
vm.runInContext(fs.readFileSync({json.dumps(str(dom_js))}, 'utf8'), context);
const result = vm.runInContext(`(() => {{
  const runScenario = (total, loadsBeforeShowAll) => {{
    const entries = Array.from({{ length: total }}, (_, index) => ({{ rank: index + 1, name: 'Player ' + (index + 1) }}));
    const container = {{ hidden: true }};
    const loadButton = {{ hidden: true, textContent: '', onclick: null }};
    const showAllButton = {{ hidden: true, textContent: '', onclick: null }};
    const state = {{ visible: Math.min(25, total), snapshots: [] }};

    const render = () => {{
      state.rendered = entries.slice(0, state.visible);
      configureIncrementalRevealButton({{
        container,
        button: loadButton,
        showAllButton,
        visibleCount: state.rendered.length,
        totalCount: entries.length,
        batchSize: 25,
        itemLabel: 'Players',
        onReveal: () => {{ state.visible = Math.min(total, state.visible + 25); render(); }},
        onShowAll: () => {{ state.visible = total; render(); }}
      }});
      state.snapshots.push({{
        visible: state.rendered.length,
        loadLabel: loadButton.textContent,
        showAllLabel: showAllButton.textContent,
        controlsHidden: container.hidden,
        loadHidden: loadButton.hidden,
        showAllHidden: showAllButton.hidden
      }});
    }};

    render();
    for (let index = 0; index < loadsBeforeShowAll; index += 1) loadButton.onclick();
    if (typeof showAllButton.onclick === 'function') showAllButton.onclick();

    return {{
      snapshots: state.snapshots,
      finalEntries: state.rendered,
      expectedEntries: entries,
      finalControlsHidden: container.hidden,
      finalLoadHidden: loadButton.hidden,
      finalShowAllHidden: showAllButton.hidden
    }};
  }};

  return {{
    immediate: runScenario(100, 0),
    afterTwoLoads: runScenario(100, 2),
    noPagination: runScenario(25, 0)
  }};
}})()`, context);
process.stdout.write(JSON.stringify(result));
"""
        completed = subprocess.run(
            ["node", "-e", node_script],
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(completed.stdout)

        self.assertEqual(result["immediate"]["snapshots"][0]["visible"], 25)
        self.assertEqual(result["immediate"]["snapshots"][0]["loadLabel"], "Load 25 More Players")
        self.assertEqual(result["immediate"]["snapshots"][0]["showAllLabel"], "Show All")
        self.assertEqual(result["immediate"]["snapshots"][-1]["visible"], 100)

        load_snapshots = result["afterTwoLoads"]["snapshots"]
        self.assertEqual([snapshot["visible"] for snapshot in load_snapshots], [25, 50, 75, 100])
        self.assertEqual(result["afterTwoLoads"]["finalEntries"], result["afterTwoLoads"]["expectedEntries"])
        self.assertTrue(result["afterTwoLoads"]["finalControlsHidden"])
        self.assertTrue(result["afterTwoLoads"]["finalLoadHidden"])
        self.assertTrue(result["afterTwoLoads"]["finalShowAllHidden"])

        no_pagination = result["noPagination"]
        self.assertEqual(no_pagination["snapshots"], [{
            "visible": 25,
            "loadLabel": "",
            "showAllLabel": "",
            "controlsHidden": True,
            "loadHidden": True,
            "showAllHidden": True,
        }])

    def test_show_all_control_is_wired_to_the_only_25_player_loader(self):
        template = Path("render/dashboard_template.html").read_text(encoding="utf-8")
        script = Path("render/script.js").read_text(encoding="utf-8")
        mobile_css = Path("render/src/css/features/mobile/mobile.css").read_text(encoding="utf-8")

        self.assertEqual(template.count("Load 25 More Players"), 1)
        self.assertEqual(template.count('id="concise-show-all-btn"'), 1)
        self.assertIn("showAllButton: conciseShowAllBtn", script)
        self.assertIn("conciseRenderedCount = totalRenderableRows;", script)
        self.assertIn("#concise-load-more-container .tl-load-more-btn", mobile_css)


if __name__ == "__main__":
    unittest.main()
