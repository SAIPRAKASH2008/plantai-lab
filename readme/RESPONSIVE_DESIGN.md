# PlantAI Lab — Responsive Design Documentation

## Overview
The PlantAI Lab monitoring system has been fully optimized for responsive (elastic) web design, adapting seamlessly to all screen sizes from mobile phones to large desktop displays.

## Responsive Breakpoints

### 1. **Large Desktop (1400px and above)**
- Full 4-column grid layouts
- Maximum font size (15px base)
- Maximum padding and spacing (32px content area)
- All status indicators visible
- Enhanced visual hierarchy

### 2. **Desktop (1024px - 1399px)**
- 2-column grid layouts for 4-column content
- Standard font size (14px base)
- Optimized spacing for comfortable viewing
- All navigation and features visible

### 3. **Tablet Landscape (768px - 1023px)**
- 2-column grids with adjusted proportions (1.5fr 1fr)
- Reduced font size (13px base)
- Compact sidebar (240px width)
- Charts adjusted to 220px height
- Vessel grid with 180px minimum width items
- Top bar remains full-featured

### 4. **Tablet Portrait (481px - 767px)**
- Horizontal navigation converted to responsive menu
- Sidebar moved to top as collapsible hamburger menu
- Full-width single-column layouts
- Reduced font size (12px base)
- Touch-friendly spacing
- Charts reduced to 180px height
- Compact cards with 14px padding

### 5. **Mobile (320px - 480px)**
- Fully stacked single-column layouts
- Mobile-optimized sidebar (top navigation bar)
- Smallest font size (11px base)
- Minimal padding (12px)
- Maximum viewport utilization
- Charts reduced to 150px height
- Touch targets minimum 44x44px for accessibility
- Responsive top bar with wrapped actions

## Key Responsive Features

### Flexible Grid Layouts
- **Grid-4**: Adapts from 4 columns → 2 columns → 1 column
- **Grid-3**: Adapts from 3 columns → 2 columns → 1 column
- **Grid-2-1**: Adapts from 2:1 ratio → balanced 1:1 → 1 column
- All grids use responsive gap sizing (16px → 12px → 10px)

### Dynamic Typography
- Font sizes adjust automatically across breakpoints
- Maintains readability on all devices
- Reduced font weight for smaller screens when needed
- Respects user's `prefers-reduced-motion` setting

### Navigation System
- **Desktop**: Fixed left sidebar (260px width)
- **Tablet & Mobile**: Collapsible top menu with hamburger toggle
- Swipe gestures supported (swipe right to open, swipe left to close)
- Auto-collapse on navigation for better UX
- Responsive sidebar footer hidden on mobile until expanded

### Chart Responsiveness
- Charts: 250px → 220px → 180px → 150px height
- Dynamic font sizing based on screen width
- Line width adjusts for mobile (1.5px vs 2px)
- Point hover radius reduced on mobile (3px vs 4px)
- Legend padding responsive (15px → 10px)

### Touch Optimization
- All interactive elements minimum 44x44px on mobile
- Prevented text selection on buttons/links (except inputs)
- `-webkit-tap-highlight-color: transparent` for cleaner interaction
- `-webkit-overflow-scrolling: touch` for momentum scrolling
- Font size 16px minimum on inputs to prevent iOS zoom

### Safe Area Support
- Respects notches and safe areas on modern phones
- Uses CSS `env(safe-area-inset-*)` variables
- Proper padding adjustment for notched devices

### Accessibility Features
- High contrast mode support (`prefers-contrast: more`)
- Reduced motion support (`prefers-reduced-motion: reduce`)
- Touch-friendly spacing
- Semantic HTML with proper ARIA labels
- Keyboard navigation support

## Component Adaptations

### Status Indicators
- **Desktop**: All 3 indicators visible (32px)
- **Tablet**: Visible with reduced spacing
- **Mobile**: Reduced to 24px, visible but compact

### DateTime Widget
- **Desktop & Tablet**: Full widget with picker
- **Mobile**: Hidden to save space (accessible via menu)

### Plant Camera Viewport
- **Desktop**: 320px height
- **Tablet Landscape**: 240px height
- **Mobile**: 200px height
- HUD overlay tags scale appropriately

### Cards & Containers
- Padding: 20px → 16px → 14px → 12px
- Border radius reduces on mobile (12px → 10px → 6px)
- Card headers stack on small screens

### Vessel Grid
- Desktop: 220px minimum width items
- Tablet: 180px minimum width items
- Mobile: 160px minimum width items on tablets, 130px on mobile

## JavaScript Enhancements

### Responsive Interactions
- Sidebar toggle functionality
- Window resize event listener (debounced for performance)
- Touch swipe detection (left/right gestures)
- Close sidebar when clicking outside on mobile
- Auto-collapse sidebar when navigating on mobile/tablet

### Chart.js Responsive Config
- Dynamic font size based on screen width
- Border width adjustment for mobile
- Point hover radius scaling
- Legend padding responsive

## Testing Recommendations

### Devices to Test
- **Mobile**: iPhone 12 Mini (375px), iPhone 12 Pro Max (428px), Samsung Galaxy S21 (360px)
- **Tablet**: iPad (768px), iPad Pro (1024px)
- **Desktop**: 1024px, 1366px, 1920px, 2560px viewports

### Testing Tools
- Chrome DevTools Device Toolbar
- Firefox Responsive Design Mode
- Safari Responsive Design Mode
- Real device testing recommended

### Orientation Testing
- Portrait mode on mobile and tablet
- Landscape mode on mobile and tablet
- Rotation transitions

## Performance Considerations

### Optimizations Applied
- Reduced re-renders with debounced resize listeners
- Mobile-first CSS approach
- Minimal animation (respects prefers-reduced-motion)
- Efficient touch event handling
- No unnecessary layout shifts (proper CLS handling)

### Future Improvements
- Service Worker for offline support
- Lazy loading of charts and images
- Progressive Web App (PWA) features
- Dynamic viewport units (dvh, dvw) for modern browsers

## CSS Custom Properties for Easy Customization

Key responsive variables that can be adjusted:
```css
--sidebar-width: 260px → 240px → 0 (changes per breakpoint)
--header-height: 64px → 56px → 48px (reduces on smaller screens)
--border-radius: 12px → 10px → 6px (reduces on mobile)
```

## Browser Support

- **Desktop**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile**: iOS Safari 14+, Chrome Mobile 90+, Samsung Internet 14+
- **Fallbacks**: Graceful degradation for older browsers

## Notes for Developers

1. Always test at multiple breakpoints during development
2. Use relative units (rem, em) for sizing
3. Test with actual touch devices when possible
4. Consider performance on lower-end mobile devices
5. Use `max-width` constraints to prevent content from becoming too wide
6. Leverage CSS Grid and Flexbox for layout flexibility

## Verification Checklist

- ✅ All grids stack to single column on mobile
- ✅ Font sizes scale appropriately
- ✅ Navigation is accessible on all screen sizes
- ✅ Touch targets are minimum 44x44px
- ✅ Charts are visible and readable on mobile
- ✅ Images and content scale properly
- ✅ No horizontal scrolling on mobile
- ✅ Safe area insets respected
- ✅ Performance maintained on slow networks
- ✅ Accessibility features working

## Quick Reference: Breakpoint Summary

| Breakpoint | Name | Width | Use Case |
|-----------|------|-------|----------|
| Mobile | Extra Small | 320-480px | Phones in portrait |
| Mobile L | Small | 481-767px | Phones in landscape, small tablets |
| Tablet | Medium | 768-1023px | Tablets in portrait |
| Desktop | Large | 1024-1399px | Tablets in landscape, small laptops |
| Large Desktop | Extra Large | 1400px+ | Large monitors |

For questions or issues, refer to the CSS custom properties and media queries in `/static/css/style.css`.
