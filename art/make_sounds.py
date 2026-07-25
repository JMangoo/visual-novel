#!/usr/bin/env python
"""「연역」 사운드 합성.

무료 음원을 받아오는 대신 직접 만든다. 저작권 문제가 없고, 게임 톤에 맞춰
어둡고 답답하게 조절할 수 있다.

사용: python art/make_sounds.py
결과: yeonyeok/game/audio/ 에 wav 파일들
"""
import math
import struct
import wave
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent / "yeonyeok" / "game" / "audio"
SR = 22050  # 앰비언스용으로 충분. 용량 절반.

rng = np.random.default_rng(20260726)


def save(name: str, data: np.ndarray, sr: int = SR):
    """-1.0~1.0 float 배열을 16bit wav로 저장."""
    data = np.clip(data, -1.0, 1.0)
    pcm = (data * 32767).astype(np.int16)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())
    kb = path.stat().st_size // 1024
    print(f"  {name}  ({kb} KB)")


def lowpass(x: np.ndarray, alpha: float) -> np.ndarray:
    """1차 IIR 저역통과. alpha가 작을수록 더 먹먹해진다."""
    out = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc += alpha * (v - acc)
        out[i] = acc
    return out


def highpass(x: np.ndarray, alpha: float) -> np.ndarray:
    return x - lowpass(x, alpha)


def loop_fade(x: np.ndarray, fade: int = 2000) -> np.ndarray:
    """앞뒤를 겹쳐 이어붙여도 티가 안 나게 만든다."""
    head = x[:fade].copy()
    tail = x[-fade:].copy()
    ramp = np.linspace(0, 1, fade)
    x[-fade:] = tail * (1 - ramp) + head * ramp
    return x[:-0] if fade == 0 else x


# ── 1. 빗소리 (메인 앰비언스, 루프) ──────────────────────────────
def rain(seconds=12.0):
    n = int(SR * seconds)
    # 굵은 빗줄기: 노이즈를 저역통과 → 먹먹한 쉭 소리
    base = lowpass(rng.normal(0, 1, n), 0.06) * 3.2
    # 잔빗방울: 고역 성분 살짝
    fine = highpass(rng.normal(0, 1, n), 0.35) * 0.10
    # 창문에 부딪히는 불규칙한 세기 변화
    env = 1.0 + 0.25 * lowpass(rng.normal(0, 1, n), 0.00012) * 6
    x = (base + fine) * env
    x *= 0.42
    return loop_fade(x)


# ── 2. 지하실 앰비언스 (낮은 웅웅거림 + 형광등) ─────────────────
def basement_hum(seconds=12.0):
    n = int(SR * seconds)
    t = np.arange(n) / SR
    # 건물 저주파
    drone = 0.16 * np.sin(2 * math.pi * 47 * t) + 0.10 * np.sin(2 * math.pi * 71.3 * t)
    # 형광등 60Hz 잡음
    buzz = 0.035 * np.sin(2 * math.pi * 120 * t) * (1 + 0.4 * np.sin(2 * math.pi * 0.7 * t))
    air = lowpass(rng.normal(0, 1, n), 0.02) * 0.9
    x = (drone + buzz + air) * 0.5
    return loop_fade(x)


# ── 3. 문자 알림음 ──────────────────────────────────────────────
def msg_beep():
    def tone(freq, dur, amp=0.5):
        t = np.linspace(0, dur, int(SR * dur), endpoint=False)
        env = np.exp(-t * 18)
        return amp * np.sin(2 * math.pi * freq * t) * env

    gap = np.zeros(int(SR * 0.05))
    x = np.concatenate([tone(1320, 0.10), gap, tone(1760, 0.16)])
    return x * 0.55


# ── 4. 전화 착신음 (루프) ───────────────────────────────────────
def phone_ring(seconds=4.0):
    n = int(SR * seconds)
    t = np.arange(n) / SR
    # 두 음이 섞인 전형적인 벨
    tone = 0.5 * np.sin(2 * math.pi * 440 * t) + 0.5 * np.sin(2 * math.pi * 480 * t)
    # 1초 울리고 1.2초 쉬는 패턴
    period = 2.2
    ph = (t % period)
    gate = np.where(ph < 1.0, 1.0, 0.0)
    gate = lowpass(gate, 0.02)
    return tone * gate * 0.30


# ── 5. 심장박동 (긴장 고조) ─────────────────────────────────────
def heartbeat(seconds=8.0, bpm=96):
    n = int(SR * seconds)
    x = np.zeros(n)
    beat = 60.0 / bpm

    def thump(length=0.16, f0=62.0):
        t = np.linspace(0, length, int(SR * length), endpoint=False)
        # 주파수가 살짝 떨어지며 '쿵'
        freq = f0 * np.exp(-t * 5)
        env = np.exp(-t * 16)
        return np.sin(2 * math.pi * freq * t) * env

    a, b = thump(0.18, 66), thump(0.13, 54) * 0.7
    pos = 0.0
    while pos < seconds - 0.5:
        i = int(pos * SR)
        x[i:i + len(a)] += a
        j = int((pos + 0.22) * SR)
        x[j:j + len(b)] += b
        pos += beat
    return loop_fade(x * 0.85)


# ── 6. 종이 스치는 소리 (예고장이 문틈으로) ────────────────────
def paper_slide():
    n = int(SR * 0.9)
    t = np.arange(n) / SR
    noise = highpass(rng.normal(0, 1, n), 0.5)
    env = np.exp(-((t - 0.35) ** 2) / 0.045)
    return noise * env * 0.30


# ── 7. 도어락 (삐빅) ────────────────────────────────────────────
def doorlock():
    def beep(freq, dur):
        t = np.linspace(0, dur, int(SR * dur), endpoint=False)
        return 0.4 * np.sign(np.sin(2 * math.pi * freq * t)) * np.exp(-t * 6)

    gap = np.zeros(int(SR * 0.06))
    return np.concatenate([beep(2100, 0.07), gap, beep(2100, 0.07)]) * 0.5


# ── 8. 긴장 스팅어 (충격 순간) ─────────────────────────────────
def stinger():
    dur = 2.0
    n = int(SR * dur)
    t = np.arange(n) / SR
    # 아래로 떨어지는 저주파 + 노이즈 충격
    freq = 220 * np.exp(-t * 2.2)
    tone = np.sin(2 * math.pi * np.cumsum(freq) / SR)
    hit = lowpass(rng.normal(0, 1, n), 0.15) * np.exp(-t * 9)
    env = np.exp(-t * 1.6)
    return (tone * 0.55 + hit * 0.5) * env * 0.8


def main():
    print("사운드 생성 중...")
    save("rain_loop.wav", rain())
    save("basement_loop.wav", basement_hum())
    save("msg.wav", msg_beep())
    save("ring_loop.wav", phone_ring())
    save("heartbeat_loop.wav", heartbeat())
    save("paper.wav", paper_slide())
    save("doorlock.wav", doorlock())
    save("stinger.wav", stinger())
    print(f"\n완료 → {OUT}")


if __name__ == "__main__":
    main()
