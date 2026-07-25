## 모션(ATL) · 트랜지션 · 파티클 -------------------------------------

## 캐릭터 배치 ------------------------------------------------------
# 스프라이트는 높이 980px. 화면 아래에 발이 닿게 세운다.
transform stand_c:
    xalign 0.5 yalign 1.0
    alpha 0.0
    easein 0.4 alpha 1.0

transform stand_l:
    xalign 0.26 yalign 1.0
    alpha 0.0
    easein 0.4 alpha 1.0

transform stand_r:
    xalign 0.74 yalign 1.0
    alpha 0.0
    easein 0.4 alpha 1.0

# 가까이 다가온 느낌 (3막 대면)
transform stand_close:
    xalign 0.5 yalign 1.0
    zoom 1.18
    alpha 0.0
    easein 0.6 alpha 1.0


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

# 파티클 — 문자(│, ❄)를 쓰면 폰트에 글리프가 없어 네모(두부)로 표시된다.
# 그래서 Solid 도형으로 만든다.

# 비: 얇고 긴 세로선이 빠르게 수직 낙하.
image rain = SnowBlossom(
    Solid("#9fb3c8aa", xsize=2, ysize=26),
    count=110, border=40, xspeed=(0, 0), yspeed=(760, 1050), fast=True
)

# 빗줄기가 굵을 때(살인 장면 등)
image rain_hard = SnowBlossom(
    Solid("#aebfd0cc", xsize=3, ysize=34),
    count=170, border=40, xspeed=(-30, 0), yspeed=(900, 1250), fast=True
)

# 눈: 작은 점이 천천히 흩날림.
image snow = SnowBlossom(
    Solid("#ffffffcc", xsize=5, ysize=5),
    count=60, border=40, xspeed=(-20, 20), yspeed=(60, 140)
)
