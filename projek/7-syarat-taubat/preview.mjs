import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const [out, ...ts] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: Number(process.env.VW || 1920), height: Number(process.env.VH || 1080) } });
p.on('pageerror', (e) => console.log('ERR', e.message)); p.on('console', (m) => { if (m.type() !== 'log') console.log(m.type(), m.text()); });
await p.goto('http://127.0.0.1:8765/' + (process.env.PAGE || 'comp.html')); await p.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
for (const t of ts) { await p.evaluate((t) => window.render(t), Number(t)); await p.screenshot({ path: `${out}/p-${String(t).padStart(6, '0')}.jpg`, type: 'jpeg', quality: 80 }); }
await b.close();
