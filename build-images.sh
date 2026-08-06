#!/bin/bash
# Downscale source banners into web-ready assets.
# Sources stay untouched in "AppSpot Banners/" and "Fahad Documents/".
# Re-run after replacing any source image.
set -euo pipefail
cd "$(dirname "$0")"

B="AppSpot Banners"
D="Fahad Documents"
OUT="assets/projects"
IMG="assets/img"
mkdir -p "$OUT" "$IMG"

# banner <source-file> <output-slug>
banner() {
  sips -s format jpeg -s formatOptions 82 "$B/$1" --resampleWidth 1600 --out "$OUT/$2.jpg" >/dev/null
  printf '  %-22s %s\n' "$2.jpg" "$(du -h "$OUT/$2.jpg" | cut -f1)"
}

echo "Project banners →  $OUT"
banner "Wgoodi App Banner.png"       wgoodi
banner "GroundView Pro Cover.png"    groundview
banner "Powermate App Banner.png"    powermate
banner "Vaqt Cover 1.png"            vaqt
banner "MEPA App Banner.png"         mepa
banner "Addi Buddy banner.png"       addibuddy
banner "4Drivers App Banner.png"     fourdrivers
banner "Frienvite App Banner.png"    frienvite
banner "Referral App Banner.png"     referral
banner "InspectStore App Banner.png" inspectstore
banner "CMedia App Banner.png"       cmedia
banner "EDU Gigs App Banner.png"     edugigs

echo "Portrait →  $IMG"
# Stays PNG: the source has a removed (transparent) background, and
# flattening to JPEG would paint it solid white. The page sits the
# cutout on a gradient, so transparency has to survive.
sips -s format png "$D/Fahad_Image-removebg.png" \
  --resampleWidth 800 --out "$IMG/fahad.png" >/dev/null
printf '  %-22s %s\n' "fahad.png" "$(du -h "$IMG/fahad.png" | cut -f1)"

echo "Resume →  ./"
cp "$D/Fahad_Hussain_CV.pdf" resume.pdf
printf '  %-22s %s\n' "resume.pdf" "$(du -h resume.pdf | cut -f1)"

echo
echo "Total: $(du -sh assets | cut -f1)"
