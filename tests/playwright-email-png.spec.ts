import { test, expect } from '@playwright/test';

async function fetchBuffer(page, url: string): Promise<Buffer> {
  const res = await page.request.get(url);
  expect(res.ok()).toBeTruthy();
  const buf = await res.body();
  return Buffer.from(buf);
}

function percentDiff(a: Buffer, b: Buffer): number {
  // Compare PNGs using pixelmatch-like manual approach via Canvas is heavy; use bounding box via sharp fallback
  const { PNG } = require('pngjs');
  const imgA = PNG.sync.read(a);
  const imgB = PNG.sync.read(b);
  if (imgA.width !== imgB.width || imgA.height !== imgB.height) return 100;
  let diffPixels = 0;
  for (let i = 0; i < imgA.data.length; i += 4) {
    const dr = Math.abs(imgA.data[i] - imgB.data[i]);
    const dg = Math.abs(imgA.data[i + 1] - imgB.data[i + 1]);
    const db = Math.abs(imgA.data[i + 2] - imgB.data[i + 2]);
    const da = Math.abs(imgA.data[i + 3] - imgB.data[i + 3]);
    if (dr + dg + db + da > 10) diffPixels++;
  }
  const total = imgA.width * imgA.height;
  return (diffPixels / total) * 100;
}

async function compareOrWriteBaseline(page, name: string, url: string) {
  const fs = require('fs');
  const path = require('path');
  const dir = path.resolve(__dirname, 'baselines');
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  const baselinePath = path.join(dir, name);
  const current = await fetchBuffer(page, url);
  if (!fs.existsSync(baselinePath)) {
    fs.writeFileSync(baselinePath, current);
    test.info().annotations.push({ type: 'baseline', description: `Created ${name}` });
    return;
  }
  const baseline = fs.readFileSync(baselinePath);
  const drift = percentDiff(baseline, current);
  expect(drift).toBeLessThanOrEqual(0.5);
}

const HOST = 'https://mode-dash-production.up.railway.app';

test('email PNG 600x400 visual parity', async ({ page }) => {
  await compareOrWriteBaseline(
    page,
    'email_ad_600x400.png',
    `${HOST}/api/email/ad.png?property=mff&w=600&h=400&send=playwright-600`
  );
});

test('email PNG 300x250 visual parity', async ({ page }) => {
  await compareOrWriteBaseline(
    page,
    'email_ad_300x250.png',
    `${HOST}/api/email/ad.png?property=mff&w=300&h=250&send=playwright-300`
  );
});
