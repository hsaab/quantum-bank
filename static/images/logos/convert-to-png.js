#!/usr/bin/env node

/**
 * PNG Export Script for Quantum Bank Logo
 * 
 * This script converts the SVG logos to PNG format.
 * 
 * Requirements:
 * npm install sharp
 * 
 * Usage:
 * node convert-to-png.js
 */

const fs = require('fs');
const sharp = require('sharp');
const path = require('path');

const conversions = [
  { input: 'quantum-bank-logo.svg', output: 'quantum-bank-logo.png', size: 512 },
  { input: 'quantum-bank-logo.svg', output: 'quantum-bank-logo-1024.png', size: 1024 },
  { input: 'quantum-bank-logo.svg', output: 'quantum-bank-logo-256.png', size: 256 },
  { input: 'quantum-bank-logo.svg', output: 'quantum-bank-logo-128.png', size: 128 },
  { input: 'quantum-bank-logo-white.svg', output: 'quantum-bank-logo-white.png', size: 512 },
  { input: 'quantum-bank-logo-black.svg', output: 'quantum-bank-logo-black.png', size: 512 },
  { input: 'favicon-16x16.svg', output: 'favicon-16x16.png', size: 16 },
  { input: 'favicon-32x32.svg', output: 'favicon-32x32.png', size: 32 },
  { input: 'apple-touch-icon.svg', output: 'apple-touch-icon.png', size: 180 },
];

async function convertSvgToPng() {
  console.log('🎨 Converting SVG logos to PNG...\n');

  for (const { input, output, size } of conversions) {
    try {
      const svgBuffer = fs.readFileSync(input);
      await sharp(svgBuffer)
        .resize(size, size)
        .png()
        .toFile(output);
      console.log(`✓ Created ${output} (${size}x${size})`);
    } catch (error) {
      console.error(`✗ Failed to convert ${input}:`, error.message);
    }
  }

  console.log('\n✨ Done! All PNGs created.');
}

convertSvgToPng().catch(console.error);
