// Configuración de URLs para la API
const API_CONFIG = {
  // Para desarrollo local
  development: {
    base: 'http://localhost:8083',
    endpoints: {
      guardarResultado: '/guardar-resultado',
      guardarHistorial: '/guardar-historial-completo'
    }
  },
  // Para servidor todo-en-uno
  todoEnUno: {
    base: '',  // Mismo dominio
    endpoints: {
      guardarResultado: '/api/guardar-resultado',
      guardarHistorial: '/api/guardar-historial-completo'
    }
  },
  // Para producción web
  production: {
    base: window.location.origin,  // Detecta automáticamente
    endpoints: {
      guardarResultado: '/api/guardar-resultado',
      guardarHistorial: '/api/guardar-historial-completo'
    }
  }
};

// Detectar entorno automáticamente
function getApiConfig() {
  const host = window.location.hostname;
  
  if (host === 'localhost' || host === '127.0.0.1') {
    // Desarrollo local - intentar servidor separado primero
    return API_CONFIG.development;
  } else {
    // Producción - usar API en mismo dominio
    return API_CONFIG.production;
  }
}

// Función para construir URL de API
function getApiUrl(endpoint) {
  const config = getApiConfig();
  return config.base + config.endpoints[endpoint];
}

// Función mejorada para guardar resultado con fallback
async function guardarResultadoConFallback(datos) {
  const configs = [
    getApiConfig(),  // Configuración detectada
    API_CONFIG.todoEnUno,  // Fallback: todo-en-uno
    API_CONFIG.development  // Fallback: desarrollo
  ];
  
  for (const config of configs) {
    try {
      const url = config.base + config.endpoints.guardarResultado;
      console.log(`🔄 Intentando guardar en: ${url}`);
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(datos)
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('✅ Resultado guardado exitosamente');
        return result;
      }
    } catch (error) {
      console.log(`⚠️ Error con ${config.base}: ${error.message}`);
      continue;  // Intentar siguiente configuración
    }
  }
  
  throw new Error('No se pudo conectar con ningún servidor de resultados');
}
