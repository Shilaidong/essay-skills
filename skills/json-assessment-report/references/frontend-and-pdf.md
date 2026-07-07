# Frontend And PDF Reference

## Website Rules

- Build the report as the first screen. Do not make a marketing landing page.
- Use a calm product/report interface with readable density.
- Use cards only for discrete evidence blocks, charts, repeated items, and recommendations.
- Do not place cards inside cards.
- Keep chart labels readable and avoid overlap.
- Give every chart a caption explaining how to read it.
- Keep image and chart assets in the project folder.
- Do not show internal notes such as "fixed", "updated", "changed", or "data cleaned" in the student-facing report.

## Suggested Charts

- Radar/polygon chart for multi-dimensional scores.
- Bar chart for exact score values.
- Scatter/coordinate map for interest and ability fit.
- Timeline or river chart for life-story chapters and key moments.
- Small score cards for action readiness or learning fit.

Charts must reflect real data or clearly stated interpretive ratings. Generated illustrations should never masquerade as data.

## Landscape 1080P PDF

Use this when the user asks for:

- "horizontal", "landscape", "1080P", "screen view", "like my computer", or "do not split text and images".

Recommended settings:

- Browser viewport: 1920 x 1080.
- PDF page size: 1920px x 1080px.
- Media: screen, unless the page has a dedicated print stylesheet for landscape.
- Hide sticky navigation and footer if they create repeated clutter.
- Preserve desktop grids and two-column layouts.

Use `scripts/export_landscape_pdf.mjs`:

```bash
node scripts/export_landscape_pdf.mjs \
  --input ./index.html \
  --output ./report-1080p.pdf \
  --screen-report
```

If `playwright` is available in a bundled runtime but not in the local project, set `NODE_PATH` to that runtime's `node_modules`. The script also handles pnpm-style `.pnpm/node_modules` under that path.

If the page needs custom fixes, add a CSS file and pass `--css custom-print.css`.

## PDF QA

Check:

- Page size is 16:9.
- Text is selectable.
- Images are embedded in the PDF.
- Charts are nonblank.
- No chart or SVG is clipped.
- No section heading sits alone at the bottom of a page.
- No obvious empty page appears between content pages.
- The PDF does not contain forbidden wording or internal agent notes.

Use Poppler when available:

```bash
pdfinfo report-1080p.pdf
pdftoppm -png -r 72 -f 1 -l 4 report-1080p.pdf preview
```
