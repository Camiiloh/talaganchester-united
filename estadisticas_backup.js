// Sistema de estadísticas de partidos
let historialPartidos = [];

// Cargar datos al iniciar
document.addEventListener('DOMContentLoaded', async () => {
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
    
    return `
      <div class="match-item" data-index="${indiceOriginal}">
        <div>
          <div>${partido.fecha_formato}</div>
          <div class="match-date">${partido.hora} hrs - ${partido.cancha}</div>
          ${partido.mvp ? `<div style="font-size: 0.9em; color: #666;">🏆 MVP: ${partido.mvp}</div>` : ''}
        </div>
        <div class="match-result">
          <span class="team-red">${partido.resultado.rojo}</span>
          -
          <span class="team-black">${partido.resultado.negro}</span>
          ${ganador !== 'empate' ? `<span style="margin-left: 10px;">${ganador === 'rojo' ? '🔴' : '⚫'}</span>` : ' 🤝'}
        </div>
        <div class="match-actions">
          <button class="btn-edit" onclick="editarPartido(${indiceOriginal})">✏️ Editar</button>
          <button class="btn-delete" onclick="eliminarPartido(${indiceOriginal})">🗑️ Eliminar</button>
        </div>
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
