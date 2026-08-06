# Fahad Hussain — Portfolio

Single-page portfolio site. Static HTML/CSS/JS, no framework, no build step
for the site itself.

The site lives at the repo root because GitHub Pages' branch source
only serves `/` or `/docs`.

```
index.html               ← the site
styles.css
main.js
resume.pdf
assets/
  projects/*.jpg         ← generated, do not edit by hand
  img/fahad.png          ← generated
build-images.sh          ← regenerates assets/ from the sources
AppSpot Banners/         ← source images (gitignored)
Fahad Documents/         ← CV and personal documents (gitignored)
Initial_Instructions.md  ← the brief this was built from (gitignored)
```

`AppSpot Banners/` and `Fahad Documents/` are deliberately excluded —
the latter holds identity and financial records that must never reach
a public repo.

## Editing content

All copy lives in `index.html`. Project cards are plain `<article
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

Downscales every banner to 1600px, writes JPEGs into `assets/projects/`,
and copies the CV to `resume.pdf`. Sources are never modified.

The portrait stays PNG on purpose — its background is transparent, and JPEG
would flatten it to white.

## Local preview

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Deploying

Live at **https://faadi619.github.io/fahad_portfolio/**

Pages serves `main` at `/`, so any push to `main` publishes:

```bash
git add -A && git commit -m "Update content"
git push
```

`.nojekyll` is present so Jekyll doesn't touch the files.
