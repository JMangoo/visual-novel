## 2막 — 균열 --------------------------------------------------------
label act2:
    scene bg hallway with fade_slow
    "[임시대사] 예고, 살인, 반복. 나는 앞서가려 했지만 매번 반 발짝 늦었다."

    # 일부러 비합리적으로 굴어본다
    menu:
        "예측을 벗어나려 일부러 엉뚱하게 행동한다":
            $ madness += 2
            "[임시대사] 아무도 예상 못 할 선택. 그렇게 믿었다."
        "냉정하게 다시 논리로 파고든다":
            $ madness += 1
            "[임시대사] 감정을 배제하면 답이 보인다. 그렇게 믿었다."

    # 그 선택마저 예고장에 있었다
    show note at slide_in_right with dissolve_slow
    killer "3페이지 봤어? 네가 방금 한 그 행동, 거기 적어놨는데."
    hide note with dissolve
    scene bg hallway at slow_zoom
    show screen call_ui("???")
    "[임시대사] 심장이 뛴다. 내 생각 중에, 대체 뭐가 내 것이지?"
    hide screen call_ui with dissolve

    # 살인마가 처음으로 플레이어 이름을 부른다 (공포 장치)
    killer "너무 애쓰지 마, [player_name]."
    "[임시대사] ...방금, 저 이름을 어떻게 알았지? 아무한테도 말한 적 없는데."

    # 언니 문자의 미세한 균열 (공정한 단서)
    show screen phone_ui("언니")
    call pmsg("sister", "괜찮아? 너 지금 표정 안 좋아 보여.")
    call pmsg("me", "...언니, 지금 내 표정을 어떻게 봐?")
    call pmsg("sister", "그냥. 느낌이 그래. 얼른 집에 가.")
    hide screen phone_ui with dissolve
    "[임시대사] 뭔가 어긋나 있다. 하지만 나는 저 수상한 남자를 쫓느라, 그 어긋남을 지나쳤다."

    jump act3
