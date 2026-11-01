---
name: handoff
description: 일을 안전하게 멈추고(pause), 다음 세션에서 이어 가고(resume), 사용자가 정한 결정을 기록해요(decide). "/my-skills:handoff pause|resume|decide"로 불러요.
disable-model-invocation: true
---

# handoff

## 목적
컨텍스트가 차거나 세션을 바꿀 때 하던 일과 결정이 사라지지 않게 해요. 이어 갈 때는 이전 세션의 "됐다"를 다시 확인해요.

## 입력
- `pause`, `resume`, `decide <결정 내용>` 중 하나.

## 산출물
- 재개 메모 `docs/progress/HANDOFF.md`. 절은 이 순서예요: `## 목적`, `## 하던 일`, `## 확인된 것`, `## 현재 상태`, `## 다음 할 일`, `## 주요 파일`, `## 정한 결정`.
- 결정 기록 `docs/decisions.md`. 줄 형식 `- YYYY-MM-DD | 결정 | 이유 | 대안`. 팀 공유 문서(예: `논의_필요.md`)가 있으면 그 파일에 써요.

## 실행 순서
**pause**
1. 지금 하던 작은 단계를 끝내거나 되돌려요. 새 일은 시작하지 않고, 맡겨 둔 작업(백그라운드 명령, 돌고 있는 에이전트)은 멈춰요.
2. 되돌리기 어려운 일(푸시, PR)은 하지 않아요.
3. 고친 파일을 남겨요. 기본은 `wip:` 커밋 하나. 프로젝트 `CLAUDE.md`에 "커밋 금지/커밋하지 마" 같은 문구가 있으면 대신 `git diff > docs/progress/wip.patch`.
4. 재개 메모를 써요. "확인된 것"에는 실제로 돌린 명령과 결과만 적어요.

**resume**
1. 재개 메모와 진행 기록(`docs/progress/`)을 읽어요.
2. `git log`, `git status`, `git diff`로 실제 상태를 맞춰 봐요. 메모와 다르면 git을 믿어요.
3. 메모가 "확인된 것"이라고 한 것을 실제 결과물로 다시 확인해요(시험 다시 돌리기).
4. 이어 갈 지점과 남은 일을 한 줄로 말하고 이어 가요.

**decide**
1. 사용자가 정한 결정 하나를 결정 기록에 한 줄로 남겨요. 이유와 고려했던 대안도 같이.

## 하지 않는 것
- 사용자가 정하지 않은 것을 결정으로 기록하기.

## 하지 말아야 할 것
- 확인하지 않은 일을 "확인된 것"에 쓰기.
- 멈추려고 푸시하거나 브랜치를 지우기.

출처: pstack pause-safely·session-pickup·show-me-your-work (MIT), addyosmani/agent-skills documentation-and-adrs (MIT).
