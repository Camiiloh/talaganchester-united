import './style.css'

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

// Lista completa de jugadores confirmados
const allPlayers = [
  { name: 'Erik Bravo', rating: 8.8, position: 'Creador' },
  { name: 'Pablo (P. Lamilladonna)', rating: 7.0, position: 'Mediocampo' },
  { name: 'Maxi Vargas', rating: 5.5, position: 'Mediocampo' },
  { name: 'Iván', rating: 7.5, position: 'Defensa' },
  { name: 'Marco', rating: 6.3, position: 'Mediocampo' },
  { name: 'Camilo', rating: 5.2, position: 'Defensa' },
  { name: 'Luis Fuentealba (Luisito)', rating: 7.3, position: 'Mediocampo' },
  { name: 'Pancho', rating: 6.0, position: 'Mediocampo' },
  { name: 'Francisco H', rating: 8.2, position: 'Delantero' },
  { name: 'Diego', rating: 7.8, position: 'Mediocampo' },
  { name: 'Riky', rating: 9.0, position: 'Atacante' },
  { name: 'Enrique', rating: 8.1, position: 'Delantero' }
];

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
function init() {
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
init();
