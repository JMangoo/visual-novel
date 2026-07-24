## 등장인물 및 전역 변수 정의 -------------------------------------------

# 플레이어 닉네임 (기본값). 게임 시작 시 입력받아 덮어씀.
default player_name = "이름 없음"

# 광기 수치 — 선택에 따라 오르내리며 '파멸의 색'을 결정(뼈대 단계에선 값만 추적).
default madness = 0

# 캐릭터 정의
# 주인공 대사는 화자 이름 없이 나레이션/독백 위주로 처리하되, 필요시 me 사용.
define me = Character("나", color="#cccccc")

# 살인마: 이름을 숨긴 채 등장. 정체 공개 전까지 '???' 로 표기.
define killer = Character("???", color="#8b0000")

# 미끼 용의자
define decoy = Character("수상한 남자", color="#6a8caf")

# 언니: 문자/통화로만 등장하므로 일반 대사창 대신 메신저 UI를 사용(messenger.rpy).
# 필요 시 통화 음성 표기용 캐릭터.
define sister_voice = Character("언니", color="#c9a227")


# 닉네임 입력 라벨 -----------------------------------------------------
# 아이폰 웹에서는 renpy.input() 키보드가 불안정할 수 있어, '직접 입력'과
# '프리셋 선택' 두 경로를 모두 제공한다(폴백 안전장치).
label ask_nickname:
    scene black
    "..."
    menu:
        "이름을 직접 입력한다":
            $ raw = renpy.input("당신을 뭐라고 부를까?", default="", length=12).strip()
            if raw == "":
                call screen preset_names
                $ player_name = _return
            else:
                $ player_name = raw
        "제시된 이름 중에 고른다":
            call screen preset_names
            $ player_name = _return
    "그래, [player_name]."
    return

# 프리셋 이름 선택 스크린 (키보드 없이도 진행 가능)
screen preset_names():
    modal True
    add Solid("#000000cc")
    frame:
        xalign 0.5 yalign 0.5
        padding (30, 24)
        background Frame(Solid("#14141c"), 12, 12)
        vbox:
            spacing 14
            text "이름을 선택해." size 28 color "#e0e0e0" xalign 0.5
            textbutton "서리" action Return("서리") xalign 0.5
            textbutton "재이" action Return("재이") xalign 0.5
            textbutton "무명" action Return("무명") xalign 0.5
            textbutton "K"   action Return("K")   xalign 0.5
