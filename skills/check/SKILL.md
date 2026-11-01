---
name: check
description: 완료 조건을 하나씩 대조하고 실행으로 증명해요. 검사는 Codex가 하고, 안 되면 독립된 Claude가 해요. "다 됐는지 검증해 줘", "명세대로 됐는지 확인해 줘"라고 할 때 써요. 시험 한 번 돌리기 같은 단순 확인에는 쓰지 않아요.
---

# check

## 목적
필요한 구현이 빠졌는지, 논리가 틀렸는지를 의견이 아니라 대조와 실행으로 잡아요. 싸게, 자주 돌리는 검사예요.

## 입력
- 명세 경로. 없으면 `docs/specs/`에서 가장 최근 파일.
- 명세가 아예 없으면(작은 작업) 요청에서 완료 조건 3~5개를 직접 만들어 보고 맨 위에 적고 진행해요. 멈추지 않아요.
- 확인할 범위: 기본은 브랜치의 기준 커밋부터 지금까지.

## 산출물
- 보고(채팅): 첫 줄에 검사자(Codex 또는 대체 문구), 완료 조건 표(`D<n> | 통과·실패·확인 불가 | 근거`), 3층으로 나눈 지적.

## 실행 순서
1. **직접 대조해요.** 완료 조건마다 확인 방법을 그대로 실행하고 결과를 적어요. 확인 불가는 통과가 아니에요.
2. **화면이 있으면 재요.** `uv run --with playwright==1.49.1 python <이 스킬 폴더>/../../scripts/measure.py <url>` 결과의 `fail`과 스크린샷을 봐요. 1층 위반은 [ui.md](../../rules/ui.md) 기준.
3. **독립 검사를 맡겨요.** 프롬프트는 [independent-checker.md](references/independent-checker.md). 바뀐 파일을 넘겨 `python3 <이 스킬 폴더>/../../scripts/ext.py codex --root <저장소> --timeout 540 --prompt-file <프롬프트> <파일...>`를 돌려요. Bash 도구는 `timeout: 600000`으로 부르고, 스크립트에는 `--timeout 540`을 넘겨요(스크립트가 먼저 끝나야 `STATUS:` 줄이 남아요). 스크립트는 [data-safety.md](../../rules/data-safety.md)대로 걸러 낸 파일의 사본만 임시 폴더에 두고 Codex를 그 폴더에서 돌려요. 저장소의 나머지 파일은 Codex에게 보이지 않아요.
4. **Codex가 안 되면 Claude로 해요.** 첫 줄이 `STATUS: unavailable` 또는 `STATUS: banned`이면 보고 첫 줄에 `Codex 사용 불가, Claude로 검증 (<이유>)`을 쓰고, 같은 프롬프트로 새 하위 에이전트를 띄워요. 모델은 만든 쪽과 다른 등급(만든 쪽이 sonnet이면 opus, 그 밖에는 sonnet)이고, 메인 대화와 만든 쪽의 생각 과정은 주지 않아요([models.md](../../rules/models.md)).
5. **받은 지적은 맞는지 확인해요.** 지적마다 코드를 보거나 실행해서 맞으면 남기고, 틀리면 근거를 들어 버려요.
6. **3층으로 처리해요.** 1층은 고치고 다시 1번부터, 2층은 한 번에 묻기([review-layers.md](../../rules/review-layers.md)).
7. **브랜치가 끝났으면 전체를 한 번 더 봐요.** 모든 작업이 끝난 뒤 브랜치 전체 diff를 opus 하위 에이전트에 같은 프롬프트로 맡겨요.
8. 다음 단계 한 줄: `finish`.

## 하지 않는 것
- 새 기능 추가, 설계 바꾸기.
- 사용자에게 매번 외부 전송 허락 묻기(거르기는 스크립트가 해요).

## 하지 말아야 할 것
- 실행하지 않고 "될 것 같다"로 통과 처리하기.
- Codex나 Claude 검사자의 지적을 확인 없이 그대로 반영하기.
- 대체했는데 첫 줄 문구를 빼기.

출처: obra/superpowers verification-before-completion·receiving-code-review, pstack prove-it-works·interrogate, github/spec-kit analyze.
