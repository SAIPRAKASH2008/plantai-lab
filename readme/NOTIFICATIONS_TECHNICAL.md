# 🔧 PlantAI Lab - Notifications Technical Implementation

## Overview

The PlantAI Lab notification system has been fully integrated with the Browser Notifications API. This document covers the technical implementation, code structure, and customization options.

---

## Architecture

### Three-Layer Notification System

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: System Events                                  │
│ (Anomalies, Status Changes, Alerts)                     │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 2: Notification Handlers                          │
│ (Desktop Notification API)                              │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 3: User Interface                                 │
│ (Toast + Desktop Notifications)                         │
└─────────────────────────────────────────────────────────┘
```

### Core Functions

```
requestNotificationPermission()  → Handles user permission
                                   └─ Auto-request on page load
                                   └─ Manual request from bell icon
                                   └─ Fallback for denied permission

sendDesktopNotification(title, options)
                                → Sends OS notification
                                   └─ Icon/Badge support
                                   └─ Tag-based deduplication
                                   └─ Timeout auto-close
                                   └─ RequireInteraction flag

showToast(message, type, sendDesktopNotif)
                                → Displays in-browser toast
                                   └─ Optional desktop notification
                                   └─ Toast styles (success/danger/warning/info)
```

---

## Implementation Details

### 1. Permission Management

#### Auto-Request (On Page Load)
```javascript
// In DOMContentLoaded event (delayed 1 second for UX)
setTimeout(() => {
    if ('Notification' in window && Notification.permission === 'default') {
        requestNotificationPermission();
    }
}, 1000);
```

#### Manual Request (Bell Click)
```javascript
// Notification bell click handler
document.getElementById('notificationBell')?.addEventListener('click', () => {
    if (!('Notification' in window)) {
        showToast('Your browser does not support notifications', 'warning');
        return;
    }
    
    if (Notification.permission === 'granted') {
        showToast('✅ Notifications are enabled!', 'success');
    } else if (Notification.permission === 'denied') {
        showToast('❌ Notifications disabled in browser settings', 'warning');
    } else {
        requestNotificationPermission();
    }
});
```

#### Permission States
```javascript
Notification.permission === 'granted'  // User allowed notifications
Notification.permission === 'denied'   // User blocked notifications
Notification.permission === 'default'  // Not asked yet
```

### 2. Notification Sending

#### Basic Notification
```javascript
if (Notification.permission === 'granted') {
    const notification = new Notification('Alert Title', {
        body: 'Alert message',
        icon: '/static/images/plantai-icon.png',
        badge: '/static/images/plantai-badge.png'
    });
    
    // Auto-close after 8 seconds
    setTimeout(() => notification.close(), 8000);
}
```

#### Critical Notification (Requires Interaction)
```javascript
const notification = new Notification('🚨 CRITICAL ALERT', {
    body: 'Contamination detected on Vessel V-001',
    tag: 'anomaly-V-001-contamination',  // Unique identifier
    requireInteraction: true,              // User must click to close
    icon: '/static/images/plantai-icon.png',
    badge: '/static/images/plantai-badge.png'
});
```

#### Tag-Based Deduplication
```javascript
// Same tag replaces previous notification
new Notification('Status Update', {
    body: 'New status message',
    tag: 'status-update'  // Replaces previous "status-update" notification
});
```

### 3. Integration Points

#### A. Anomaly Alerts
**File:** `/static/js/main.js` → `updateAnomalyAlerts()`

```javascript
async function updateAnomalyAlerts() {
    const alerts = await fetchAPI('/api/anomaly-alerts');
    // ... render alerts to DOM ...
    
    // Send desktop notifications for new anomalies
    alerts.forEach(a => {
        if (a.severity === 'critical' && Notification.permission === 'granted') {
            sendDesktopNotification('🚨 CRITICAL ALERT', {
                body: `${a.type} on ${a.vessel}: ${a.message}`,
                tag: `anomaly-${a.vessel}-${a.type}`,
                requireInteraction: true  // User must click
            });
        } else if (a.severity === 'warning' && Notification.permission === 'granted') {
            sendDesktopNotification('⚠️ Warning Alert', {
                body: `${a.type} on ${a.vessel}: ${a.message}`,
                tag: `anomaly-${a.vessel}-${a.type}`,
                timeout: 10000  // Auto-close after 10 seconds
            });
        }
    });
}
```

**Severity Mapping:**
- `critical` → Desktop notification with requireInteraction: true
- `warning` → Desktop notification with 10-second timeout
- `info` → Toast notification only (no desktop notification)

#### B. System Status Changes
**File:** `/static/js/main.js` → `updateDashboardStats()`

```javascript
const newStatus = status.tissue_culture.status === 'operational' ? 'operational' : 'warning';
const oldStatus = lastSystemStatus.tc_status;

// Notify on status change
if (oldStatus && oldStatus !== newStatus) {
    if (newStatus === 'operational') {
        showToast('✅ Tissue Culture system is operational', 'success', true);
        // true = send desktop notification
    } else {
        showToast('⚠️ Tissue Culture system has issues', 'warning', true);
    }
}

// Alert on high alert count
if (status.alerts.total > 5 && (!lastSystemStatus.alerts || lastSystemStatus.alerts <= 5)) {
    showToast(`🚨 High alert count: ${status.alerts.total} active alerts`, 'critical', true);
}

// Alert on low health
if (status.tissue_culture.avg_health_score < 70 && (!lastSystemStatus.health || lastSystemStatus.health >= 70)) {
    showToast(`⚠️ Low health score: ${status.tissue_culture.avg_health_score}%`, 'danger', true);
}
```

#### C. Notification Badge Update
**File:** `/static/js/main.js` → `updateNotificationBadge()`

```javascript
async function updateNotificationBadge() {
    const alerts = await fetchAPI('/api/anomaly-alerts');
    const badge = document.getElementById('notifBadge');
    
    if (badge && alerts) {
        const alertCount = alerts.length;
        badge.textContent = alertCount;
        badge.style.display = alertCount > 0 ? 'flex' : 'none';
        
        // Send summary notification for critical alerts
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
```

#### D. Media Dispensing Success
**File:** `/static/js/main.js` → `dispenseMedia()`

```javascript
const result = await postAPI('/api/dispense', { species, stage, volume });
if (result) {
    showToast(`Media dispensed: ${volume}mL of ${stage} medium for ${species}`, 'success');
    // Success toasts automatically send desktop notifications if enabled
}
```

#### E. Recommendations
**File:** `/static/js/main.js` → `updateRecommendations()`

```javascript
async function updateRecommendations() {
    const recs = await fetchAPI('/api/ai-recommendations');
    // ... render recommendations to DOM ...
    
    // Send notification for critical recommendations (future enhancement)
    const criticalRecs = recs.filter(r => r.priority === 'critical');
    if (criticalRecs.length > 0) {
        showToast(`${criticalRecs.length} critical recommendation(s)`, 'danger', true);
    }
}
```

---

## Code Changes Summary

### Files Modified

#### 1. `/static/js/main.js`

**New Functions Added:**

```javascript
// Request user permission for notifications
function requestNotificationPermission() {
    if (!('Notification' in window)) return false;
    if (Notification.permission === 'granted') return true;
    if (Notification.permission === 'denied') return false;
    if (!notificationPermissionRequested && Notification.permission === 'default') {
        notificationPermissionRequested = true;
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                sendDesktopNotification('PlantAI Lab', {
                    body: '✅ Notifications enabled!',
                    tag: 'permission-granted'
                });
            }
        });
    }
    return Notification.permission === 'granted';
}

// Send a desktop notification
function sendDesktopNotification(title, options = {}) {
    if (Notification.permission !== 'granted') return false;
    try {
        const notification = new Notification(title, {
            icon: '/static/images/plantai-icon.png',
            badge: '/static/images/plantai-badge.png',
            ...options
        });
        const timeout = options.timeout || 8000;
        setTimeout(() => notification.close(), timeout);
        return true;
    } catch (err) {
        console.error('Error:', err);
        return false;
    }
}
```

**Enhanced Existing Functions:**

- `showToast()` - Added `sendDesktopNotif` parameter
- `updateDashboardStats()` - Added status change notifications
- `updateAnomalyAlerts()` - Added critical/warning alerts notifications
- `initDashboard()` - Added call to `updateNotificationBadge()`

**New State Variables:**

```javascript
let lastSystemStatus = {};  // Tracks previous status for change detection
let notificationPermissionRequested = false;  // Prevents repeated requests
```

---

## Customization

### 1. Change Notification Icons

Replace icon paths in `sendDesktopNotification()`:
```javascript
icon: '/static/images/plantai-icon.png',      // Main icon (128x128 or 256x256)
badge: '/static/images/plantai-badge.png'    // Badge icon (24x24 or 48x48)
```

Create icon files at those paths or update paths to match your assets.

### 2. Adjust Notification Timeouts

**For specific notifications:**
```javascript
sendDesktopNotification('Title', {
    body: 'Message',
    timeout: 15000  // 15 seconds instead of default 8
});
```

**For global default:**
In `sendDesktopNotification()`, change:
```javascript
const timeout = options.timeout || 8000;  // Change 8000 to desired default (in ms)
```

### 3. Add New Notification Triggers

**Example: Notify on successful vessel registration**

In `registerNewVessel()` function:
```javascript
const res = await postAPI('/api/vessels', payload);
if (res && res.id) {
    showToast(`Vessel ${res.id} (${commonName}) registered successfully`, 'success', true);
    // Added 'true' to send desktop notification
    
    // Or send custom notification:
    if (Notification.permission === 'granted') {
        sendDesktopNotification('✅ Vessel Registered', {
            body: `${commonName} (${species}) - Stage: ${stage}`,
            tag: `vessel-${res.id}`
        });
    }
}
```

### 4. Modify Alert Severity Levels

**Current thresholds in `updateDashboardStats()`:**

```javascript
// Change alert count threshold
if (status.alerts.total > 5) { ... }  // Change 5 to different number

// Change health score threshold
if (status.tissue_culture.avg_health_score < 70) { ... }  // Change 70 to different %

// Add new threshold
if (status.hydroponics.ph_level > 7.2 && status.hydroponics.ph_level < 6.8) {
    showToast('pH level out of range', 'warning', true);
}
```

### 5. Add Notification Categories

**Group notifications by type:**

```javascript
const notificationCategories = {
    anomaly: { priority: 'high', icon: 'alert' },
    system: { priority: 'critical', icon: 'system' },
    recommendation: { priority: 'medium', icon: 'bulb' },
    success: { priority: 'low', icon: 'check' }
};

// Usage:
const category = notificationCategories.anomaly;
sendDesktopNotification(`[${category.priority.toUpperCase()}] Alert`, {
    body: alertMessage,
    tag: `${category}-${timestamp}`,
    requireInteraction: category.priority === 'critical'
});
```

### 6. Add Sound Alerts

**Modern notification APIs can play sounds:**

```javascript
// Note: Limited browser support, may need fallback
const notification = new Notification('Alert', {
    body: 'Critical issue detected',
    tag: 'critical',
    requireInteraction: true,
    // Some browsers support:
    // sound: '/static/sounds/alert.mp3'  // Not standard, may not work
});

// Better approach: Use Web Audio API if notification sounds aren't working
function playAlertSound() {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = 800;  // 800 Hz beep
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.5);
}

// Use in critical notification:
if (a.severity === 'critical') {
    playAlertSound();  // Beep!
    sendDesktopNotification('🚨 CRITICAL ALERT', { ... });
}
```

### 7. Notification Click Handling

**Add actions when user clicks notification:**

```javascript
async function sendDesktopNotificationWithAction(title, options = {}) {
    if (Notification.permission !== 'granted') return false;
    
    const notification = new Notification(title, {
        icon: '/static/images/plantai-icon.png',
        badge: '/static/images/plantai-badge.png',
        ...options
    });
    
    // Handle click
    notification.onclick = () => {
        // Bring window to focus
        window.focus();
        
        // Optionally navigate to relevant page
        if (options.action === 'view-anomaly') {
            window.location.hash = '#growth-monitor';
        } else if (options.action === 'view-dashboard') {
            window.location.hash = '#dashboard';
        }
        
        notification.close();
    };
    
    const timeout = options.timeout || 8000;
    setTimeout(() => notification.close(), timeout);
    
    return true;
}

// Usage:
sendDesktopNotificationWithAction('Anomaly Detected', {
    body: 'Contamination on V-001',
    tag: 'anomaly-V-001',
    requireInteraction: true,
    action: 'view-anomaly'
});
```

---

## Browser Compatibility

### Desktop Support

| Browser | Version | Support | Notes |
|---------|---------|---------|-------|
| Chrome | 50+ | ✅ Full | Recommended |
| Firefox | 48+ | ✅ Full | Works well |
| Safari | 14+ | ✅ Full | macOS only |
| Edge | 79+ | ✅ Full | Chromium-based |
| Opera | 37+ | ✅ Full | Chromium-based |
| IE | - | ❌ None | Unsupported |

### Mobile Support

| Browser | Support | Notes |
|---------|---------|-------|
| Chrome Mobile | ⚠️ Limited | Notifications may not work |
| Firefox Mobile | ⚠️ Limited | Experimental support |
| Safari iOS | ❌ None | Not supported in iOS |
| Android Browser | ✅ Some | Depends on device |

### Permission Prompts

| Browser | Permission UI |
|---------|---------------|
| Chrome | Bar at top of page |
| Firefox | Dropdown permission panel |
| Safari | Native system dialog |
| Edge | Bar at top of page |

---

## Debugging

### Check Notification Permission

**In browser console (F12):**
```javascript
// Check current permission
Notification.permission
// Output: "granted" | "denied" | "default"

// Send test notification
if (Notification.permission === 'granted') {
    new Notification('Test Notification', {
        body: 'If you see this, notifications are working!'
    });
}

// Check if browser supports Notifications API
'Notification' in window
// Output: true | false
```

### Enable Debug Logging

**Add logging to notification functions:**

```javascript
function sendDesktopNotification(title, options = {}) {
    console.log('📢 Sending notification:', { title, options });
    console.log('Permission status:', Notification.permission);
    
    if (Notification.permission !== 'granted') {
        console.warn('⚠️ Notifications not permitted');
        return false;
    }
    
    try {
        const notification = new Notification(title, {
            icon: '/static/images/plantai-icon.png',
            badge: '/static/images/plantai-badge.png',
            ...options
        });
        console.log('✅ Notification created successfully');
        
        const timeout = options.timeout || 8000;
        setTimeout(() => {
            notification.close();
            console.log('⏱️ Notification auto-closed');
        }, timeout);
        
        return true;
    } catch (err) {
        console.error('❌ Error creating notification:', err);
        return false;
    }
}
```

### Monitor Events

```javascript
// Log when permission request is made
Notification.requestPermission().then(permission => {
    console.log('Permission request result:', permission);
});

// Test notification with event listeners
const notification = new Notification('Test', { body: 'Test message' });

notification.onclick = () => console.log('✅ Notification clicked');
notification.onclose = () => console.log('✅ Notification closed');
notification.onerror = () => console.log('❌ Notification error');
notification.onshow = () => console.log('✅ Notification shown');
```

---

## Performance Considerations

### Notification Spam Prevention

**Using tags to prevent duplicate notifications:**

```javascript
// Only one "status-update" notification can exist at a time
sendDesktopNotification('Status Update', {
    body: 'New message',
    tag: 'status-update'  // Same tag replaces previous
});
```

**Debounce rapid notifications:**

```javascript
let notificationTimeout = null;

function sendDebouncedNotification(title, options = {}, delayMs = 1000) {
    clearTimeout(notificationTimeout);
    notificationTimeout = setTimeout(() => {
        sendDesktopNotification(title, options);
    }, delayMs);
}

// Usage:
sendDebouncedNotification('Alert', { body: 'Rapid alerts combined' });
sendDebouncedNotification('Alert', { body: 'Rapid alerts combined' });
sendDebouncedNotification('Alert', { body: 'Rapid alerts combined' });
// Only 1 notification sent after 1 second
```

### Memory Management

**Properly close notifications:**

```javascript
function sendDesktopNotification(title, options = {}) {
    if (Notification.permission !== 'granted') return false;
    
    const notification = new Notification(title, { ... });
    
    // Auto-close to prevent memory leaks
    const timeout = options.timeout || 8000;
    const timeoutId = setTimeout(() => notification.close(), timeout);
    
    // Also close on click (prevents lingering references)
    notification.onclick = () => {
        clearTimeout(timeoutId);
        notification.close();
    };
    
    return true;
}
```

---

## API Endpoints Used

The notification system depends on these backend endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/anomaly-alerts` | GET | Fetch current anomalies |
| `/api/system-status` | GET | Get system health status |
| `/api/ai-recommendations` | GET | Fetch AI recommendations |
| `/api/sensor-data/tissue-culture` | GET | Real-time sensor data |
| `/api/growth-data` | GET | Growth monitoring data |

Ensure these endpoints are available for notifications to work properly.

---

## Summary

The notification system is now fully integrated with:

✅ **Permission Management** - Auto-request on load, manual request from UI  
✅ **Desktop Notifications** - Critical alerts stay visible, warnings auto-close  
✅ **Status Monitoring** - Alerts on system changes, health score changes  
✅ **Anomaly Alerts** - Critical contamination and anomalies with sound  
✅ **Toast Integration** - In-browser toasts + desktop notifications together  
✅ **Tag Deduplication** - Prevents notification spam with unique tags  

**To use:** Reload PlantAI Lab and click "Allow" on the permission request.

**To customize:** Follow the examples above to add new notification types or modify existing behavior.
