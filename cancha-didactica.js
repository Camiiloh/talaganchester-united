// Cancha Didáctica - JavaScript Interactivo
class SoccerFieldInteractive {
    constructor() {
        this.currentTip = 0;
        this.tips = document.querySelectorAll('.tip');
        this.showInfoMode = false;
        this.showPositionsMode = false;
        this.showStatsMode = false;
        this.animationMode = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.startTipCarousel();
        this.setupPlayerInteractions();
        this.createPassLines();
    }
    
    setupEventListeners() {
        // Botones de control
        document.getElementById('showInfo').addEventListener('click', () => this.toggleInfo());
        document.getElementById('showPositions').addEventListener('click', () => this.togglePositions());
        document.getElementById('showStats').addEventListener('click', () => this.toggleStats());
        document.getElementById('animateFormation').addEventListener('click', () => this.animateFormation());
        
        // Eventos de teclado para accesibilidad
        document.addEventListener('keydown', (e) => {
            if (e.key === ' ') {
                e.preventDefault();
                this.nextTip();
            }
        });
    }
    
    setupPlayerInteractions() {
        const players = document.querySelectorAll('.player.interactive');
        
        players.forEach(player => {
            // Efectos de hover mejorados
            player.addEventListener('mouseenter', () => {
                this.highlightPlayerConnections(player);
                this.showPlayerStats(player);
            });
            
            player.addEventListener('mouseleave', () => {
                this.hidePlayerConnections();
                this.hidePlayerStats();
            });
            
            // Click para mostrar información detallada
            player.addEventListener('click', () => {
                this.showPlayerDetailModal(player);
            });
        });
    }
    
    highlightPlayerConnections(player) {
        const playerTeam = player.classList.contains('black-team') ? 'black-team' : 'red-team';
        const teammates = document.querySelectorAll(`.player.${playerTeam}`);
        
        teammates.forEach(teammate => {
            if (teammate !== player) {
                teammate.style.opacity = '0.6';
                this.drawConnectionLine(player, teammate);
            }
        });
        
        // Resaltar zona del campo
        const playerPosition = player.dataset.position;
        this.highlightFieldZone(playerPosition, playerTeam);
    }
    
    hidePlayerConnections() {
        const players = document.querySelectorAll('.player.interactive');
        players.forEach(player => {
            player.style.opacity = '1';
        });
        
        // Ocultar líneas de conexión
        const passLines = document.querySelector('.pass-lines');
        passLines.style.opacity = '0';
        
        // Ocultar destacado de zona
        this.hideFieldZoneHighlight();
    }
    
    drawConnectionLine(player1, player2) {
        const passLines = document.querySelector('.pass-lines');
        const field = document.querySelector('.soccer-field');
        const fieldRect = field.getBoundingClientRect();
        
        const rect1 = player1.getBoundingClientRect();
        const rect2 = player2.getBoundingClientRect();
        
        const x1 = rect1.left + rect1.width / 2 - fieldRect.left;
        const y1 = rect1.top + rect1.height / 2 - fieldRect.top;
        const x2 = rect2.left + rect2.width / 2 - fieldRect.left;
        const y2 = rect2.top + rect2.height / 2 - fieldRect.top;
        
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2);
        line.setAttribute('stroke', '#3b82f6');
        line.setAttribute('stroke-width', '2');
        line.setAttribute('stroke-dasharray', '5,5');
        line.setAttribute('opacity', '0.7');
        
        // Animación de la línea
        line.style.strokeDashoffset = '100';
        line.style.animation = 'dashAnimation 2s linear infinite';
        
        passLines.appendChild(line);
        passLines.style.opacity = '1';
    }
    
    highlightFieldZone(position, team) {
        let zoneClass = '';
        
        if (position.includes('Arquero')) {
            zoneClass = team === 'black-team' ? '.defensive-zone.left' : '.offensive-zone.right';
        } else if (position.includes('Defensa')) {
            zoneClass = team === 'black-team' ? '.defensive-zone.left' : '.offensive-zone.right';
        } else if (position.includes('Mediocampo')) {
            zoneClass = '.midfield-zone';
        } else if (position.includes('Delantero')) {
            zoneClass = team === 'black-team' ? '.offensive-zone.right' : '.defensive-zone.left';
        }
        
        const zone = document.querySelector(zoneClass);
        if (zone) {
            zone.style.background = 'rgba(59, 130, 246, 0.2)';
            zone.style.borderColor = '#3b82f6';
        }
    }
    
    hideFieldZoneHighlight() {
        const zones = document.querySelectorAll('.field-zone');
        zones.forEach(zone => {
            zone.style.background = 'rgba(255,255,255,0.05)';
            zone.style.borderColor = 'rgba(255,255,255,0.3)';
        });
    }
    
    showPlayerStats(player) {
        const name = player.dataset.name;
        const position = player.dataset.position;
        const role = player.dataset.role;
        const skills = player.dataset.skills;
        
        // Crear indicador de estadísticas flotante
        if (!document.querySelector('.floating-stats')) {
            const statsDiv = document.createElement('div');
            statsDiv.className = 'floating-stats';
            statsDiv.innerHTML = `
                <div class="stats-content">
                    <h4>${name}</h4>
                    <p><strong>Posición:</strong> ${position}</p>
                    <p><strong>Rol:</strong> ${role}</p>
                    <p><strong>Habilidades:</strong> ${skills}</p>
                    <div class="skill-bars">
                        <div class="skill-bar">
                            <span>Técnica</span>
                            <div class="bar"><div class="fill" style="width: ${Math.random() * 40 + 60}%"></div></div>
                        </div>
                        <div class="skill-bar">
                            <span>Físico</span>
                            <div class="bar"><div class="fill" style="width: ${Math.random() * 40 + 60}%"></div></div>
                        </div>
                        <div class="skill-bar">
                            <span>Mental</span>
                            <div class="bar"><div class="fill" style="width: ${Math.random() * 40 + 60}%"></div></div>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(statsDiv);
            
            // Posicionar cerca del jugador
            const rect = player.getBoundingClientRect();
            statsDiv.style.left = rect.right + 10 + 'px';
            statsDiv.style.top = rect.top + 'px';
            
            // Animación de entrada
            setTimeout(() => statsDiv.classList.add('visible'), 10);
        }
    }
    
    hidePlayerStats() {
        const floatingStats = document.querySelector('.floating-stats');
        if (floatingStats) {
            floatingStats.remove();
        }
        
        // Limpiar líneas SVG
        const passLines = document.querySelector('.pass-lines');
        passLines.innerHTML = '';
    }
    
    showPlayerDetailModal(player) {
        const name = player.dataset.name;
        const position = player.dataset.position;
        const role = player.dataset.role;
        const skills = player.dataset.skills;
        
        // Crear modal detallado
        const modal = document.createElement('div');
        modal.className = 'player-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>${name}</h2>
                    <button class="close-modal">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="player-image">
                        <img src="${player.querySelector('img').src}" alt="${name}">
                    </div>
                    <div class="player-details">
                        <h3>Información del Jugador</h3>
                        <p><strong>🎯 Posición:</strong> ${position}</p>
                        <p><strong>⚽ Rol Principal:</strong> ${role}</p>
                        <p><strong>💪 Habilidades Clave:</strong> ${skills}</p>
                        
                        <h4>Consejos Tácticos:</h4>
                        <div class="tactical-tips">
                            ${this.getTacticalTips(position)}
                        </div>
                        
                        <h4>Estadísticas Simuladas:</h4>
                        <div class="player-stats-detailed">
                            <div class="stat">
                                <span>Velocidad</span>
                                <div class="stat-bar">
                                    <div class="stat-fill" style="width: ${Math.random() * 30 + 70}%"></div>
                                </div>
                            </div>
                            <div class="stat">
                                <span>Precisión</span>
                                <div class="stat-bar">
                                    <div class="stat-fill" style="width: ${Math.random() * 30 + 70}%"></div>
                                </div>
                            </div>
                            <div class="stat">
                                <span>Resistencia</span>
                                <div class="stat-bar">
                                    <div class="stat-fill" style="width: ${Math.random() * 30 + 70}%"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Event listener para cerrar
        modal.querySelector('.close-modal').addEventListener('click', () => {
            modal.remove();
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.remove();
        });
        
        // Animación de entrada
        setTimeout(() => modal.classList.add('visible'), 10);
    }
    
    getTacticalTips(position) {
        const tips = {
            'Arquero': [
                '🥅 Mantén siempre la comunicación con la defensa',
                '👀 Anticípate a los movimientos del rival',
                '🤲 Usa ambas manos para mayor seguridad en las atajadas'
            ],
            'Defensa': [
                '🛡️ Mantén la línea defensiva organizada',
                '👥 Comunícate constantemente con tus compañeros',
                '⚡ Despeja el balón hacia las bandas cuando tengas presión'
            ],
            'Mediocampo': [
                '🎯 Busca siempre el pase que rompa líneas',
                '🔄 Mantén el equilibrio entre ataque y defensa',
                '👁️ Ten visión periférica para encontrar espacios'
            ],
            'Delantero': [
                '🏃‍♂️ Busca constantemente espacios entre defensores',
                '⚽ Define con tranquilidad y precisión',
                '💡 Crea jugadas para tus compañeros cuando no puedas rematar'
            ]
        };
        
        const positionTips = tips[position] || tips['Mediocampo'];
        return positionTips.map(tip => `<p>${tip}</p>`).join('');
    }
    
    toggleInfo() {
        this.showInfoMode = !this.showInfoMode;
        const players = document.querySelectorAll('.player.interactive');
        
        players.forEach(player => {
            if (this.showInfoMode) {
                player.classList.add('info-mode');
                this.showPermanentTooltip(player);
            } else {
                player.classList.remove('info-mode');
                this.hidePermanentTooltip(player);
            }
        });
    }
    
    togglePositions() {
        this.showPositionsMode = !this.showPositionsMode;
        const zones = document.querySelectorAll('.field-zone');
        
        zones.forEach(zone => {
            if (this.showPositionsMode) {
                zone.style.background = 'rgba(59, 130, 246, 0.15)';
                zone.style.borderColor = '#3b82f6';
            } else {
                zone.style.background = 'rgba(255,255,255,0.05)';
                zone.style.borderColor = 'rgba(255,255,255,0.3)';
            }
        });
    }
    
    toggleStats() {
        this.showStatsMode = !this.showStatsMode;
        // Implementar visualización de estadísticas avanzadas
        console.log('Modo estadísticas:', this.showStatsMode);
    }
    
    animateFormation() {
        const players = document.querySelectorAll('.player.interactive');
        
        players.forEach((player, index) => {
            // Animación de formación
            player.style.transform = 'translate(-50%, -50%) scale(0.8) rotate(360deg)';
            
            setTimeout(() => {
                player.style.transform = 'translate(-50%, -50%) scale(1) rotate(0deg)';
            }, index * 200);
        });
        
        // Efecto de campo
        const field = document.querySelector('.soccer-field');
        field.style.transform = 'scale(1.02)';
        
        setTimeout(() => {
            field.style.transform = 'scale(1)';
        }, 2000);
    }
    
    startTipCarousel() {
        setInterval(() => {
            this.nextTip();
        }, 4000);
    }
    
    nextTip() {
        this.tips[this.currentTip].classList.remove('active');
        this.currentTip = (this.currentTip + 1) % this.tips.length;
        this.tips[this.currentTip].classList.add('active');
    }
    
    createPassLines() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes dashAnimation {
                0% { stroke-dashoffset: 100; }
                100% { stroke-dashoffset: 0; }
            }
            
            .floating-stats {
                position: fixed;
                background: linear-gradient(135deg, #1f2937, #374151);
                color: white;
                padding: 15px;
                border-radius: 12px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.3);
                z-index: 1000;
                max-width: 300px;
                transform: translateY(20px);
                opacity: 0;
                transition: all 0.3s ease;
                border: 1px solid rgba(255,255,255,0.2);
            }
            
            .floating-stats.visible {
                transform: translateY(0);
                opacity: 1;
            }
            
            .floating-stats h4 {
                margin-bottom: 10px;
                color: #fbbf24;
            }
            
            .floating-stats p {
                margin: 5px 0;
                font-size: 0.9rem;
                line-height: 1.4;
            }
            
            .skill-bars {
                margin-top: 15px;
            }
            
            .skill-bar {
                margin: 8px 0;
            }
            
            .skill-bar span {
                display: block;
                font-size: 0.8rem;
                margin-bottom: 3px;
                color: #d1d5db;
            }
            
            .bar {
                background: rgba(255,255,255,0.2);
                height: 6px;
                border-radius: 3px;
                overflow: hidden;
            }
            
            .fill {
                height: 100%;
                background: linear-gradient(45deg, #3b82f6, #8b5cf6);
                transition: width 1s ease;
                border-radius: 3px;
            }
            
            .player-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                backdrop-filter: blur(5px);
                z-index: 2000;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .player-modal.visible {
                opacity: 1;
            }
            
            .modal-content {
                background: white;
                border-radius: 20px;
                max-width: 600px;
                width: 90%;
                max-height: 80%;
                overflow-y: auto;
                transform: scale(0.9);
                transition: transform 0.3s ease;
            }
            
            .player-modal.visible .modal-content {
                transform: scale(1);
            }
            
            .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px;
                border-bottom: 1px solid #e5e7eb;
                background: linear-gradient(45deg, #3b82f6, #8b5cf6);
                color: white;
                border-radius: 20px 20px 0 0;
            }
            
            .close-modal {
                background: none;
                border: none;
                font-size: 2rem;
                color: white;
                cursor: pointer;
                padding: 0;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .modal-body {
                padding: 20px;
                display: grid;
                grid-template-columns: 150px 1fr;
                gap: 20px;
            }
            
            .player-image img {
                width: 100%;
                border-radius: 12px;
            }
            
            .player-details h3, .player-details h4 {
                color: #374151;
                margin: 15px 0 10px;
            }
            
            .player-details p {
                margin: 8px 0;
                line-height: 1.5;
            }
            
            .tactical-tips p {
                background: #f3f4f6;
                padding: 8px;
                border-radius: 8px;
                margin: 5px 0;
                border-left: 3px solid #3b82f6;
            }
            
            .stat {
                margin: 10px 0;
            }
            
            .stat span {
                display: block;
                font-size: 0.9rem;
                margin-bottom: 5px;
                color: #6b7280;
            }
            
            .stat-bar {
                background: #e5e7eb;
                height: 8px;
                border-radius: 4px;
                overflow: hidden;
            }
            
            .stat-fill {
                height: 100%;
                background: linear-gradient(45deg, #10b981, #3b82f6);
                transition: width 1.5s ease;
                border-radius: 4px;
            }
            
            @media (max-width: 768px) {
                .modal-body {
                    grid-template-columns: 1fr;
                    text-align: center;
                }
                
                .floating-stats {
                    max-width: 250px;
                    font-size: 0.8rem;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new SoccerFieldInteractive();
});

// Funciones adicionales para efectos especiales
function addSparkleEffect(element) {
    const sparkles = ['✨', '⭐', '🌟', '💫'];
    const sparkle = document.createElement('span');
    sparkle.textContent = sparkles[Math.floor(Math.random() * sparkles.length)];
    sparkle.style.position = 'absolute';
    sparkle.style.animation = 'sparkle 2s ease-out forwards';
    sparkle.style.pointerEvents = 'none';
    sparkle.style.fontSize = '1.2rem';
    
    const rect = element.getBoundingClientRect();
    sparkle.style.left = rect.left + Math.random() * rect.width + 'px';
    sparkle.style.top = rect.top + Math.random() * rect.height + 'px';
    
    document.body.appendChild(sparkle);
    
    setTimeout(() => sparkle.remove(), 2000);
}

// Añadir animación de sparkles al CSS
const sparkleStyle = document.createElement('style');
sparkleStyle.textContent = `
    @keyframes sparkle {
        0% {
            opacity: 0;
            transform: scale(0) rotate(0deg);
        }
        50% {
            opacity: 1;
            transform: scale(1) rotate(180deg);
        }
        100% {
            opacity: 0;
            transform: scale(0) rotate(360deg);
        }
    }
`;
document.head.appendChild(sparkleStyle);
