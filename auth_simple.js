// Funciones de autenticación simples

// Variables globales para autenticación
let isAdminAuthenticated = false;
let adminPasswords = ['admin2025', 'talaga123', 'manchester2025'];
let configCargada = false;

// Cargar configuración de autenticación
async function cargarConfiguracionAuth() {
  try {
    const response = await fetch('auth_config.json?_=' + Date.now());
    if (response.ok) {
      const config = await response.json();
      adminPasswords = config.admin_passwords || adminPasswords;
      console.log('Configuración de auth cargada:', adminPasswords);
    }
  } catch (error) {
    console.log('Usando contraseñas por defecto:', adminPasswords);
  }
  configCargada = true;
  // Actualizar las variables globales
  window.adminPasswords = adminPasswords;
}

// Verificar sesión activa
function verificarSesionActiva() {
  const sesion = localStorage.getItem('admin_session');
  if (sesion) {
    try {
      const data = JSON.parse(sesion);
      const ahora = Date.now();
      // Sesión válida por 1 hora
      if (ahora - data.timestamp < 3600000) {
        isAdminAuthenticated = true;
        window.isAdminAuthenticated = true;
        console.log('Sesión activa restaurada - Estado:', isAdminAuthenticated);
        mostrarEstadoAdmin();
        return;
      } else {
        localStorage.removeItem('admin_session');
      }
    } catch (error) {
      localStorage.removeItem('admin_session');
    }
  }
  
  isAdminAuthenticated = false;
  mostrarEstadoNoAdmin();
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
  const errorDiv = document.getElementById('login-error');
  if (errorDiv) errorDiv.style.display = 'none';
}

// Verificar si necesita login antes de agregar
function mostrarLoginSiNecesario() {
  if (isAdminAuthenticated) {
    // Intentar abrir modal de resultado directamente
    const modal = document.getElementById('modal-resultado');
    if (modal) {
      modal.style.display = 'block';
      
      // Prellenar fecha
      const fechaInput = document.getElementById('fecha-partido');
      if (fechaInput) {
        const hoy = new Date().toISOString().split('T')[0];
        fechaInput.value = hoy;
      }
    } else {
      console.error('Modal de resultado no encontrado');
    }
  } else {
    mostrarModalLogin();
  }
}

// Verificar credenciales
function verificarCredenciales(password) {
  console.log('Verificando contraseña:', password);
  console.log('Contraseñas disponibles:', adminPasswords);
  const esValida = adminPasswords.includes(password);
  console.log('¿Es válida?:', esValida);
  return esValida;
}

// Manejar login
function manejarLogin(event) {
  event.preventDefault();
  
  const password = document.getElementById('password-admin').value.trim();
  const errorDiv = document.getElementById('login-error');
  
  if (verificarCredenciales(password)) {
    // Login exitoso
    isAdminAuthenticated = true;
    window.isAdminAuthenticated = true;
    localStorage.setItem('admin_session', JSON.stringify({ timestamp: Date.now() }));
    
    console.log('Login exitoso - Estado actualizado a:', isAdminAuthenticated);
    
    mostrarEstadoAdmin();
    cerrarModalLogin();
    
    // Mostrar mensaje de confirmación
    alert('¡Login exitoso! Ahora puedes editar y eliminar partidos.');
  } else {
    // Login fallido
    errorDiv.textContent = 'Contraseña incorrecta';
    errorDiv.style.display = 'block';
    document.getElementById('password-admin').value = '';
  }
}

// Mostrar estado de administrador
function mostrarEstadoAdmin() {
  // Actualizar variables globales
  isAdminAuthenticated = true;
  window.isAdminAuthenticated = true;
  
  console.log('mostrarEstadoAdmin - Estado actualizado a:', isAdminAuthenticated);
  
  // Crear indicador si no existe
  let indicator = document.getElementById('admin-indicator');
  if (!indicator) {
    indicator = document.createElement('div');
    indicator.id = 'admin-indicator';
    indicator.className = 'admin-indicator';
    document.body.appendChild(indicator);
  }
  
  indicator.innerHTML = `
    👤 Admin conectado 
    <button class="logout-btn" onclick="cerrarSesion()">Salir</button>
  `;
  
  // Ocultar prompt de autenticación
  const authPrompt = document.getElementById('auth-prompt');
  if (authPrompt) authPrompt.style.display = 'none';
  
  // Mostrar botones de acción en partidos
  const matchActions = document.querySelectorAll('.match-actions');
  matchActions.forEach(action => {
    action.style.opacity = '1';
    action.style.pointerEvents = 'auto';
  });
}

// Mostrar estado de no administrador
function mostrarEstadoNoAdmin() {
  // Actualizar variables globales
  isAdminAuthenticated = false;
  window.isAdminAuthenticated = false;
  
  console.log('mostrarEstadoNoAdmin - Estado actualizado a:', isAdminAuthenticated);
  
  // Remover indicador de admin
  const indicator = document.getElementById('admin-indicator');
  if (indicator) indicator.remove();
  
  // Mostrar prompt de autenticación
  const authPrompt = document.getElementById('auth-prompt');
  if (authPrompt) authPrompt.style.display = 'block';
  
  // Ocultar botones de acción en partidos
  const matchActions = document.querySelectorAll('.match-actions');
  matchActions.forEach(action => {
    action.style.opacity = '0.3';
    action.style.pointerEvents = 'none';
  });
}

// Cerrar sesión
function cerrarSesion() {
  isAdminAuthenticated = false;
  localStorage.removeItem('admin_session');
  mostrarEstadoNoAdmin();
}

// Verificar autenticación para editar/eliminar
function verificarParaEditar(callback, index) {
  // Verificar sesión activa primero
  verificarSesionActiva();
  
  // Verificar múltiples fuentes de verdad
  const localAuth = isAdminAuthenticated;
  const globalAuth = window.isAdminAuthenticated;
  const hasSession = !!localStorage.getItem('admin_session');
  const hasIndicator = !!document.getElementById('admin-indicator');
  
  console.log('=== verificarParaEditar DEBUG ===');
  console.log('Local auth:', localAuth);
  console.log('Global auth:', globalAuth);
  console.log('Has session:', hasSession);
  console.log('Has indicator:', hasIndicator);
  
  // Si cualquiera indica que está autenticado, proceder
  if (localAuth || globalAuth || hasSession) {
    console.log('Usuario autenticado, ejecutando acción directamente');
    // Asegurar sincronización
    isAdminAuthenticated = true;
    window.isAdminAuthenticated = true;
    callback(index);
  } else {
    console.log('Usuario no autenticado, debe hacer login primero');
    alert('Necesitas hacer login como administrador primero. Usa el botón "Login" en la parte superior.');
  }
}

// Configurar event listeners cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', async function() {
  // Cargar configuración de autenticación primero
  await cargarConfiguracionAuth();
  
  // Verificar sesión activa
  verificarSesionActiva();
  
  // Event listener para el formulario de login
  const formLogin = document.getElementById('form-login');
  if (formLogin) {
    formLogin.addEventListener('submit', manejarLogin);
  }
  
  // Event listener para cerrar modal haciendo clic fuera
  const modalLogin = document.getElementById('modal-login');
  if (modalLogin) {
    modalLogin.addEventListener('click', function(e) {
      if (e.target.id === 'modal-login') {
        cerrarModalLogin();
      }
    });
  }
});

// Funciones globales
window.mostrarModalLogin = mostrarModalLogin;
window.cerrarModalLogin = cerrarModalLogin;
window.mostrarLoginSiNecesario = mostrarLoginSiNecesario;
window.cerrarSesion = cerrarSesion;
window.verificarParaEditar = verificarParaEditar;

// Variables globales para debug
window.adminPasswords = adminPasswords;
window.isAdminAuthenticated = isAdminAuthenticated;
window.verificarCredenciales = verificarCredenciales;

// Función de debug para verificar estado
window.debugAuth = function() {
  console.log('=== DEBUG AUTENTICACIÓN ===');
  console.log('isAdminAuthenticated (local):', isAdminAuthenticated);
  console.log('window.isAdminAuthenticated (global):', window.isAdminAuthenticated);
  console.log('localStorage sesión:', localStorage.getItem('admin_session'));
  console.log('Admin indicator visible:', !!document.getElementById('admin-indicator'));
  return {
    local: isAdminAuthenticated,
    global: window.isAdminAuthenticated,
    session: localStorage.getItem('admin_session'),
    indicator: !!document.getElementById('admin-indicator')
  };
};

// Función para cerrar modal de resultado
window.cerrarModalResultado = function() {
  const modal = document.getElementById('modal-resultado');
  if (modal) {
    modal.style.display = 'none';
  }
  const form = document.getElementById('form-resultado');
  if (form) {
    form.reset();
  }
};
