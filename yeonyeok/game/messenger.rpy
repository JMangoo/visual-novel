## 메신저 / 통화 UI ---------------------------------------------------

# 대화 로그: (발신자, 본문) 튜플 리스트. "me"=주인공, 그 외=상대.
default phone_log = []

# 메신저 화면
screen phone_ui(title="언니"):
    zorder 90
    # 어둡게 깔린 배경 — 대사창을 가리지 않도록 상단 영역에만.
    add Solid("#000000aa") ysize 780
    frame:
        xalign 0.5 yalign 0.42
        xsize 620 ysize 720
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
            # 메시지 목록 — 최근 것만 보여준다.
            # 스크롤을 직접 내리지 않아도 늘 최신 메시지가 보이게 하기 위함.
            viewport:
                id "vp"
                xfill True yfill True
                mousewheel True
                vbox:
                    spacing 10
                    # body 가 "img:이미지이름" 이면 사진 말풍선으로 그린다.
                    for who, body in phone_log[-8:]:
                        $ is_img = body.startswith("img:")
                        if who == "me":
                            hbox:
                                xfill True
                                null width 120
                                frame:
                                    xalign 1.0
                                    background Frame(Solid("#2e6b4f"), 10, 10)
                                    padding ((8, 8) if is_img else (14, 10))
                                    if is_img:
                                        add body[4:] xysize (300, 190)
                                    else:
                                        text body color "#ffffff" size 26
                        else:
                            hbox:
                                xfill True
                                frame:
                                    xalign 0.0
                                    background Frame(Solid("#22303a"), 10, 10)
                                    padding ((8, 8) if is_img else (14, 10))
                                    if is_img:
                                        add body[4:] xysize (300, 190)
                                    else:
                                        text body color "#e7f0f5" size 26
                                null width 120

# 통화 착신 화면
# 주의: 어두운 배경은 대사창 위 영역(상단 72%)에만 깐다.
# 화면 전체를 덮으면 대사가 안 읽힌다.
screen call_ui(caller="언니"):
    zorder 95
    add Solid("#000000dd") ysize 780
    vbox:
        xalign 0.5 yalign 0.30
        spacing 24
        text caller xalign 0.5 color "#c9a227" size 60 bold True
        text "통화 중..." xalign 0.5 color "#88aabb" size 30 at idle_sway

# 메시지 한 줄 출력 라벨 (클릭으로 넘어감)
# 상대가 보낸 메시지에만 알림음. 내가 보낸 건 조용히.
label pmsg(who, body):
    $ phone_log.append((who, body))
    if who != "me":
        play sound msg
    $ renpy.restart_interaction()
    pause
    return

# 대화 로그 초기화
label pclear:
    $ phone_log = []
    return
