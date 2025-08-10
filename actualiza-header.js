// Script para actualizar automáticamente la fecha, hora y cancha en el header
document.addEventListener('DOMContentLoaded', function() {
  console.log('🔄 DOM cargado, iniciando actualización de header...');
  
  fetch('equipos.json')
    .then(response => {
      console.log('📡 Respuesta del fetch:', response.status);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('📊 Datos cargados:', data);
      const info = document.getElementById('partido-info');
      console.log('🎯 Elemento encontrado:', info);
      
      if (info && data.fecha && data.hora && data.cancha) {
        // Verificar si la hora ya incluye "hrs" para evitar duplicación
        const horaFormateada = data.hora.includes('hrs') ? data.hora : `${data.hora} hrs`;
        
        // Formatear la cancha correctamente
        let canchaFormateada;
        if (data.cancha.toLowerCase().includes('por confirmar')) {
          canchaFormateada = data.cancha;
        } else if (/^\d+$/.test(data.cancha.trim())) {
          // Si es solo un número, agregar "Cancha"
          canchaFormateada = `Cancha ${data.cancha}`;
        } else {
          // Si ya tiene texto, usar tal como está
          canchaFormateada = data.cancha;
        }
        
        const nuevoTexto = `⚽ Partido ${data.fecha} - ${horaFormateada} - ${canchaFormateada}`;
        
        console.log('✅ Actualizando header a:', nuevoTexto);
        info.textContent = nuevoTexto;
      } else {
        console.warn('⚠️ Faltan datos o elemento:', { info: !!info, fecha: data.fecha, hora: data.hora, cancha: data.cancha });
      }
    })
    .catch(err => {
      // Si hay error, no se actualiza el header
      console.error('❌ Error cargando equipos.json:', err);
    });
});
