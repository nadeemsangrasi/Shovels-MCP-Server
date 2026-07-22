# Quick Reference: Landing Page 2026

## Tailwind Config (Eco-conscious Dark Mode)
```typescript
// tailwind.config.ts fragment
theme: {
  extend: {
    colors: {
      background: '#0a0a0a', // Deep black saves energy on OLED
      foreground: '#ededed',
      accent: {
        500: '#3b82f6',
        600: '#2563eb',
      },
      surface: '#121212',
    },
    fontFamily: {
      sans: ['var(--font-geist-sans)'],
      hero: ['var(--font-display)', 'Inter', 'sans-serif'],
    },
  },
}
```

## Framer Motion: Hover Micro-interaction
```tsx
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
  className="px-6 py-3 rounded-full bg-accent-500 text-white font-medium"
>
  Start Creating
</motion.button>
```

## Responsive Hero Typography (Fluid font-size)
```css
.hero-title {
  font-size: clamp(3rem, 10vw, 8rem);
  line-height: 0.9;
  letter-spacing: -0.04em;
  font-weight: 800;
}
```

## Anticipatory UX Checklist
- [ ] Adaptive Hero text (change "Creator" to "Agency" if URL param `src=agency`)
- [ ] Dynamic CTA Priority (Show 'Join' if new, 'Dashboard' if returning)
- [ ] Scroll-completion progress bar
- [ ] Haptic-imitating micro-animations for mobile
