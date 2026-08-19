/* ═══════════════════════════════════════════════════════════
   PlantAI Lab — Main JavaScript
   Real-time data fetching, charts, gauges, and interactions
   ═══════════════════════════════════════════════════════════ */

// ─── Globals ────────────────────────────────────────────────
const chartInstances = {};
let refreshInterval = null;
let isLiveTimeMode = true;
let customSelectedDate = null;

// ─── Live Date & Time Utilities ──────────────────────────────
function formatDate(d = new Date()) {
    return d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
}

function formatTime(d = new Date()) {
    return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

function toLocalDatetimeInputValue(d = new Date()) {
    const pad = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}

function updateDateTimeDisplay() {
    const dateEl = document.getElementById('headerDate');
    const clockEl = document.getElementById('headerClock');
    const pickerEl = document.getElementById('liveDateTimePicker');
    const resetBtn = document.getElementById('liveResetBtn');

    const targetDate = isLiveTimeMode ? new Date() : (customSelectedDate || new Date());

    if (dateEl) dateEl.textContent = formatDate(targetDate);
    if (clockEl) clockEl.textContent = formatTime(targetDate);

    // Sync input picker if in live mode and user is not actively typing
    if (pickerEl && isLiveTimeMode && document.activeElement !== pickerEl) {
        pickerEl.value = toLocalDatetimeInputValue(targetDate).slice(0, 19);
    }

    if (resetBtn) {
        if (isLiveTimeMode) {
            resetBtn.classList.remove('paused');
            resetBtn.innerHTML = `<i class="fas fa-rotate fa-spin-pulse"></i> Live`;
        } else {
            resetBtn.classList.add('paused');
            resetBtn.innerHTML = `<i class="fas fa-pause"></i> Override`;
        }
    }
}

setInterval(() => {
    if (isLiveTimeMode) {
        updateDateTimeDisplay();
    }
}, 1000);

// Initialize date & time controls on page load
document.addEventListener('DOMContentLoaded', () => {
    updateDateTimeDisplay();

    const pickerEl = document.getElementById('liveDateTimePicker');
    const resetBtn = document.getElementById('liveResetBtn');

    if (pickerEl) {
        pickerEl.value = toLocalDatetimeInputValue(new Date()).slice(0, 19);
        pickerEl.addEventListener('change', (e) => {
            if (e.target.value) {
                isLiveTimeMode = false;
                customSelectedDate = new Date(e.target.value);
                updateDateTimeDisplay();
                showToast(`System date & time overridden to: ${formatDate(customSelectedDate)} ${formatTime(customSelectedDate)}`, 'info');
            }
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            isLiveTimeMode = true;
            customSelectedDate = null;
            updateDateTimeDisplay();
            showToast('Switched back to Live System Date & Time', 'success');
        });
    }

    // Sidebar toggle for mobile & tablet
    const toggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    if (toggle && sidebar) {
        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            sidebar.classList.toggle('open');
        });
        sidebar.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 1023) {
                    sidebar.classList.remove('open');
                }
            });
        });
    }

    // Close sidebar when clicking outside on mobile/tablet
    document.addEventListener('click', (e) => {
        if (sidebar && toggle && !sidebar.contains(e.target) && !toggle.contains(e.target)) {
            if (window.innerWidth <= 1023 && sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
            }
        }
    });

    // Handle window resize events for responsive behavior
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            if (window.innerWidth > 1023 && sidebar) {
                sidebar.classList.remove('open');
            }
        }, 250);
    });

    // Add touch support for better mobile interaction
    let touchStartX = 0;
    document.addEventListener('touchstart', (e) => {
        touchStartX = e.touches[0].clientX;
    }, false);

    document.addEventListener('touchend', (e) => {
        const touchEndX = e.changedTouches[0].clientX;
        const diff = touchStartX - touchEndX;
        
        if (sidebar && toggle) {
            // Swipe left to close sidebar on mobile
            if (diff > 50 && sidebar.classList.contains('open') && window.innerWidth <= 1023) {
                sidebar.classList.remove('open');
            }
            // Swipe right to open sidebar on mobile
            if (diff < -50 && !sidebar.classList.contains('open') && window.innerWidth <= 1023) {
                sidebar.classList.add('open');
            }
        }
    }, false);

    // ─── Request Browser Notification Permission ──────────
    // Request permission to show notifications (1 second delay for better UX)
    setTimeout(() => {
        if ('Notification' in window && Notification.permission === 'default') {
            requestNotificationPermission();
        }
    }, 1000);

    // Add notification bell click handler to manually request permission
    const notificationBell = document.getElementById('notificationBell');
    if (notificationBell) {
        notificationBell.addEventListener('click', () => {
            if ('Notification' in window) {
                if (Notification.permission === 'granted') {
                    showToast('🔔 Notifications are enabled!', 'success');
                } else if (Notification.permission === 'denied') {
                    showToast('❌ Notification permissions denied. Enable in browser settings.', 'warning');
                } else {
                    requestNotificationPermission();
                }
            } else {
                showToast('❌ Your browser does not support notifications.', 'danger');
            }
        });
    }
});

// ─── Browser Notification System ───────────────────────────
let notificationPermissionRequested = false;

// Request notification permission from user
function requestNotificationPermission() {
    if (!('Notification' in window)) {
        console.log('This browser does not support notifications');
        return false;
    }

    if (Notification.permission === 'granted') {
        console.log('Notification permission already granted');
        return true;
    }

    if (Notification.permission === 'denied') {
        console.log('Notification permission denied');
        return false;
    }

    if (!notificationPermissionRequested && Notification.permission === 'default') {
        notificationPermissionRequested = true;
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                console.log('Notification permission granted');
                sendDesktopNotification('PlantAI Lab', {
                    body: '✅ Notifications enabled! You will receive system alerts here.',
                    icon: '/static/images/plantai-icon.png',
                    tag: 'permission-granted'
                });
            }
        }).catch(err => {
            console.error('Error requesting notification permission:', err);
        });
    }

    return Notification.permission === 'granted';
}

// Send desktop/browser notification
function sendDesktopNotification(title, options = {}) {
    if (!('Notification' in window)) {
        return false;
    }

    if (Notification.permission !== 'granted') {
        console.log('Notification permission not granted');
        return false;
    }

    try {
        const notification = new Notification(title, {
            icon: '/static/images/plantai-icon.png',
            badge: '/static/images/plantai-badge.png',
            ...options
        });

        // Auto-close notification after specified time (default 8 seconds)
        const timeout = options.timeout || 8000;
        setTimeout(() => notification.close(), timeout);

        return true;
    } catch (err) {
        console.error('Error sending desktop notification:', err);
        return false;
    }
}

// Toast Notification System (with optional desktop notification)
function showToast(message, type = 'info', sendDesktopNotif = false) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const icons = {
        success: 'fa-circle-check',
        warning: 'fa-triangle-exclamation',
        danger: 'fa-circle-xmark',
        info: 'fa-circle-info',
        critical: 'fa-exclamation-circle'
    };

    const notificationTitles = {
        success: '✅ Success',
        warning: '⚠️ Warning',
        danger: '❌ Error',
        info: 'ℹ️ Information',
        critical: '🚨 Critical Alert'
    };

    // Show toast notification in browser
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas ${icons[type] || icons.info} toast-icon"></i>
        <span class="toast-message">${message}</span>
    `;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);

    // Send desktop notification for critical events
    if (sendDesktopNotif || type === 'danger' || type === 'critical') {
        if (Notification.permission === 'granted') {
            sendDesktopNotification(notificationTitles[type] || 'Notification', {
                body: message,
                tag: type,
                requireInteraction: type === 'critical'
            });
        }
    }
}

// ─── API Fetch Helper ───────────────────────────────────────
async function fetchAPI(endpoint) {
    try {
        const res = await fetch(endpoint);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (err) {
        console.error(`API Error (${endpoint}):`, err);
        return null;
    }
}

async function postAPI(endpoint, body) {
    try {
        const res = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (err) {
        console.error(`API Error (${endpoint}):`, err);
        return null;
    }
}

// ─── Chart.js Responsive Defaults ──────────────────────────
if (typeof Chart !== 'undefined') {
    Chart.defaults.color = '#9cb8a6';
    Chart.defaults.font.family = 'Inter, sans-serif';
    
    // Responsive font sizes
    const isMobile = window.innerWidth <= 480;
    const isTablet = window.innerWidth <= 768;
    
    Chart.defaults.font.size = isMobile ? 9 : (isTablet ? 10 : 11);
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
    Chart.defaults.plugins.legend.labels.pointStyleWidth = 8;
    Chart.defaults.plugins.legend.labels.padding = isMobile ? 10 : 15;
    Chart.defaults.elements.line.tension = 0.4;
    Chart.defaults.elements.line.borderWidth = isMobile ? 1.5 : 2;
    Chart.defaults.elements.point.radius = 0;
    Chart.defaults.elements.point.hoverRadius = isMobile ? 3 : 4;
    Chart.defaults.scale.grid = { color: 'rgba(45, 120, 80, 0.08)' };
    Chart.defaults.scale.border = { color: 'rgba(45, 120, 80, 0.08)' };
}

function createGradient(ctx, color1, color2) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 250);
    gradient.addColorStop(0, color1);
    gradient.addColorStop(1, color2);
    return gradient;
}

// ─── Gauge SVG Helper ───────────────────────────────────────
function createGaugeSVG(containerId, value, min, max, color = '#2dd4a8', unit = '') {
    const container = document.getElementById(containerId);
    if (!container) return;

    const percent = Math.min(100, Math.max(0, ((value - min) / (max - min)) * 100));
    const circumference = 2 * Math.PI * 42;
    const dashoffset = circumference * (1 - percent / 100);

    container.innerHTML = `
        <div class="gauge">
            <svg viewBox="0 0 100 100">
                <circle class="gauge-bg" cx="50" cy="50" r="42"/>
                <circle class="gauge-fill" cx="50" cy="50" r="42"
                    stroke="${color}"
                    stroke-dasharray="${circumference}"
                    stroke-dashoffset="${dashoffset}"/>
            </svg>
            <div class="gauge-value">
                <div class="gauge-number">${value}</div>
                <div class="gauge-unit">${unit}</div>
            </div>
        </div>
    `;
}

// ─── Update Notification Badge ──────────────────────────────
async function updateNotificationBadge() {
    const alerts = await fetchAPI('/api/anomaly-alerts');
    const badge = document.getElementById('notifBadge');
    if (badge && alerts) {
        badge.textContent = alerts.length;
        badge.style.display = alerts.length > 0 ? 'flex' : 'none';
    }
}

// ─── DASHBOARD PAGE ─────────────────────────────────────────
let lastSystemStatus = {};

async function initDashboard() {
    await Promise.all([
        updateDashboardStats(),
        updateDashboardGauges(),
        updateDashboardChart(),
        updateRecommendations(),
        updateNotificationBadge()
    ]);

    // Refresh every 5 seconds
    refreshInterval = setInterval(async () => {
        await Promise.all([
            updateDashboardStats(),
            updateDashboardGauges(),
            updateRecommendations(),
            updateNotificationBadge()
        ]);
    }, 5000);
}

async function updateDashboardStats() {
    const status = await fetchAPI('/api/system-status');
    if (!status) return;

    const el = (id) => document.getElementById(id);

    if (el('statActiveVessels')) el('statActiveVessels').textContent = `${status.tissue_culture.active_vessels}/${status.tissue_culture.total_vessels}`;
    if (el('statAvgHealth')) el('statAvgHealth').textContent = `${status.tissue_culture.avg_health_score}%`;
    if (el('statAlerts')) el('statAlerts').textContent = status.alerts.total;
    if (el('statAIRecs')) el('statAIRecs').textContent = status.ai_engine.recommendations_pending;

    // Update status indicators with notifications for status changes
    const tcStatus = document.querySelector('.status-dot[title*="Tissue"]');
    if (tcStatus) {
        const newStatus = status.tissue_culture.status === 'operational' ? 'operational' : 'warning';
        const oldStatus = lastSystemStatus.tc_status;
        
        tcStatus.className = `status-dot ${newStatus}`;

        // Send notification if status changed
        if (oldStatus && oldStatus !== newStatus) {
            if (newStatus === 'operational') {
                showToast('✅ Tissue Culture system is operational', 'success', true);
            } else {
                showToast('⚠️ Tissue Culture system has issues', 'warning', true);
            }
        }
        lastSystemStatus.tc_status = newStatus;
    }

    // Check for high alert count
    if (status.alerts.total > 5 && (!lastSystemStatus.alerts || lastSystemStatus.alerts <= 5)) {
        showToast(`🚨 High alert count: ${status.alerts.total} active alerts`, 'critical', true);
    }
    lastSystemStatus.alerts = status.alerts.total;

    // Check for low health score
    if (status.tissue_culture.avg_health_score < 70 && (!lastSystemStatus.health || lastSystemStatus.health >= 70)) {
        showToast(`⚠️ Low health score: ${status.tissue_culture.avg_health_score}%`, 'danger', true);
    }
    lastSystemStatus.health = status.tissue_culture.avg_health_score;
}

async function updateNotificationBadge() {
    const alerts = await fetchAPI('/api/anomaly-alerts');
    const badge = document.getElementById('notifBadge');
    if (badge && alerts) {
        const alertCount = alerts.length;
        badge.textContent = alertCount;
        badge.style.display = alertCount > 0 ? 'flex' : 'none';

        // Send summary notification if critical alerts exist
        const criticalAlerts = alerts.filter(a => a.severity === 'critical');
        if (criticalAlerts.length > 0 && Notification.permission === 'granted') {
            sendDesktopNotification('🚨 Critical Alerts', {
                body: `${criticalAlerts.length} critical alert(s) detected`,
                tag: 'critical-summary',
                requireInteraction: true
            });
        }
    }
}

async function updateDashboardGauges() {
    const tcData = await fetchAPI('/api/sensor-data/tissue-culture');
    if (!tcData) return;

    createGaugeSVG('gaugeTemp', tcData.temperature.value, tcData.temperature.min, tcData.temperature.max, '#2dd4a8', '°C');
    createGaugeSVG('gaugeHumidity', tcData.humidity.value, tcData.humidity.min, tcData.humidity.max, '#3b82f6', '%');
    createGaugeSVG('gaugeLight', tcData.light_intensity.value, tcData.light_intensity.min, tcData.light_intensity.max, '#f59e0b', 'lux');
    createGaugeSVG('gaugeCO2', tcData.co2_level.value, tcData.co2_level.min, tcData.co2_level.max, '#8b5cf6', 'ppm');
}

async function updateDashboardChart() {
    const tempData = await fetchAPI('/api/trend-data/temperature?points=24');
    const humData = await fetchAPI('/api/trend-data/humidity?points=24');
    if (!tempData || !humData) return;

    const ctx = document.getElementById('dashboardChart');
    if (!ctx) return;

    if (chartInstances['dashboard']) {
        chartInstances['dashboard'].destroy();
    }

    chartInstances['dashboard'] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: tempData.map(d => d.time),
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: tempData.map(d => d.value),
                    borderColor: '#2dd4a8',
                    backgroundColor: createGradient(ctx.getContext('2d'), 'rgba(45,212,168,0.15)', 'rgba(45,212,168,0)'),
                    fill: true,
                },
                {
                    label: 'Humidity (%)',
                    data: humData.map(d => d.value),
                    borderColor: '#3b82f6',
                    backgroundColor: 'transparent',
                    yAxisID: 'y1',
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: { position: 'top' },
                tooltip: {
                    backgroundColor: 'rgba(10,15,13,0.9)',
                    borderColor: 'rgba(45,120,80,0.2)',
                    borderWidth: 1,
                    padding: 10,
                    cornerRadius: 8,
                }
            },
            scales: {
                x: { display: true, ticks: { maxTicksLimit: 8 } },
                y: { display: true, position: 'left', title: { display: true, text: '°C' } },
                y1: { display: true, position: 'right', title: { display: true, text: '%' }, grid: { drawOnChartArea: false } }
            }
        }
    });
}

async function updateRecommendations() {
    const recs = await fetchAPI('/api/ai-recommendations');
    const container = document.getElementById('recsContainer');
    if (!recs || !container) return;

    const priorityIcons = {
        critical: 'fa-circle-exclamation',
        high: 'fa-triangle-exclamation',
        medium: 'fa-circle-info',
        low: 'fa-lightbulb'
    };

    container.innerHTML = recs.map(r => `
        <div class="rec-item ${r.priority}">
            <div class="rec-priority ${r.priority}">
                <i class="fas ${priorityIcons[r.priority]}"></i>
            </div>
            <div class="rec-content">
                <div class="rec-title">${r.title}</div>
                <div class="rec-desc">${r.description}</div>
                <div class="rec-meta">
                    <span><i class="fas fa-tag"></i> ${r.category}</span>
                    <span><i class="fas fa-chart-simple"></i> ${r.confidence}% confidence</span>
                    <span><i class="fas fa-clock"></i> ${r.timestamp}</span>
                </div>
            </div>
        </div>
    `).join('');
}

// ─── MEDIA DISPENSING PAGE ──────────────────────────────────
async function initMediaDispensing() {
    await updateDispensingLog();

    // Species selector change
    const speciesSelect = document.getElementById('speciesSelect');
    const stageSelect = document.getElementById('stageSelect');

    if (speciesSelect) {
        speciesSelect.addEventListener('change', optimizeMedia);
    }
    if (stageSelect) {
        stageSelect.addEventListener('change', optimizeMedia);
    }

    // Auto-optimize on load
    await optimizeMedia();
}

async function optimizeMedia() {
    const species = document.getElementById('speciesSelect')?.value;
    const stage = document.getElementById('stageSelect')?.value;
    if (!species || !stage) return;

    const result = await postAPI('/api/optimize-media', { species, stage });
    if (!result) return;

    // Update formulation display
    const formulationGrid = document.getElementById('formulationGrid');
    if (formulationGrid) {
        let html = '';
        for (const [name, data] of Object.entries(result.growth_regulators)) {
            const cleanName = name.replace('auxin_', '').replace('cytokinin_', '').replace('gibberellin_', '');
            html += `
                <div class="formulation-item">
                    <div class="formulation-name">${cleanName}</div>
                    <div class="formulation-value">${data.concentration}<span class="formulation-unit">${data.unit}</span></div>
                </div>
            `;
        }
        formulationGrid.innerHTML = html;
    }

    // Update confidence
    const confFill = document.getElementById('confidenceFill');
    const confValue = document.getElementById('confidenceValue');
    if (confFill) confFill.style.width = `${result.ai_confidence}%`;
    if (confValue) confValue.textContent = `${result.ai_confidence}%`;

    // Update notes
    const notesContainer = document.getElementById('aiNotes');
    if (notesContainer && result.optimization_notes) {
        notesContainer.innerHTML = result.optimization_notes.map(n =>
            `<div style="padding:6px 0;font-size:0.82rem;color:var(--text-secondary);border-bottom:1px solid rgba(45,120,80,0.06);">
                ${n}
            </div>`
        ).join('');
    }

    // Update env recommendations
    const envContainer = document.getElementById('envRecommendations');
    if (envContainer && result.environmental) {
        envContainer.innerHTML = `
            <div class="formulation-item">
                <div class="formulation-name">Temperature</div>
                <div class="formulation-value">${result.environmental.temperature}<span class="formulation-unit">°C</span></div>
            </div>
            <div class="formulation-item">
                <div class="formulation-name">Photoperiod</div>
                <div class="formulation-value">${result.environmental.photoperiod}<span class="formulation-unit">h/d</span></div>
            </div>
            <div class="formulation-item">
                <div class="formulation-name">Light</div>
                <div class="formulation-value">${result.environmental.light_intensity}<span class="formulation-unit">lux</span></div>
            </div>
        `;
    }
}

async function dispenseMedia() {
    const species = document.getElementById('speciesSelect')?.value;
    const stage = document.getElementById('stageSelect')?.value;
    const volume = document.getElementById('volumeSlider')?.value || 500;

    // Trigger animation
    const wave = document.querySelector('.dispense-wave');
    if (wave) {
        wave.classList.remove('active');
        void wave.offsetWidth; // trigger reflow
        wave.classList.add('active');
    }

    const result = await postAPI('/api/dispense', { species, stage, volume });
    if (result) {
        showToast(`Media dispensed: ${volume}mL of ${stage} medium for ${species}`, 'success');
        await updateDispensingLog();
    }
}

async function updateDispensingLog() {
    const log = await fetchAPI('/api/dispensing-log');
    const container = document.getElementById('dispensingLog');
    if (!container) return;

    if (!log || log.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-flask"></i>
                <p>No dispensing history yet</p>
            </div>
        `;
        return;
    }

    container.innerHTML = log.map(entry => `
        <div class="log-entry">
            <div class="log-status completed"></div>
            <div class="log-time">${entry.timestamp.split(' ')[1]}</div>
            <div style="flex:1;font-size:0.82rem;color:var(--text-secondary);">
                ${entry.id} — ${entry.volume_ml}mL ${entry.stage} medium
            </div>
            <div style="font-size:0.72rem;color:var(--text-muted);">${entry.duration_seconds}s</div>
        </div>
    `).join('');
}

// ─── GROWTH MONITOR PAGE ────────────────────────────────────
async function initGrowthMonitor() {
    const dtInput = document.getElementById('vesselInoculationDatetime');
    if (dtInput) {
        dtInput.value = toLocalDatetimeInputValue(new Date()).slice(0, 19);
    }

    await Promise.all([
        updateVesselGrid(),
        updateGrowthChart(),
        updateAnomalyAlerts(),
        initPlantVisionStream()
    ]);

    refreshInterval = setInterval(async () => {
        await Promise.all([
            updateVesselGrid(),
            updateAnomalyAlerts(),
            renderPlantVisionFrame()
        ]);
    }, 3000);
}

let activeVisionVessel = 'V-001';

async function initPlantVisionStream() {
    const selectEl = document.getElementById('visionVesselSelect');
    if (selectEl) {
        selectEl.addEventListener('change', (e) => {
            activeVisionVessel = e.target.value;
            renderPlantVisionFrame();
            showToast(`Switched Live Vision Stream to Camera (${activeVisionVessel})`, 'info');
        });
    }
    await renderPlantVisionFrame();
}

async function renderPlantVisionFrame() {
    const canvas = document.getElementById('plantVisionCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const data = await fetchAPI(`/api/live-plant-vision/${activeVisionVessel}`);
    if (!data) return;

    // Update HUD timestamp
    const tsEl = document.getElementById('hudTimestamp');
    if (tsEl) tsEl.textContent = data.timestamp;

    // Update Stats
    if (document.getElementById('visionShootCount')) document.getElementById('visionShootCount').textContent = data.shoot_count;
    if (document.getElementById('visionRootLength')) document.getElementById('visionRootLength').innerHTML = `${data.root_length_mm} <span style="font-size:0.9rem;font-weight:400;">mm</span>`;
    if (document.getElementById('visionNDVI')) document.getElementById('visionNDVI').textContent = data.ndvi_index;
    if (document.getElementById('visionLeafArea')) document.getElementById('visionLeafArea').innerHTML = `${data.leaf_area_mm2} <span style="font-size:0.9rem;font-weight:400;">mm²</span>`;
    if (document.getElementById('visionHeight')) document.getElementById('visionHeight').textContent = data.height_mm;

    // Canvas dimensions
    const w = canvas.width;
    const h = canvas.height;

    // 1. Draw In Vitro Vessel Graphics Background
    ctx.fillStyle = '#06110a';
    ctx.fillRect(0, 0, w, h);

    // Grid lines (camera sensor grid)
    ctx.strokeStyle = 'rgba(45, 120, 80, 0.12)';
    ctx.lineWidth = 1;
    for (let x = 0; x < w; x += 40) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
    }
    for (let y = 0; y < h; y += 40) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
    }

    // Glass vessel tube contour
    ctx.strokeStyle = 'rgba(45, 212, 168, 0.25)';
    ctx.lineWidth = 2;
    ctx.strokeRect(w * 0.2, h * 0.1, w * 0.6, h * 0.82);

    // Agar nutrient medium base
    const agarGradient = ctx.createLinearGradient(0, h * 0.65, 0, h * 0.92);
    agarGradient.addColorStop(0, 'rgba(45, 212, 168, 0.45)');
    agarGradient.addColorStop(1, 'rgba(13, 148, 136, 0.7)');
    ctx.fillStyle = agarGradient;
    ctx.fillRect(w * 0.205, h * 0.65, w * 0.59, h * 0.26);

    // Plantlet Stem & Shoots (Green botanical drawing)
    ctx.strokeStyle = '#22c55e';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(w * 0.5, h * 0.7);
    ctx.quadraticCurveTo(w * 0.48, h * 0.45, w * 0.52, h * 0.25);
    ctx.stroke();

    // Leaves
    ctx.fillStyle = '#10b981';
    for (let i = 0; i < 5; i++) {
        const lx = w * (0.42 + (i % 3) * 0.07);
        const ly = h * (0.3 + i * 0.08);
        ctx.beginPath();
        ctx.ellipse(lx, ly, 16, 9, (i % 2 === 0 ? 0.4 : -0.4), 0, 2 * Math.PI);
        ctx.fill();
    }

    // Roots inside agar
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(w * 0.5, h * 0.68);
    ctx.lineTo(w * 0.42, h * 0.82);
    ctx.moveTo(w * 0.5, h * 0.68);
    ctx.lineTo(w * 0.56, h * 0.85);
    ctx.stroke();

    // 2. Draw AI Computer Vision Bounding Boxes Overlay
    if (data.bounding_boxes) {
        data.bounding_boxes.forEach(box => {
            const bx = (box.x / 100) * w;
            const by = (box.y / 100) * h;
            const bw = (box.w / 100) * w;
            const bh = (box.h / 100) * h;

            let color = '#2dd4a8';
            if (box.type === 'root') color = '#3b82f6';
            if (box.type === 'anomaly') color = '#ef4444';

            // Draw bounding box
            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            ctx.strokeRect(bx, by, bw, bh);

            // Glowing corner accents
            ctx.fillStyle = color;
            ctx.fillRect(bx - 2, by - 2, 6, 6);
            ctx.fillRect(bx + bw - 4, by - 2, 6, 6);
            ctx.fillRect(bx - 2, by + bh - 4, 6, 6);
            ctx.fillRect(bx + bw - 4, by + bh - 4, 6, 6);

            // Bounding Box Label
            ctx.fillStyle = 'rgba(10, 25, 18, 0.9)';
            ctx.fillRect(bx, by - 20, ctx.measureText(box.label).width + 50, 18);

            ctx.fillStyle = color;
            ctx.font = '600 10px Inter, sans-serif';
            ctx.fillText(`${box.label} (${Math.round(box.confidence * 100)}%)`, bx + 4, by - 6);
        });
    }
}

async function registerNewVessel(event) {
    event.preventDefault();
    const species = document.getElementById('vesselSpeciesInput')?.value;
    const commonName = document.getElementById('vesselCommonNameInput')?.value;
    const stage = document.getElementById('vesselStageSelect')?.value;
    const dtValue = document.getElementById('vesselInoculationDatetime')?.value;

    const stages = ['Inoculation', 'Callus Induction', 'Shoot Multiplication', 'Root Regeneration', 'Hardening'];
    const stageIndex = stages.indexOf(stage);

    const payload = {
        species: species,
        common_name: commonName,
        stage: stage,
        stage_index: stageIndex >= 0 ? stageIndex : 0,
        progress: 10.0,
        growth_rate: 1.5,
        contamination_risk: 0.5,
        days_in_culture: 1,
        health_score: 98.0,
        inoculation_time: dtValue || new Date().toISOString()
    };

    const res = await postAPI('/api/vessels', payload);
    if (res && res.id) {
        showToast(`Vessel ${res.id} (${commonName}) registered at live datetime: ${dtValue || formatTime()}`, 'success');
        document.getElementById('newVesselForm')?.reset();
        if (dtInput) dtInput.value = toLocalDatetimeInputValue(new Date()).slice(0, 19);
        await updateVesselGrid();
    }
}

async function updateVesselGrid() {
    const vessels = await fetchAPI('/api/growth-data');
    const container = document.getElementById('vesselGrid');
    if (!vessels || !container) return;

    const stages = ['Inoculation', 'Callus Induction', 'Shoot Multiplication', 'Root Regeneration', 'Hardening'];

    container.innerHTML = vessels.map(v => {
        const healthClass = v.health_score >= 85 ? 'good' : v.health_score >= 70 ? 'warning' : 'danger';
        const progressClass = v.contamination_risk > 10 ? 'danger' : v.contamination_risk > 5 ? 'warning' : '';

        return `
            <div class="vessel-card" onclick="showToast('${v.id}: ${v.species} — ${v.stage}', 'info')">
                <div class="vessel-header">
                    <span class="vessel-id">${v.id}</span>
                    <span class="vessel-health ${healthClass}">${v.health_score}%</span>
                </div>
                <div class="vessel-species">${v.species}</div>
                <div class="vessel-stage"><i class="fas fa-layer-group"></i> ${v.stage}</div>
                <div class="stage-pipeline">
                    ${stages.map((s, i) => `
                        ${i > 0 ? `<div class="stage-line ${i <= v.stage_index ? 'completed' : ''}"></div>` : ''}
                        <div class="stage-dot ${i < v.stage_index ? 'completed' : i === v.stage_index ? 'current' : ''}"></div>
                    `).join('')}
                </div>
                <div class="progress-bar">
                    <div class="progress-fill ${progressClass}" style="width:${v.progress}%"></div>
                </div>
                <div class="vessel-stats">
                    <span><i class="fas fa-clock"></i> ${v.days_in_culture}d</span>
                    <span><i class="fas fa-arrow-up"></i> ${v.growth_rate}×/wk</span>
                    <span class="${v.contamination_risk > 5 ? 'text-warning' : ''}"><i class="fas fa-shield-virus"></i> ${v.contamination_risk}%</span>
                </div>
            </div>
        `;
    }).join('');
}

async function updateGrowthChart() {
    const data = await fetchAPI('/api/trend-data/growth_rate?points=24');
    const ctx = document.getElementById('growthChart');
    if (!data || !ctx) return;

    if (chartInstances['growth']) chartInstances['growth'].destroy();

    chartInstances['growth'] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => d.time),
            datasets: [{
                label: 'Avg Growth Rate (×/week)',
                data: data.map(d => d.value),
                borderColor: '#2dd4a8',
                backgroundColor: createGradient(ctx.getContext('2d'), 'rgba(45,212,168,0.2)', 'rgba(45,212,168,0)'),
                fill: true,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(10,15,13,0.9)',
                    borderColor: 'rgba(45,120,80,0.2)',
                    borderWidth: 1,
                    padding: 10,
                    cornerRadius: 8,
                }
            },
            scales: {
                x: { ticks: { maxTicksLimit: 8 } },
                y: { title: { display: true, text: '×/week' } }
            }
        }
    });
}

async function updateAnomalyAlerts() {
    const alerts = await fetchAPI('/api/anomaly-alerts');
    const container = document.getElementById('anomalyAlerts');
    if (!container) return;

    if (!alerts || alerts.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-shield-check"></i>
                <p>No active anomaly alerts</p>
            </div>
        `;
        return;
    }

    const severityIcons = {
        critical: 'fa-circle-exclamation',
        warning: 'fa-triangle-exclamation',
        info: 'fa-circle-info'
    };

    container.innerHTML = alerts.map(a => `
        <div class="rec-item ${a.severity === 'critical' ? 'critical' : a.severity === 'warning' ? 'high' : 'medium'}">
            <div class="rec-priority ${a.severity === 'critical' ? 'critical' : a.severity === 'warning' ? 'high' : 'medium'}">
                <i class="fas ${severityIcons[a.severity]}"></i>
            </div>
            <div class="rec-content">
                <div class="rec-title">${a.type}: ${a.vessel}</div>
                <div class="rec-desc">${a.message}</div>
                <div class="rec-meta">
                    <span><i class="fas fa-clock"></i> ${a.timestamp}</span>
                </div>
            </div>
        </div>
    `).join('');

    // Send desktop notifications for new anomalies (especially critical ones)
    alerts.forEach(a => {
        if (a.severity === 'critical' && Notification.permission === 'granted') {
            sendDesktopNotification('🚨 CRITICAL ALERT', {
                body: `${a.type} on ${a.vessel}: ${a.message}`,
                tag: `anomaly-${a.vessel}-${a.type}`,
                requireInteraction: true
            });
        } else if (a.severity === 'warning' && Notification.permission === 'granted') {
            sendDesktopNotification('⚠️ Warning Alert', {
                body: `${a.type} on ${a.vessel}: ${a.message}`,
                tag: `anomaly-${a.vessel}-${a.type}`,
                timeout: 10000
            });
        }
    });
}

// ─── HYDROPONICS PAGE ──────────────────────────────────────
async function initHydroponics() {
    await Promise.all([
        updateHydroSensors(),
        updateHydroCharts()
    ]);

    refreshInterval = setInterval(updateHydroSensors, 5000);
}

async function updateHydroSensors() {
    const data = await fetchAPI('/api/sensor-data/hydroponics');
    if (!data) return;

    const params = ['ph', 'ec', 'dissolved_oxygen', 'water_temperature', 'flow_rate'];
    params.forEach(p => {
        const valEl = document.getElementById(`hydro-${p}-value`);
        if (valEl && data[p]) {
            valEl.innerHTML = `${data[p].value}<span class="unit">${data[p].unit}</span>`;

            // Color based on optimal range
            const [optLow, optHigh] = data[p].optimal;
            if (data[p].value >= optLow && data[p].value <= optHigh) {
                valEl.style.color = 'var(--status-success)';
            } else {
                valEl.style.color = 'var(--status-warning)';
            }
        }
    });

    // Update gauges
    if (data.ph) createGaugeSVG('hydroGaugePH', data.ph.value, data.ph.min, data.ph.max, '#2dd4a8', 'pH');
    if (data.ec) createGaugeSVG('hydroGaugeEC', data.ec.value, data.ec.min, data.ec.max, '#3b82f6', 'mS/cm');
    if (data.dissolved_oxygen) createGaugeSVG('hydroGaugeDO', data.dissolved_oxygen.value, data.dissolved_oxygen.min, data.dissolved_oxygen.max, '#f59e0b', 'mg/L');
}

async function updateHydroCharts() {
    const phData = await fetchAPI('/api/trend-data/ph?points=24');
    const ecData = await fetchAPI('/api/trend-data/ec?points=24');
    const ctx = document.getElementById('hydroChart');
    if (!phData || !ecData || !ctx) return;

    if (chartInstances['hydro']) chartInstances['hydro'].destroy();

    chartInstances['hydro'] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: phData.map(d => d.time),
            datasets: [
                {
                    label: 'pH',
                    data: phData.map(d => d.value),
                    borderColor: '#2dd4a8',
                    backgroundColor: createGradient(ctx.getContext('2d'), 'rgba(45,212,168,0.15)', 'rgba(45,212,168,0)'),
                    fill: true,
                },
                {
                    label: 'EC (mS/cm)',
                    data: ecData.map(d => d.value),
                    borderColor: '#3b82f6',
                    backgroundColor: 'transparent',
                    yAxisID: 'y1',
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: { position: 'top' },
                tooltip: {
                    backgroundColor: 'rgba(10,15,13,0.9)',
                    borderColor: 'rgba(45,120,80,0.2)',
                    borderWidth: 1,
                    padding: 10,
                    cornerRadius: 8,
                }
            },
            scales: {
                x: { ticks: { maxTicksLimit: 8 } },
                y: { position: 'left', title: { display: true, text: 'pH' } },
                y1: { position: 'right', title: { display: true, text: 'mS/cm' }, grid: { drawOnChartArea: false } }
            }
        }
    });
}

// ─── COLLABORATION PAGE ─────────────────────────────────────
async function initCollaboration() {
    await Promise.all([
        updateConnectedLabs(),
        updateProtocols()
    ]);
}

async function updateConnectedLabs() {
    const labs = await fetchAPI('/api/connected-labs');
    const container = document.getElementById('labsContainer');
    if (!labs || !container) return;

    container.innerHTML = labs.map(lab => `
        <div class="lab-card">
            <div class="lab-status-dot ${lab.status}"></div>
            <div class="lab-info">
                <div class="lab-name">${lab.name}</div>
                <div class="lab-location"><i class="fas fa-map-marker-alt"></i> ${lab.location}</div>
            </div>
            <div class="lab-stats">
                <div>${lab.active_cultures} cultures</div>
                <div>${lab.researchers} researchers</div>
            </div>
        </div>
    `).join('');
}

async function updateProtocols() {
    const protocols = await fetchAPI('/api/protocols');
    const container = document.getElementById('protocolsContainer');
    if (!protocols || !container) return;

    container.innerHTML = protocols.map(p => `
        <div class="protocol-card">
            <div class="protocol-title">${p.title}</div>
            <div class="protocol-author"><i class="fas fa-user-circle"></i> ${p.author}</div>
            <div class="protocol-desc">${p.description}</div>
            <div class="protocol-meta">
                <span class="success-rate"><i class="fas fa-check-circle"></i> ${p.success_rate}%</span>
                <span><i class="fas fa-download"></i> ${p.downloads}</span>
                <span><i class="fas fa-star"></i> ${p.rating}</span>
                <span><i class="fas fa-clock"></i> ${p.shared_date}</span>
            </div>
        </div>
    `).join('');
}

// ─── Cleanup on page navigation ─────────────────────────────
window.addEventListener('beforeunload', () => {
    if (refreshInterval) clearInterval(refreshInterval);
    Object.values(chartInstances).forEach(c => c.destroy());
});
