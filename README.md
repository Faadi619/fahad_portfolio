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

After replacing anything in `AppSpot Banners/`:

```bash
./build-images.sh
```

Downscales every banner to 1600px, writes JPEGs into `assets/projects/`,
and copies the Client CV to `resume.pdf`. Sources are never modified.

The portrait stays PNG on purpose — its background is transparent, and JPEG
would flatten it to white.

## Updating the résumé

`resume.pdf` is the Client version of the CV. Both CV versions (Full and
Client) come from one source, `../Vision 2030/Documents/cv/cv.html`.
Edit that file, then run:

```bash
"../Vision 2030/Documents/cv/build.sh"
```

It renders both PDFs into `../Vision 2030/Documents/`, refuses to continue
if the Client version runs past 2 pages, and copies it here as `resume.pdf`.

## Local preview

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Deploying

Live at **https://fahadhussain.dev/**

Pages serves `main` at `/`, so any push to `main` publishes:

```bash
git add -A && git commit -m "Update content"
git push
```

`.nojekyll` is present so Jekyll doesn't touch the files.
`CNAME` holds the custom domain (`fahadhussain.dev`). Keep it at the repo root,
or Pages drops the domain.
