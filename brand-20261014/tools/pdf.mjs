// Print an HTML page to A4 PDF with Chromium. Usage: node tools/pdf.mjs page.html out.pdf
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import path from 'path';
const [src, out] = process.argv.slice(2);
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('file://' + path.resolve(src), { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
await browser.close();
console.log('wrote', out);
