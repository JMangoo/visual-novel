# 「연역」 비주얼 노벨 — 플레이 가능한 뼈대(Walking Skeleton) 제작 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 「연역」을 처음부터 끝까지 클릭으로 완주할 수 있는 Ren'Py 게임 뼈대를 만들고, **웹으로 빌드해 GitHub Pages에 배포**하여 **아이폰 사파리에서 링크로 플레이**되게 한다. 임시 그림/임시 대사를 쓰되, 닉네임 입력·메신저 UI·모션 연출·3막 구조·저장/불러오기 등 모든 커스텀 시스템이 실제로 작동한다.

**배포 타깃(중요):** 최종 플레이 환경은 **아이폰 사파리(웹)**, 단 1명 공유, 스토어·비용 없음. Ren'Py "Web" 배포 → GitHub Pages 호스팅 → URL 접속(홈화면 추가 시 앱처럼). 아이폰은 세로 화면이므로 **가로 회전 권장 안내**를 넣고, **닉네임 키보드 입력이 웹에서 불안정할 위험**에 대비해 폴백을 둔다.

**Architecture:** Ren'Py 프로젝트를 `C:\Users\jinwoo\Visual Novel\yeonyeok\`에 생성한다. `game/` 폴더 안에서 **책임별로 파일을 분리**한다 — 캐릭터/변수, 모션/트랜지션, 메신저 UI, 막별 스토리 스크립트. 임시 아트는 Ren'Py 내장 `Placeholder`/`Solid` 디스플레이어블로 대체해, 실제 이미지 없이도 전 구간이 돌아가게 한다. 검증은 각 단계마다 `lint`(문법 검사) 통과 + PC에서 화면 확인, 그리고 마지막에 **실제 아이폰 사파리 확인**이다.

**Tech Stack:** Ren'Py 8.x (Python 기반 VN 엔진), Ren'Py Screen Language(UI), ATL(애니메이션), Ren'Py Web 빌드, GitHub Pages(호스팅), Git(버전 관리).

**참고:** GitHub 저장소는 이미 연결됨 — remote `origin` = https://github.com/JMangoo/visaul-novel.git, 브랜치 `main`. 최초 커밋(기획서·계획서)도 푸시 완료. 따라서 아래 Task 0은 이미 수행된 상태다(재실행 불필요).

---

## 사전 안내 (실행자 필독)

- **Ren'Py는 유닛 테스트가 아니라 `lint` + 수동 플레이로 검증한다.** 각 태스크의 검증 단계는 (1) `lint` 오류 0건, (2) 게임을 실행해 특정 화면/동작을 눈으로 확인, 두 가지다. 가짜 유닛 테스트를 만들지 말 것.
- **`lint` 실행 방법:**
  - GUI: Ren'Py 런처 → 프로젝트 선택 → 좌측 "Lint" 버튼.
  - CLI(설치 경로 확인 후): `"<RenPy설치폴더>\renpy.exe" "C:\Users\jinwoo\Visual Novel\yeonyeok" lint`
- **게임 실행:** 런처의 "Launch Project" 버튼, 또는 CLI `"<RenPy설치폴더>\renpy.exe" "C:\Users\jinwoo\Visual Novel\yeonyeok" run`
- **`[표시]` 표기의 태스크는 사용자(사람)가 직접 해야 하는 단계**다(설치 등). 실행자는 이 단계에서 사용자에게 안내하고 완료를 기다린다.
- 모든 커밋 메시지 끝에 다음 줄을 넣는다:
  `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

---

## 파일 구조 (완성 시점)

```
C:\Users\jinwoo\Visual Novel\
  docs\superpowers\...                (기획서·계획서 — 이미 존재)
  yeonyeok\                           (Ren'Py 프로젝트 루트)
    game\
      script.rpy                      진입 흐름: 스플래시 → 닉네임 → 1막 → 2막 → 3막 → 종료
      characters.rpy                  Character 정의, player_name 등 변수, 닉네임 입력 라벨
      images.rpy                      임시 이미지(Placeholder/Solid) 정의 모음
      motion.rpy                      ATL 트랜스폼, 트랜지션, 파티클 정의
      messenger.rpy                   메신저/통화 UI 스크린 + 메시지 출력 라벨
      story_act1.rpy                  1막 장면
      story_act2.rpy                  2막 장면
      story_act3.rpy                  3막 장면 + 결말
      options.rpy                     (런처 생성) 제목·창 크기 등 설정
      gui.rpy / screens.rpy           (런처 생성) 다크 톤 테마 커스터마이즈
```

**분리 원칙:** 함께 바뀌는 것끼리 모은다. 시스템(모션/메신저)과 콘텐츠(막별 스토리)를 분리해, 나중에 스토리 본문을 채울 때 시스템 코드를 건드리지 않게 한다.

---

## Task 0: Git 저장소 초기화 ✅ (완료됨 — 참고용)

> 이 태스크는 이미 수행되었다: `git init`, `.gitignore` 작성, 기획서·계획서 최초 커밋, remote `origin` 연결(https://github.com/JMangoo/visaul-novel.git), `main` 브랜치 푸시까지 완료. 아래는 기록용이며 재실행 불필요.

**Files:**
- Create: `C:\Users\jinwoo\Visual Novel\.gitignore`

- [x] **Step 1: 저장소 초기화**

작업 폴더에서:
```bash
cd "C:/Users/jinwoo/Visual Novel"
git init
```

- [ ] **Step 2: .gitignore 작성**

`C:\Users\jinwoo\Visual Novel\.gitignore` 생성:
```
# Ren'Py
*.rpyc
*.rpa
*.rpymc
/yeonyeok/game/saves/
/yeonyeok/game/cache/
/yeonyeok/log.txt
/yeonyeok/errors.txt
/yeonyeok/traceback.txt

# OS
Thumbs.db
.DS_Store
```

- [ ] **Step 3: 최초 커밋 (이미 있는 기획서·계획서 포함)**

```bash
cd "C:/Users/jinwoo/Visual Novel"
git add .gitignore docs/
git commit -m "chore: init repo with design spec and skeleton plan

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

Expected: 커밋 생성됨. `git log --oneline`에 1건 표시.

---

## Task 1: Ren'Py 설치 `[사용자]`

**Files:** 없음 (환경 설정)

- [ ] **Step 1: Ren'Py SDK 다운로드·설치 `[사용자]`**

사용자가 직접 수행. 실행자는 아래를 안내한다:
1. https://www.renpy.org/latest.html 접속
2. Windows SDK(7z/zip 또는 인스톨러) 다운로드
3. 압축 해제 또는 설치 → `renpy.exe`(런처)를 실행할 수 있는 상태로 둔다
4. 설치 경로를 메모 (예: `C:\renpy-8.3.0\`)

- [ ] **Step 2: 런처 실행 확인 `[사용자]`**

`renpy.exe`(또는 `renpy32.exe`) 실행 → Ren'Py 런처 창이 뜨는지 확인.
Expected: "The Ren'Py Launcher" 창이 정상적으로 표시됨.

- [ ] **Step 3: 프로젝트 디렉터리 지정 `[사용자]`**

런처 → "preferences" → "Projects Directory" → `C:\Users\jinwoo\Visual Novel` 로 설정.
Expected: 이후 생성/조회되는 프로젝트가 이 폴더에 저장됨.

---

## Task 2: Ren'Py 프로젝트 생성

**Files:**
- Create(런처가 생성): `yeonyeok\game\script.rpy`, `options.rpy`, `gui.rpy`, `screens.rpy` 등

- [ ] **Step 1: 새 프로젝트 생성 `[사용자]`**

런처 → "Create New Project" → 이름 `yeonyeok` 입력 → 해상도는 1920x1080(아이폰 레티나 대비 선명도, Ren'Py 권장 절충안), 색상 테마는 아무거나(뒤에서 커스터마이즈) → 생성.
Expected: `C:\Users\jinwoo\Visual Novel\yeonyeok\` 폴더와 `game\` 하위 파일들이 생성됨.

- [ ] **Step 2: 기본 실행 확인**

런처에서 `yeonyeok` 선택 → "Launch Project".
Expected: 기본 Ren'Py 메인 메뉴(Start/Load/Preferences...)가 뜨고, Start 시 샘플 대사가 나옴.

- [ ] **Step 3: 커밋**

```bash
cd "C:/Users/jinwoo/Visual Novel"
git add yeonyeok/
git commit -m "chore: scaffold Ren'Py project 'yeonyeok'

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 3: 캐릭터·변수·닉네임 입력

**Files:**
- Create: `yeonyeok\game\characters.rpy`

- [ ] **Step 1: characters.rpy 작성**

```renpy
## 등장인물 및 전역 변수 정의 -------------------------------------------

# 플레이어 닉네임 (기본값). 게임 시작 시 입력받아 덮어씀.
default player_name = "이름 없음"

# 광기 수치 — 선택에 따라 오르내리며 '파멸의 색'을 결정(뼈대 단계에선 값만 추적).
default madness = 0

# 캐릭터 정의
# 주인공 대사는 화자 이름 없이 나레이션/독백 위주로 처리하되, 필요시 me 사용.
define me = Character("나", color="#cccccc")

# 살인마: 이름을 숨긴 채 등장. 정체 공개 전까지 '???' 로 표기.
define killer = Character("???", color="#8b0000")

# 미끼 용의자
define decoy = Character("수상한 남자", color="#6a8caf")

# 언니: 문자/통화로만 등장하므로 일반 대사창 대신 메신저 UI를 사용(messenger.rpy).
# 필요 시 통화 음성 표기용 캐릭터.
define sister_voice = Character("언니", color="#c9a227")


# 닉네임 입력 라벨 -----------------------------------------------------
# 아이폰 웹에서는 renpy.input() 키보드가 불안정할 수 있어, '직접 입력'과
# '프리셋 선택' 두 경로를 모두 제공한다(폴백 안전장치).
label ask_nickname:
    scene black
    "..."
    menu:
        "이름을 직접 입력한다":
            $ raw = renpy.input("당신을 뭐라고 부를까?", default="", length=12).strip()
            if raw == "":
                call screen preset_names
                $ player_name = _return
            else:
                $ player_name = raw
        "제시된 이름 중에 고른다":
            call screen preset_names
            $ player_name = _return
    "그래, [player_name]."
    return

# 프리셋 이름 선택 스크린 (키보드 없이도 진행 가능)
screen preset_names():
    modal True
    add Solid("#000000cc")
    frame:
        xalign 0.5 yalign 0.5
        padding (30, 24)
        background Frame(Solid("#14141c"), 12, 12)
        vbox:
            spacing 14
            text "이름을 선택해." size 28 color "#e0e0e0" xalign 0.5
            textbutton "서리" action Return("서리") xalign 0.5
            textbutton "재이" action Return("재이") xalign 0.5
            textbutton "무명" action Return("무명") xalign 0.5
            textbutton "K"   action Return("K")   xalign 0.5
```

- [ ] **Step 2: lint 통과 확인**

Run: 런처 "Lint" (또는 CLI lint)
Expected: "creating list of all script files ... " 후 오류(Errors) 0건. 경고는 무시 가능.

- [ ] **Step 3: 커밋**

```bash
cd "C:/Users/jinwoo/Visual Novel"
git add yeonyeok/game/characters.rpy
git commit -m "feat: add characters, globals, and nickname input label

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 4: 임시 이미지(Placeholder) 정의

**Files:**
- Create: `yeonyeok\game\images.rpy`

- [ ] **Step 1: images.rpy 작성**

Ren'Py 내장 `Placeholder`/`Solid`로 실제 그림 없이 배경·캐릭터·CG 자리표시.

```renpy
## 임시 이미지 정의 (실제 아트로 교체 예정) ----------------------------

# 배경 — Solid 색으로 대체, 라벨은 장면에서 텍스트로 안내.
image bg room     = Solid("#141420")
image bg hallway  = Solid("#101014")
image bg alley    = Solid("#0c0f14")
image bg store    = Solid("#161a12")
image bg climax   = Solid("#1a0a0a")
image black       = Solid("#000000")

# 캐릭터 — 내장 Placeholder 실루엣.
image decoy_ph = Placeholder("boy")

# 살인마 — 가려진 형상. 어두운 실루엣으로 대체.
image killer_ph = Placeholder("bg")

# 최후의 진실 CG 자리표시.
image cg_truth = Solid("#2a0000")

# 예고장(문서) 자리표시.
image note = Solid("#e8e4d8")
```

- [ ] **Step 2: lint 통과 확인**

Run: 런처 "Lint"
Expected: 오류 0건.

- [ ] **Step 3: 커밋**

```bash
cd "C:/Users/jinwoo/Visual Novel"
git add yeonyeok/game/images.rpy
git commit -m "feat: add placeholder images for backgrounds, sprites, CG

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 5: 모션·트랜지션·파티클

**Files:**
- Create: `yeonyeok\game\motion.rpy`

- [ ] **Step 1: motion.rpy 작성**

```renpy
## 모션(ATL) · 트랜지션 · 파티클 -------------------------------------

# 왼쪽에서 슬라이드 등장
transform slide_in_left:
    xpos -0.4 yalign 1.0 alpha 0.0
    easein 0.5 xpos 0.0 alpha 1.0

# 오른쪽에서 슬라이드 등장
transform slide_in_right:
    xpos 1.4 yalign 1.0 alpha 0.0
    easein 0.5 xpos 0.0 alpha 1.0

# 미세하게 숨쉬듯 흔들리는 idle 모션
transform idle_sway:
    block:
        linear 2.0 yoffset -6
        linear 2.0 yoffset 0
        repeat

# 놀람/충격 시 좌우 진동 (요소 단위)
transform shudder:
    block:
        linear 0.04 xoffset 8
        linear 0.04 xoffset -8
        linear 0.04 xoffset 0
        repeat 4

# 천천히 확대(줌 인) — 긴장 고조
transform slow_zoom:
    zoom 1.0
    linear 6.0 zoom 1.12

# 커스텀 페이드 트랜지션
define fade_slow = Fade(1.0, 0.5, 1.0)
define dissolve_slow = Dissolve(1.5)

# 비 파티클 (임시: 얇은 흰 선)
image rain = SnowBlossom(
    Solid("#8899aa", xsize=2, ysize=18),
    count=120, border=20, xspeed=(0, 0), yspeed=(600, 900), fast=True
)

# 눈 파티클 (임시: 작은 흰 점)
image snow = SnowBlossom(
    Solid("#ffffff", xsize=4, ysize=4), count=80, border=20, yspeed=(60, 140)
)
```

- [ ] **Step 2: lint 통과 확인**

Run: 런처 "Lint"
Expected: 오류 0건. (`SnowBlossom` 인자 관련 경고가 나오면 인자를 조정하되 오류가 아니면 진행.)

- [ ] **Step 3: 임시 테스트 장면으로 눈으로 확인**

`script.rpy`의 기존 `label start:` 블록을 잠시 아래로 교체해 실행:
```renpy
label start:
    scene bg room
    "테스트: 비 내림"
    show rain
    pause 1.0
    hide rain
    "테스트: 실루엣 등장 + 흔들림"
    show decoy_ph at slide_in_left
    "슬라이드 등장 확인"
    show decoy_ph at shudder
    "흔들림 확인"
    return
```
Run: 런처 "Launch Project" → Start.
Expected: 배경 위로 비가 떨어지고, 실루엣이 왼쪽에서 미끄러져 들어오며, 이후 좌우로 진동한다.

- [ ] **Step 4: 테스트 장면 원복**

위 임시 `label start`를 삭제(다음 태스크에서 script.rpy를 정식 구성). motion.rpy 자체는 변경 없음.

- [ ] **Step 5: 커밋**

```bash
cd "C:/Users/jinwoo/Visual Novel"
git add yeonyeok/game/motion.rpy
git commit -m "feat: add ATL transforms, transitions, and particle effects

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 6: 메신저 / 통화 UI

**Files:**
- Create: `yeonyeok\game\messenger.rpy`

- [ ] **Step 1: messenger.rpy 작성**

메시지 로그를 화면에 쌓아 보여주는 스크린 + 한 줄씩 출력하는 라벨.

```renpy
## 메신저 / 통화 UI ---------------------------------------------------

# 대화 로그: (발신자, 본문) 튜플 리스트. "me"=주인공, 그 외=상대.
default phone_log = []

# 메신저 화면
screen phone_ui(title="언니"):
    zorder 90
    # 어둡게 깔린 배경
    add Solid("#000000aa")
    frame:
        xalign 0.5 yalign 0.5
        xsize 560 ysize 720
        background Frame(Solid("#0b141a"), 12, 12)
        padding (12, 12)
        vbox:
            spacing 6
            # 헤더
            frame:
                xfill True
                background Solid("#14202a")
                padding (12, 8)
                text title color "#e7f0f5" size 26 bold True
            # 메시지 목록
            viewport:
                id "vp"
                xfill True yfill True
                mousewheel True
                yadjustment ui.adjustment()  # 아래에서 재조정
                vbox:
                    spacing 8
                    for who, body in phone_log:
                        if who == "me":
                            hbox:
                                xfill True
                                null width 90
                                frame:
                                    xalign 1.0
                                    background Frame(Solid("#2e6b4f"), 10, 10)
                                    padding (12, 8)
                                    text body color "#ffffff" size 22
                        else:
                            hbox:
                                xfill True
                                frame:
                                    xalign 0.0
                                    background Frame(Solid("#22303a"), 10, 10)
                                    padding (12, 8)
                                    text body color "#e7f0f5" size 22
                                null width 90

# 통화 착신 화면
screen call_ui(caller="언니"):
    zorder 95
    add Solid("#000000dd")
    vbox:
        xalign 0.5 yalign 0.35
        spacing 20
        text caller xalign 0.5 color "#c9a227" size 48 bold True
        text "통화 중..." xalign 0.5 color "#88aabb" size 24 at idle_sway

# 메시지 한 줄 출력 라벨 (클릭으로 넘어감)
label pmsg(who, body):
    $ phone_log.append((who, body))
    $ renpy.restart_interaction()
    pause
    return

# 대화 로그 초기화
label pclear:
    $ phone_log = []
    return
```

- [ ] **Step 2: lint 통과 확인**

Run: 런처 "Lint"
Expected: 오류 0건. (viewport의 `yadjustment` 관련 경고가 나오면 해당 줄을 삭제하고 진행 — 자동 스크롤은 필수 아님.)

- [ ] **Step 3: 임시 테스트 장면으로 눈으로 확인**

`script.rpy`에 임시 start:
```renpy
label start:
    scene bg room
    show screen phone_ui("언니")
    call pmsg("sister", "너 지금 어디야?")
    call pmsg("me", "집. 왜.")
    call pmsg("sister", "그 사람한테서 또 연락 왔어?")
    call pmsg("me", "...어떻게 알았어?")
    hide screen phone_ui
    "통화 테스트"
    show screen call_ui("언니")
    pause
    hide screen call_ui
    return
```
Run: Launch → Start.
Expected: 메신저 창이 뜨고, 클릭할 때마다 좌/우 말풍선이 하나씩 쌓인다("me"는 오른쪽 초록, 상대는 왼쪽). 이어 통화 착신 화면이 뜬다.

- [ ] **Step 4: 테스트 start 삭제**

임시 `label start` 제거(다음 태스크에서 정식 구성).

- [ ] **Step 5: 커밋**

```bash
cd "C:/Users/jinwoo/Visual Novel"
git add yeonyeok/game/messenger.rpy
git commit -m "feat: add messenger and incoming-call UI screens

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 7: 1막 스크립트 (예고)

**Files:**
- Create: `yeonyeok\game\story_act1.rpy`

임시 대사로 1막의 흐름·시스템 사용을 모두 시연한다(정식 대사는 이후 콘텐츠 단계에서 교체).

- [ ] **Step 1: story_act1.rpy 작성**

```renpy
## 1막 — 예고 --------------------------------------------------------
label act1:
    scene bg room with fade_slow
    "[임시대사] 나는 감정에 휘둘리지 않는다. 모든 건 논리로 설명된다."
    me "이 세상에 내가 못 읽는 사건은 없어."

    # 첫 예고장
    show note at slide_in_right with dissolve_slow
    "[임시대사] 책상 위에, 오지 않아야 할 편지가 놓여 있다."
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
            "[임시대사] 나는 다음 수를 읽었다. 완벽하다고 믿었다."
        "무시하고 상대를 도발한다":
            $ madness += 2
            "[임시대사] 장난에 놀아나지 않겠다. 그렇게 생각했다."

    # 예고대로 살인 발생
    scene bg alley with fade_slow
    show rain
    "[임시대사] 예고된 시간, 예고된 장소. 내 대응은 전부 빗나갔다."
    killer "봤지? 난 네가 뭘 할지 이미 알고 있었어."
    hide rain

    # 미끼 용의자 등장
    scene bg store with dissolve
    show decoy_ph at slide_in_left
    show decoy_ph at idle_sway
    decoy "당신, 그 사건 쫓고 있죠? ...나도 관심 있는데."
    "[임시대사] 이 남자, 수상하다. 논리가 그를 가리킨다."

    jump act2
```

- [ ] **Step 2: lint 통과 확인**

Run: 런처 "Lint"
Expected: 오류 0건. (`jump act2`는 Task 8에서 정의되므로, act2가 아직 없으면 lint가 "unknown label act2" 경고를 낼 수 있다 — Task 8 완료 후 사라진다. 오류로 뜨면 Task 8을 먼저 만든 뒤 재확인.)

- [ ] **Step 3: 커밋**

```bash
cd "C:/Users/jinwoo/Visual Novel"
git add yeonyeok/game/story_act1.rpy
git commit -m "feat: add Act 1 skeleton scenes (notice, sister text, decoy)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 8: 2막 스크립트 (균열)

**Files:**
- Create: `yeonyeok\game\story_act2.rpy`

- [ ] **Step 1: story_act2.rpy 작성**

```renpy
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
```

- [ ] **Step 2: lint 통과 확인**

Run: 런처 "Lint"
Expected: 오류 0건. (`jump act3`는 Task 9에서 정의.)

- [ ] **Step 3: 커밋**

```bash
cd "C:/Users/jinwoo/Visual Novel"
git add yeonyeok/game/story_act2.rpy
git commit -m "feat: add Act 2 skeleton scenes (madness, name-call, sister crack)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 9: 3막 스크립트 (연역) + 결말

**Files:**
- Create: `yeonyeok\game\story_act3.rpy`

- [ ] **Step 1: story_act3.rpy 작성**

```renpy
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
```

- [ ] **Step 2: lint 통과 확인**

Run: 런처 "Lint"
Expected: 오류 0건. 이 시점에서 act1/act2/act3의 `jump` 경고가 모두 사라져야 한다.

- [ ] **Step 3: 커밋**

```bash
cd "C:/Users/jinwoo/Visual Novel"
git add yeonyeok/game/story_act3.rpy
git commit -m "feat: add Act 3 skeleton scenes (deduction, truth reveal, ending)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 10: 진입 흐름 연결 (script.rpy)

**Files:**
- Modify: `yeonyeok\game\script.rpy`

- [ ] **Step 1: script.rpy를 진입 흐름으로 교체**

런처가 생성한 기존 샘플 내용을 지우고 아래로 교체(주석 상단부는 남겨도 무방):
```renpy
## 진입 흐름 ---------------------------------------------------------
label start:
    scene black
    # 아이폰 웹 대비: 가로 화면 권장 안내(PC에서도 무해).
    centered "{size=22}편안한 감상을 위해 기기를 가로로 눕히고,\n소리를 켜 주세요.{/size}"
    "당신은 감정을 신뢰하지 않는다. 오직 논리만이 세상을 설명한다고 믿는다."

    call ask_nickname

    jump act1
```

- [ ] **Step 2: lint 통과 확인**

Run: 런처 "Lint"
Expected: 오류 0건.

- [ ] **Step 3: 전체 완주 플레이 확인**

Run: 런처 "Launch Project" → Start.
Expected(순서대로 관찰):
1. 검은 화면 도입 대사
2. 닉네임 입력창 → 입력한 이름이 다음 대사에 반영됨
3. 1막: 예고장 등장 → 언니 메신저 대화 → 선택지 → 비 내리는 골목 살인 → 미끼 남자 실루엣 등장
4. 2막: 선택지 → 예고장 재등장 → 통화 착신 화면 → **살인마가 입력한 닉네임을 부름** → 언니 문자 균열
5. 3막: 눈 내리는 클라이맥스 → 진실 CG + "언니=살인마" 폭로 → 결말 대사(광기 수치 표시) → 끝 → 메인 메뉴 복귀
중간에 크래시/미정의 라벨/이미지 오류가 없어야 한다.

- [ ] **Step 4: 저장/불러오기 확인**

플레이 도중 아무 지점에서 우클릭/메뉴 → Save → 슬롯 저장 → Main Menu → Load → 해당 슬롯 → 그 지점부터 재개되는지 확인.
Expected: Ren'Py 기본 저장/불러오기가 정상 작동(추가 구현 불필요).

- [ ] **Step 5: 커밋**

```bash
cd "C:/Users/jinwoo/Visual Novel"
git add yeonyeok/game/script.rpy
git commit -m "feat: wire entry flow start -> nickname -> act1/2/3

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 11: 다크 톤 테마 커스터마이즈

**Files:**
- Modify: `yeonyeok\game\options.rpy`
- Modify: `yeonyeok\game\gui.rpy`

- [ ] **Step 1: 게임 제목 설정 (options.rpy)**

`options.rpy`에서 `config.name` 을 찾아 교체:
```renpy
define config.name = _("연역")
```
(창 타이틀·저장 파일명에 반영)

- [ ] **Step 2: gui.rpy 색상을 다크 스릴러 톤으로 조정**

`gui.rpy`에서 아래 값들을 찾아 교체(변수명은 Ren'Py 버전에 따라 존재; 있는 것만 수정):
```renpy
define gui.accent_color = '#8b0000'
define gui.idle_color = '#6b6b6b'
define gui.hover_color = '#c9a227'
define gui.selected_color = '#ffffff'
define gui.text_color = '#d8d8d8'

define gui.interface_text_color = '#d8d8d8'
```
그리고 대사창을 어둡게:
```renpy
define gui.text_color = '#e0e0e0'
```

- [ ] **Step 3: lint 통과 확인**

Run: 런처 "Lint"
Expected: 오류 0건.

- [ ] **Step 4: 눈으로 확인**

Run: Launch Project.
Expected: 창 제목이 "연역", 메뉴/선택지 강조색이 붉은/황금 톤으로 바뀜. 전체적으로 어두운 분위기.

- [ ] **Step 5: 커밋**

```bash
cd "C:/Users/jinwoo/Visual Novel"
git add yeonyeok/game/options.rpy yeonyeok/game/gui.rpy
git commit -m "style: set title and dark thriller GUI theme

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 12: 최종 점검 + 배포 빌드(선택)

**Files:** 없음 (검증)

- [ ] **Step 1: 최종 lint**

Run: 런처 "Lint"
Expected: 오류 0건. 경고 목록을 훑어 이미지/라벨 미정의 경고가 없는지 확인.

- [ ] **Step 2: 처음부터 끝까지 1회 완주 (최종 확인)**

Run: Launch Project → 새 게임으로 엔딩까지.
Expected: Task 10 Step 3의 1~5가 전부 재현되고, 어떤 크래시도 없음. 두 선택지 조합을 바꿔가며 최소 2회 완주해 양쪽 분기 모두 정상 종료 확인.

- [ ] **Step 3: 최종 커밋 + 태그**

```bash
cd "C:/Users/jinwoo/Visual Novel"
git add -A
git commit -m "chore: walking skeleton complete (playable end-to-end on desktop)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git tag skeleton-v1
git push origin main --tags
```

> PC에서 완주가 검증되면, 이제 웹 빌드 → 아이폰 배포로 넘어간다(Task 13~15).

---

## Task 13: Ren'Py 웹 빌드 생성

**Files:** 빌드 산출물 (git 미추적)

- [ ] **Step 1: Web 플랫폼 지원 설치 `[사용자]`**

런처 → 프로젝트 `yeonyeok` 선택 → "Build Distributions" → 목록에 "Web"이 없으면 런처가 안내하는 대로 **Web 지원(웹 빌드용 파일)**을 먼저 다운로드/설치한다. (Ren'Py 런처가 자동으로 받아준다.)
Expected: Build Distributions 화면에 "Web" 항목 체크박스가 나타남.

- [ ] **Step 2: 웹 빌드 실행**

런처 → "Build Distributions" → **Web** 만 체크 → "Build".
Expected: `C:\Users\jinwoo\Visual Novel\yeonyeok-dists\` (또는 런처가 알려주는 경로)에 `yeonyeok-<버전>-web\` 폴더가 생성됨. 그 안에 `index.html`, `game.zip`, `web/` 등이 있음.

- [ ] **Step 3: 로컬에서 웹 빌드 동작 확인**

웹 빌드는 `file://`로 바로 못 열고 로컬 서버가 필요하다. 빌드된 web 폴더에서:
```bash
cd "<web 빌드 폴더 경로>"
python -m http.server 8000
```
브라우저에서 `http://localhost:8000/` 접속.
Expected: 게임이 브라우저에서 로드되어 시작 화면이 뜨고, 클릭으로 진행된다. (닉네임은 '프리셋 선택' 경로로도 진행 가능한지 반드시 확인.)

---

## Task 14: GitHub Pages 배포 (coi-serviceworker 포함)

> **중요(회색 화면 원인/해결):** Ren'Py 웹은 SharedArrayBuffer(`crossOriginIsolated`)가 필요한데, GitHub Pages는 COOP/COEP 헤더를 못 붙여서 그냥 올리면 **회색 화면**이 된다. 그래서 `web-deploy/coi-serviceworker.js`를 빌드에 주입하고 Ren'Py 기본 서비스워커 등록을 끈다. 이 과정을 `web-deploy/deploy-web.sh`가 자동 처리한다. (런처 "브라우저로 열기"는 자체 서버가 헤더를 붙여줘서 로컬에선 그냥 됨.)

**Files:**
- `web-deploy/coi-serviceworker.js`, `web-deploy/patch_index.py`, `web-deploy/deploy-web.sh` (저장소에 커밋됨)
- 배포 대상: `gh-pages` 브랜치

- [ ] **Step 1: 배포 스크립트 실행**

Ren'Py 런처 "배포본 빌드 > Web" 결과 폴더(index.html 포함)를 인자로 넘긴다:
```bash
cd "C:/Users/jinwoo/Visual Novel"
bash web-deploy/deploy-web.sh "/c/Users/jinwoo/Visual Novel/yeonyeok-1.0-dists/yeonyeok-1.0-web"
```
스크립트가 하는 일: 빌드 복사 → `coi-serviceworker.js` 추가 → `index.html` 패치 → `.nojekyll` 추가 → `gh-pages`로 강제 푸시.
Expected: `gh-pages` 브랜치에 패치된 `index.html`과 `coi-serviceworker.js`가 루트에 올라감. 재배포 후 테스트는 옛 서비스워커 캐시를 피해 **시크릿 창**으로.
Expected: `gh-pages` 브랜치에 `index.html`이 루트에 있는 상태로 푸시됨.

- [ ] **Step 2: GitHub Pages 활성화 `[사용자]`**

GitHub 저장소 웹페이지 → Settings → Pages → "Build and deployment" → Source: **Deploy from a branch** → Branch: **gh-pages** / **/(root)** → Save.
Expected: 잠시 후 상단에 배포 URL이 표시됨. 예상 URL: `https://jmangoo.github.io/visaul-novel/`

- [ ] **Step 3: PC 브라우저에서 배포 URL 확인**

배포 URL을 PC 브라우저에서 연다(반영까지 1~2분 걸릴 수 있음).
Expected: 게임이 정상 로드·완주됨.

---

## Task 15: 아이폰 실기기 확인 `[사용자]`

**Files:** 없음 (검증)

- [ ] **Step 1: 아이폰 사파리에서 접속 `[사용자]`**

아이폰 사파리에서 배포 URL 접속.
Expected: 게임 로드, 탭으로 진행, 닉네임 선택 가능, 메신저 UI 정상.

- [ ] **Step 2: 가로 화면 확인**

기기를 가로로 회전.
Expected: 가로 화면에서 레이아웃이 깨지지 않고 텍스트·UI가 읽힘. (세로에서 답답하면 게임 시작부의 회전 안내 문구가 보임.)

- [ ] **Step 3: 홈 화면에 추가(앱처럼) 확인 `[사용자]`**

사파리 공유 버튼 → "홈 화면에 추가".
Expected: 홈 화면에 아이콘 생성, 탭하면 전체화면으로 실행.

- [ ] **Step 4: 결과 피드백**

닉네임 입력 방식(직접 입력이 되는지/프리셋만 되는지), 성능, 조작감, 깨지는 부분을 사용자가 알려준다 → 필요 시 후속 조정.

---

## 이 계획 완료 후 다음 단계 (별도 진행)

이 뼈대가 완성되면, 다음 두 가지는 각각 별도의 반복 작업으로 진행한다:

1. **스토리 본문 집필** — `story_act1/2/3.rpy`의 `[임시대사]`를 사용자와 장면 단위로 함께 실제 대사·선택지·복선으로 교체. 예고 살인 3건의 구체 내용, 언니 문자의 '공정한 단서' 배치, 미끼 서브플롯 전개 확정.
2. **AI 아트 제작** — 기획서의 파이프라인(디자인 시트 승인 → 기준 스프라이트 → 얼굴 교체)대로 미끼 용의자 스프라이트, 배경, 살인마 형상, 언니 진실 CG를 생성해 `images.rpy`의 Placeholder를 실제 이미지로 교체.
```
