# Troubleshooting Landing Page 2026

## Performance

### Issue: Low Framer Motion FPS
**Cause:** Animating non-composite properties (width, height, top/left).
**Solution:** Use only `x`, `y`, `scale`, `rotate`, and `opacity`. Add `will-change: transform` to heavy layers.

### Issue: Font Flash (Layout Shift)
**Cause:** Heavy variable fonts loading after text rendering.
**Solution:**
- Use WOFF2 format.
- Preload the font in `<head>`.
- Set `font-display: swap`.

## Visuals

### Issue: Poor Contrast in Dark Mode
**Cause:** Using pure black (#000) with thin dark grey text.
**Solution:** Use "Ink" blacks (#050505 or #0a0a0a) and ensure text follows APCA contrast targets for large display type.

### Issue: Horizontal Scroll Jitter
**Cause:** Scrollytelling content width exceeding viewport.
**Solution:** Wrap scrollytelling components in `overflow-x-hidden`.

## Animation

### Issue: Trigger not firing
**Cause:** Viewport margin too tight.
**Solution:** Adjust `viewport={{ margin: "-20%' }}` in Framer Motion to trigger earlier.
