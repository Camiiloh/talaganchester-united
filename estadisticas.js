// Sistema de estadísticas de partidos
let historialPartidos = [];
let authConfig = null;
let isAuthenticated = false;

// Cargar datos al iniciar
document.addEventListener('DOMContentLoaded', async () => {
  await cargarConfiguracionAuth();
  verificarSesionActiva();
  await cargarHistorial();
  
  // Cargar datos del localStorage si existen (para cambios locales)
  const historialGuardado = localStorage.getItem('historial_partidos');
  if (historialGuardado) {
    try {
      const historialLocal = JSON.parse(historialGuardado);
      if (historialLocal.length > historialPartidos.length) {
        historialPartidos = historialLocal;
      }
    } catch (error) {
      console.log('Error al cargar del localStorage');
    }
  }
  
  actualizarEstadisticas();
  mostrarHistorial();
  mostrarGoleadores();
});

// Cargar historial desde JSON
async function cargarHistorial() {
  try {
    const response = await fetch('historial_partidos.json?_=' + Date.now());
    if (response.ok) {
      historialPartidos = await response.json();
      console.log('Historial cargado:', historialPartidos);
    }
  } catch (error) {
    console.log('No se pudo cargar el historial, iniciando vacío');
    historialPartidos = [];
  }
}

// Guardar historial en localStorage
function guardarHistorial() {
  localStorage.setItem('historial_partidos', JSON.stringify(historialPartidos));
  console.log('Historial actualizado:', JSON.stringify(historialPartidos, null, 2));
}

// Actualizar estadísticas generales
function actualizarEstadisticas() {
  const totalPartidos = historialPartidos.filter(p => p.estado === 'finalizado').length;
  const victoriasRojo = historialPartidos.filter(p => 
    p.estado === 'finalizado' && p.resultado.rojo > p.resultado.negro
  ).length;
  const victoriasNegro = historialPartidos.filter(p => 
    p.estado === 'finalizado' && p.resultado.negro > p.resultado.rojo
  ).length;
  const empates = historialPartidos.filter(p => 
    p.estado === 'finalizado' && p.resultado.rojo === p.resultado.negro
  ).length;

  document.getElementById('total-partidos').textContent = totalPartidos;
  document.getElementById('victorias-rojo').textContent = victoriasRojo;
  document.getElementById('victorias-negro').textContent = victoriasNegro;
  document.getElementById('empates').textContent = empates;
}

// Mostrar historial de partidos
function mostrarHistorial() {
  console.log('mostrarHistorial() llamada');
  console.log('historialPartidos:', historialPartidos);
  
  const container = document.getElementById('historial-container');
  console.log('container encontrado:', container);
  
  if (!container) {
    console.error('No se encontró el contenedor historial-container');
    return;
  }
  
  if (historialPartidos.length === 0) {
    console.log('No hay partidos en el historial');
    container.innerHTML = '<p style="text-align: center; color: #666; padding: 20px;">No hay partidos registrados aún</p>';
    return;
  }

  const partidosOrdenados = [...historialPartidos]
    .filter(p => p.estado === 'finalizado')
    .sort((a, b) => new Date(b.fecha) - new Date(a.fecha));
    
  console.log('partidosOrdenados:', partidosOrdenados);

  container.innerHTML = partidosOrdenados.map((partido, index) => {
    const ganador = partido.resultado.rojo > partido.resultado.negro ? 'rojo' : 
                   partido.resultado.negro > partido.resultado.rojo ? 'negro' : 'empate';
    
    // Encontrar el índice original en el historial
    const indiceOriginal = historialPartidos.findIndex(p => 
      p.fecha === partido.fecha && 
      p.hora === partido.hora && 
      p.resultado.rojo === partido.resultado.rojo && 
      p.resultado.negro === partido.resultado.negro
    );
    
  container.innerHTML = partidosOrdenados.map((partido, index) => {
    const ganador = partido.resultado.rojo > partido.resultado.negro ? 'rojo' : 
                   partido.resultado.negro > partido.resultado.rojo ? 'negro' : 'empate';
    
    // Encontrar el índice original en el historial
    const indiceOriginal = historialPartidos.findIndex(p => 
      p.fecha === partido.fecha && 
      p.hora === partido.hora && 
      p.resultado.rojo === partido.resultado.rojo && 
      p.resultado.negro === partido.resultado.negro
    );
    
    // Mostrar jugadores de los equipos
    const equipoRojoJugadores = partido.equipo_rojo ? partido.equipo_rojo.join(', ') : 'No registrado';
    const equipoNegroJugadores = partido.equipo_negro ? partido.equipo_negro.join(', ') : 'No registrado';
    
    return `
      <div class="match-item" data-index="${indiceOriginal}" style="background: white; color: black; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 15px; padding: 15px;">
        <div class="match-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
          <div>
            <div style="font-weight: bold; color: black;">${partido.fecha_formato}</div>
            <div class="match-date" style="color: #555;">${partido.hora} hrs - ${partido.cancha}</div>
            ${partido.mvp ? `<div style="font-size: 0.9em; color: #333;">🏆 MVP: ${partido.mvp}</div>` : ''}
          </div>
          <div class="match-result" style="text-align: center;">
            <div style="font-size: 1.5em; font-weight: bold; color: black;">
              <span class="team-red" style="color: #d32f2f;">${partido.resultado.rojo}</span>
              <span style="color: black;"> - </span>
              <span class="team-black" style="color: #424242;">${partido.resultado.negro}</span>
              ${ganador !== 'empate' ? `<span style="margin-left: 10px;">${ganador === 'rojo' ? '🔴' : '⚫'}</span>` : ' 🤝'}
            </div>
          </div>
          <div class="match-actions">
            <button class="btn-edit" onclick="verificarParaEditar(editarPartido, ${indiceOriginal})">✏️ Editar</button>
            <button class="btn-delete" onclick="verificarParaEditar(eliminarPartido, ${indiceOriginal})">🗑️ Eliminar</button>
          </div>
        </div>
        
        <div class="teams-lineup" style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 10px; border-top: 1px solid #eee; padding-top: 10px;">
          <div class="team-red-lineup">
            <div style="font-weight: bold; color: #d32f2f; margin-bottom: 5px;">🔴 Equipo Rojo</div>
            <div style="font-size: 0.9em; color: black; line-height: 1.4;">${equipoRojoJugadores}</div>
          </div>
          <div class="team-black-lineup">
            <div style="font-weight: bold; color: #424242; margin-bottom: 5px;">⚫ Equipo Negro</div>
            <div style="font-size: 0.9em; color: black; line-height: 1.4;">${equipoNegroJugadores}</div>
          </div>
        </div>
        
        ${partido.goleadores && partido.goleadores.length > 0 ? `
          <div class="goleadores-partido" style="margin-top: 10px; border-top: 1px solid #eee; padding-top: 10px;">
            <div style="font-weight: bold; color: black; margin-bottom: 5px;">⚽ Goleadores</div>
            <div style="font-size: 0.9em; color: black;">
              ${partido.goleadores.map(g => `${g.jugador} (${g.goles})`).join(' • ')}
            </div>
          </div>
        ` : ''}
      </div>
    `;
  }).join('');
}

// Calcular y mostrar goleadores
function mostrarGoleadores() {
  const container = document.getElementById('goleadores-container');
  
  if (!container) return;
  
  // Sumar goles por jugador
  const golesPorJugador = {};
  historialPartidos
    .filter(p => p.estado === 'finalizado')
    .forEach(partido => {
      if (partido.goleadores) {
        partido.goleadores.forEach(gol => {
          if (!golesPorJugador[gol.jugador]) {
            golesPorJugador[gol.jugador] = 0;
          }
          golesPorJugador[gol.jugador] += gol.goles;
        });
      }
    });

  const topGoleadores = Object.entries(golesPorJugador)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 10);

  if (topGoleadores.length === 0) {
    container.innerHTML = '<p style="text-align: center; color: #666; padding: 20px;">No hay goleadores registrados</p>';
    return;
  }

  container.innerHTML = topGoleadores.map(([jugador, goles], index) => `
    <div class="scorer-item">
      <div>
        <span style="font-weight: bold;">${index + 1}. ${jugador}</span>
      </div>
      <div style="font-weight: bold; color: #e53935;">⚽ ${goles}</div>
    </div>
  `).join('');
}

// Modal para agregar resultado
function abrirModalResultado() {
  // Prellenar con datos del último partido programado
  const hoy = new Date().toISOString().split('T')[0];
  document.getElementById('fecha-partido').value = hoy;
  
  document.getElementById('modal-resultado').style.display = 'block';
}

function cerrarModalResultado() {
  document.getElementById('modal-resultado').style.display = 'none';
  document.getElementById('form-resultado').reset();
  
  // Limpiar estado de edición
  delete document.getElementById('form-resultado').dataset.editingIndex;
  document.querySelector('#modal-resultado h3').textContent = '📝 Agregar Resultado de Partido';
}

// Hacer accesibles las funciones globalmente
window.abrirModalResultado = abrirModalResultado;
window.cerrarModalResultado = cerrarModalResultado;

// Editar un partido existente
function editarPartido(index) {
  console.log('Editando partido:', index, historialPartidos[index]);
  
  const partido = historialPartidos[index];
  if (!partido) return;
  
  // Llenar el formulario con los datos del partido
  document.getElementById('fecha-partido').value = partido.fecha;
  document.getElementById('hora-partido').value = partido.hora || '21:00';
  document.getElementById('cancha-partido').value = partido.cancha || '';
  document.getElementById('goles-rojo').value = partido.resultado.rojo;
  document.getElementById('goles-negro').value = partido.resultado.negro;
  document.getElementById('mvp-partido').value = partido.mvp || '';
  document.getElementById('asistencia-partido').value = partido.asistencia || '';
  
  // Cambiar el título y comportamiento del modal
  const modal = document.getElementById('modal-resultado');
  const titulo = modal.querySelector('h3');
  titulo.textContent = '✏️ Editar Resultado de Partido';
  
  // Guardar el índice para la edición
  document.getElementById('form-resultado').dataset.editingIndex = index;
  
  // Mostrar el modal
  modal.style.display = 'block';
}

// Eliminar un partido
function eliminarPartido(index) {
  const partido = historialPartidos[index];
  if (!partido) return;
  
  const confirmar = confirm(
    `¿Estás seguro de que quieres eliminar el partido del ${partido.fecha_formato}?\n` +
    `Resultado: Rojo ${partido.resultado.rojo} - ${partido.resultado.negro} Negro`
  );
  
  if (confirmar) {
    historialPartidos.splice(index, 1);
    guardarHistorial();
    actualizarEstadisticas();
    mostrarHistorial();
    mostrarGoleadores();
    
    alert('Partido eliminado correctamente');
  }
}

// Manejar envío del formulario
document.getElementById('form-resultado').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const editingIndex = e.target.dataset.editingIndex;
  
  if (editingIndex !== undefined) {
    // Modo edición
    actualizarPartido(parseInt(editingIndex));
  } else {
    // Modo agregar nuevo
    await agregarNuevoPartido();
  }
});

// Función para agregar un nuevo partido
async function agregarNuevoPartido() {
  const fecha = document.getElementById('fecha-partido').value;
  const hora = document.getElementById('hora-partido').value;
  const cancha = document.getElementById('cancha-partido').value;
  const golesRojo = parseInt(document.getElementById('goles-rojo').value);
  const golesNegro = parseInt(document.getElementById('goles-negro').value);
  const mvp = document.getElementById('mvp-partido').value;
  const asistencia = parseInt(document.getElementById('asistencia-partido').value) || 0;

  // Obtener equipos del último sorteo
  let equipoRojo = [];
  let equipoNegro = [];
  
  try {
    const response = await fetch('equipos.json?_=' + Date.now());
    if (response.ok) {
      const equipos = await response.json();
      equipoRojo = equipos.rojo || [];
      equipoNegro = equipos.negro || [];
    }
  } catch (error) {
    console.log('No se pudieron cargar los equipos');
  }

  const nuevoPartido = {
    id: Date.now(),
    fecha: fecha,
    fecha_formato: formatearFecha(fecha),
    hora: hora,
    cancha: cancha,
    equipo_rojo: equipoRojo,
    equipo_negro: equipoNegro,
    resultado: {
      rojo: golesRojo,
      negro: golesNegro
    },
    mvp: mvp,
    asistencia: asistencia,
    estado: 'finalizado'
  };

  historialPartidos.push(nuevoPartido);
  
  guardarHistorial();
  actualizarEstadisticas();
  mostrarHistorial();
  mostrarGoleadores();
  
  cerrarModalResultado();
  alert('✅ Resultado guardado correctamente!');
}

// Función para actualizar un partido existente
function actualizarPartido(index) {
  const fecha = document.getElementById('fecha-partido').value;
  const hora = document.getElementById('hora-partido').value;
  const cancha = document.getElementById('cancha-partido').value;
  const golesRojo = parseInt(document.getElementById('goles-rojo').value);
  const golesNegro = parseInt(document.getElementById('goles-negro').value);
  const mvp = document.getElementById('mvp-partido').value;
  const asistencia = document.getElementById('asistencia-partido').value;

  if (!fecha || golesRojo < 0 || golesNegro < 0) {
    alert('Por favor, completa todos los campos requeridos correctamente.');
    return;
  }

  // Actualizar el partido en el historial
  historialPartidos[index] = {
    ...historialPartidos[index],
    fecha: fecha,
    fecha_formato: formatearFecha(fecha),
    hora: hora,
    cancha: cancha,
    resultado: {
      rojo: golesRojo,
      negro: golesNegro
    },
    mvp: mvp,
    asistencia: asistencia ? parseInt(asistencia) : null
  };

  guardarHistorial();
  actualizarEstadisticas();
  mostrarHistorial();
  mostrarGoleadores();
  
  cerrarModalResultado();
  alert('Partido actualizado correctamente');
}

// Función auxiliar para formatear fecha
function formatearFecha(fecha) {
  const date = new Date(fecha + 'T00:00:00');
  const opciones = { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  };
  return date.toLocaleDateString('es-ES', opciones);
}

// Cerrar modal al hacer clic fuera
document.getElementById('modal-resultado').addEventListener('click', (e) => {
  if (e.target.id === 'modal-resultado') {
    cerrarModalResultado();
  }
});

// === SISTEMA DE AUTENTICACIÓN ===

// Cargar configuración de autenticación
async function cargarConfiguracionAuth() {
  try {
    const response = await fetch('auth_config.json?_=' + Date.now());
    if (response.ok) {
      authConfig = await response.json();
    }
  } catch (error) {
    console.log('No se pudo cargar la configuración de autenticación');
    authConfig = { admin_passwords: [], session_duration: 3600000 };
  }
}

// Verificar si hay una sesión activa
function verificarSesionActiva() {
  const sesionData = localStorage.getItem('admin_session');
  if (sesionData) {
    try {
      const { timestamp } = JSON.parse(sesionData);
      const ahora = Date.now();
      const duracionSesion = authConfig?.session_duration || 3600000; // 1 hora por defecto
      
      if (ahora - timestamp < duracionSesion) {
        isAuthenticated = true;
        authExpirationTime = timestamp + duracionSesion;
        mostrarEstadoAdmin();
        return;
      } else {
        // Sesión expirada
        localStorage.removeItem('admin_session');
      }
    } catch (error) {
      localStorage.removeItem('admin_session');
    }
  }
  
  isAuthenticated = false;
  ocultarFuncionesAdmin();
}

// Mostrar modal de login
function mostrarModalLogin() {
  document.getElementById('modal-login').style.display = 'block';
  document.getElementById('password-admin').focus();
}

// Cerrar modal de login
function cerrarModalLogin() {
  document.getElementById('modal-login').style.display = 'none';
  document.getElementById('form-login').reset();
  document.getElementById('login-error').style.display = 'none';
}

// Verificar credenciales de administrador
function verificarCredenciales(password) {
  if (!authConfig || !authConfig.admin_passwords) return false;
  return authConfig.admin_passwords.includes(password);
}

// Manejar login
document.getElementById('form-login').addEventListener('submit', (e) => {
  e.preventDefault();
  
  const password = document.getElementById('password-admin').value;
  const errorDiv = document.getElementById('login-error');
  
  if (verificarCredenciales(password)) {
    // Login exitoso
    isAuthenticated = true;
    const timestamp = Date.now();
    authExpirationTime = timestamp + (authConfig?.session_duration || 3600000);
    
    localStorage.setItem('admin_session', JSON.stringify({ timestamp }));
    
    mostrarEstadoAdmin();
    cerrarModalLogin();
    
    // Verificar si había una acción pendiente
    const accionPendiente = sessionStorage.getItem('accion_pendiente');
    if (accionPendiente) {
      sessionStorage.removeItem('accion_pendiente');
      if (accionPendiente === 'agregar') {
        abrirModalResultado();
      }
    }
  } else {
    // Login fallido
    errorDiv.textContent = 'Contraseña incorrecta';
    errorDiv.style.display = 'block';
    document.getElementById('password-admin').value = '';
    document.getElementById('password-admin').focus();
  }
});

// Mostrar estado de administrador autenticado
function mostrarEstadoAdmin() {
  // Remover indicador existente si existe
  const existingIndicator = document.getElementById('admin-indicator');
  if (existingIndicator) {
    existingIndicator.remove();
  }
  
  // Crear indicador de admin
  const indicator = document.createElement('div');
  indicator.id = 'admin-indicator';
  indicator.className = 'admin-indicator';
  indicator.innerHTML = `
    👤 Admin conectado 
    <button class="logout-btn" onclick="cerrarSesion()">Salir</button>
  `;
  document.body.appendChild(indicator);
  
  // Mostrar botones de administración
  mostrarFuncionesAdmin();
  
  // Ocultar prompt de autenticación
  const authPrompt = document.getElementById('auth-prompt');
  if (authPrompt) authPrompt.style.display = 'none';
}

// Mostrar funciones de administración
function mostrarFuncionesAdmin() {
  // Mostrar botones de editar/eliminar en partidos
  const matchActions = document.querySelectorAll('.match-actions');
  matchActions.forEach(action => {
    action.style.opacity = '1';
    action.style.pointerEvents = 'auto';
  });
  
  // Habilitar botón de agregar
  const addBtn = document.querySelector('.add-result-btn');
  if (addBtn) {
    addBtn.onclick = () => abrirModalResultado();
    addBtn.style.opacity = '1';
    addBtn.style.pointerEvents = 'auto';
  }
}

// Ocultar funciones de administración
function ocultarFuncionesAdmin() {
  // Ocultar botones de editar/eliminar
  const matchActions = document.querySelectorAll('.match-actions');
  matchActions.forEach(action => {
    action.style.opacity = '0.3';
    action.style.pointerEvents = 'none';
  });
  
  // Cambiar comportamiento del botón agregar
  const addBtn = document.querySelector('.add-result-btn');
  if (addBtn) {
    addBtn.onclick = () => verificarAdmin('agregar');
  }
  
  // Mostrar prompt de autenticación
  const authPrompt = document.getElementById('auth-prompt');
  if (authPrompt) authPrompt.style.display = 'block';
}

// Verificar autenticación antes de acción administrativa
function verificarAdmin(accion) {
  if (isAuthenticated) {
    // Verificar si la sesión sigue activa
    const ahora = Date.now();
    if (ahora < authExpirationTime) {
      if (accion === 'agregar') {
        abrirModalResultado();
      }
      return true;
    } else {
      // Sesión expirada
      cerrarSesion();
    }
  }
  
  // No autenticado, guardar acción pendiente y mostrar login
  sessionStorage.setItem('accion_pendiente', accion);
  mostrarModalLogin();
  return false;
}

// Cerrar sesión de administrador
function cerrarSesion() {
  isAuthenticated = false;
  authExpirationTime = null;
  localStorage.removeItem('admin_session');
  sessionStorage.removeItem('accion_pendiente');
  
  // Remover indicador de admin
  const indicator = document.getElementById('admin-indicator');
  if (indicator) {
    indicator.remove();
  }
  
  ocultarFuncionesAdmin();
}

// Modificar funciones de editar y eliminar para verificar autenticación
const editarPartidoOriginal = editarPartido;
const eliminarPartidoOriginal = eliminarPartido;

window.editarPartido = function(index) {
  if (verificarAdmin('editar')) {
    editarPartidoOriginal(index);
  }
};

window.eliminarPartido = function(index) {
  if (verificarAdmin('eliminar')) {
    eliminarPartidoOriginal(index);
  }
};

// Hacer disponible globalmente las funciones necesarias
window.verificarAdmin = verificarAdmin;
window.mostrarModalLogin = mostrarModalLogin;
window.cerrarModalLogin = cerrarModalLogin;
window.cerrarSesion = cerrarSesion;
