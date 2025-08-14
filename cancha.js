// Script para hacer dinámico cancha.html
async function cargarEquipos() {
  const resp = await fetch('equipos.json?_=' + Date.now());
  const data = await resp.json();
  
  // Actualizar título de la página
  actualizarTitulo(data);
  
  return data;
}

function actualizarTitulo(equipos) {
  // Formatear fecha igual que en los scripts de Python
  let fechaTexto = equipos.fecha || 'Fecha por confirmar';
  if (fechaTexto !== 'Fecha por confirmar' && fechaTexto !== 'Por confirmar') {
    try {
      const fecha = new Date(fechaTexto + 'T00:00:00');
      const diasSemana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
      const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                     'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
      
      const diaSemana = diasSemana[fecha.getDay()];
      const dia = fecha.getDate();
      const mes = meses[fecha.getMonth()];
      
      fechaTexto = `${diaSemana} ${dia} de ${mes}`;
    } catch (e) {
      // Si no se puede parsear, usar el texto original
    }
  }
  
  // Formatear hora igual que en Python
  let hora = equipos.hora || 'Por confirmar';
  if (hora !== 'Por confirmar') {
    hora = `${hora} hrs`;
  }
  
  // Formatear cancha igual que en Python
  let cancha = equipos.cancha || 'Por confirmar';
  if (cancha !== 'Por confirmar' && /^\d+$/.test(cancha.toString().trim())) {
    cancha = `Cancha ${cancha}`;
  }
  
  // Crear nuevo título con el formato exacto
  const nuevoTitulo = `⚽ Partido ${fechaTexto} - ${hora} - ${cancha}`;
  
  // Actualizar title del documento
  document.title = nuevoTitulo;
  
  // Actualizar el h1 con id partido-info
  const partidoInfo = document.getElementById('partido-info');
  if (partidoInfo) {
    partidoInfo.textContent = nuevoTitulo;
  }
}

// Posiciones para los jugadores en la cancha (basado en el HTML original)
const posicionesCancha = {
  negro: [
    { left: '2%', top: '50%' },   // Arquero
    { left: '18%', top: '25%' },  // Defensa
    { left: '35%', top: '25%' },  // Defensa
    { left: '35%', top: '75%' },  // Mediocampo
    { left: '18%', top: '75%' },  // Mediocampo
    { left: '45%', top: '50%' },  // Delantero
    { left: '45%', top: '30%' },  // Extra posición 1
    { left: '45%', top: '70%' },  // Extra posición 2
  ],
  rojo: [
    { left: '98%', top: '50%' },  // Arquero
    { left: '82%', top: '75%' },  // Defensa
    { left: '65%', top: '25%' },  // Defensa
    { left: '82%', top: '25%' },  // Mediocampo
    { left: '65%', top: '75%' },  // Mediocampo
    { left: '55%', top: '50%' },  // Delantero
    { left: '55%', top: '30%' },  // Extra posición 1
    { left: '55%', top: '70%' },  // Extra posición 2
  ]
};

function crearJugadorCancha(nombre, color, posicion) {
  const style = Object.entries(posicion).map(([k, v]) => `${k}: ${v}`).join('; ');
  return `<div class="player ${color}-team has-photo" style="${style}">
    <img src="fotos/${nombre}.png" alt="${nombre}" class="player-photo player-photo-borde-sombra">
  </div>`;
}

function crearListadoEquipo(jugadores, color) {
  return jugadores.map(nombre => 
    `<li><img src="fotos/${nombre}.png" alt="${nombre}" style="width:28px;height:28px;vertical-align:middle;border-radius:6px;margin-right:6px;box-shadow:0 2px 8px ${color === 'black' ? '#222a3655' : '#e5393555'};"> <strong>${nombre}</strong></li>`
  ).join('\n');
}

async function renderCancha() {
  try {
    const equipos = await cargarEquipos();
    
    // Limpiar jugadores actuales de la cancha
    const field = document.querySelector('.soccer-field');
    const existingPlayers = field.querySelectorAll('.player');
    existingPlayers.forEach(player => player.remove());
    
    // Agregar jugadores del equipo negro
    equipos.negro.forEach((nombre, i) => {
      if (i < posicionesCancha.negro.length) {
        const div = document.createElement('div');
        div.innerHTML = crearJugadorCancha(nombre, 'black', posicionesCancha.negro[i]);
        field.appendChild(div.firstElementChild);
      }
    });
    
    // Agregar jugadores del equipo rojo
    equipos.rojo.forEach((nombre, i) => {
      if (i < posicionesCancha.rojo.length) {
        const div = document.createElement('div');
        div.innerHTML = crearJugadorCancha(nombre, 'red', posicionesCancha.rojo[i]);
        field.appendChild(div.firstElementChild);
      }
    });
    
    // Actualizar listados de equipos abajo de la cancha
    const teamBlack = document.querySelector('.team-info.black ul');
    const teamRed = document.querySelector('.team-info.red ul');
    
    if (teamBlack) {
      teamBlack.innerHTML = crearListadoEquipo(equipos.negro, 'black');
    }
    
    if (teamRed) {
      teamRed.innerHTML = crearListadoEquipo(equipos.rojo, 'red');
    }
    
    console.log('✅ Cancha actualizada con jugadores:', {
      negro: equipos.negro,
      rojo: equipos.rojo
    });
    
  } catch (error) {
    console.error('❌ Error cargando equipos:', error);
  }
}

// Actualización automática
let ultimaActualizacion = 0;
const INTERVALO_VERIFICACION = 5000; // 5 segundos

async function verificarYActualizar() {
  try {
    const response = await fetch('equipos.json');
    const lastModified = new Date(response.headers.get('Last-Modified') || 0).getTime();
    
    if (lastModified > ultimaActualizacion) {
      ultimaActualizacion = lastModified;
      await renderCancha();
    }
  } catch (error) {
    console.log('Error verificando actualizaciones:', error);
  }
}

// Inicializar cuando carga la página
window.addEventListener('DOMContentLoaded', renderCancha);

// Verificar actualizaciones periódicamente
setInterval(verificarYActualizar, INTERVALO_VERIFICACION);
