// Analytics selector helpers prepended during final JS assembly.

function findRosterEntryByName(rosterData, name) {
    if (!name) return null;
    return rosterData.find(c => c.profile && c.profile.name && c.profile.name.toLowerCase() === name.toLowerCase()) || null;
}

function getTrendEntry(rosterData, kind) {
    const candidates = [...rosterData]
        .filter(c => c.profile)
        .filter(c => {
            if (kind === 'pvp') return (c.profile.trend_pvp || c.profile.trend_hks || 0) > 0;
            return (c.profile.trend_pve || c.profile.trend_ilvl || 0) > 0;
        });
    const sorted = rankCurrentLeaderboardCharacters(candidates, character => (
        kind === 'pvp'
            ? (character.profile.trend_pvp || character.profile.trend_hks || 0)
            : (character.profile.trend_pve || character.profile.trend_ilvl || 0)
    ));
    return sorted[0] || null;
}

function getTopRoleAnchor(rosterData, roleName) {
    const candidates = [...filterMainCharacters(rosterData)]
        .filter(c => c.profile && c.profile.level === 70)
        .filter(c => getCharacterRole(getCharClass(c), c.profile.active_spec || '') === roleName);
    return rankCurrentLeaderboardCharacters(
        candidates,
        character => character.profile.equipped_item_level || 0
    )[0] || null;
}
