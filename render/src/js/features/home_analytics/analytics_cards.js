// Home and analytics card render helpers prepended during final JS assembly.

function formatHashName(name) {
    return (name || '').toLowerCase();
}

function setHomeRoute(el, route) {
    if (!el) return;
    if (route) el.setAttribute('data-home-route', route);
    else el.removeAttribute('data-home-route');
}

function resolvePortrait(entry) {
    if (!entry) return getClassIcon('Warrior');
    return entry.render_url || getClassIcon(getCharClass(entry));
}

function applyPressureCard(id, count, stateText, metaText) {
    const card = document.getElementById(id);
    if (!card) return;

    const valueEl = card.querySelector('.analytics-pressure-value');
    const stateEl = card.querySelector('.analytics-pressure-state');
    const metaEl = card.querySelector('.analytics-pressure-meta');

    if (valueEl) valueEl.textContent = count.toLocaleString();
    if (stateEl) stateEl.textContent = stateText;
    if (metaEl) metaEl.textContent = metaText;
}

function applyReadinessCard(id, config) {
    const card = document.getElementById(id);
    if (!card) return;

    const {
        eyebrow = '',
        name = 'Awaiting deployment',
        value = 'No geared hero logged',
        meta = 'This slot updates when a matching endgame hero is available.',
        route = '',
        portrait = getClassIcon('Warrior'),
        alt = '',
        cta = 'Inspect dossier ➔'
    } = config || {};

    const eyebrowEl = card.querySelector('.analytics-readiness-kicker');
    const nameEl = card.querySelector('.analytics-readiness-name');
    const valueEl = card.querySelector('.analytics-readiness-value');
    const metaEl = card.querySelector('.analytics-readiness-meta');
    const ctaEl = card.querySelector('.analytics-readiness-cta');
    const portraitEl = card.querySelector('.analytics-readiness-portrait');

    if (eyebrowEl) eyebrowEl.textContent = eyebrow;
    if (nameEl) nameEl.textContent = name;
    if (valueEl) valueEl.textContent = value;
    if (metaEl) metaEl.textContent = meta;
    if (ctaEl) ctaEl.textContent = cta;
    if (portraitEl) {
        portraitEl.src = portrait;
        portraitEl.alt = alt || name;
    }

    setHomeRoute(card, route);
}

function applySpotlightCard(id, config) {
    const card = document.getElementById(id);
    if (!card) return;

    const {
        eyebrow = '',
        name = 'Awaiting data',
        value = 'No movement recorded',
        meta = 'This slot will populate when the guild logs more history.',
        route = '',
        portrait = getClassIcon('Warrior'),
        alt = '',
        cta = 'Inspect ➔'
    } = config || {};

    const eyebrowEl = card.querySelector('.analytics-spotlight-kicker');
    const nameEl = card.querySelector('.analytics-spotlight-name');
    const valueEl = card.querySelector('.analytics-spotlight-value');
    const metaEl = card.querySelector('.analytics-spotlight-meta');
    const ctaEl = card.querySelector('.analytics-spotlight-cta');
    const portraitEl = card.querySelector('.analytics-spotlight-portrait');

    if (eyebrowEl) eyebrowEl.textContent = eyebrow;
    if (nameEl) nameEl.textContent = name;
    if (valueEl) valueEl.textContent = value;
    if (metaEl) metaEl.textContent = meta;
    if (ctaEl) ctaEl.textContent = cta;
    if (portraitEl) {
        portraitEl.src = portrait;
        portraitEl.alt = alt || name;
    }

    setHomeRoute(card, route);
}

function formatAnalyticsSnapshotDelta(deltaValue) {
    const numericDelta = Number(deltaValue);
    if (!Number.isFinite(numericDelta)) return 'No prior scan';
    if (numericDelta === 0) return 'No change since previous scan';

    const sign = numericDelta > 0 ? '+' : '-';
    return `${sign}${Math.abs(numericDelta).toLocaleString()} since previous scan`;
}

function formatAnalyticsSnapshotValue(value) {
    const numericValue = Number(value);
    if (!Number.isFinite(numericValue)) return '—';
    return numericValue.toLocaleString();
}

function renderAnalyticsSnapshotCard(cardId, config = {}) {
    const cardEl = document.getElementById(cardId);
    if (!cardEl) return;

    const valueEl = cardEl.querySelector('.analytics-snapshot-value');
    const statusEl = cardEl.querySelector('.analytics-snapshot-status');
    const scopeEl = cardEl.querySelector('.analytics-snapshot-scope');

    if (valueEl) valueEl.textContent = config.valueText || '—';
    if (statusEl) statusEl.textContent = config.statusText || 'Current snapshot';
    if (scopeEl) scopeEl.textContent = config.scopeText || '';
}

function renderAnalyticsSnapshotStrip(snapshot = {}) {
    renderAnalyticsSnapshotCard('analytics-snapshot-guild-roster', {
        valueText: formatAnalyticsSnapshotValue(snapshot.guildRosterValue),
        statusText: formatAnalyticsSnapshotDelta(snapshot.guildRosterDelta),
        scopeText: 'Raw guild roster total from the roster endpoint.'
    });

    renderAnalyticsSnapshotCard('analytics-snapshot-active-mains', {
        valueText: formatAnalyticsSnapshotValue(snapshot.activeMainsValue),
        statusText: formatAnalyticsSnapshotDelta(snapshot.activeMainsDelta),
        scopeText: 'Mains seen in the configured activity window.'
    });

    renderAnalyticsSnapshotCard('analytics-snapshot-raid-ready', {
        valueText: formatAnalyticsSnapshotValue(snapshot.raidReadyValue),
        statusText: formatAnalyticsSnapshotDelta(snapshot.raidReadyDelta),
        scopeText: 'Mains meeting the configured readiness threshold.'
    });

    renderAnalyticsSnapshotCard('analytics-snapshot-ilvl', {
        valueText: formatAnalyticsSnapshotValue(snapshot.avgIlvlValue),
        statusText: 'No prior scan',
        scopeText: 'Tracking from this scan. Level 70 mains only.'
    });
}

function getPressureState(count, role) {
    if (role === 'Tank') {
        if (count <= 2) return { state: 'Thin shield wall', meta: 'Priority role for dependable raid structure and dungeon leadership.' };
        if (count <= 4) return { state: 'Serviceable line', meta: 'Enough tanks to field content, but depth can still improve.' };
        return { state: 'Fortified line', meta: 'Tank coverage is healthy across the known-spec roster.' };
    }

    if (role === 'Healer') {
        if (count <= 3) return { state: 'Fragile sustain', meta: 'Healing coverage is light and should stay on the officer radar.' };
        if (count <= 6) return { state: 'Stable support', meta: 'Healing depth can sustain most nights without feeling wasteful.' };
        return { state: 'Sanctified reserve', meta: 'Healer depth looks comfortable for split groups and absences.' };
    }

    if (role === 'Ranged DPS') {
        if (count <= 4) return { state: 'Arcane gap', meta: 'Caster and ranged pressure feels thin for larger raid compositions.' };
        if (count <= 8) return { state: 'Balanced volley', meta: 'Ranged support is present, but still worth growing for flexibility.' };
        return { state: 'Volley secured', meta: 'Ranged depth is strong and well represented in the current roster.' };
    }

    if (count <= 5) return { state: 'Lean blade line', meta: 'Melee coverage exists, though substitutions could still feel tight.' };
    if (count <= 10) return { state: 'Battle-ready line', meta: 'Melee presence is healthy for most progression and farm nights.' };
    return { state: 'Frontline overflowing', meta: 'Melee pressure is abundant across the current warband.' };
}
