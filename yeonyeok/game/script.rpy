# 「연역」 진입 흐름 ---------------------------------------------------
# 등장인물/변수는 characters.rpy, 시스템은 motion.rpy / messenger.rpy,
# 스토리는 story_act1~3.rpy 에 분리되어 있다.

# 여기에서부터 게임이 시작합니다.
label start:
    scene black
    # 아이폰 웹 대비: 가로 화면 권장 안내(PC에서도 무해).
    centered "{size=30}편안한 감상을 위해 기기를 가로로 눕히고,\n소리를 켜 주세요.{/size}"
    "당신은 감정을 신뢰하지 않는다. 오직 논리만이 세상을 설명한다고 믿는다."

    call ask_nickname

    jump act1
