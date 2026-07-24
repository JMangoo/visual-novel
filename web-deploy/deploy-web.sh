#!/usr/bin/env bash
# Ren'Py 웹 빌드 산출물을 coi-serviceworker 패치와 함께 GitHub Pages(gh-pages)로 배포.
#
# 사용법:
#   bash web-deploy/deploy-web.sh "<웹빌드폴더>"
# 예:
#   bash web-deploy/deploy-web.sh "/c/Users/jinwoo/Visual Novel/yeonyeok-1.0-dists/yeonyeok-1.0-web"
#
# 웹빌드폴더 = Ren'Py 런처 "배포본 빌드 > Web" 결과 폴더(index.html 포함).
set -euo pipefail

BUILD_DIR="${1:-}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE="https://github.com/JMangoo/visual-novel.git"
PAGES_URL="https://jmangoo.github.io/visual-novel/"

if [ -z "$BUILD_DIR" ] || [ ! -f "$BUILD_DIR/index.html" ]; then
  echo "오류: 웹 빌드 폴더(index.html 포함)를 인자로 주세요."
  echo "예: bash web-deploy/deploy-web.sh \"/c/Users/jinwoo/Visual Novel/yeonyeok-1.0-dists/yeonyeok-1.0-web\""
  exit 1
fi

STAGE="$(mktemp -d)"
echo "▶ 스테이징: $STAGE"
cp -r "$BUILD_DIR"/. "$STAGE"/
cp "$REPO_DIR/web-deploy/coi-serviceworker.js" "$STAGE/coi-serviceworker.js"
touch "$STAGE/.nojekyll"                       # Jekyll 처리 방지
rm -f "$STAGE/index.html.symbols"              # 배포에 불필요한 디버그 심볼 제거

echo "▶ index.html 패치 (coi-serviceworker 주입)"
python "$REPO_DIR/web-deploy/patch_index.py" "$STAGE/index.html"

echo "▶ gh-pages 로 강제 푸시"
cd "$STAGE"
git init -q
git checkout -q -b gh-pages
git config user.name "JMangoo"
git config user.email "kjw2546@gmail.com"
git add -A
git commit -q -m "deploy: 연역 web build ($(date -u +%FT%TZ))

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git remote add origin "$REMOTE"
git push -f origin gh-pages

echo "✅ 배포 완료: $PAGES_URL (반영까지 1~2분)"
