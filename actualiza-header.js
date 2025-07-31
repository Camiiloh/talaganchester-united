// Script para actualizar automáticamente la fecha, hora y cancha en el header
fetch('equipos.json')
  .then(response => response.json())
  .then(data => {
    const info = document.getElementById('partido-info');
    if (info && data.fecha && data.hora && data.cancha) {
      info.textContent = `⚽ Partido ${data.fecha} - ${data.hora} hrs - Cancha ${data.cancha}`;
    }
  })
  .catch(err => {
    // Si hay error, no se actualiza el header
    console.error('No se pudo cargar equipos.json:', err);
  });
