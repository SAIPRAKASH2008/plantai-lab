# 🔔 PlantAI Lab - Browser Notifications Setup Guide

## Overview

Your PlantAI Lab monitoring system now supports **browser/desktop notifications** that will alert you to important events on your host machine, even when you're not actively viewing the website.

---

## ✨ Features

### Desktop Notifications Send for:

✅ **Critical Alerts**
- Contamination detected
- System failures
- Anomalies in cultures
- *Stay visible on screen until dismissed*

✅ **Warning Alerts**
- Low health scores
- Environmental out-of-range values
- Media dispensing issues
- *Auto-dismiss after 10 seconds*

✅ **System Status Changes**
- When tissue culture system goes offline/online
- When alert count exceeds threshold
- When health scores drop critically

✅ **Successful Operations**
- Media successfully dispensed
- New vessel registered
- Systems back to operational

✅ **Information Notifications**
- Live vision stream changed
- Date/time overrides
- Settings updated

---

## 🎯 Quick Start

### Step 1: Enable Notifications

When you first load the PlantAI Lab dashboard, you'll see a **permission request**:

```
🔔 "PlantAI Lab wants to show notifications"
```

**Click "Allow"** to enable browser notifications.

### Step 2: Grant Browser Permission

Depending on your browser:

**Chrome/Edge/Brave:**
1. Click the lock icon 🔒 in the address bar
2. Find "Notifications"
3. Set to "Allow"

**Firefox:**
1. Click the info icon ℹ️ in the address bar
2. Click "Permissions"
3. Toggle "Notifications" on

**Safari:**
1. Go to Safari → Settings → Notifications
2. Find "localhost" (or your domain)
3. Select "Allow"

### Step 3: You're Done! 🎉

Notifications will now appear on your desktop when:
- Critical events occur
- System status changes
- Alerts are detected

---

## 📱 How to Use

### View Notification Permission Status

Click the **🔔 notification bell** in the top bar:

```
Bell Icon Location:
┌─────────────────────────────────────────┐
│ ☰ LOGO [Indicators] [🔔] [🕐]         │
│                          ↑
│                    Notification Bell
└─────────────────────────────────────────┘
```

**When you click:**
- ✅ If enabled: Shows "Notifications are enabled!"
- ❌ If denied: Shows "Enable in browser settings"
- ? If default: Prompts for permission

### Notification Types

**Critical Alert (🚨) - REQUIRES INTERACTION**
```
╔════════════════════════════════════╗
║  🚨 CRITICAL ALERT                 ║
║                                    ║
║  Contamination on Vessel V-001:    ║
║  Fungal growth detected (92% sure) ║
║                                    ║
║  [×] Dismiss  [Open] PlantAI Lab   ║
╚════════════════════════════════════╝
```
- Stays on screen until clicked
- Sound alert on most systems
- Click to open PlantAI Lab

**Warning Alert (⚠️) - AUTO-DISMISS**
```
╔════════════════════════════════════╗
║  ⚠️ Warning Alert                   ║
║                                    ║
║  Low health score: 65%             ║
║  Vessel V-002 needs attention      ║
║                                    ║
║  (auto-closes in 10 seconds)       ║
╚════════════════════════════════════╝
```
- Auto-dismisses after 10 seconds
- Click to open PlantAI Lab
- Visible in notification history

**Success (✅) - AUTO-DISMISS**
```
╔════════════════════════════════════╗
║  ✅ Success                         ║
║                                    ║
║  Media dispensed: 500mL            ║
║  Shoot multiplication medium       ║
╚════════════════════════════════════╝
```
- Auto-dismisses after 8 seconds
- Confirmation of successful action

---

## 🔧 Notification Settings

### Desktop Settings

**Windows 10/11:**
1. Settings → System → Notifications & actions
2. Find "PlantAI Lab" in the list
3. Choose your preferences:
   - Sound: On/Off
   - Banner: Show/Hide
   - Priority: Normal/Important

**macOS:**
1. System Preferences → Notifications
2. Find "Your Browser" in the list
3. Select notification style
4. Check "Show in Notification Center"

**Linux:**
1. Settings → Notifications
2. Enable notifications for your browser
3. Test notification sound

### Browser Settings

**Chrome/Edge:**
```
Settings → Privacy and security → Site settings → Notifications
→ Allow  (add "localhost" or your domain)
```

**Firefox:**
```
about:preferences → Privacy & Security → Permissions → Notifications
→ Allow (add "localhost" or your domain)
```

**Safari:**
```
Safari → Settings → Websites → Notifications
→ Allow for localhost/domain
```

---

## 🚨 Critical Alert Types

### 1. Contamination Detection (🦠)
```
🚨 CRITICAL ALERT

Contamination on Vessel V-001:
Fungal growth detected (92% sure)

Action: Check vessel immediately
Status: Requires manual intervention
```

### 2. System Failure (❌)
```
🚨 CRITICAL ALERT

Tissue Culture system is offline
Connection lost to control unit

Action: Check hardware connections
Status: Manual mode activated
```

### 3. Environmental Failure (🌡️)
```
⚠️ Warning Alert

Temperature critically low: 12°C
Expected range: 24-26°C

Action: Check temperature controller
Status: Cultures at risk
```

### 4. High Alert Count (📊)
```
🚨 CRITICAL ALERT

High alert count: 8 active alerts
Multiple issues detected

Action: Review dashboard
Status: Urgent review needed
```

---

## ⚠️ Warning Alert Types

### 1. Low Health Score (📉)
```
⚠️ Warning Alert

Low health score: 65%
Vessel V-002 needs attention

Action: Check growth conditions
Status: Monitor closely
```

### 2. Contamination Risk (⚠️)
```
⚠️ Warning Alert

Contamination risk elevated: 8%
Vessel V-003 showing signs

Action: Review culture conditions
Status: Preventive care needed
```

### 3. Anomaly Detected (🔍)
```
⚠️ Warning Alert

Anomaly on Vessel V-004:
Unusual growth pattern detected

Action: Review images
Status: AI confidence: 78%
```

---

## ✅ Success Notifications

### 1. Media Dispensed (✅)
```
✅ Success

Media dispensed: 500mL
Shoot multiplication medium for A. thaliana
```

### 2. Vessel Registered (✅)
```
✅ Success

Vessel V-005 registered
Arabidopsis thaliana - Shoot Multiplication
```

### 3. System Online (✅)
```
✅ Success

Tissue Culture system is operational
All sensors responding normally
```

---

## 📊 Notification History

Most operating systems keep a notification history:

**Windows 10/11:**
- Notification Center (bottom right)
- Keeps last 24 hours of notifications

**macOS:**
- Notification Center (top right)
- Shows notifications from past hours

**Linux:**
- Varies by desktop environment
- Usually in notification panel

### Accessing History:
1. Click notification area (Windows/macOS)
2. Scroll through recent notifications
3. Click any notification to view details
4. Click "Open" to go back to app

---

## 🔇 Muting Notifications

### Temporarily Disable for Session:
1. Click notification bell (🔔)
2. Current status will show
3. Browser will still show alerts to toast containers

### Permanently Disable:
**Browser Level:**
1. Go to Browser Permissions for PlantAI Lab
2. Set Notifications to "Block"
3. Reload page

**System Level:**
1. Open system notification settings
2. Find your browser
3. Disable notifications globally

### Re-enable Later:
1. Browser settings → Clear permissions
2. Reload PlantAI Lab
3. Click "Allow" on permission prompt
4. Notifications resume

---

## 🎯 Use Cases

### Scenario 1: Working Elsewhere
```
You're in a meeting, but PlantAI Lab is running:

16:45 → 🚨 Critical contamination alert
16:46 → Notification pops up on your desktop
16:47 → You step out and check the system
16:48 → Problem resolved before it spreads
```

### Scenario 2: Routine Monitoring
```
Monitoring multiple systems:

09:00 → Dashboard open in one monitor
09:05 → ✅ Vessel V-001 healthy
09:15 → ✅ Media dispensing successful
09:30 → ⚠️ Humidity slightly out of range
09:35 → You adjust controls
09:40 → ✅ All systems normal
```

### Scenario 3: Overnight Operations
```
Running long-term cultures overnight:

22:00 → PlantAI Lab monitoring active
23:15 → ⚠️ Warning notification sent
23:45 → Another warning received
06:00 → 🚨 Critical alert wakes you
06:05 → You check and address issue
```

---

## 🐛 Troubleshooting

### Notifications Not Appearing?

**Problem 1: Permission Denied**
```
Solution:
1. Check browser permission for PlantAI Lab
2. Click notification bell (🔔)
3. If denied, reset permissions:
   - Clear site data for PlantAI Lab
   - Reload page
   - Click "Allow" on new prompt
```

**Problem 2: Browser in "Do Not Disturb"**
```
Solution:
- Windows: Check notification settings
- macOS: Disable "Do Not Disturb" (⌘+Option+V)
- Linux: Check desktop environment settings
```

**Problem 3: Notifications Silenced**
```
Solution:
- Check system volume is not muted
- Check browser audio is enabled
- Check notification sound is not set to silent
```

**Problem 4: Wrong Browser**
```
Solution:
- Desktop notifications work in modern browsers
- Ensure: Chrome 50+, Firefox 48+, Safari 14+, Edge 79+
- Update your browser to latest version
```

### Notifications Too Frequent?

**Solution:**
- Notifications only trigger on critical/warning events
- Info notifications are shown as toast only
- Adjust alert thresholds in system settings (future feature)

### Notifications Not Auto-Dismissing?

**Critical alerts stay visible** (by design)
- This ensures you see critical messages
- Click anywhere to dismiss
- Or wait for system behavior

---

## 🔒 Privacy & Security

### What Data is Sent?
- **Notification Title**: Event type
- **Notification Body**: Alert details
- **No Personal Data**: Only system health info

### Notifications Are Local Only
- Notifications appear on your device only
- Not shared with other users
- Not logged to external servers
- Stored in browser notification history only

### Notification Permissions
- Granted per-site in browser
- Easy to revoke anytime
- Different per device
- Independent of PlantAI account

---

## 📚 Advanced Options

### Notification Tags (Prevents Duplicates)
```
Behind the scenes, notifications use "tags":
- anomaly-V-001-contamination
- system-status-change
- critical-alert

Same tag replaces previous notification
Prevents notification pile-up
```

### Require Interaction
```
Critical notifications require clicking:
- Won't disappear automatically
- Forces acknowledgment
- Important for critical alerts
```

### Notification Timeout
```
Different timeout for different types:
- Critical: No timeout (stays until clicked)
- Warning: 10 seconds
- Info: 8 seconds
- Success: 8 seconds
```

---

## 🎓 Tips & Tricks

### Tip 1: Keep Browser in Background
- Open PlantAI Lab in background tab
- Notifications still work
- Focus on other work
- Get alerted immediately

### Tip 2: Use Separate Workspace
- Open PlantAI Lab in different desktop/space
- Switch back when notified
- Keeps focused on current task

### Tip 3: Mobile Notifications (Beta)
- Some mobile browsers support notifications
- Less reliable than desktop
- Good as backup alert

### Tip 4: Combined with Toast Notifications
- Toast notifications also shown in-browser
- Desktop notifications shown on system
- Redundancy ensures you see alerts

---

## ✅ Verification Checklist

Make sure notifications are working:

- [ ] Permission granted in browser
- [ ] Notification bell shows enabled status
- [ ] Test notification appears when you:
  - [ ] Refresh page (should see permission request)
  - [ ] Change vision camera (see info notification)
  - [ ] Trigger anomaly alert (see critical notification)
- [ ] System sound plays (if enabled)
- [ ] Notification appears in system tray/history
- [ ] You can click to bring app to focus

---

## 📞 Support

### If notifications aren't working:

1. **Check browser version** - Update to latest
2. **Check system notifications** - May be globally disabled
3. **Check browser permissions** - Allow PlantAI Lab notifications
4. **Check sound volume** - Might be muted
5. **Test notification** - Refresh page, trigger an action
6. **Check notification history** - Might not see them but they're logged
7. **Try different browser** - Rule out browser-specific issues

### Enable Browser Developer Logging

```javascript
// In browser console (F12):
Notification.permission
// Should return "granted"

// Test sending notification:
new Notification("Test Alert", {body: "If you see this, notifications work!"})
```

---

## 🚀 Next Steps

1. ✅ **Reload PlantAI Lab** to start using notifications
2. ✅ **Click "Allow"** when permission is requested
3. ✅ **Verify** notifications are working
4. ✅ **Adjust system settings** for your preferences
5. ✅ **Monitor with confidence** knowing you'll be alerted!

---

## Summary

Your PlantAI Lab now sends **real-time desktop notifications** for:
- 🚨 Critical system alerts
- ⚠️ Warning conditions
- ✅ Successful operations
- ℹ️ Status changes

**Notifications are:**
- 📲 Sent to your host/desktop
- 🔔 Visible even if app is minimized
- 🎯 Targeted to important events only
- 🔐 Private and secure
- ⚙️ Fully configurable

**Get notified. Stay informed. React faster.** 🎉

---

For technical support or feature requests, refer to the main PlantAI Lab documentation.
