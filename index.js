#!/usr/bin/env node
// usage: node index.js <photo> 

import { getColor, getPalette, getSwatches } from 'colorthief';


const [imagePath, countArg] = process.argv.slice(2);

if (!imagePath) {
    console.error('Usage: node index.js <image-path> [colorCount]');
    process.exit(1);
}

// TODO: modify this number to see if accuracy improves? 
const colorCount = Number(countArg ?? 5);

// helper function just to make output look good
function swatch(color) {
    const { r, g, b } = color.rgb();
    return `\x1b[48;2;${r};${g};${b}m      \x1b[0m`;
}

// dominant
const dominant = await getColor(imagePath);
console.log('Dominant color:');
console.log(`  ${swatch(dominant)} ${dominant.hex()}  ${dominant.css()}  ${dominant.css('oklch')}\n`);

// palette 
const palette = await getPalette(imagePath, { colorCount });
console.log(`Palette (${palette.length} colors):`);
for (const color of palette) {
    const pct = (color.proportion * 100).toFixed(1).padStart(5);
    console.log(`  ${swatch(color)} ${color.hex()}  ${pct}%`);
}

// perceptual 
const perceptual = await getPalette(imagePath, { colorCount: 6, colorSpace: 'oklch' });
console.log(`Perceptual (${perceptual.length} colors):`);
for (const color of perceptual) {
    const pct = (color.proportion * 100).toFixed(1).padStart(5);
    console.log(`  ${swatch(color)} ${color.hex()}  ${pct}%`);
}

// semantic -> might be useless but good for contrast
// const swatches = await getSwatches(imagePath);


