// Toggle da sidebar no mobile
document.addEventListener("DOMContentLoaded", () => {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.overlay');

    sidebarToggle?.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('open');
    });

    overlay?.addEventListener('click', () => {
        sidebar.classList.remove('open');
        overlay.classList.remove('open');
    });

    // Gráfico de vendas
    const ctx = document.getElementById('salesChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: [...Array(30).keys()].map(i => i + 1),
                datasets: [{
                    label: 'Vendas',
                    data: [1200, 1900, 1500, 2000, 1800, 2500, 2200, 3000, 2800, 3500, 4000, 3800, 4200, 4500, 5000, 4800, 5200, 5500, 6000, 5800, 6200, 6500, 7000, 6800, 7200, 7500, 8000, 7800, 8200, 8500],
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    borderColor: '#4f46e5',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: val => 'R$ ' + val.toLocaleString()
                        }
                    },
                    x: {
                        grid: { display: false }
                    }
                }
            }
        });
    }
});
