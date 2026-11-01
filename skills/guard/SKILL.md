---
name: guard
description: 위험한 명령(운영 브랜치 푸시, rm -rf, 비밀키 읽기 등) 앞에서 확인을 요청하는 훅을 켜고 꺼요. "/my-skills:guard on|off|status"로 불러요.
disable-model-invocation: true
---

# guard

## 목적
운영 서버, 실제 돈이 걸린 봇, 비밀키를 실수로 건드리지 않게 해요. 기본은 꺼져 있어요.

## 입력
- `on`, `off`, `status` 중 하나.

## 산출물
- 상태 파일 `~/.claude/my-skills-guard.on`(있으면 켜짐).
- 보고: 현재 상태와 확인하는 명령 목록.

## 실행 순서
1. `on`: `touch ~/.claude/my-skills-guard.on`
2. `off`: `rm -f ~/.claude/my-skills-guard.on`
3. `status`: 파일이 있는지 보고, 있으면 켜짐.
4. 어느 경우든 [guard.py](../../hooks/guard.py)의 `RISKY` 목록을 읽어 무엇을 확인하는지 한 줄씩 보여 줘요.
5. 켜져 있으면 해당 명령에서 Claude Code가 실행 전에 확인을 물어요. 막는 게 아니라 묻는 거예요.

## 하지 않는 것
- 명령을 완전히 막기, 다른 훅 설정 바꾸기.

## 하지 말아야 할 것
- 사용자가 시키지 않았는데 끄기.

출처: garrytan/gstack careful·guard, toss/apps-in-toss-unity-sdk PreToolUse 훅.
