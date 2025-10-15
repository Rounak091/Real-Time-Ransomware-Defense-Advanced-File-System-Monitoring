// Dashboard functionality
class RansomwareDashboard {
    constructor() {
        this.performanceChart = null;
        this.detectionChart = null;
        this.init();
    }

    init() {
        this.loadStats();
        this.loadAlerts();
        this.initCharts();
        this.startAutoRefresh();
    }

    async loadStats() {
        try {
            const response = await fetch('/api/metrics');
            const stats = await response.json();
            this.updateStatsGrid(stats);
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    async loadAlerts() {
        try {
            const response = await fetch('/api/alerts');
            const alerts = await response.json();
            this.updateAlertsList(alerts);
        } catch (error) {
            console.error('Error loading alerts:', error);
        }
    }

    updateStatsGrid(stats) {
        const statsGrid = document.getElementById('statsGrid');
        statsGrid.innerHTML = `
            <div class="stat-card high">
                <h3>${stats.total_alerts}</h3>
                <p>Total Alerts</p>
            </div>
            <div class="stat-card medium">
                <h3>${stats.recent_alerts}</h3>
                <p>Recent Alerts (1h)</p>
            </div>
            <div class="stat-card low">
                <h3>${stats.detection_accuracy}%</h3>
                <p>Detection Accuracy</p>
            </div>
            <div class="stat-card">
                <h3>${stats.cpu_usage}%</h3>
                <p>CPU Usage</p>
            </div>
            <div class="stat-card">
                <h3>${stats.memory_usage}%</h3>
                <p>Memory Usage</p>
            </div>
            <div class="stat-card low">
                <h3>${stats.system_status}</h3>
                <p>System Status</p>
            </div>
        `;
    }

    updateAlertsList(alerts) {
        const alertsList = document.getElementById('alertsList');
        if (alerts.length === 0) {
            alertsList.innerHTML = '<p>No recent alerts</p>';
            return;
        }

        alertsList.innerHTML = alerts.reverse().map(alert => `
            <div class="alert-item">
                <strong>${new Date(alert.timestamp).toLocaleString()}</strong><br>
                <span style="color: ${this.getSeverityColor(alert.severity)}">${alert.severity.toUpperCase()}</span> - 
                ${alert.message}<br>
                <small>File: ${alert.file_path}</small><br>
                <small>Confidence: ${(alert.confidence * 100).toFixed(1)}%</small>
            </div>
        `).join('');
    }

    getSeverityColor(severity) {
        const colors = {
            'high': '#e74c3c',
            'medium': '#f39c12',
            'low': '#27ae60'
        };
        return colors[severity] || '#95a5a6';
    }

    initCharts() {
        // Performance Chart
        const perfCtx = document.getElementById('performanceChart').getContext('2d');
        this.performanceChart = new Chart(perfCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'CPU Usage %',
                        data: [],
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        tension: 0.4
                    },
                    {
                        label: 'Memory Usage %',
                        data: [],
                        borderColor: '#2ecc71',
                        backgroundColor: 'rgba(46, 204, 113, 0.1)',
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });

        // Detection Chart
        const detCtx = document.getElementById('detectionChart').getContext('2d');
        this.detectionChart = new Chart(detCtx, {
            type: 'doughnut',
            data: {
                labels: ['Detected', 'False Positives', 'Missed'],
                datasets: [{
                    data: [85, 5, 10],
                    backgroundColor: ['#27ae60', '#f39c12', '#e74c3c']
                }]
            }
        });
    }

    startAutoRefresh() {
        setInterval(() => {
            this.loadStats();
            this.loadAlerts();
        }, 5000); // Refresh every 5 seconds
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    new RansomwareDashboard();
});

// Demo trigger function
async function triggerDemo() {
    try {
        await fetch('/api/trigger_demo', { method: 'POST' });
        // Reload alerts to show the new demo alert
        setTimeout(() => window.location.reload(), 1000);
    } catch (error) {
        console.error('Error triggering demo:', error);
    }
}