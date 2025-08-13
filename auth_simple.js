// Funciones de autenticación simples

// Variables globales para autenticación
let isAdminAuthenticated = false;
let adminPasswords = ['admin2025', 'talaga123', 'manchester2025'];

// Cargar configuración de autenticación
async function cargarConfiguracionAuth() {
  try {
    const response = await fetch('auth_config.json?_=' + Date.now());
    if (response.ok) {
      const config = await response.json();
      adminPasswords = config.admin_passwords || adminPasswords;
    }
  } catch (error) {
    console.log('Usando contraseñas por defecto');
  }
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
  return adminPasswords.includes(password);
}

// Manejar login
function manejarLogin(event) {
  event.preventDefault();
  
  const password = document.getElementById('password-admin').value;
  const errorDiv = document.getElementById('login-error');
  
  if (verificarCredenciales(password)) {
    // Login exitoso
    isAdminAuthenticated = true;
    localStorage.setItem('admin_session', JSON.stringify({ timestamp: Date.now() }));
    
    mostrarEstadoAdmin();
    cerrarModalLogin();
    
    // Abrir modal de resultado automáticamente
    setTimeout(() => {
      const modal = document.getElementById('modal-resultado');
      if (modal) {
        modal.style.display = 'block';
        const fechaInput = document.getElementById('fecha-partido');
        if (fechaInput) {
          const hoy = new Date().toISOString().split('T')[0];
          fechaInput.value = hoy;
        }
      }
    }, 200);
  } else {
    // Login fallido
    errorDiv.textContent = 'Contraseña incorrecta';
    errorDiv.style.display = 'block';
    document.getElementById('password-admin').value = '';
  }
}

// Mostrar estado de administrador
function mostrarEstadoAdmin() {
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
  if (isAdminAuthenticated) {
    callback(index);
  } else {
    alert('Necesitas autenticarte como administrador para realizar esta acción');
    mostrarModalLogin();
  }
}

// Configurar event listeners cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
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
