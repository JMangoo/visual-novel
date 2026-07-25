## 사운드 정의 ------------------------------------------------------
## 파일은 art/make_sounds.py 로 합성한 것(저작권 문제 없음).

# 채널: music(앰비언스) / sound(단발 효과음) / ambient(보조 루프)
init python:
    renpy.music.register_channel("ambient", "sfx", loop=True)

# 앰비언스
define audio.rain = "audio/rain_loop.wav"
define audio.basement = "audio/basement_loop.wav"
define audio.heartbeat = "audio/heartbeat_loop.wav"
define audio.ring = "audio/ring_loop.wav"

# 단발 효과음
define audio.msg = "audio/msg.wav"
define audio.paper = "audio/paper.wav"
define audio.doorlock = "audio/doorlock.wav"
define audio.stinger = "audio/stinger.wav"

# 기본 볼륨 — 앰비언스는 대사를 방해하지 않게 낮게.
define config.default_music_volume = 0.55
define config.default_sfx_volume = 0.75


## 편의 라벨 --------------------------------------------------------

# 빗소리 시작/정지 (장마철 내내 깔린다)
label rain_on:
    play music rain fadein 2.0 loop
    return

label rain_off:
    stop music fadeout 2.0
    return

# 지하실 앰비언스로 교체
label basement_on:
    play music basement fadein 3.0 loop
    return

# 심장박동 (긴장 고조 구간)
label heart_on:
    play ambient heartbeat fadein 1.0 loop
    return

label heart_off:
    stop ambient fadeout 1.5
    return
