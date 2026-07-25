## 연출 장치 — 감시 시점 · 뉴스 · 통화 실패 · 예고장 · 회상 -----------

## 감시 시점 (CCTV/홈캠) -------------------------------------------
# 규칙: 정체를 절대 보여주지 않는다. 대사·설명 금지. 소름만 남긴다.

# 화면 거칠게 만드는 스캔라인(가로줄) 오버레이
image surveil_scanlines = Tile(Solid("#00000055", xsize=4, ysize=2))

# 미세하게 떨리는 손떨림/노이즈 모션
transform surveil_jitter:
    subpixel True
    block:
        linear 0.08 xoffset 1 yoffset 0
        linear 0.08 xoffset 0 yoffset 1
        linear 0.08 xoffset -1 yoffset 0
        linear 0.08 xoffset 0 yoffset 0
        repeat

# 감시 화면 오버레이(타임스탬프 + REC 표시)
screen surveil_overlay(stamp="2026-07-24 00:03:41", rec=True):
    zorder 100
    add "surveil_scanlines"
    # 비네팅(가장자리 어둡게) 대용
    add Solid("#00000033")
    text stamp:
        xalign 0.98 yalign 0.96
        size 28 color "#c8c8c8"
        font "DejaVuSans.ttf"
    if rec:
        hbox:
            xalign 0.03 yalign 0.96
            spacing 10
            text "●" size 30 color "#cc2222" at rec_blink
            text "REC" size 28 color "#c8c8c8"

# REC 점멸
transform rec_blink:
    block:
        linear 0.6 alpha 1.0
        linear 0.6 alpha 0.2
        repeat

# REC 표시만 단독으로. 감시 화면 전환 없이 '녹화 중'만 알린다.
# 3막에서 "나는 갔어"가 거짓임을 암시하는 용도. 주인공은 모르고 플레이어만 본다.
screen rec_only():
    zorder 100
    hbox:
        xalign 0.03 yalign 0.96
        spacing 10
        text "●" size 30 color "#cc2222" at rec_blink
        text "REC" size 28 color "#c8c8c8"

# 감시 시점 진입/이탈 (흑백 + 스캔라인 + 떨림)
label surveil_start(stamp="2026-07-24 00:03:41", rec=True):
    $ renpy.show_screen("surveil_overlay", stamp=stamp, rec=rec)
    show layer master at surveil_gray
    return

label surveil_end:
    hide screen surveil_overlay
    show layer master
    return

# 화면 전체를 흑백 + 살짝 떨리게
transform surveil_gray:
    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.15)
    subpixel True
    block:
        linear 0.09 xoffset 1
        linear 0.09 xoffset -1
        linear 0.09 xoffset 0
        repeat


## 뉴스 기사 화면 ---------------------------------------------------
screen news_article(headline="", body=""):
    zorder 80
    # 대사창(하단)을 가리지 않도록 상단 영역에만 깐다.
    add Solid("#000000cc") ysize 780
    frame:
        xalign 0.5 yalign 0.40
        xsize 1100
        background Frame(Solid("#f2f2ef"), 10, 10)
        padding (40, 34)
        vbox:
            spacing 20
            text "속보" size 26 color "#b03030" bold True
            text headline size 42 color "#141414" bold True
            add Solid("#cccccc", xsize=1020, ysize=2)
            text body size 28 color "#333333"


## 통화 시도 실패 (신호만 가고 끊김) --------------------------------
screen call_failed(caller="언니"):
    zorder 95
    add Solid("#000000dd") ysize 780
    vbox:
        xalign 0.5 yalign 0.30
        spacing 24
        text caller xalign 0.5 color "#c9a227" size 60 bold True
        text "발신 중..." xalign 0.5 color "#88aabb" size 30 at idle_sway


## 예고장(문서) 표시 ------------------------------------------------
# 본문은 killer 캐릭터 대사로 출력하고, 이 화면은 종이 배경 역할.
screen notice_paper():
    zorder 70
    add Solid("#00000099")
    frame:
        xalign 0.5 yalign 0.5
        xsize 900 ysize 700
        background Frame(Solid("#e8e4d8"), 8, 8)
        padding (40, 40)
        text "" size 1


## 회상 컷 ---------------------------------------------------------
# clear=True  → 선명하게(들어준 경우)
# clear=False → 흐릿한 실루엣(무시한 경우)
transform recall_clear:
    matrixcolor SaturationMatrix(0.35) * BrightnessMatrix(-0.05)
    zoom 1.02

transform recall_blur:
    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.35)
    alpha 0.55
    zoom 1.02

label recall_start(clear=False):
    if clear:
        show layer master at recall_clear
    else:
        show layer master at recall_blur
    return

label recall_end:
    show layer master
    return
