// Funções principais do Stoots

// Navegação do menu
function initializeNavigation() {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function() {
            // Remove active de todos os itens
            document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
            // Adiciona active ao item clicado
            this.classList.add('active');
            
            // Navegação baseada no texto
            const text = this.querySelector('span').textContent.toLowerCase();
            const routes = {
                'dashboard': '/dashboard',
                'gastos': '/expenses',
                'metas': '/goals',
                'gamificação': '/gamification',
                'educação': '/education',
                'investimentos': '/investments',
                'notificações': '/notifications',
                'configurações': '/settings'
            };
            
            if (routes[text]) {
                window.location.href = routes[text];
            }
        });
    });
}

// Logout
function initializeLogout() {
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            window.location.href = '/logout';
        });
    }
}

// Animações de entrada
function animateElements() {
    const cards = document.querySelectorAll('.card');
    const sections = document.querySelectorAll('.section');
    
    cards.forEach((card, index) => {
        card.style.animation = `fadeIn 0.5s ease ${index * 0.1}s both`;
    });
    
    sections.forEach((section, index) => {
        section.style.animation = `slideIn 0.5s ease ${index * 0.2}s both`;
    });
}

// Atualizar progresso das metas
function updateGoalProgress() {
    const progressBars = document.querySelectorAll('.progress-fill');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });
}

// Formulários interativos
function initializeForms() {
    // Formulário de gastos
    const expenseForm = document.getElementById('expense-form');
    if (expenseForm) {
        expenseForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const description = document.getElementById('expense-description').value;
            const amount = parseFloat(document.getElementById('expense-amount').value);
            const category = document.getElementById('expense-category').value;
            
            // Simular envio para o backend
            console.log('Novo gasto:', { description, amount, category });
            
            // Limpar formulário
            this.reset();
            
            // Mostrar mensagem de sucesso
            showNotification('Gasto adicionado com sucesso!', 'success');
        });
    }
    
    // Formulário de metas
    const goalForm = document.getElementById('goal-form');
    if (goalForm) {
        goalForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('goal-name').value;
            const target = parseFloat(document.getElementById('goal-target').value);
            const deadline = document.getElementById('goal-deadline').value;
            
            // Enviar para o backend
            fetch('/api/add_goal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name,
                    target_amount: target,
                    deadline: deadline
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Meta criada com sucesso!', 'success');
                    this.reset();
                }
            })
            .catch(error => {
                showNotification('Erro ao criar meta', 'error');
            });
        });
    }
}

// Sistema de notificações
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Estilos da notificação
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        animation: slideInRight 0.3s ease;
        background: ${type === 'success' ? 'var(--accent-green)' : type === 'error' ? 'var(--accent-red)' : 'var(--primary-blue)'};
    `;
    
    document.body.appendChild(notification);
    
    // Remover após 3 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Gráficos interativos (se Plotly estiver disponível)
function initializeCharts() {
    if (typeof Plotly !== 'undefined') {
        // Exemplo de gráfico de linha para investimentos
        const chartContainer = document.getElementById('investment-chart');
        if (chartContainer) {
            const data = [{
                x: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                y: [1000, 1200, 1150, 1400, 1600, 1800],
                type: 'scatter',
                mode: 'lines+markers',
                line: { color: '#00a8ff', width: 3 },
                marker: { size: 8, color: '#00a8ff' }
            }];
            
            const layout = {
                title: 'Evolução do Patrimônio',
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: { color: '#ffffff' },
                xaxis: { gridcolor: '#2c3e50' },
                yaxis: { gridcolor: '#2c3e50' }
            };
            
            Plotly.newPlot(chartContainer, data, layout);
        }
    }
}

// Atualizar dados em tempo real
function updateRealTimeData() {
    // Simular atualização de dados
    setInterval(() => {
        const balanceElements = document.querySelectorAll('.card-value');
        balanceElements.forEach(element => {
            if (element.textContent.includes('R$')) {
                // Simular pequenas variações
                const currentValue = parseFloat(element.textContent.replace('R$ ', '').replace('.', ''));
                const variation = (Math.random() - 0.5) * 10;
                const newValue = Math.max(0, currentValue + variation);
                element.textContent = `R$ ${newValue.toFixed(0)}`;
            }
        });
    }, 30000); // Atualizar a cada 30 segundos
}

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeLogout();
    animateElements();
    updateGoalProgress();
    initializeForms();
    initializeCharts();
    
    // Atualizar dados em tempo real apenas no dashboard
    if (window.location.pathname === '/dashboard') {
        updateRealTimeData();
    }
});

// Adicionar estilos CSS para animações
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .card, .section {
        opacity: 0;
        transform: translateY(20px);
    }
`;
document.head.appendChild(style); 