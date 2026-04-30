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

function formatAnalyticsCampaignArchiveWeek(weekValue) {
    const rawWeek = String(weekValue || '').trim();
    if (!rawWeek) return '—';

    const parsedWeek = new Date(rawWeek);
    if (Number.isNaN(parsedWeek.getTime())) return rawWeek;

    return parsedWeek.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    });
}

function renderAnalyticsCampaignHistoryCard(archive = {}) {
    const cardEl = document.getElementById('analytics-campaign-history-card');
    if (!cardEl) return;

    const summaryEl = document.getElementById('analytics-campaign-history-summary');
    const emptyEl = document.getElementById('analytics-campaign-history-empty');
    const weeksValueEl = document.getElementById('analytics-campaign-history-weeks');
    const latestValueEl = document.getElementById('analytics-campaign-history-latest');
    const entriesValueEl = document.getElementById('analytics-campaign-history-entries');
    const reigningValueEl = document.getElementById('analytics-campaign-history-reigning');
    const metricsEl = document.getElementById('analytics-campaign-history-metrics');
    const ctaEl = document.getElementById('analytics-campaign-history-cta');

    const weeks = Array.isArray(archive.weeks) ? archive.weeks : [];
    const derivedWeekCount = Number.isFinite(Number(archive.archived_weeks))
        ? Number(archive.archived_weeks)
        : weeks.length;
    const latestWeekRaw = String(archive.latest_week || weeks[0]?.week_anchor || '').trim();
    const derivedEntryCount = Number.isFinite(Number(archive.total_campaign_entries))
        ? Number(archive.total_campaign_entries)
        : weeks.reduce((sum, week) => {
            return sum + Number(week?.war_effort_entry_count || 0) + Number(week?.ladder_entry_count || 0);
        }, 0);
    const derivedReigningCount = Number.isFinite(Number(archive.reigning_titles_logged))
        ? Number(archive.reigning_titles_logged)
        : weeks.reduce((sum, week) => sum + Number(week?.reigning_entry_count || 0), 0);
    const hasArchive = derivedWeekCount > 0 || !!latestWeekRaw || derivedEntryCount > 0 || derivedReigningCount > 0;

    if (weeksValueEl) weeksValueEl.textContent = hasArchive ? derivedWeekCount.toLocaleString() : '—';
    if (latestValueEl) latestValueEl.textContent = hasArchive ? formatAnalyticsCampaignArchiveWeek(latestWeekRaw) : '—';
    if (entriesValueEl) entriesValueEl.textContent = hasArchive ? derivedEntryCount.toLocaleString() : '—';
    if (reigningValueEl) reigningValueEl.textContent = hasArchive ? derivedReigningCount.toLocaleString() : '—';

    if (summaryEl) {
        if (hasArchive) {
            const weekLabel = formatAnalyticsCampaignArchiveWeek(latestWeekRaw);
            const weekNoun = derivedWeekCount === 1 ? 'week' : 'weeks';
            const entryNoun = derivedEntryCount === 1 ? 'entry' : 'entries';
            summaryEl.textContent = `${derivedWeekCount.toLocaleString()} archived ${weekNoun} are currently recorded. Latest week: ${weekLabel}. ${derivedEntryCount.toLocaleString()} campaign ${entryNoun} are represented in the archive.`;
        } else {
            summaryEl.textContent = 'No archived campaign weeks are available yet.';
        }
    }

    if (emptyEl) {
        emptyEl.hidden = hasArchive;
        emptyEl.textContent = 'No archived campaign weeks are available yet.';
    }

    if (metricsEl) {
        metricsEl.setAttribute('data-archive-state', hasArchive ? 'populated' : 'empty');
    }

    if (ctaEl) {
        ctaEl.setAttribute('href', '#campaign-archive');
    }
}

function formatAnalyticsFunnelPercent(count, total) {
    const numericCount = Number(count);
    const numericTotal = Number(total);
    if (!Number.isFinite(numericCount) || !Number.isFinite(numericTotal) || numericTotal <= 0) return null;
    return Math.round((numericCount / numericTotal) * 100);
}

function renderAnalyticsReadinessFunnel(funnel = {}) {
    const cardEl = document.getElementById('analytics-readiness-funnel-card');
    if (!cardEl) return;

    const stagesEl = document.getElementById('analytics-readiness-funnel-stages');
    const summaryEl = document.getElementById('analytics-readiness-funnel-summary');
    const noteEl = document.getElementById('analytics-readiness-funnel-note');
    const emptyEl = document.getElementById('analytics-readiness-funnel-empty');

    if (!stagesEl || !summaryEl || !noteEl || !emptyEl) return;

    const hasSnapshotData = !!funnel.hasSnapshotData;
    const totalRoster = Number(funnel.guildRoster);
    const activeMains = Number(funnel.activeMains);
    const level70Mains = Number(funnel.level70Mains);
    const raidReadyMains = Number(funnel.raidReadyMains);

    if (!hasSnapshotData || !Number.isFinite(totalRoster) || totalRoster <= 0) {
        stagesEl.innerHTML = '';
        summaryEl.textContent = 'Readiness funnel data is not available for this snapshot.';
        noteEl.hidden = true;
        emptyEl.hidden = false;
        return;
    }

    const hasActive = Number.isFinite(activeMains) && activeMains >= 0;
    const hasLevel70 = Number.isFinite(level70Mains) && level70Mains >= 0;
    const hasRaidReady = Number.isFinite(raidReadyMains) && raidReadyMains >= 0;

    const stageDefinitions = [
        {
            key: 'guild-roster',
            label: 'Guild Roster',
            value: totalRoster,
            meterPercent: 100,
            helper: 'Known characters in the current roster snapshot.',
            meta: '100% of known roster',
            available: true
        },
        {
            key: 'active-mains',
            label: 'Active Mains',
            value: activeMains,
            meterPercent: formatAnalyticsFunnelPercent(activeMains, totalRoster),
            helper: 'Mains seen in the configured recent activity window.',
            meta: hasActive ? `${formatAnalyticsFunnelPercent(activeMains, totalRoster)}% of known roster` : 'Not available from current snapshot',
            available: hasActive
        },
        {
            key: 'level-70-mains',
            label: 'Level 70 Mains',
            value: level70Mains,
            meterPercent: formatAnalyticsFunnelPercent(level70Mains, totalRoster),
            helper: 'Tracked mains currently at level 70.',
            meta: hasLevel70 ? `${formatAnalyticsFunnelPercent(level70Mains, totalRoster)}% of known roster` : 'Not available from current snapshot',
            available: hasLevel70
        },
        {
            key: 'raid-ready-mains',
            label: 'Raid-Ready Mains',
            value: raidReadyMains,
            meterPercent: formatAnalyticsFunnelPercent(raidReadyMains, totalRoster),
            helper: 'Mains meeting the current raid-ready threshold.',
            meta: hasRaidReady
                ? (() => {
                    const rosterShare = formatAnalyticsFunnelPercent(raidReadyMains, totalRoster);
                    const levelShare = hasLevel70 ? formatAnalyticsFunnelPercent(raidReadyMains, level70Mains) : null;
                    if (levelShare === null) return `${rosterShare}% of known roster`;
                    return `${rosterShare}% of known roster · ${levelShare}% of level 70 mains`;
                })()
                : 'Not available from current snapshot',
            available: hasRaidReady
        }
    ];

    const availableStages = stageDefinitions.filter(stage => stage.available);
    const hasPartialData = availableStages.length > 0 && availableStages.length < stageDefinitions.length;

    if (!availableStages.length) {
        stagesEl.innerHTML = '';
        summaryEl.textContent = 'Readiness funnel data is not available for this snapshot.';
        noteEl.hidden = true;
        emptyEl.hidden = false;
        return;
    }

    stagesEl.innerHTML = availableStages.map(stage => {
        const meterPercent = Number.isFinite(Number(stage.meterPercent)) ? Math.max(0, Math.min(100, Number(stage.meterPercent))) : 0;
        return `
            <div class="analytics-readiness-funnel-stage" data-stage="${stage.key}">
                <div class="analytics-readiness-funnel-stage-head">
                    <span class="analytics-readiness-funnel-label">${stage.label}</span>
                    <strong class="analytics-readiness-funnel-value">${Number(stage.value).toLocaleString()}</strong>
                </div>
                <div class="analytics-readiness-funnel-meter" aria-hidden="true">
                    <span class="analytics-readiness-funnel-fill" style="width: ${meterPercent}%;"></span>
                </div>
                <span class="analytics-readiness-funnel-meta">${stage.meta}</span>
                <span class="analytics-readiness-funnel-helper">${stage.helper}</span>
            </div>
        `;
    }).join('');

    summaryEl.textContent = 'This funnel compares the same snapshot across raw roster size, active mains, level 70 mains, and raid-ready mains. Activity and level-cap stages are parallel readiness cuts, while raid-ready mains remain a subset of level 70 mains.';
    noteEl.hidden = !hasPartialData;
    emptyEl.hidden = true;
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
