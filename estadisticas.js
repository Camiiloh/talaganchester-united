// Sistema de estadísticas de partidos
let historialPartidos = [];
let authConfig = null;
let isAuthenticated = false;

// Cargar datos al iniciar
document.addEventListener('DOMContentLoaded', async () => {
  console.log('🚀 Iniciando carga de estadísticas...');
  
  // Cargar datos del partido para actualizar título
  await cargarDatosPartidoParaTitulo();
  
  // Cargar historial primero (es lo más importante)
  await cargarHistorial();
  
  // Cargar configuración de autenticación
  await cargarConfiguracionAuth();
  verificarSesionActiva();
  
  console.log('✅ Carga inicial completada');
});

// Función para cargar datos del partido y actualizar título
async function cargarDatosPartidoParaTitulo() {
  try {
    const response = await fetch('equipos.json?_=' + Date.now());
    const equipos = await response.json();
    actualizarTituloEstadisticas(equipos);
  } catch (error) {
    console.log('No se pudieron cargar datos para el título');
  }
}

// Función para actualizar título de estadísticas
function actualizarTituloEstadisticas(equipos) {
  // Formatear fecha
  let fechaTexto = equipos.fecha || 'Fecha por confirmar';
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
  
  const hora = equipos.hora || 'Por confirmar';
  const cancha = equipos.cancha || 'Por confirmar';
  
  // Actualizar título del documento
  document.title = `Estadísticas - ${fechaTexto} - ${hora} - Cancha ${cancha}`;
}

// Cargar historial desde la base de datos vía API
async function cargarHistorial() {
  try {
    console.log('🔄 Intentando cargar historial desde API...');
    const response = await fetch('/api/historial?_=' + Date.now());
    console.log('📡 Respuesta de la API:', response.status, response.statusText);
    
    if (response.ok) {
      let rawData = await response.json();
      console.log('📊 Datos crudos recibidos:', rawData);
      
      // Procesar datos de PostgreSQL - parsear campos JSON
      historialPartidos = rawData.map(partido => {
        // Parsear campos que vienen como strings JSON desde PostgreSQL
        if (typeof partido.resultado === 'string') {
          try {
            partido.resultado = JSON.parse(partido.resultado);
          } catch (e) {
            console.warn('⚠️ No se pudo parsear resultado:', partido.resultado);
          }
        }
        
        if (typeof partido.equipos === 'string') {
          try {
            partido.equipos = JSON.parse(partido.equipos);
          } catch (e) {
            console.warn('⚠️ No se pudo parsear equipos:', partido.equipos);
          }
        }
        
        if (typeof partido.jugadores_confirmados === 'string') {
          try {
            // Este campo puede venir en diferentes formatos
            if (partido.jugadores_confirmados.startsWith('{') || partido.jugadores_confirmados.startsWith('[')) {
              partido.jugadores_confirmados = JSON.parse(partido.jugadores_confirmados);
            }
          } catch (e) {
            console.warn('⚠️ No se pudo parsear jugadores_confirmados:', partido.jugadores_confirmados);
          }
        }
        
        return partido;
      });
      
      console.log('✅ Historial procesado desde API:', historialPartidos.length, 'partidos');
      console.log('📊 Datos procesados:', historialPartidos);
      
      // Actualizar interfaz inmediatamente después de cargar datos
      setTimeout(() => {
        actualizarEstadisticas();
        mostrarHistorial();
        mostrarGoleadores();
      }, 50);
      
    } else {
      console.log('❌ Error al cargar historial de la API:', response.status);
      // Fallback: intentar cargar desde JSON como respaldo
      console.log('🔄 Intentando fallback a JSON...');
      const fallbackResponse = await fetch('historial_partidos.json?_=' + Date.now());
      if (fallbackResponse.ok) {
        historialPartidos = await fallbackResponse.json();
        console.log('✅ Historial cargado desde JSON (fallback):', historialPartidos.length, 'partidos');
        // Actualizar interfaz para fallback también
        setTimeout(() => {
          actualizarEstadisticas();
          mostrarHistorial();
          mostrarGoleadores();
        }, 50);
      } else {
        historialPartidos = [];
      }
    }
  } catch (error) {
    console.log('❌ Error al cargar el historial:', error);
    // Fallback: intentar cargar desde JSON como respaldo
    try {
      console.log('🔄 Intentando fallback a JSON...');
      const fallbackResponse = await fetch('historial_partidos.json?_=' + Date.now());
      if (fallbackResponse.ok) {
        historialPartidos = await fallbackResponse.json();
        console.log('✅ Historial cargado desde JSON (fallback):', historialPartidos.length, 'partidos');
        // Actualizar interfaz para fallback también
        setTimeout(() => {
          actualizarEstadisticas();
          mostrarHistorial();
          mostrarGoleadores();
        }, 50);
      } else {
        historialPartidos = [];
        // Actualizar interfaz incluso sin datos
        setTimeout(() => {
          actualizarEstadisticas();
          mostrarHistorial();
          mostrarGoleadores();
        }, 50);
      }
    } catch (fallbackError) {
      console.log('❌ Error en fallback:', fallbackError);
      historialPartidos = [];
      // Actualizar interfaz incluso con error
      setTimeout(() => {
        actualizarEstadisticas();
        mostrarHistorial();
        mostrarGoleadores();
      }, 50);
    }
  }
}

// Guardar historial en localStorage
function guardarHistorial() {
  // Guardar localmente primero
  localStorage.setItem('historial_partidos', JSON.stringify(historialPartidos));
  console.log('Historial actualizado localmente:', JSON.stringify(historialPartidos, null, 2));
  
  // Intentar guardar en el servidor
  guardarHistorialCompleto().catch(error => {
    console.error('Error al sincronizar con servidor:', error);
    alert('⚠️ Cambios guardados localmente, pero no se pudo sincronizar con el servidor. Los cambios se perderán al recargar la página.');
  });
}

// Actualizar estadísticas generales
function actualizarEstadisticas() {
  console.log('🔍 Iniciando actualizarEstadisticas()');
  console.log('📊 historialPartidos completo:', historialPartidos);
  
  // Considerar partidos finalizados los que tienen resultado válido
  const totalPartidos = historialPartidos.filter(p => {
    const tieneResultado = p.resultado && 
      (p.resultado.rojo !== undefined && p.resultado.negro !== undefined);
    const noCancelado = !(p.resultado.rojo === 0 && p.resultado.negro === 0 && p.mvp === 'Cancelado');
    const incluir = tieneResultado && noCancelado;
    
    console.log(`🏆 Partido ${p.fecha}: resultado=${JSON.stringify(p.resultado)}, mvp=${p.mvp}, incluir=${incluir}`);
    return incluir;
  }).length;
  
  console.log(`📈 Total partidos calculado: ${totalPartidos}`);
  
  const victoriasRojo = historialPartidos.filter(p => 
    p.resultado && p.resultado.rojo > p.resultado.negro &&
    !(p.resultado.rojo === 0 && p.resultado.negro === 0 && p.mvp === 'Cancelado')
  ).length;
  
  const victoriasNegro = historialPartidos.filter(p => 
    p.resultado && p.resultado.negro > p.resultado.rojo &&
    !(p.resultado.rojo === 0 && p.resultado.negro === 0 && p.mvp === 'Cancelado')
  ).length;
  
  const empates = historialPartidos.filter(p => 
    p.resultado && p.resultado.rojo === p.resultado.negro &&
    !(p.resultado.rojo === 0 && p.resultado.negro === 0 && p.mvp === 'Cancelado')
  ).length;

  console.log(`📊 Estadísticas: total=${totalPartidos}, rojo=${victoriasRojo}, negro=${victoriasNegro}, empates=${empates}`);

  document.getElementById('total-partidos').textContent = totalPartidos;
  document.getElementById('victorias-rojo').textContent = victoriasRojo;
  document.getElementById('victorias-negro').textContent = victoriasNegro;
  document.getElementById('empates').textContent = empates;
}

// Mostrar historial de partidos
function mostrarHistorial() {
  console.log('🏁 mostrarHistorial() llamada');
  console.log('📊 historialPartidos array:', historialPartidos);
  console.log('📊 historialPartidos.length:', historialPartidos.length);
  
  const container = document.getElementById('historial-container');
  console.log('📦 container encontrado:', !!container);
  
  if (!container) {
    console.error('❌ No se encontró el contenedor historial-container');
    return;
  }
  
  if (historialPartidos.length === 0) {
    console.log('⚠️ No hay partidos en el historial');
    container.innerHTML = '<p style="text-align: center; color: #666; padding: 20px;">No hay partidos registrados aún</p>';
    return;
  }

  console.log('🔍 Analizando cada partido:');
  historialPartidos.forEach((p, i) => {
    console.log(`Partido ${i+1}:`, {
      fecha: p.fecha,
      resultado: p.resultado,
      tieneResultado: !!(p.resultado && p.resultado.rojo !== undefined && p.resultado.negro !== undefined)
    });
  });

  const partidosOrdenados = [...historialPartidos]
    .filter(p => {
      const tieneResultado = p.resultado && 
        (p.resultado.rojo !== undefined && p.resultado.negro !== undefined);
      console.log(`🔍 Partido ${p.fecha}: tieneResultado=${tieneResultado}, resultado=`, p.resultado);
      return tieneResultado;
    })
    .sort((a, b) => new Date(b.fecha) - new Date(a.fecha));
    
  console.log('✅ partidosOrdenados:', partidosOrdenados.length, 'partidos');
  console.log('📊 partidosOrdenados detalle:', partidosOrdenados);

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
    
    // Mostrar jugadores de los equipos - compatible con ambas estructuras
    const equipoRojo = partido.equipo_rojo || (partido.equipos && partido.equipos.rojo) || [];
    const equipoNegro = partido.equipo_negro || (partido.equipos && partido.equipos.negro) || [];
    const equipoRojoJugadores = equipoRojo.length > 0 ? equipoRojo.join(', ') : 'No registrado';
    const equipoNegroJugadores = equipoNegro.length > 0 ? equipoNegro.join(', ') : 'No registrado';
    
    return `
      <div class="match-item" data-index="${indiceOriginal}" style="background: white; color: black; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 15px; padding: 15px;">
        <div class="match-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
          <div>
            <div style="font-weight: bold; color: black;">${partido.fecha_formato}</div>
            <div class="match-date" style="color: #555;">${partido.hora} hrs - ${partido.cancha}</div>
            ${partido.mvp ? `<div style="font-size: 0.9em; color: #333;">🏆 MVP: ${partido.mvp}</div>` : ''}
          </div>
          <div class="match-result" style="text-align: center;">
            <div style="font-size: 1.5em; font-weight: bold; color: black; background: none;">
              <span class="team-red" style="color: black;">${partido.resultado.rojo}</span>
              <span style="color: black;"> - </span>
              <span class="team-black" style="color: black;">${partido.resultado.negro}</span>
              ${ganador !== 'empate' ? `<span style="margin-left: 10px;">${ganador === 'rojo' ? '🔴' : '⚫'}</span>` : ' 🤝'}
            </div>
          </div>
          <div class="match-actions" ${!isAuthenticated ? 'style="display: none;"' : ''}>
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
        
        ${partido.jugadores_confirmados && partido.jugadores_confirmados.length > 0 ? `
          <div class="jugadores-confirmados" style="margin-top: 10px; border-top: 1px solid #eee; padding-top: 10px;">
            <div style="font-weight: bold; color: #2196f3; margin-bottom: 5px;">👥 Jugadores Confirmados (${partido.jugadores_confirmados.length})</div>
            <div style="font-size: 0.9em; color: black; line-height: 1.4;">
              ${partido.jugadores_confirmados.join(' • ')}
            </div>
          </div>
        ` : ''}
        
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
  
  console.log('✅ HTML del historial generado, length:', container.innerHTML.length);
  
  // Si no hay partidos filtrados pero sí hay datos, mostrar mensaje específico
  if (partidosOrdenados.length === 0 && historialPartidos.length > 0) {
    container.innerHTML = '<p style="text-align: center; color: #666; padding: 20px;">Los partidos están en la base de datos pero no tienen resultados válidos para mostrar</p>';
    console.log('⚠️ Partidos sin resultados válidos');
  }
}

// Función de debugging para llamar manualmente
window.debugEstadisticas = function() {
  console.log('🔧 DEBUG MANUAL DE ESTADÍSTICAS');
  console.log('historialPartidos:', historialPartidos);
  console.log('historialPartidos.length:', historialPartidos.length);
  
  // Forzar recarga
  cargarHistorial().then(() => {
    console.log('✅ Recarga completada');
    actualizarEstadisticas();
    mostrarHistorial();
    mostrarGoleadores();
  });
};

// Función para forzar actualización manual
window.forzarActualizacion = function() {
  console.log('🔄 Forzando actualización...');
  actualizarEstadisticas();
  mostrarHistorial();
  mostrarGoleadores();
};

// Calcular y mostrar goleadores
function mostrarGoleadores() {
  const container = document.getElementById('goleadores-container');
  
  if (!container) return;
  
  // Sumar goles por jugador
  const golesPorJugador = {};
  historialPartidos
    .filter(p => 
      p.resultado && 
      (p.resultado.rojo !== undefined && p.resultado.negro !== undefined)
    )
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
  
  // Cargar jugadores automáticamente
  cargarJugadoresAutomaticamente();
  
  document.getElementById('modal-resultado').style.display = 'block';
}

// Función para cargar jugadores automáticamente
async function cargarJugadoresAutomaticamente() {
  let jugadoresConfirmados = [];
  let fuente = '';
  
  const fechaHoy = new Date().toISOString().split('T')[0];
  
  try {
    // Opción 1: Intentar cargar desde confirmaciones automáticas (servidor)
    try {
      const responseAuto = await fetch(`http://localhost:5000/lista-jugadores/${fechaHoy}`);
      if (responseAuto.ok) {
        const dataAuto = await responseAuto.json();
        if (dataAuto.jugadores && dataAuto.jugadores.length > 0) {
          jugadoresConfirmados = dataAuto.jugadores;
          fuente = 'confirmaciones automáticas (servidor)';
          console.log('✅ Jugadores cargados desde confirmaciones automáticas:', jugadoresConfirmados);
        }
      }
    } catch (error) {
      console.log('⚠️ Servidor de confirmaciones no disponible:', error.message);
    }
    
    // Opción 1b: Si no hay servidor, intentar cargar desde archivo local
    if (jugadoresConfirmados.length === 0) {
      try {
        const responseAutoLocal = await fetch('confirmaciones_automaticas.json?_=' + Date.now());
        if (responseAutoLocal.ok) {
          const confirmacionesData = await responseAutoLocal.json();
          if (confirmacionesData[fechaHoy] && confirmacionesData[fechaHoy].jugadores) {
            jugadoresConfirmados = confirmacionesData[fechaHoy].jugadores;
            fuente = 'confirmaciones automáticas (archivo)';
            console.log('✅ Jugadores cargados desde confirmaciones automáticas locales:', jugadoresConfirmados);
          }
        }
      } catch (error) {
        console.log('⚠️ Archivo de confirmaciones automáticas no disponible:', error.message);
      }
    }
    
    // Opción 2: Si no hay confirmaciones automáticas, intentar cargar desde equipos.json (último sorteo)
    if (jugadoresConfirmados.length === 0) {
      try {
        const responseEquipos = await fetch('equipos.json?_=' + Date.now());
        if (responseEquipos.ok) {
          const equipos = await responseEquipos.json();
          const equipoRojo = equipos.rojo || [];
          const equipoNegro = equipos.negro || [];
          
          // Combinar ambos equipos para obtener la lista completa
          const jugadoresSorteo = [...equipoRojo, ...equipoNegro];
          
          if (jugadoresSorteo.length > 0) {
            jugadoresConfirmados = jugadoresSorteo;
            fuente = 'último sorteo';
            console.log('✅ Jugadores cargados desde último sorteo:', jugadoresConfirmados);
          }
        }
      } catch (error) {
        console.log('❌ No se pudo cargar desde equipos.json:', error);
      }
    }
    
    // Opción 3: Si no hay sorteo, intentar cargar desde confirmados.txt
    if (jugadoresConfirmados.length === 0) {
      try {
        const responseConfirmados = await fetch('confirmados.txt?_=' + Date.now());
        if (responseConfirmados.ok) {
          const textoConfirmados = await responseConfirmados.text();
          jugadoresConfirmados = textoConfirmados
            .split('\n')
            .map(linea => linea.trim())
            .filter(linea => linea.length > 0);
          
          if (jugadoresConfirmados.length > 0) {
            fuente = 'lista de confirmados';
            console.log('✅ Jugadores cargados desde confirmados.txt:', jugadoresConfirmados);
          }
        }
      } catch (error) {
        console.log('❌ No se pudo cargar desde confirmados.txt:', error);
      }
    }
    
    // Llenar el campo si se encontraron jugadores
    if (jugadoresConfirmados.length > 0) {
      document.getElementById('jugadores-confirmados').value = jugadoresConfirmados.join(', ');
      
      // Mostrar notificación al usuario indicando la fuente
      mostrarNotificacionCarga(jugadoresConfirmados.length, fuente);
    } else {
      console.log('ℹ️ No se encontraron jugadores para cargar automáticamente');
    }
  } catch (error) {
    console.error('❌ Error en carga automática:', error);
  }
}

// Mostrar notificación de carga automática
function mostrarNotificacionCarga(cantidad, fuente = 'origen desconocido') {
  const campo = document.getElementById('jugadores-confirmados');
  const notificacion = document.createElement('div');
  notificacion.innerHTML = `✅ Se cargaron automáticamente ${cantidad} jugadores desde ${fuente}`;
  notificacion.style.cssText = `
    color: #16a34a;
    font-size: 0.9em;
    margin-top: 5px;
    padding: 5px;
    background: #f0f9ff;
    border-radius: 4px;
    border: 1px solid #16a34a;
  `;
  
  // Insertar después del campo
  campo.parentNode.insertBefore(notificacion, campo.nextSibling);
  
  // Remover después de 3 segundos
  setTimeout(() => {
    if (notificacion.parentNode) {
      notificacion.parentNode.removeChild(notificacion);
    }
  }, 3000);
}

function cerrarModalResultado() {
  document.getElementById('modal-resultado').style.display = 'none';
  document.getElementById('form-resultado').reset();
  
  // Limpiar campos específicos
  document.getElementById('jugadores-confirmados').value = '';
  document.getElementById('equipo-rojo').value = '';
  document.getElementById('equipo-negro').value = '';
  
  // Limpiar estado de edición
  delete document.getElementById('form-resultado').dataset.editingIndex;
  document.querySelector('#modal-resultado h3').textContent = '📝 Agregar Resultado de Partido';
}

// Función para recargar jugadores manualmente
async function recargarJugadores() {
  const boton = event.target;
  const textoOriginal = boton.innerHTML;
  
  // Mostrar indicador de carga
  boton.innerHTML = '⏳ Cargando...';
  boton.disabled = true;
  
  try {
    await cargarJugadoresAutomaticamente();
  } catch (error) {
    console.error('Error al recargar jugadores:', error);
    alert('❌ Error al cargar jugadores automáticamente');
  } finally {
    // Restaurar botón
    boton.innerHTML = textoOriginal;
    boton.disabled = false;
  }
}

// Verificar automáticamente si hay nuevos sorteos
let ultimoSorteoTimestamp = null;

async function verificarNuevoSorteo() {
  try {
    const response = await fetch('equipos.json?_=' + Date.now());
    if (response.ok) {
      const lastModified = response.headers.get('Last-Modified');
      if (lastModified) {
        const timestamp = new Date(lastModified).getTime();
        
        if (ultimoSorteoTimestamp && timestamp > ultimoSorteoTimestamp) {
          // Hay un nuevo sorteo
          console.log('🆕 Nuevo sorteo detectado');
          
          // Si el modal está abierto, ofrecer recargar
          const modal = document.getElementById('modal-resultado');
          if (modal && modal.style.display === 'block') {
            mostrarSugerenciaRecarga();
          }
        }
        
        ultimoSorteoTimestamp = timestamp;
      }
    }
  } catch (error) {
    console.log('No se pudo verificar nuevo sorteo:', error);
  }
}

// Mostrar sugerencia de recarga
function mostrarSugerenciaRecarga() {
  const sugerencia = document.createElement('div');
  sugerencia.innerHTML = `
    <div style="background: #fff3cd; border: 1px solid #ffc107; border-radius: 4px; padding: 10px; margin: 10px 0;">
      <strong>🆕 Nuevo sorteo detectado</strong><br>
      <small>¿Quieres actualizar la lista de jugadores?</small>
      <button onclick="recargarJugadores(); this.parentNode.parentNode.remove();" style="background: #ffc107; border: none; padding: 4px 8px; border-radius: 4px; margin-left: 10px; cursor: pointer;">
        Actualizar
      </button>
      <button onclick="this.parentNode.parentNode.remove();" style="background: #6c757d; color: white; border: none; padding: 4px 8px; border-radius: 4px; margin-left: 5px; cursor: pointer;">
        Ignorar
      </button>
    </div>
  `;
  
  const campo = document.getElementById('jugadores-confirmados');
  campo.parentNode.insertBefore(sugerencia, campo);
}

// Verificar cada 30 segundos si hay cambios
setInterval(verificarNuevoSorteo, 30000);
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
  
  // Llenar jugadores confirmados
  const jugadoresConfirmados = partido.jugadores_confirmados || [];
  document.getElementById('jugadores-confirmados').value = jugadoresConfirmados.join(', ');
  
  // Llenar equipos - compatible con ambas estructuras
  const equipoRojo = partido.equipo_rojo || (partido.equipos && partido.equipos.rojo) || [];
  const equipoNegro = partido.equipo_negro || (partido.equipos && partido.equipos.negro) || [];
  
  document.getElementById('equipo-rojo').value = equipoRojo.join(', ');
  document.getElementById('equipo-negro').value = equipoNegro.join(', ');
  
  console.log('📝 Cargando equipos para edición:');
  console.log('🔴 Equipo Rojo:', equipoRojo);
  console.log('⚫ Equipo Negro:', equipoNegro);
  
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
  
  // Validar si ya existe un partido en esta fecha
  const partidoExistente = historialPartidos.find(p => p.fecha === fecha);
  if (partidoExistente) {
    const confirmar = confirm(`⚠️ Ya existe un partido registrado para el ${fecha}.\n¿Deseas sobrescribirlo?`);
    if (!confirmar) {
      return;
    }
    // Remover partido existente
    const indice = historialPartidos.findIndex(p => p.fecha === fecha);
    historialPartidos.splice(indice, 1);
    console.log(`🗑️ Partido existente del ${fecha} removido para evitar duplicados`);
  }
  
  // Procesar jugadores confirmados
  const jugadoresConfirmadosTexto = document.getElementById('jugadores-confirmados').value;
  let jugadoresConfirmados = [];
  
  if (jugadoresConfirmadosTexto.trim()) {
    // Dividir por comas o saltos de línea y limpiar espacios
    jugadoresConfirmados = jugadoresConfirmadosTexto
      .split(/[,\n]/)
      .map(jugador => jugador.trim())
      .filter(jugador => jugador.length > 0);
  }

  // Obtener equipos - priorizar campos del formulario, luego último sorteo
  let equipoRojo = [];
  let equipoNegro = [];
  
  // Primero intentar obtener desde los campos del formulario
  const equipoRojoFormulario = document.getElementById('equipo-rojo').value.trim();
  const equipoNegroFormulario = document.getElementById('equipo-negro').value.trim();
  
  if (equipoRojoFormulario) {
    equipoRojo = equipoRojoFormulario
      .split(',')
      .map(jugador => jugador.trim())
      .filter(jugador => jugador.length > 0);
  }
  
  if (equipoNegroFormulario) {
    equipoNegro = equipoNegroFormulario
      .split(',')
      .map(jugador => jugador.trim())
      .filter(jugador => jugador.length > 0);
  }
  
  // Si no hay equipos en el formulario, obtener del último sorteo
  if (equipoRojo.length === 0 || equipoNegro.length === 0) {
    try {
      const response = await fetch('equipos.json?_=' + Date.now());
      if (response.ok) {
        const equipos = await response.json();
        if (equipoRojo.length === 0) equipoRojo = equipos.rojo || [];
        if (equipoNegro.length === 0) equipoNegro = equipos.negro || [];
      }
    } catch (error) {
      console.log('No se pudieron cargar los equipos del sorteo');
    }
  }
  
  console.log('🏆 Equipos procesados:');
  console.log('🔴 Equipo Rojo:', equipoRojo);
  console.log('⚫ Equipo Negro:', equipoNegro);

  // Generar ID único más robusto
  const fechaTimestamp = new Date(fecha + 'T' + hora).getTime();
  const timestampAdicional = Date.now();
  const randomComponent = Math.floor(Math.random() * 10000);
  let idUnico = fechaTimestamp + randomComponent;
  
  // Validar que el ID no exista ya (prevenir duplicados)
  while (historialPartidos.some(p => p.id === idUnico)) {
    idUnico = fechaTimestamp + Math.floor(Math.random() * 100000);
    console.log(`⚠️ ID duplicado detectado, generando nuevo: ${idUnico}`);
  }
  
  // Validar duplicados por fecha, hora y equipos (prevenir partidos duplicados)
  const partidoDuplicado = historialPartidos.find(p => {
    const pEquipoRojo = p.equipo_rojo || (p.equipos && p.equipos.rojo) || [];
    const pEquipoNegro = p.equipo_negro || (p.equipos && p.equipos.negro) || [];
    
    return p.fecha === fecha && 
           p.hora === hora && 
           p.cancha === cancha &&
           JSON.stringify(pEquipoRojo.sort()) === JSON.stringify(equipoRojo.sort()) &&
           JSON.stringify(pEquipoNegro.sort()) === JSON.stringify(equipoNegro.sort());
  });
  
  if (partidoDuplicado) {
    alert(`⚠️ Ya existe un partido registrado para la fecha ${fecha} a las ${hora} en cancha ${cancha} con estos equipos.`);
    console.log('❌ Partido duplicado detectado, cancelando registro');
    return false;
  }

  const nuevoPartido = {
    id: idUnico,
    fecha: fecha,
    fecha_formato: formatearFecha(fecha),
    hora: hora,
    cancha: cancha,
    jugadores_confirmados: jugadoresConfirmados,
    equipos: {
      rojo: equipoRojo,
      negro: equipoNegro
    },
    // Mantener compatibilidad con estructura antigua
    equipo_rojo: equipoRojo,
    equipo_negro: equipoNegro,
    resultado: {
      rojo: golesRojo,
      negro: golesNegro
    },
    mvp: mvp,
    asistencia: asistencia,
    estado: 'finalizado',
    timestamp: new Date().toISOString()
  };

  historialPartidos.push(nuevoPartido);
  console.log(`✅ Nuevo partido agregado con ID: ${idUnico} para fecha: ${fecha}`);
  
  // Guardar en localStorage
  guardarHistorial();
  
  // Enviar al servidor para persistir en JSON
  try {
    await enviarResultadoAlServidor(nuevoPartido);
    console.log('✅ Resultado enviado al servidor correctamente');
  } catch (error) {
    console.error('❌ Error al enviar resultado al servidor:', error);
    alert('⚠️ Resultado guardado localmente pero no se pudo sincronizar con el servidor');
  }
  
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
  
  // Procesar jugadores confirmados
  const jugadoresConfirmadosTexto = document.getElementById('jugadores-confirmados').value;
  let jugadoresConfirmados = [];
  
  if (jugadoresConfirmadosTexto.trim()) {
    jugadoresConfirmados = jugadoresConfirmadosTexto
      .split(/[,\n]/)
      .map(jugador => jugador.trim())
      .filter(jugador => jugador.length > 0);
  }
  
  // Procesar equipos desde los campos del formulario
  const equipoRojoFormulario = document.getElementById('equipo-rojo').value.trim();
  const equipoNegroFormulario = document.getElementById('equipo-negro').value.trim();
  
  let equipoRojo = [];
  let equipoNegro = [];
  
  if (equipoRojoFormulario) {
    equipoRojo = equipoRojoFormulario
      .split(',')
      .map(jugador => jugador.trim())
      .filter(jugador => jugador.length > 0);
  }
  
  if (equipoNegroFormulario) {
    equipoNegro = equipoNegroFormulario
      .split(',')
      .map(jugador => jugador.trim())
      .filter(jugador => jugador.length > 0);
  }
  
  console.log('📝 Actualizando equipos:');
  console.log('🔴 Equipo Rojo:', equipoRojo);
  console.log('⚫ Equipo Negro:', equipoNegro);

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
    jugadores_confirmados: jugadoresConfirmados,
    equipos: {
      rojo: equipoRojo,
      negro: equipoNegro
    },
    // Mantener compatibilidad con estructura antigua
    equipo_rojo: equipoRojo,
    equipo_negro: equipoNegro,
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
  const modal = document.getElementById('modal-login');
  modal.style.display = 'none';
  document.getElementById('form-login').reset();
  document.getElementById('login-error').style.display = 'none';
}

// Mejorar UX del modal - cerrar con Escape y click fuera
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const modalLogin = document.getElementById('modal-login');
    const modalResultado = document.getElementById('modal-resultado');
    
    if (modalLogin && modalLogin.style.display !== 'none') {
      cerrarModalLogin();
    }
    if (modalResultado && modalResultado.style.display !== 'none') {
      cerrarModalResultado();
    }
  }
});

// Cerrar modal al hacer click fuera
document.getElementById('modal-login').addEventListener('click', (e) => {
  if (e.target === e.currentTarget) {
    cerrarModalLogin();
  }
});

document.getElementById('modal-resultado').addEventListener('click', (e) => {
  if (e.target === e.currentTarget) {
    cerrarModalResultado();
  }
});

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
    // Login exitoso - mostrar feedback visual
    errorDiv.style.display = 'block';
    errorDiv.style.color = 'green';
    errorDiv.textContent = '✅ Login exitoso';
    
    // Esperar un momento para que el usuario vea el mensaje
    setTimeout(() => {
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
    }, 500);
  } else {
    // Login fallido
    errorDiv.style.color = 'red';
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
  // Actualizar historial para mostrar botones
  mostrarHistorial();
  
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
  // Actualizar historial para ocultar botones
  mostrarHistorial();
  
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
  
  // Ocultar funciones de administración
  ocultarFuncionesAdmin();
  
  alert('Sesión cerrada correctamente');
}

// Modificar funciones de editar y eliminar para verificar autenticación
const editarPartidoOriginal = editarPartido;
const eliminarPartidoOriginal = eliminarPartido;

window.editarPartido = function(index) {
  console.log('window.editarPartido llamado con index:', index);
  editarPartidoOriginal(index);
};

window.eliminarPartido = function(index) {
  console.log('window.eliminarPartido llamado con index:', index);
  eliminarPartidoOriginal(index);
};

// Función para enviar resultado al servidor
async function enviarResultadoAlServidor(partido) {
  try {
    return await guardarResultadoConFallback(partido);
  } catch (error) {
    console.error('Error enviando resultado:', error);
    throw error;
  }
}

// Función para guardar todo el historial en el servidor
async function guardarHistorialCompleto() {
  try {
    const configs = [getApiConfig(), API_CONFIG.todoEnUno, API_CONFIG.development];
    
    for (const config of configs) {
      try {
        const url = config.base + config.endpoints.guardarHistorial;
        console.log(`🔄 Intentando guardar historial en: ${url}`);
        
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(historialPartidos)
        });
        
        if (response.ok) {
          console.log('✅ Historial completo guardado en servidor');
          return await response.json();
        }
      } catch (error) {
        console.log(`⚠️ Error con ${config.base}: ${error.message}`);
        continue;
      }
    }
    
    throw new Error('No se pudo guardar el historial en ningún servidor');
  } catch (error) {
    console.error('❌ Error al guardar historial completo:', error);
    throw error;
  }
}

// Hacer disponible globalmente las funciones necesarias
window.verificarAdmin = verificarAdmin;
window.mostrarModalLogin = mostrarModalLogin;
window.cerrarModalLogin = cerrarModalLogin;
window.cerrarSesion = cerrarSesion;
