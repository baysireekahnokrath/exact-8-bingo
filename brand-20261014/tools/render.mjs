// Render SVG or HTML files to PNG with Chromium. Usage: node render.mjs jobs.json
// jobs.json: [{"src": "path.svg|html", "out": "path.png", "w": 1080, "h": 1080, "scale": 1}]
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs'; import path from 'path';
const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const browser = await chromium.launch();
for (const j of jobs) {
  const page = await browser.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: j.scale || 1 });
  await page.goto('file://' + path.resolve(j.src));
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: j.out, omitBackground: !!j.transparent, clip: { x: 0, y: 0, width: j.w, height: j.h } });
  await page.close();
}
await browser.close();
console.log('rendered', jobs.length);
