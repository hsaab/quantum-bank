# Quantum Bank Logo Package 🎨

Complete logo package for Quantum Bank (qbank.dev) - Banking Built for Developers

## Logo Concept

The logo represents quantum superposition where |0⟩ + |1⟩ = Q
- **0** represents traditional banking (the circle)
- **1** represents the future/digital (the vertical line)
- **Q** represents Quantum Bank (the fusion of both)

The quantum particles and interference effects symbolize the probabilistic, cutting-edge nature of quantum computing and modern fintech.

## Files Included

### Main Logos (SVG)
- `quantum-bank-logo.svg` - Full color version with quantum effects (200x200)
- `quantum-bank-logo-white.svg` - Monochrome white for dark backgrounds
- `quantum-bank-logo-black.svg` - Monochrome black for light backgrounds

### Favicon Sizes (SVG)
- `favicon-16x16.svg` - Browser favicon (16x16)
- `favicon-32x32.svg` - Browser favicon (32x32)
- `apple-touch-icon.svg` - iOS home screen icon (180x180)

### React Component
- `QuantumBankLogo.tsx` - Fully typed React/TypeScript component
  - Props: `size`, `className`, `animated`
  - Usage: `<QuantumBankLogo size={64} animated={true} />`

### Conversion Scripts
- `convert-to-png.js` - Node.js script (requires `sharp`)
- `convert-to-png.py` - Python script (requires `cairosvg`)

## Color Palette

```css
/* Primary Gradient */
--quantum-start: #a78bfa;
--quantum-mid: #8b7ff4;
--quantum-end: #6366f1;

/* Background */
--bg-dark: #0f0f23;

/* Accent */
--particle-color: #c4b5fd;
```

## Usage

### Web (HTML)
```html
<img src="quantum-bank-logo.svg" alt="Quantum Bank" width="200" />
```

### React/Next.js
```tsx
import QuantumBankLogo from './QuantumBankLogo';

function Header() {
  return <QuantumBankLogo size={48} animated={true} />;
}
```

### Favicon Setup
```html
<link rel="icon" type="image/svg+xml" href="/favicon-32x32.svg" />
<link rel="apple-touch-icon" href="/apple-touch-icon.svg" />
```

## Converting to PNG

### Option 1: Node.js (Recommended)
```bash
npm install sharp
node convert-to-png.js
```

### Option 2: Python
```bash
pip install cairosvg
python3 convert-to-png.py
```

### Option 3: Online Converter
Upload the SVG files to:
- https://cloudconvert.com/svg-to-png
- https://svgtopng.com/

## PNG Sizes Generated

- 1024x1024 - Hero/marketing
- 512x512 - Standard app icon
- 256x256 - Social media
- 128x128 - Small app icon
- 180x180 - Apple touch icon
- 32x32 - Browser favicon
- 16x16 - Browser favicon

## Design Guidelines

### Spacing
- Minimum clear space: 20% of logo height on all sides
- Never stretch or distort the logo

### Backgrounds
- **Primary**: Dark navy (#0f0f23)
- **Alternative**: Pure black or very dark grays
- **Avoid**: Light backgrounds (use black version instead)

### Minimum Sizes
- Digital: 32px minimum
- Print: 0.5 inch minimum
- Favicon: 16px minimum (use simplified version)

## Animation

The SVG logos include subtle quantum particle animations:
- Particles pulse with varying opacity
- Creates a "quantum uncertainty" effect
- Animation can be disabled by removing `<animate>` tags

For React component, set `animated={false}` to disable.

## License

© 2024 Quantum Bank. All rights reserved.

---

Built with quantum-inspired design for developers who demand more from their banking infrastructure.

**qbank.dev** | API-First | CLI-Native | AI-Forward
