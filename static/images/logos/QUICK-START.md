# Quantum Bank Logo - Quick Start Guide

## 📦 What You Have

Your complete logo package with everything needed for qbank.dev:

### SVG Files (Vector - Infinite Quality)
- ✨ `quantum-bank-logo.svg` - Main logo (purple gradient)
- ⚪ `quantum-bank-logo-white.svg` - White version
- ⚫ `quantum-bank-logo-black.svg` - Black version
- 🔖 `favicon-16x16.svg`, `favicon-32x32.svg` - Browser icons
- 🍎 `apple-touch-icon.svg` - iOS icon

### Code
- ⚛️ `QuantumBankLogo.tsx` - React component
- 📜 `convert-to-png.js` - Node.js PNG converter
- 🐍 `convert-to-png.py` - Python PNG converter

### Documentation
- 📖 `README.md` - Full documentation
- 🎨 `logo-showcase.html` - Visual showcase

## 🚀 Get Started in 30 Seconds

### For Your Website
```html
<!-- Just drop this in your HTML -->
<img src="quantum-bank-logo.svg" alt="Quantum Bank" width="200" />
```

### For React/Next.js
```tsx
import QuantumBankLogo from './QuantumBankLogo';

// In your component
<QuantumBankLogo size={48} animated={true} />
```

### For Favicon
```html
<link rel="icon" type="image/svg+xml" href="/favicon-32x32.svg" />
<link rel="apple-touch-icon" href="/apple-touch-icon.svg" />
```

## 🎨 Which Version to Use?

| Context | Use This |
|---------|----------|
| Dark background | `quantum-bank-logo.svg` (purple) or `quantum-bank-logo-white.svg` |
| Light background | `quantum-bank-logo-black.svg` |
| Browser tab | `favicon-32x32.svg` |
| iOS home screen | `apple-touch-icon.svg` |
| React app | `QuantumBankLogo.tsx` |

## 🖼️ Need PNG Files?

Run one of these scripts:

**Node.js:**
```bash
npm install sharp
node convert-to-png.js
```

**Python:**
```bash
pip install cairosvg
python3 convert-to-png.py
```

This generates:
- 1024×1024 - Hero/marketing
- 512×512 - App icon
- 256×256 - Social media
- 128×128 - Small app
- Plus all favicon sizes

## 💡 Pro Tips

1. **SVG First**: Use SVG whenever possible - perfect quality at any size
2. **Dark Mode**: The purple gradient looks best on dark backgrounds (#0f0f23)
3. **Animations**: The quantum particles pulse subtly - disable with `animated={false}` in React
4. **Brand Colors**: Use the gradient colors (#a78bfa → #8b7ff4 → #6366f1) throughout your site

## 🎯 Brand Identity

**Name:** Quantum Bank  
**Domain:** qbank.dev  
**Tagline:** Banking Built for Developers  
**Core Values:** API-First | CLI-Native | AI-Forward

**Logo Meaning:**
- The **0** = Traditional banking
- The **1** = Digital future  
- The **Q** = Quantum Bank (fusion of both)
- Particles = Quantum computing / uncertainty / innovation

## 📱 Social Media

For Twitter/X, LinkedIn, etc., convert the main logo to PNG:
- **Profile**: 512×512
- **Cover**: Use logo-showcase.html for inspiration

## 🎨 View Your Logos

Open `logo-showcase.html` in a browser to see all variations!

## ❓ Questions?

- Logo looks blurry? → You're using PNG at the wrong size, use SVG
- Want different colors? → Edit the gradient in the SVG files
- Need more sizes? → Run the conversion scripts or edit the SVG viewBox

---

**Ready to ship! 🚀**

Your quantum-powered brand identity is ready for qbank.dev.
