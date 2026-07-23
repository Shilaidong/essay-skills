#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createRequire } from "node:module";
import Module from "node:module";

if (process.env.NODE_PATH) {
  const nodePathEntries = [];
  for (const entry of process.env.NODE_PATH.split(path.delimiter).filter(Boolean)) {
    nodePathEntries.push(entry);
    const pnpmEntry = path.join(entry, ".pnpm", "node_modules");
    if (fs.existsSync(pnpmEntry)) nodePathEntries.push(pnpmEntry);
  }
  process.env.NODE_PATH = [...new Set(nodePathEntries)].join(path.delimiter);
  Module._initPaths();
}

const require = createRequire(import.meta.url);
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const LINUX_PRINT_FIX_CSS = path.join(__dirname, "print-fix.linux.css");

function parseArgs(argv) {
  const out = {
    width: 1920,
    height: 1080,
    screenReport: false,
    noLinuxFix: false,
  };
  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--screen-report") {
      out.screenReport = true;
    } else if (arg === "--no-linux-fix") {
      out.noLinuxFix = true;
    } else if (arg.startsWith("--")) {
      const key = arg.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      const value = argv[++i];
      if (!value) throw new Error(`Missing value for ${arg}`);
      out[key] = value;
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  if (!out.input || !out.output) {
    throw new Error("Usage: node export_landscape_pdf.mjs --input <html-or-url> --output <pdf> [--screen-report] [--css file] [--chrome path] [--no-linux-fix]");
  }
  out.width = Number(out.width);
  out.height = Number(out.height);
  return out;
}

function resolveInput(input) {
  if (/^https?:\/\//i.test(input) || input.startsWith("file://")) return input;
  return pathToFileURL(path.resolve(input)).href;
}

function findChrome(explicit) {
  const candidates = [
    explicit,
    process.env.CHROME_PATH,
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
  ].filter(Boolean);
  return candidates.find((candidate) => fs.existsSync(candidate));
}

function loadPlaywright() {
  try {
    return require("playwright");
  } catch (firstError) {
    const nodePath = process.env.NODE_PATH || "";
    for (const entry of nodePath.split(path.delimiter).filter(Boolean)) {
      for (const base of [entry, path.join(entry, ".pnpm", "node_modules")]) {
        const candidate = path.join(base, "playwright");
        try {
          return require(candidate);
        } catch {
          // Try the next NODE_PATH entry.
        }
      }
    }
    throw firstError;
  }
}

function screenReportCss(width, height) {
  return `
@page { size: ${width}px ${height}px; margin: 0; }
html, body { width: ${width}px; min-width: ${width}px; background: white !important; }
body { overflow: visible !important; print-color-adjust: exact; -webkit-print-color-adjust: exact; }
.topbar, .skip-link, .footer { display: none !important; }
main { width: ${width}px; overflow: visible !important; }
.hero { min-height: ${height}px; max-width: ${width}px; padding: 86px 96px 70px; break-after: page; page-break-after: always; }
.section { max-width: ${Math.round(width * 0.895)}px; padding: 62px 96px; border-top: 0; break-inside: auto; page-break-inside: auto; }
.section-heading { break-inside: avoid; break-after: avoid; page-break-inside: avoid; page-break-after: avoid; }
.section-kicker, h1, h2, h3, .subheading, .panel-heading, .river-header { break-after: avoid; page-break-after: avoid; }
.quality-card, .method-card, .trait-card, .evidence-card, .synthesis-card, .plan-card, .source-card, .story-card, .future-card, .fit-card, .chart-panel, .image-panel, .river-panel, figure, img, canvas, svg { break-inside: avoid; page-break-inside: avoid; }
.fit-grid { grid-template-columns: repeat(6, minmax(0, 1fr)); }
.river-svg-wrap { overflow: hidden; }
#lifeRiver { width: 100%; min-width: 0; height: auto; }
p, li, blockquote { orphans: 3; widows: 3; }
`;
}

async function main() {
  const args = parseArgs(process.argv);
  let playwright;
  try {
    playwright = loadPlaywright();
  } catch (error) {
    throw new Error("Could not load the 'playwright' package. Install it or run with NODE_PATH pointing to a node_modules directory that contains playwright.");
  }

  const executablePath = findChrome(args.chrome);
  const browser = await playwright.chromium.launch({
    headless: true,
    executablePath,
  });
  const page = await browser.newPage({
    viewport: { width: args.width, height: args.height },
    deviceScaleFactor: 1,
  });

  const errors = [];
  page.on("console", (msg) => {
    if (["error", "warning"].includes(msg.type())) errors.push(`${msg.type()}: ${msg.text()}`);
  });
  page.on("pageerror", (err) => errors.push(`pageerror: ${err.message}`));

  await page.goto(resolveInput(args.input), { waitUntil: "networkidle", timeout: 60000 });
  await page.emulateMedia({ media: "screen" });

  if (args.screenReport) {
    await page.addStyleTag({ content: screenReportCss(args.width, args.height) });
  }
  const cssFiles = [];
  if (args.css) cssFiles.push(path.resolve(args.css));
  if (!args.noLinuxFix && process.platform === "linux" && fs.existsSync(LINUX_PRINT_FIX_CSS)) {
    cssFiles.push(LINUX_PRINT_FIX_CSS);
  }
  for (const cssFile of cssFiles) {
    await page.addStyleTag({ content: fs.readFileSync(cssFile, "utf-8") });
  }

  await page.waitForFunction(
    () => [...document.images].every((img) => img.complete && img.naturalWidth > 0),
    null,
    { timeout: 30000 },
  ).catch(() => undefined);
  await page.waitForTimeout(500);

  const output = path.resolve(args.output);
  fs.mkdirSync(path.dirname(output), { recursive: true });
  await page.evaluate(() => document.fonts.ready).catch(() => undefined);
  await page.waitForTimeout(800);
  await page.pdf({
    path: output,
    width: `${args.width}px`,
    height: `${args.height}px`,
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: false,
  });
  await browser.close();

  console.log(JSON.stringify({
    output,
    width: args.width,
    height: args.height,
    consoleIssues: errors,
  }, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
