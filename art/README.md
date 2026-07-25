# 배경 사진 준비 가이드

실사 사진을 받아 필터를 입혀 게임 배경으로 쓴다.

## 순서
1. 아래 목록대로 사진을 구한다
2. **`art/raw/`** 폴더에 넣는다 — **파일명을 반드시 지정된 이름으로** (예: `room.jpg`)
3. Claude에게 "사진 넣었어"라고 말하면 변환 + 게임 적용

## 어디서 구하나 (전부 무료 · 상업이용 가능 · 출처표기 불필요)
- **Unsplash** https://unsplash.com — 가장 추천. 도시·밤·비 사진이 많고 감성적
- **Pexels** https://pexels.com
- **Pixabay** https://pixabay.com

> 검색은 **영어로** 하는 게 결과가 훨씬 많다. 한국 배경이 아니어도 괜찮다 —
> 어차피 어둡게 필터링하면 국적이 잘 안 드러나고, 밤·비 분위기가 더 중요하다.

## 고를 때 기준
- **가로가 긴 사진**(16:9에 가깝게). 세로 사진은 잘린다
- **사람이 없는 것**. 있으면 시선을 뺏긴다
- **밤/흐림/비**가 이미 찍힌 것이면 최상
- 너무 밝고 화창한 사진은 피한다 (필터를 먹여도 티가 난다)
- 해상도는 클수록 좋다 (최소 가로 1920px)

---

## 필요한 사진 11장

| 파일명 | 장면 | 검색어 (영어) |
|---|---|---|
| `room.jpg` | 주인공의 집 703호 · 좁은 원룸, 밤 | `small apartment room night desk`<br>`studio apartment interior dark` |
| `hallway.jpg` | 아파트 7층 복도 | `apartment corridor night`<br>`hallway dim fluorescent` |
| `elevator.jpg` | 아파트 1층 엘리베이터 앞 | `elevator lobby night`<br>`apartment entrance hall` |
| `guard.jpg` | 1층 경비실 | `security guard booth night`<br>`small office window night` |
| `store.jpg` | 편의점 (야간) | `convenience store night rain`<br>`konbini interior night` |
| `alley.jpg` | 비 오는 골목 | `dark alley rain night`<br>`wet alley neon` |
| `villa.jpg` | 낡은 빌라 복도/계단 | `old apartment stairwell`<br>`concrete stairway dim` |
| `backyard.jpg` | 빌라 뒤편 (시멘트 바닥) | `back alley concrete ground night`<br>`wet pavement night` |
| `shops.jpg` | 삼거리 상가 (셔터 내린) | `closed shutter shops street night`<br>`empty street storefront night` |
| `stairsdown.jpg` | 지하로 내려가는 계단 | `basement stairs dark`<br>`underground stairway concrete` |
| `basement.jpg` | 지하 작업실 (창고) | `abandoned basement room`<br>`empty warehouse dark concrete` |
| `morning.jpg` | 비 그친 아침 거리 | `city street morning after rain`<br>`empty street dawn` |

> 12장이지만 `morning.jpg`은 마지막 한 장면에만 나오므로 급하지 않다.

## 우선순위
급하면 이 5장만 먼저 구해도 게임의 80%가 채워진다:
1. `room.jpg` (가장 많이 나옴)
2. `store.jpg`
3. `hallway.jpg`
4. `alley.jpg`
5. `basement.jpg` (클라이맥스)

---

## 필터 직접 돌리기
```bash
python art/process_bg.py --preset indoor    # 실내
python art/process_bg.py --preset night     # 야외 밤
python art/process_bg.py --preset rain      # 형광등 아래(편의점 등)
```
결과는 `yeonyeok/game/images/bg/` 에 1920x1080 png로 저장된다.
