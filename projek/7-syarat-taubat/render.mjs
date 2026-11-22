import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { spawn } from 'node:child_process';
const [from, to, out] = [Number(process.argv[2]), Number(process.argv[3]), process.argv[4]]; const RATE = 30;
const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(RATE), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: Number(process.env.VW || 1920), height: Number(process.env.VH || 1080) } });
p.on('pageerror', (e) => console.log('ERR', e.message));
await p.goto('http://127.0.0.1:8765/' + (process.env.PAGE || 'comp.html')); await p.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
const t0 = Date.now();
for (let f = from; f < to; f++) {
  await p.evaluate((t) => window.render(t), f / RATE);
  const buf = await p.screenshot({ type: 'jpeg', quality: 93 });
  if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
  if ((f - from) % 300 === 0) console.log(out, f, `${((Date.now() - t0) / 1000).toFixed(0)}s`);
}
ff.stdin.end(); await new Promise((r) => ff.on('close', r)); await b.close();
console.log('done', out, `${((Date.now() - t0) / 1000).toFixed(0)}s`);
