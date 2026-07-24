## 3막 — 연역 + 결말 -------------------------------------------------
label act3:
    scene bg climax with fade_slow
    show snow
    "[임시대사] 모든 단서가 한 점으로 모인다. 나는 마침내 '유일하게 합리적인' 결론에 도달했다."
    me "이게 맞아. 이렇게 하는 게 유일한 답이야."
    hide snow

    # 주인공이 제 손으로 파국을 실행 (임시 처리)
    scene black with fade_slow
    "[임시대사] 나는 내 논리를 믿고, 내 손으로 그것을 실행했다."

    # 최후의 진실 CG — 언니의 정체
    scene cg_truth with dissolve_slow
    show screen phone_ui("언니")
    call pmsg("sister", "잘했어, [player_name].")
    hide screen phone_ui with dissolve
    killer "이제 알겠어? 네 언니는, 이 게임이 시작되기 전에 이미 죽었어."
    killer "넌 처음부터 나랑 문자하고, 나랑 통화한 거야. 얼굴 한 번 안 보고."
    killer "본질을 본다며. 네가 제일 사랑한 사람의 본질은, 끝까지 못 봤네."

    # 마무리
    scene black with fade_slow
    killer "1페이지에서 결말을 다 알려줬어, [player_name]. 그래도 넌 계속 읽었지."
    "[임시대사] (광기 수치: [madness]) — 이성과 사랑이, 서로를 죽였다."
    "── 끝 ──"
    return
