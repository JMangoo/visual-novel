## 모션(ATL) · 트랜지션 · 파티클 -------------------------------------

# 왼쪽에서 슬라이드 등장
transform slide_in_left:
    xpos -0.4 yalign 1.0 alpha 0.0
    easein 0.5 xpos 0.0 alpha 1.0

# 오른쪽에서 슬라이드 등장
transform slide_in_right:
    xpos 1.4 yalign 1.0 alpha 0.0
    easein 0.5 xpos 0.0 alpha 1.0

# 미세하게 숨쉬듯 흔들리는 idle 모션
transform idle_sway:
    block:
        linear 2.0 yoffset -6
        linear 2.0 yoffset 0
        repeat

# 놀람/충격 시 좌우 진동 (요소 단위)
transform shudder:
    block:
        linear 0.04 xoffset 8
        linear 0.04 xoffset -8
        linear 0.04 xoffset 0
        repeat 4

# 천천히 확대(줌 인) — 긴장 고조
transform slow_zoom:
    zoom 1.0
    linear 6.0 zoom 1.12

# 커스텀 페이드 트랜지션
define fade_slow = Fade(1.0, 0.5, 1.0)
define dissolve_slow = Dissolve(1.5)

# 파티클 — 에셋 없이 Text 글리프로 구현.
# 비: 얇은 세로선이 빠르게 수직 낙하.
image rain = SnowBlossom(
    Text("│", size=30, color="#9fb3c8"),
    count=100, border=40, xspeed=(0, 0), yspeed=(700, 1000), fast=True
)

# 눈: 천천히 흩날림.
image snow = SnowBlossom(
    Text("❄", size=22, color="#ffffff"),
    count=60, border=40, xspeed=(-20, 20), yspeed=(60, 140)
)
