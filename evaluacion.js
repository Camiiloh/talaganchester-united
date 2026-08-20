const POSITION_ORDER = ['GK', 'LCB', 'CB', 'RCB', 'LM', 'CM', 'RM', 'CF'];
const EVALUATIONS_API = '/api/evaluaciones';
const POSITION_GROUPS = { GK: 'GK', LCB: 'defense', CB: 'defense', RCB: 'defense', LM: 'midfield', CM: 'midfield', RM: 'midfield', CF: 'attack' };
const PLAYERS = [
  ['Erik', 'CM, LM, RM'], ['Pablo', 'CM, CF'], ['Maxi Vargas', 'GK, CF'], ['Felipe Sepúlveda', 'RM, CM, LM, CF'],
  ['Iván', 'RM, LM, CM'], ['Marco', 'LCB, RCB, CB'], ['Camilo', 'GK, CM, CF'], ['Luis F', 'GK, LCB, RCB, CB'],
  ['José F', 'CM, RM, GK'], ['Alonso F', 'CF, LM, RM'], ['Pancho', 'LM, CF, CB, LCB'], ['Francisco H', 'LCB, RCB, CM, LM, RM'],
  ['José V', ''], ['Izrock', 'CM, RM, LM, CF'], ['Riky', 'LCB, RCB, CF, CB'], ['Jano', 'LCB, RCB, CB, LM, RM'],
  ['Nacho', 'LM, RM'], ['Benito', 'LCB, RCB, CB'], ['Enrique', 'LCB, RCB, CB'], ['Juan R', 'CM, LM, RM, CF'],
  ['Carlos P', 'LM, LCB, CM, RCB, CB, GK'], ['Willians', 'LCB, RCB, CM, CB'], ['Vicente', 'CM, LM, RM, CF'],
  ['Ruben', 'LCB, RCB, CF, CB'], ['Pantera', 'CF'], ['Seba Turra', 'CM, LM, RM, CF'], ['Fabián', 'CM, LM, RM, CF'],
  ['Jaime', 'CM, LM, RM, CF'], ['Nel', 'LCB, RCB, GK, CB'], ['Félix', 'LCB, RCB, CF, CB'], ['José A', 'LCB, RCB, CB'],
  ['Seba', 'CM, LM, RM'], ['Felipe S', 'LCB, RCB, CB'], ['Juan HG', 'CF, LM, RM']
].map(([name, positions]) => ({ name, positions: positions ? positions.split(', ') : [] }));

const PLAYER_PASSWORDS = {
  'Erik': 'pYqvTn8FdFaff5JJ', 'Pablo': '6eQ2jDaz6orEY2pT', 'Maxi Vargas': 'o3ZJNnKwq3A2JbNP',
  'Felipe Sepúlveda': 'jobdpZGWgTawaxsd', 'Iván': 'NXdExEQvKVDzyQVh', 'Marco': 'BZH8F2n5BeU6Mgrq',
  'Camilo': 'LtbZN5MpWG4tG6K8', 'Luis F': 'rLesQ9SmRNYc3BYv', 'José F': 'DcUaWdqqKDFz36Rk',
  'Alonso F': 'U2jRYpQrvpxxoiUS', 'Pancho': 'ZoXVRhTtyrwDbdnb', 'Francisco H': 'K9co4YRXcVWmJbzz',
  'José V': 'QasSGkixnwLBtrqV', 'Izrock': 'Y2oPGfcyBzQXBA7X', 'Riky': 'jrV5Vk9DhfSqiSET',
  'Jano': 'VkHBg35NtJumsZdu', 'Nacho': 'GxJx2y9Mh3APMkps', 'Benito': 'J5vCDW4K6DEyGaYs',
  'Enrique': 'i3LdX6MkRUhF2x6m', 'Juan R': '5e3jHDRjoP7HHVsN', 'Carlos P': 'oxUEKZBZ3EBKeZ9z',
  'Willians': 'FSF2CPwRHvxPyW3H', 'Vicente': 'vZobVkGAD2yKRGfr', 'Ruben': 'PjW9wedTEuYARofF',
  'Pantera': 'seP3XWvFLKdgoVDu', 'Seba Turra': 'kdWGvbHpTx3kZxxQ', 'Fabián': 'mhAviGXCxDpFeJEi',
  'Jaime': '7w2gXgj9GpW9wJgD', 'Nel': 'JajUoEnrYUDq3GNV', 'Félix': 'vCza3tMRsG35TaRd',
  'José A': 'YiogNGmfP4USeQk3', 'Seba': 'UrEQpTxQq3vztBfu', 'Felipe S': '8fxn3DssewcywWZL',
  'Juan HG': 'otyEsQCV7FSqhbqX'
};

const state = { evaluator: sessionStorage.getItem('usuario-evaluacion') || '', scores: JSON.parse(localStorage.getItem('evaluaciones-posiciones') || '{}'), filter: 'all', search: '' };
const $ = selector => document.querySelector(selector);
const esc = value => String(value).replace(/[&<>'"]/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[char]));
const playerKey = name => name.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-');
const playerPassword = name => PLAYER_PASSWORDS[name];
const positionsFor = player => player.positions.filter(position => POSITION_ORDER.includes(position));
const playerPhoto = (player, className) => `<img class="${className}" src="fotos/${encodeURIComponent(player.name)}.png" alt="${esc(player.name)}" loading="lazy">`;

function valuesFor(player, evaluator = null) {
  const evaluations = evaluator ? [state.scores[evaluator] || {}] : Object.values(state.scores);
  return evaluations.flatMap(evaluation => positionsFor(player).map(position => Number(evaluation[playerKey(player.name)]?.[position]))).filter(value => Number.isFinite(value) && value > 0);
}
function valueFor(player, position, evaluator = state.evaluator) { return Number(state.scores[evaluator]?.[playerKey(player.name)]?.[position]) || ''; }
function average(player) { const values = valuesFor(player); return values.length ? (values.reduce((sum, value) => sum + value, 0) / values.length).toFixed(2) : '--'; }
function positionAverage(player, position) { const values = Object.values(state.scores).map(evaluation => Number(evaluation[playerKey(player.name)]?.[position])).filter(value => Number.isFinite(value) && value > 0); return values.length ? (values.reduce((sum, value) => sum + value, 0) / values.length).toFixed(2) : 0; }
function voterCount(player) { return Object.values(state.scores).filter(evaluation => positionsFor(player).some(position => Number(evaluation[playerKey(player.name)]?.[position]) > 0)).length; }
function bestPosition(player) { const values = positionsFor(player).map(position => ({ position, value: Number(positionAverage(player, position)) })).filter(item => item.value > 0); return values.sort((a, b) => b.value - a.value)[0]?.position || '--'; }
function playerMatches(player) { return (state.filter === 'all' || positionsFor(player).some(position => POSITION_GROUPS[position] === state.filter)) && player.name.toLowerCase().includes(state.search.toLowerCase()); }

function renderIdentity() {
  $('#evaluator-select').innerHTML = '<option value="">Selecciona tu nombre</option>' + PLAYERS.map(player => `<option value="${esc(player.name)}">${esc(player.name)}</option>`).join('');
  $('#evaluator-select').value = state.evaluator;
  $('#identity-panel').hidden = Boolean(state.evaluator) || $('#players-view').hidden === false;
  $('#evaluating-label').innerHTML = state.evaluator ? `Evaluando como <strong>${esc(state.evaluator)}</strong>` : 'Selecciona tu nombre para comenzar';
}
function renderSummary() {
  const rated = PLAYERS.filter(player => valuesFor(player).length);
  const allValues = rated.flatMap(valuesFor);
  const total = allValues.length ? (allValues.reduce((sum, value) => sum + value, 0) / allValues.length).toFixed(2) : '0';
  $('#summary').innerHTML = [['Jugadores', PLAYERS.length], ['Promedio general', total], ['Puntaje máximo', allValues.length ? Math.max(...allValues) : 0], ['Con evaluaciones', rated.length]].map(([label, value]) => `<div class="summary-card"><span>${label}</span><strong>${value}</strong></div>`).join('');
}
function renderEvaluations() {
  if (!state.evaluator) {
    $('#evaluation-list').innerHTML = '<div class="identity-required">Selecciona tu nombre para comenzar a evaluar.</div>';
    return;
  }
  $('#evaluation-list').innerHTML = PLAYERS.filter(player => player.name !== state.evaluator).map(player => `<article class="evaluation-card"><div class="player-heading"><div class="avatar">${playerPhoto(player, 'player-photo')}</div><div><h2>${esc(player.name)}</h2><p>${positionsFor(player).join(', ') || 'Sin posiciones asignadas'}</p></div><div class="current-average"><span>Promedio de todos</span><strong>${average(player)}</strong></div></div><div class="score-grid">${positionsFor(player).map(position => { const value = valueFor(player, position); return `<label>${position}<input class="score-input" data-player="${esc(player.name)}" data-position="${position}" type="number" min="1" max="10" step="0.1" value="${value}" placeholder="1-10"></label>`; }).join('') || '<p class="empty-position">Este jugador aún no tiene posiciones marcadas.</p>'}</div></article>`).join('');
}
function renderPlayers() {
  const visiblePlayers = PLAYERS.filter(playerMatches).sort((first, second) => Number(average(second) === '--' ? -1 : average(second)) - Number(average(first) === '--' ? -1 : average(first)));
  $('#players-table').innerHTML = visiblePlayers.map(player => `<tr><td><span class="player-cell"><img class="table-avatar player-photo" src="fotos/${encodeURIComponent(player.name)}.png" alt="${esc(player.name)}" loading="lazy"><strong>${esc(player.name)}</strong></span></td><td>${positionsFor(player).join(', ') || '--'}</td><td class="global-score">${average(player)}</td>${POSITION_ORDER.map(position => `<td>${positionsFor(player).includes(position) ? positionAverage(player, position) : '<span class="muted">-</span>'}</td>`).join('')}<td><span class="best-position">${bestPosition(player)}</span></td><td>${voterCount(player)}</td></tr>`).join('');
}
function render() { renderIdentity(); renderSummary(); renderEvaluations(); renderPlayers(); }
function showToast(message) { const toast = $('#toast'); toast.textContent = message; toast.classList.add('visible'); setTimeout(() => toast.classList.remove('visible'), 2400); }
function cerrarSesion() { state.evaluator = ''; sessionStorage.removeItem('usuario-evaluacion'); document.body.classList.remove('authenticated'); $('#login-screen').hidden = false; $('#login-password').value = ''; $('#login-error').textContent = ''; }
function iniciarLogin() { $('#login-user').innerHTML = '<option value="">Selecciona tu jugador</option>' + PLAYERS.map(player => `<option value="${esc(player.name)}">${esc(player.name)}</option>`).join(''); if (state.evaluator) { document.body.classList.add('authenticated'); $('#login-screen').hidden = true; } }
async function cargarEvaluaciones() { try { const response = await fetch(EVALUATIONS_API); if (!response.ok) return; state.scores = await response.json(); localStorage.setItem('evaluaciones-posiciones', JSON.stringify(state.scores)); render(); } catch (error) { console.info('API de evaluaciones no disponible; usando almacenamiento local.'); } }
async function guardarEvaluaciones() { localStorage.setItem('evaluaciones-posiciones', JSON.stringify(state.scores)); try { const response = await fetch(EVALUATIONS_API, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(state.scores) }); if (!response.ok) throw new Error('No se pudo guardar en el servidor'); showToast('Puntuaciones guardadas para todos los votantes'); } catch (error) { showToast('Guardadas localmente; servidor no disponible'); } }

$('#login-form').addEventListener('submit', event => { event.preventDefault(); const user = $('#login-user').value; const password = $('#login-password').value; if (!user || password !== playerPassword(user)) { $('#login-error').textContent = 'Usuario o contraseña incorrectos.'; return; } state.evaluator = user; sessionStorage.setItem('usuario-evaluacion', user); document.body.classList.add('authenticated'); $('#login-screen').hidden = true; $('#login-error').textContent = ''; render(); });
$('#evaluator-select').addEventListener('change', event => { state.evaluator = event.target.value; sessionStorage.setItem('usuario-evaluacion', state.evaluator); render(); });
$('#change-evaluator').addEventListener('click', cerrarSesion);
$('#save-button').addEventListener('click', guardarEvaluaciones);
$('#evaluation-list').addEventListener('input', event => { if (!event.target.matches('.score-input') || !state.evaluator || event.target.dataset.player === state.evaluator) return; const { player, position } = event.target.dataset; const value = Number(event.target.value); state.scores[state.evaluator] ||= {}; state.scores[state.evaluator][playerKey(player)] ||= {}; if (value >= 1 && value <= 10) state.scores[state.evaluator][playerKey(player)][position] = value; else delete state.scores[state.evaluator][playerKey(player)][position]; localStorage.setItem('evaluaciones-posiciones', JSON.stringify(state.scores)); renderSummary(); event.target.closest('.evaluation-card').querySelector('.current-average strong').textContent = average(PLAYERS.find(item => item.name === player)); });
$('#search-input').addEventListener('input', event => { state.search = event.target.value; renderPlayers(); });
document.querySelectorAll('.filter').forEach(button => button.addEventListener('click', () => { document.querySelectorAll('.filter').forEach(item => item.classList.remove('active')); button.classList.add('active'); state.filter = button.dataset.filter; renderPlayers(); }));
document.querySelectorAll('.nav-tab').forEach(button => button.addEventListener('click', () => { document.querySelectorAll('.nav-tab').forEach(item => item.classList.remove('active')); button.classList.add('active'); const playersView = button.dataset.view === 'players'; $('#evaluate-view').hidden = playersView; $('#players-view').hidden = !playersView; $('#identity-panel').hidden = playersView || Boolean(state.evaluator); $('#page-title').textContent = playersView ? 'Plantel de jugadores' : 'Evaluación de compañeros'; $('#page-description').textContent = playersView ? 'Ranking y desglose por posiciones.' : 'Califica a cada compañero solo en las posiciones que juega.'; $('#save-button').hidden = playersView; }));
iniciarLogin();
render();
cargarEvaluaciones();
