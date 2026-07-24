#!/usr/bin/env python
"""Ren'Py 웹 빌드 index.html 패치.

GitHub Pages는 COOP/COEP 헤더를 못 붙이므로 Ren'Py 웹(SharedArrayBuffer 필요)이
회색 화면이 된다. coi-serviceworker.js 를 붙여 브라우저에서 cross-origin isolation을
켜고, Ren'Py 기본 서비스워커 등록은 꺼서 스코프 충돌을 막는다.

사용: python patch_index.py <배포폴더>/index.html
"""
import sys

def main(path):
    s = open(path, encoding="utf-8").read()

    # A. coi-serviceworker.js 를 <head> 최상단(charset 직후)에 삽입 (중복 방지)
    if "coi-serviceworker.js" not in s:
        s = s.replace(
            '<meta charset="utf-8">',
            '<meta charset="utf-8">\n'
            '  <!-- GitHub Pages COOP/COEP 우회: cross-origin isolation 활성화 -->\n'
            '  <script src="coi-serviceworker.js"></script>',
            1,
        )

    # B. Ren'Py 기본 캐시 서비스워커 등록 비활성화 (coi 가 스코프 단독 제어)
    s = s.replace(
        "navigator.serviceWorker.register('./service-worker.js', { updateViaCache: 'all' });",
        "/* Ren'Py 기본 SW 비활성화: coi-serviceworker 가 COOP/COEP 위해 스코프 제어 */",
    )

    open(path, "w", encoding="utf-8").write(s)
    print("patched:", path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python patch_index.py <path-to-index.html>")
        sys.exit(1)
    main(sys.argv[1])
