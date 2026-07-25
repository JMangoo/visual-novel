#!/usr/bin/env python
"""대사 속 대괄호 오용 검사.

Ren'Py는 대사 안의 [foo]를 변수 삽입으로 해석한다. 표시용으로 [단서: ...] 같은
걸 쓰면 런타임에 NameError/SyntaxError로 터진다. lint는 이걸 못 잡으므로
스토리 파일에서 '변수가 아닌 대괄호'를 찾아 경고한다.

사용: python web-deploy/check_brackets.py
"""
import re
import sys
from pathlib import Path

# 실제로 존재하는 변수만 허용. 새 변수를 추가하면 여기에도 넣는다.
ALLOWED = {"player_name", "madness"}

GAME_DIR = Path(__file__).resolve().parent.parent / "yeonyeok" / "game"
# 런처가 생성한 파일은 Ren'Py 내부 변수를 정상적으로 쓰므로 제외
SKIP = {"screens.rpy", "gui.rpy", "options.rpy"}

pattern = re.compile(r"\[([^\[\]]*)\]")
problems = []

for path in sorted(GAME_DIR.glob("*.rpy")):
    if path.name in SKIP:
        continue
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for match in pattern.finditer(line):
            inner = match.group(1).strip()
            if inner == "":          # 파이썬 빈 리스트
                continue
            if inner in ALLOWED:
                continue
            problems.append((path.name, lineno, match.group(0)))

if problems:
    print("대사 속 대괄호 오용 의심:")
    for name, lineno, text in problems:
        print(f"  {name}:{lineno}  {text}")
    print("\n표시용이라면 [ ] 대신 ― 나 ( ) 를 쓸 것.")
    sys.exit(1)

print("대괄호 검사 통과 (변수 삽입만 사용 중)")
