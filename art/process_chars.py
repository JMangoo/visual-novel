#!/usr/bin/env python
"""캐릭터 이미지 → 게임용 스프라이트.

AI로 뽑은 인물 이미지(단색 배경)에서 배경을 지우고, 배경 톤에 맞게 색을
맞춘 뒤 게임 크기로 저장한다.

사용법
  1) art/chars/ 에 캐릭터 이미지를 넣는다. 파일명이 게임에서 쓸 이름이 된다.
     예) char_neighbor.png, char_boss.png ...
  2) python art/process_chars.py
  3) yeonyeok/game/images/char/ 에 투명 png 로 저장된다.

배경 제거는 '가장자리에서 시작해 비슷한 색을 따라가며 지우는' 방식이라
인물 안쪽의 비슷한 색은 지워지지 않는다.
"""
import sys
from collections import deque
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "chars"
OUT = ROOT.parent / "yeonyeok" / "game" / "images" / "char"

TARGET_H = 980          # 1080 화면에서 인물 높이
TOLERANCE = 42          # 배경으로 볼 색 차이. 크게 하면 더 많이 지운다.


def remove_bg(img: Image.Image, tol: int = TOLERANCE) -> Image.Image:
    """가장자리에서 시작하는 flood fill 로 단색 배경만 지운다."""
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()

    # 네 모서리 색의 평균을 배경색으로 본다
    corners = [px[0, 0], px[w - 1, 0], px[0, h - 1], px[w - 1, h - 1]]
    bg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))

    def close(c):
        return (abs(c[0] - bg[0]) + abs(c[1] - bg[1]) + abs(c[2] - bg[2])) < tol * 3

    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if close(px[x, y]):
                q.append((x, y)); seen[y * w + x] = 1
    for y in range(h):
        for x in (0, w - 1):
            if close(px[x, y]):
                q.append((x, y)); seen[y * w + x] = 1

    while q:
        x, y = q.popleft()
        px[x, y] = (0, 0, 0, 0)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                if close(px[nx, ny]):
                    seen[ny * w + nx] = 1
                    q.append((nx, ny))

    return img


def trim(img: Image.Image) -> Image.Image:
    """투명 여백을 잘라낸다."""
    box = img.getbbox()
    return img.crop(box) if box else img


def match_tone(img: Image.Image) -> Image.Image:
    """배경(어둡고 푸르고 탈채도)과 톤을 맞춘다. 안 맞추면 인물만 붕 뜬다."""
    rgb = img.convert("RGB")
    rgb = ImageEnhance.Color(rgb).enhance(0.55)
    rgb = ImageEnhance.Brightness(rgb).enhance(0.78)
    r, g, b = rgb.split()
    r = r.point(lambda v: max(0, v - 8))
    b = b.point(lambda v: min(255, v + 10))
    rgb = Image.merge("RGB", (r, g, b))
    rgb = rgb.filter(ImageFilter.GaussianBlur(radius=0.4))
    out = rgb.convert("RGBA")
    out.putalpha(img.getchannel("A"))
    return out


def main():
    if not SRC.exists() or not any(SRC.iterdir()):
        SRC.mkdir(parents=True, exist_ok=True)
        print(f"{SRC} 에 캐릭터 이미지를 넣고 다시 실행하세요.")
        return

    files = [p for p in sorted(SRC.iterdir())
             if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}]
    if not files:
        print(f"{SRC} 에 이미지가 없습니다.")
        return

    OUT.mkdir(parents=True, exist_ok=True)
    for p in files:
        img = Image.open(p)
        img = remove_bg(img)
        img = trim(img)
        # 높이 기준으로 축소
        w, h = img.size
        scale = TARGET_H / h
        img = img.resize((int(w * scale), TARGET_H), Image.LANCZOS)
        img = match_tone(img)
        out = OUT / f"{p.stem}.png"
        img.save(out, "PNG")
        print(f"  {p.name:24} -> game/images/char/{out.name}  ({img.size[0]}x{img.size[1]})")

    print(f"\n{len(files)}장 변환 완료")


if __name__ == "__main__":
    main()
