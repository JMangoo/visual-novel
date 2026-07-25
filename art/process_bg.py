#!/usr/bin/env python
"""실사 사진 → 「연역」 배경으로 변환.

사진을 그대로 쓰면 캐릭터와 톤이 안 맞고 너무 밝다. 어둡게·탈채도·푸른 기운·
그레인·비네팅을 입혀 회화적인 야간 톤으로 만든다.

사용법
  1) art/raw/ 에 사진을 넣는다. 파일명 = 게임에서 쓸 배경 이름.
     예) room.jpg, store.jpg, hallway.jpg ...
  2) python art/process_bg.py
  3) yeonyeok/game/images/bg/ 에 1920x1080 png 로 저장된다.

옵션
  --preset night|indoor|rain   (기본 night)
"""
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageDraw

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
OUT = ROOT.parent / "yeonyeok" / "game" / "images" / "bg"
SIZE = (1920, 1080)

# 프리셋: (밝기, 채도, 대비, 푸른기, 그레인세기, 비네팅세기)
PRESETS = {
    # 야외 밤 · 비 — 가장 어둡고 푸르게
    "night":  dict(bright=0.42, sat=0.35, contrast=1.10, blue=26, grain=14, vignette=0.55),
    # 실내 — 조금 덜 어둡게(대사 가독성)
    "indoor": dict(bright=0.52, sat=0.40, contrast=1.05, blue=18, grain=11, vignette=0.45),
    # 형광등 아래(편의점 등) — 차갑고 창백하게
    "rain":   dict(bright=0.48, sat=0.30, contrast=1.15, blue=30, grain=16, vignette=0.60),
}


def fit_cover(img: Image.Image, size) -> Image.Image:
    """비율 유지하며 꽉 채우고 가운데를 자른다."""
    tw, th = size
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - tw) // 2, (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def add_blue(img: Image.Image, amount: int) -> Image.Image:
    """푸른 야간 색조. 빨강을 빼고 파랑을 더한다."""
    r, g, b = img.split()
    r = r.point(lambda v: max(0, v - amount))
    b = b.point(lambda v: min(255, v + amount))
    return Image.merge("RGB", (r, g, b))


def add_grain(img: Image.Image, strength: int) -> Image.Image:
    """필름 그레인. 사진 티를 지우고 회화적으로 만든다."""
    import random
    noise = Image.new("L", img.size)
    px = bytearray(img.size[0] * img.size[1])
    for i in range(len(px)):
        px[i] = 128 + random.randint(-strength, strength)
    noise.frombytes(bytes(px))
    noise = noise.convert("RGB")
    return Image.blend(img, noise, 0.10)


def add_vignette(img: Image.Image, strength: float) -> Image.Image:
    """가장자리를 어둡게. 시선을 가운데로 모으고 답답한 느낌을 준다."""
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    # 가운데를 밝게 두는 타원
    draw.ellipse((-w * 0.25, -h * 0.35, w * 1.25, h * 1.35), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=min(w, h) // 6))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    faded = Image.composite(img, dark, mask)
    return Image.blend(img, faded, strength)


def process(path: Path, preset: str) -> Image.Image:
    cfg = PRESETS[preset]
    img = Image.open(path).convert("RGB")
    img = fit_cover(img, SIZE)
    img = ImageEnhance.Color(img).enhance(cfg["sat"])
    img = ImageEnhance.Brightness(img).enhance(cfg["bright"])
    img = ImageEnhance.Contrast(img).enhance(cfg["contrast"])
    img = add_blue(img, cfg["blue"])
    img = add_grain(img, cfg["grain"])
    img = add_vignette(img, cfg["vignette"])
    # 살짝 흐리게 — 사진 특유의 선명함을 죽여 캐릭터와 붙게 만든다
    img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
    return img


def main():
    preset = "night"
    if "--preset" in sys.argv:
        preset = sys.argv[sys.argv.index("--preset") + 1]
    if preset not in PRESETS:
        print(f"알 수 없는 프리셋: {preset}. 가능: {', '.join(PRESETS)}")
        sys.exit(1)

    if not RAW.exists():
        RAW.mkdir(parents=True)
        print(f"{RAW} 를 만들었습니다. 여기에 사진을 넣고 다시 실행하세요.")
        return

    photos = [p for p in sorted(RAW.iterdir())
              if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
    if not photos:
        print(f"{RAW} 에 사진이 없습니다.")
        return

    OUT.mkdir(parents=True, exist_ok=True)
    for p in photos:
        out = OUT / f"{p.stem}.png"
        process(p, preset).save(out, "PNG")
        print(f"  {p.name}  ->  game/images/bg/{out.name}")

    print(f"\n{len(photos)}장 변환 완료 (프리셋: {preset})")


if __name__ == "__main__":
    main()
