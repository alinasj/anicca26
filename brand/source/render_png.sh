#!/bin/zsh
# Render PNGs from the exported SVGs with headless Chrome (transparent background).
# Usage: ./render_png.sh   (run from brand/source)
set -e
cd "$(dirname "$0")/.."
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP=$(mktemp -d)
render() { # svg out w h [bg]
  local bg=${5:-transparent}
  print "<html><body style='margin:0;background:$bg'><img src='file://$PWD/$1' width='$3' height='$4' style='display:block'></body></html>" > $TMP/p.html
  "$CH" --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files \
    --default-background-color=00000000 --window-size=$3,$4 --screenshot="$PWD/$2" "file://$TMP/p.html" >/dev/null 2>&1
  echo "rendered $2"
}
mkdir -p logo/png
render logo/anicca26-app-icon.svg logo/png/anicca26-app-icon-1024.png 1024 1024
render logo/anicca26-app-icon.svg logo/png/anicca26-app-icon-512.png 512 512
render logo/anicca26-app-icon.svg ../docs/assets/img/apple-touch-icon.png 180 180
render logo/anicca26-app-icon.svg ../docs/assets/img/icon-512.png 512 512
render logo/anicca26-app-icon.svg ../docs/assets/img/icon-192.png 192 192
render logo/anicca26-favicon.svg ../docs/assets/img/favicon-32.png 32 32
render logo/anicca26-favicon.svg logo/png/anicca26-favicon-32.png 32 32
render logo/anicca26-favicon.svg logo/png/anicca26-favicon-16.png 16 16
for v in on-dark on-light; do
  render logo/anicca26-mark-$v.svg logo/png/anicca26-mark-$v-512.png 512 512
  W=$(grep -o 'width="[0-9]*"' logo/anicca26-lockup-$v.svg | head -1 | tr -dc 0-9)
  render logo/anicca26-lockup-$v.svg logo/png/anicca26-lockup-$v@4x.png $((W*4)) 256
  W=$(grep -o 'width="[0-9]*"' logo/anicca26-stacked-$v.svg | head -1 | tr -dc 0-9)
  H=$(grep -o 'height="[0-9]*"' logo/anicca26-stacked-$v.svg | head -1 | tr -dc 0-9)
  render logo/anicca26-stacked-$v.svg logo/png/anicca26-stacked-$v@4x.png $((W*4)) $((H*4))
done
rm -rf $TMP
