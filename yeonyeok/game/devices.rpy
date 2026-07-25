## 연출 장치 — 감시 시점 · 뉴스 · 통화 실패 · 예고장 · 회상 -----------

## 햅틱(진동) ------------------------------------------------------
# 웹에서만 동작한다. 안드로이드 크롬은 지원, iOS 사파리는 진동 API를 막아둬서
# 아무 일도 일어나지 않는다. 지원 안 되면 조용히 넘어가므로 넣어둬도 무해하다.
init python:
    def buzz(ms=60):
        try:
            if renpy.emscripten:
                import emscripten
                emscripten.run_script(
                    "if (navigator.vibrate) { navigator.vibrate(%d); }" % ms
                )
        except Exception:
            pass  # 지원 안 하는 환경에서는 그냥 무시


## 감시 시점 (CCTV/홈캠) -------------------------------------------
# 규칙: 정체를 절대 보여주지 않는다. 대사·설명 금지. 소름만 남긴다.

# 스캔라인.
# 예전엔 Tile(Solid(4x2)) 로 깔았는데, 1920x1080 이면 타일이 26만 개라
# 매 프레임 그 수만큼 그려야 해서 아이폰이 멈췄다. 미리 구운 PNG 한 장으로 대체.
image surveil_scanlines = "images/scanlines.png"

# 감시 화면 오버레이(타임스탬프 + REC 표시)
# 모바일에서 멈추지 않도록 최대한 단순하게 유지한다.
# 폰트는 지정하지 않는다(게임 기본 폰트 사용) — 웹에서 폰트 로딩이 걸릴 수 있어서.
screen surveil_overlay(stamp="2026-07-24 00:03:41", rec=True):
    zorder 100
    add "surveil_scanlines"
    add Solid("#00000033")
    text stamp xalign 0.98 yalign 0.96 size 28 color "#c8c8c8"
    if rec:
        hbox:
            xalign 0.03 yalign 0.96
            spacing 10
            text "●" size 30 color "#cc2222" at rec_blink
            text "REC" size 28 color "#c8c8c8"

# REC 점멸. 한 요소에만 걸리는 가벼운 애니메이션.
transform rec_blink:
    block:
        linear 0.7 alpha 1.0
        linear 0.7 alpha 0.25
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

# 감시 시점 진입/이탈
#
# 예전에는 `show layer master at surveil_gray` 로 화면 전체에 matrixcolor 를
# 걸고 무한 떨림까지 돌렸다. PC에서는 돌아갔지만 아이폰 사파리에서는 매 프레임
# 전체 화면을 셰이더로 재합성하느라 그대로 멈춰버렸다.
# 그래서 흑백 처리는 미리 만들어둔 *_cam.jpg 로 대체하고(런타임 비용 0),
# 이 라벨은 오버레이만 켜고 끈다.
label surveil_start(stamp="2026-07-24 00:03:41", rec=True):
    $ renpy.show_screen("surveil_overlay", stamp=stamp, rec=rec)
    return

label surveil_end:
    hide screen surveil_overlay
    return


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
# clear=True  → 선명하게(들어준 경우) / clear=False → 흐릿하게(무시한 경우)
#
# 감시 연출과 같은 이유로 matrixcolor + show layer master 를 걷어냈다.
# 대신 반투명 막을 덮어 '기억이 흐리다'를 표현한다. 모바일에서도 가볍다.
screen recall_veil(clear=False):
    zorder 85
    if clear:
        add Solid("#0a0c1044")
    else:
        add Solid("#0a0c10bb")

label recall_start(clear=False):
    $ renpy.show_screen("recall_veil", clear=clear)
    return

label recall_end:
    hide screen recall_veil
    return
