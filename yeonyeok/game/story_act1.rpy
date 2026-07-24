## 1막 — 예고 --------------------------------------------------------
label act1:
    scene bg room with fade_slow
    "(임시) 나는 감정에 휘둘리지 않는다. 모든 건 논리로 설명된다."
    me "이 세상에 내가 못 읽는 사건은 없어."

    # 첫 예고장
    show note at slide_in_right with dissolve_slow
    "(임시) 책상 위에, 오지 않아야 할 편지가 놓여 있다."
    killer "안녕. 나는 곧 사람을 죽일 거야. 시간도, 방법도 여기 적어뒀어."
    killer "그리고 넌 그걸 못 막아. 왜냐하면 넌 완벽하게 이성적이거든."
    hide note with dissolve

    # 언니와 문자 (플레이어는 상대가 살인마인 걸 모름)
    show screen phone_ui("언니")
    call pmsg("sister", "너 방금 그거 봤어? 나 취재 중인 사건이랑 똑같아.")
    call pmsg("me", "언니가 왜 이걸 알아?")
    call pmsg("sister", "기자잖아. 조심해. 나 곧 다시 연락할게.")
    hide screen phone_ui with dissolve

    # 첫 선택지 (모든 선택은 결국 파멸로 수렴; madness만 조정)
    menu:
        "예고장의 논리를 분석해 앞질러 간다":
            $ madness += 1
            "(임시) 나는 다음 수를 읽었다. 완벽하다고 믿었다."
        "무시하고 상대를 도발한다":
            $ madness += 2
            "(임시) 장난에 놀아나지 않겠다. 그렇게 생각했다."

    # 예고대로 살인 발생
    scene bg alley with fade_slow
    show rain
    "(임시) 예고된 시간, 예고된 장소. 내 대응은 전부 빗나갔다."
    killer "봤지? 난 네가 뭘 할지 이미 알고 있었어."
    hide rain

    # 미끼 용의자 등장
    scene bg store with dissolve
    show decoy_ph at slide_in_left
    show decoy_ph at idle_sway
    decoy "당신, 그 사건 쫓고 있죠? ...나도 관심 있는데."
    "(임시) 이 남자, 수상하다. 논리가 그를 가리킨다."

    jump act2
