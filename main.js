import './style.css'

// Mapeo de posiciones técnicas a nombres en español
const positionMapping = {
  'CF': 'Delantero',
  'LM': 'Mediocampo Izquierdo',
  'CM': 'Mediocampo Centro',
  'RM': 'Mediocampo Derecho',
  'LCB': 'Defensa Izquierdo',
  'RCB': 'Defensa Derecho',
  'GK': 'Arquero'
};

// Variables globales para datos dinámicos
let equiposDinamicos = null;
let jugadoresEspecificos = [];

// Función para cargar jugadores con posiciones específicas
async function cargarJugadoresEspecificos() {
  try {
    const response = await fetch('jugadores_posiciones_especificas.json?_=' + Date.now());
    jugadoresEspecificos = await response.json();
    console.log('Jugadores con posiciones específicas cargados:', jugadoresEspecificos.length);
  } catch (error) {
    console.log('No se pudieron cargar jugadores específicos:', error);
  }
}

// Función para obtener la posición principal de un jugador
function obtenerPosicionPrincipal(posiciones) {
  if (!posiciones) return 'Posición desconocida';
  
  // Si es un string con múltiples posiciones, tomar la primera
  if (typeof posiciones === 'string') {
    const posArray = posiciones.split(',').map(p => p.trim());
    const primeraPosicion = posArray[0];
    return positionMapping[primeraPosicion] || primeraPosicion;
  }
  
  return 'Posición desconocida';
}

// Función para cargar datos del partido actual
async function cargarDatosPartido() {
  try {
    const response = await fetch('equipos.json?_=' + Date.now());
    equiposDinamicos = await response.json();
    actualizarTituloPartido();
    actualizarEquiposDinamicos();
  } catch (error) {
    console.log('No se pudieron cargar datos dinámicos, usando datos estáticos');
  }
}

// Función para actualizar el título del partido
function actualizarTituloPartido() {
  if (!equiposDinamicos) return;
  
  // Formatear fecha
  let fechaTexto = equiposDinamicos.fecha || 'Fecha por confirmar';
  if (fechaTexto !== 'Fecha por confirmar' && fechaTexto !== 'Por confirmar') {
    try {
      const fecha = new Date(fechaTexto + 'T00:00:00');
      fechaTexto = fecha.toLocaleDateString('es-ES', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch (e) {
      // Si no se puede parsear, usar el texto original
    }
  }
  
  const hora = equiposDinamicos.hora || 'Por confirmar';
  const cancha = equiposDinamicos.cancha || 'Por confirmar';
  
  // Actualizar título del documento
  document.title = `Partido ${fechaTexto} - ${hora} - Cancha ${cancha}`;
  
  // Actualizar h1 en la página
  const partidoInfo = document.getElementById('partido-info');
  if (partidoInfo) {
    partidoInfo.textContent = `⚽ Partido ${fechaTexto} - ${hora} - Cancha ${cancha}`;
  }
}

// Función para actualizar equipos con datos dinámicos
function actualizarEquiposDinamicos() {
  if (!equiposDinamicos) return;
  
  // Si hay equipos dinámicos, usarlos en lugar de los estáticos
  if (equiposDinamicos.rojo && equiposDinamicos.negro) {
    // Actualizar la visualización con los equipos reales
    console.log('Equipos actualizados desde equipos.json');
  }
}

// Team data (actualizado con los datos más recientes)
const teams = {
  team1: {
    name: 'Equipo Negro',
    players: [
      { name: 'Erik Bravo', rating: 8.8, position: 'Creador' },
      { name: 'Riky', rating: 9.0, position: 'Atacante' },
      { name: 'Luis Fuentealba (Luisito)', rating: 7.3, position: 'Mediocampo' },
      { name: 'Pablo (P. Lamilladonna)', rating: 7.0, position: 'Mediocampo' },
      { name: 'Marco', rating: 6.3, position: 'Mediocampo' },
      { name: 'Camilo', rating: 5.2, position: 'Defensa' }
    ]
  },
  team2: {
    name: 'Equipo Rojo',
    players: [
      { name: 'Francisco H', rating: 8.2, position: 'Delantero' },
      { name: 'Enrique', rating: 8.1, position: 'Delantero' },
      { name: 'Diego', rating: 7.8, position: 'Mediocampo' },
      { name: 'Iván', rating: 7.5, position: 'Defensa' },
      { name: 'Pancho', rating: 6.0, position: 'Mediocampo' },
      { name: 'Maxi Vargas', rating: 5.5, position: 'Mediocampo' }
    ]
  }
};

// Lista completa de jugadores confirmados - construida dinámicamente
let allPlayers = [];

// Calculate team average
function calculateAverage(players) {
  if (players.length === 0) return 0;
  const sum = players.reduce((acc, player) => acc + player.rating, 0);
  return (sum / players.length).toFixed(2);
}

// Update team display
function updateTeamDisplay(teamId) {
  const team = teams[teamId];
  const playersContainer = document.getElementById(`${teamId}-players`);
  const averageElement = document.getElementById(`${teamId}-average`);
  
  // Clear current players
  playersContainer.innerHTML = '';
  
  // Add players
  team.players.forEach(player => {
    const playerElement = document.createElement('div');
    playerElement.className = 'player';
    playerElement.innerHTML = `
      <span class="player-name">${player.name}</span>
      <span class="player-rating">${player.rating}</span>
    `;
    playersContainer.appendChild(playerElement);
  });
  
  // Update average
  const average = calculateAverage(team.players);
  averageElement.textContent = average;
}

// Add player to team
function addPlayerToTeam(teamId, player) {
  teams[teamId].players.push(player);
  updateTeamDisplay(teamId);
}

// Initialize the app
async function init() {
  // Cargar datos dinámicos del partido y jugadores específicos
  await cargarDatosPartido();
  await cargarJugadoresEspecificos();
  
  // Construir allPlayers desde los datos cargados
  allPlayers = jugadoresEspecificos.map(jugador => ({
    name: jugador.nombre,
    rating: jugador.puntaje,
    position: obtenerPosicionPrincipal(jugador.posicion),
    posiciones: jugador.posicion,
    puntajesPorPosicion: jugador.puntajes_posicion
  }));
  
  // Update team averages button
  document.getElementById('update-teams').addEventListener('click', () => {
    const erikTeam = document.getElementById('erik-team').value;
    const rikyTeam = document.getElementById('riky-team').value;
    const diegoTeam = document.getElementById('diego-team').value;
    
    // Add new players to selected teams
    if (erikTeam) {
      const erikExists = teams[erikTeam].players.find(p => p.name === 'Erik');
      if (!erikExists) {
        addPlayerToTeam(erikTeam, newPlayers.erik);
      }
    }
    
    if (rikyTeam) {
      const rikyExists = teams[rikyTeam].players.find(p => p.name === 'Riky');
      if (!rikyExists) {
        addPlayerToTeam(rikyTeam, newPlayers.riky);
      }
    }
    
    if (diegoTeam) {
      const diegoExists = teams[diegoTeam].players.find(p => p.name === 'Diego');
      if (!diegoExists) {
        addPlayerToTeam(diegoTeam, newPlayers.diego);
      }
    }
    
    // Show success message
    alert('¡Promedios de equipos actualizados exitosamente!');
  });
  
  // Add new player form
  document.getElementById('add-player').addEventListener('click', () => {
    const name = document.getElementById('player-name').value.trim();
    const rating = parseFloat(document.getElementById('player-rating').value);
    const position = document.getElementById('player-position').value.trim();
    const teamId = document.getElementById('player-team').value;
    
    if (!name || isNaN(rating) || !teamId) {
      alert('Por favor complete todos los campos');
      return;
    }
    
    if (rating < 0 || rating > 10) {
      alert('La calificación debe estar entre 0 y 10');
      return;
    }
    
    // Check if player already exists
    const playerExists = teams[teamId].players.find(p => p.name === name);
    if (playerExists) {
      alert('El jugador ya existe en este equipo');
      return;
    }
    
    // Add player
    const newPlayer = { name, rating, position };
    addPlayerToTeam(teamId, newPlayer);
    
    // Clear form
    document.getElementById('player-name').value = '';
    document.getElementById('player-rating').value = '';
    document.getElementById('player-position').value = '';
    document.getElementById('player-team').value = '';
    
    alert(`${name} agregado a ${teams[teamId].name} exitosamente!`);
  });
}

// Start the app
init().catch(error => console.error('Error al inicializar la aplicación:', error));
