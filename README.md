# Fahad Hussain — Portfolio

Single-page portfolio site. Static HTML/CSS/JS, no framework, no build step
for the site itself.

```
site/                    ← everything that gets deployed
  index.html
  styles.css
  main.js
  resume.pdf
  assets/
    projects/*.jpg       ← generated, do not edit by hand
    img/fahad.png        ← generated
AppSpot Banners/         ← source images (not deployed)
Fahad Documents/         ← CV and source material (not deployed)
build-images.sh          ← regenerates site/assets from the sources
Initial_Instructions.md  ← the brief this was built from
```

## Editing content

All copy lives in `site/index.html`. Project cards are plain `<article
class="card">` blocks — copy one to add a project.

Every card carries an authorship line. Keep it accurate:

```html
<span class="authorship__built">Built end-to-end</span>
<span class="authorship__led">… directed — built by the engineering team</span>
```

## Regenerating images

After replacing anything in `AppSpot Banners/` or swapping the CV:

```bash
./build-images.sh
```

Downscales every banner to 1600px, writes JPEGs into `site/assets/projects/`,
and copies the CV to `site/resume.pdf`. Sources are never modified.

The portrait stays PNG on purpose — its background is transparent, and JPEG
would flatten it to white.

## Local preview

```bash
cd site && python3 -m http.server 8000
```

Then open http://localhost:8000.

## Deploying to GitHub Pages

See the "Deploy" section of the handover notes, or:

```bash
git init && git add -A && git commit -m "Portfolio site"
git branch -M main
git remote add origin https://github.com/faadi619/<repo>.git
git push -u origin main
```

Then in the repo: **Settings → Pages → Source: Deploy from a branch →
Branch: `main`, folder: `/site`** → Save.

`.nojekyll` is present so Jekyll doesn't touch the files.
