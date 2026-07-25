## 임시 이미지 정의 (실제 아트로 교체 예정) ----------------------------

# 배경 — Solid 색으로 대체, 라벨은 장면에서 텍스트로 안내.
image bg room     = Solid("#141420")   # 703호 주인공의 집
image bg hallway  = Solid("#101014")   # 7층 복도
image bg alley    = Solid("#0c0f14")   # 골목/빌라 앞
image bg store    = Solid("#161a12")   # 편의점
image bg climax   = Solid("#1a0a0a")   # 작업실(3막)
image black       = Solid("#000000")

# 1막 추가 배경
image bg elevator = Solid("#12141a")   # 아파트 1층 엘리베이터 앞
image bg guard    = Solid("#15161a")   # 1층 경비실
image bg shops    = Solid("#181410")   # 삼거리 상가
image bg villa    = Solid("#0e1014")   # 박정호의 빌라(복도/실내)
image bg backyard = Solid("#0a0c10")   # 빌라 뒤편

# 3막 추가 배경
image bg stairsdown = Solid("#08090c")  # 지하로 내려가는 계단
image bg basement   = Solid("#0b0a0c")  # 지하 2층 작업실
image bg empty704   = Solid("#131316")  # 텅 빈 704호
image bg morning    = Solid("#2a2c33")  # 비 그친 아침 거리

# 캐릭터 — 내장 Placeholder 실루엣.
image decoy_ph = Placeholder("boy")

# 살인마 — 가려진 형상. 어두운 실루엣으로 대체.
image killer_ph = Placeholder("bg")

# 최후의 진실 CG 자리표시.
image cg_truth = Solid("#2a0000")

# 예고장(문서) 자리표시.
image note = Solid("#e8e4d8")
