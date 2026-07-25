## 임시 이미지 정의 (실제 아트로 교체 예정) ----------------------------

# 배경 — 실사 사진에 필터를 입힌 것. 원본은 art/raw/, 변환은 art/process_bg.py
image bg room     = "images/bg/room.png"        # 703호 주인공의 집
image bg hallway  = "images/bg/hallway.png"     # 7층 복도
image bg alley    = "images/bg/alley.png"       # 골목/빌라 앞
image bg store    = "images/bg/store.png"       # 편의점
image black       = Solid("#000000")

image bg elevator = "images/bg/elevator.png"    # 아파트 1층 엘리베이터 앞
image bg guard    = "images/bg/guard.png"       # 1층 경비실
image bg shops    = "images/bg/shops.png"       # 삼거리 상가
image bg villa    = "images/bg/villa.png"       # 빌라 복도/계단
image bg backyard = "images/bg/backyard.png"    # 빌라 뒤편

image bg stairsdown = "images/bg/stairsdown.png"  # 지하로 내려가는 계단
image bg basement   = "images/bg/basement.png"    # 지하 2층 작업실
image bg morning    = "images/bg/morning.png"     # 비 그친 아침 거리

# 아직 사진이 없는 것
image bg empty704 = Solid("#131316")   # 텅 빈 704호 (복도 사진으로 대체 가능)
image bg climax   = "images/bg/basement.png"   # 구 스켈레톤 호환

# 캐릭터 — 내장 Placeholder 실루엣.
image decoy_ph = Placeholder("boy")

# 살인마 — 가려진 형상. 어두운 실루엣으로 대체.
image killer_ph = Placeholder("bg")

# 최후의 진실 CG 자리표시.
image cg_truth = Solid("#2a0000")

# 예고장(문서) 자리표시.
image note = Solid("#e8e4d8")
