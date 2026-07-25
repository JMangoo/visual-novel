## 임시 이미지 정의 (실제 아트로 교체 예정) ----------------------------

# 배경 — 실사 사진에 필터를 입힌 것. 원본은 art/raw/, 변환은 art/process_bg.py
image bg room     = "images/bg/room.jpg"        # 703호 주인공의 집
image bg hallway  = "images/bg/hallway.jpg"     # 7층 복도
image bg alley    = "images/bg/alley.jpg"       # 골목/빌라 앞
image bg store    = "images/bg/store.jpg"       # 편의점
image black       = Solid("#000000")

image bg elevator = "images/bg/elevator.jpg"    # 아파트 1층 엘리베이터 앞
image bg guard    = "images/bg/guard.jpg"       # 1층 경비실
image bg shops    = "images/bg/shops.jpg"       # 삼거리 상가
image bg villa    = "images/bg/villa.jpg"       # 빌라 복도/계단
image bg backyard = "images/bg/backyard.jpg"    # 빌라 뒤편

image bg stairsdown = "images/bg/stairsdown.jpg"  # 지하로 내려가는 계단
image bg basement   = "images/bg/basement.jpg"    # 지하 2층 작업실
image bg morning    = "images/bg/morning.jpg"     # 비 그친 아침 거리

image bg empty704 = "images/bg/empty704.jpg"   # 텅 빈 704호
image bg climax   = "images/bg/basement.jpg"   # 구 스켈레톤 호환

# 최후의 진실 CG — 역광 실루엣
image cg_truth = "images/bg/cg_sister.jpg"

# 예고장(문서)
image note = "images/bg/note.jpg"


## 캐릭터 스프라이트 ------------------------------------------------
## 원본 art/chars/, 변환 art/process_chars.py (rembg로 배경 제거)
image nb_normal = "images/char/char_neighbor.png"    # 이웃A 평상시
image nb_true   = "images/char/char_neighbor_x.png"  # 이웃A 정체 공개
image park_ch   = "images/char/char_park.png"        # 박 사장
image nurse_ch  = "images/char/char_nurse.png"       # 윤미경
image boss_ch   = "images/char/char_boss.png"        # 편의점 사장
image guard_ch  = "images/char/char_guard.png"       # 경비원
image clerk_ch  = "images/char/char_clerk.png"       # 알바생

# 구 스켈레톤 호환
image decoy_ph = "images/char/char_clerk.png"
image killer_ph = "images/char/char_neighbor_x.png"
