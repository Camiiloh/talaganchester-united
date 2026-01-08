// Theme Toggle Script
(function() {
  const themeToggle = document.getElementById('theme-toggle');
  const themeIcon = document.querySelector('.theme-icon');
  const body = document.body;
  
  // Cargar tema guardado o usar oscuro por defecto
  const savedTheme = localStorage.getItem('theme') || 'dark';
  
  // Aplicar tema inicial
  if (savedTheme === 'light') {
    body.classList.add('light-theme');
    themeIcon.textContent = '☀️';
  } else {
    themeIcon.textContent = '🌙';
  }
  
  // Toggle theme
  themeToggle.addEventListener('click', () => {
    body.classList.toggle('light-theme');
    
    if (body.classList.contains('light-theme')) {
      themeIcon.textContent = '☀️';
      localStorage.setItem('theme', 'light');
    } else {
      themeIcon.textContent = '🌙';
      localStorage.setItem('theme', 'dark');
    }
  });
})();
