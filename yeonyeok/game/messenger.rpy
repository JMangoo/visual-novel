## 메신저 / 통화 UI ---------------------------------------------------

# 대화 로그: (발신자, 본문) 튜플 리스트. "me"=주인공, 그 외=상대.
default phone_log = []

# 메신저 화면
screen phone_ui(title="언니"):
    zorder 90
    # 어둡게 깔린 배경
    add Solid("#000000aa")
    frame:
        xalign 0.5 yalign 0.5
        xsize 620 ysize 860
        background Frame(Solid("#0b141a"), 12, 12)
        padding (14, 14)
        vbox:
            spacing 8
            # 헤더
            frame:
                xfill True
                background Solid("#14202a")
                padding (14, 10)
                text title color "#e7f0f5" size 30 bold True
            # 메시지 목록
            viewport:
                id "vp"
                xfill True yfill True
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 10
                    for who, body in phone_log:
                        if who == "me":
                            hbox:
                                xfill True
                                null width 120
                                frame:
                                    xalign 1.0
                                    background Frame(Solid("#2e6b4f"), 10, 10)
                                    padding (14, 10)
                                    text body color "#ffffff" size 26
                        else:
                            hbox:
                                xfill True
                                frame:
                                    xalign 0.0
                                    background Frame(Solid("#22303a"), 10, 10)
                                    padding (14, 10)
                                    text body color "#e7f0f5" size 26
                                null width 120

# 통화 착신 화면
screen call_ui(caller="언니"):
    zorder 95
    add Solid("#000000dd")
    vbox:
        xalign 0.5 yalign 0.35
        spacing 24
        text caller xalign 0.5 color "#c9a227" size 60 bold True
        text "통화 중..." xalign 0.5 color "#88aabb" size 30 at idle_sway

# 메시지 한 줄 출력 라벨 (클릭으로 넘어감)
label pmsg(who, body):
    $ phone_log.append((who, body))
    $ renpy.restart_interaction()
    pause
    return

# 대화 로그 초기화
label pclear:
    $ phone_log = []
    return
