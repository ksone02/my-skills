# 비교 시험

같은 과제를 Superpowers와 my-skills로 각각 돌려 비교해요.

## 과제
1. **작은 웹 기능**: 정적 페이지(`examples/list.html`, 항목 30개 목록)에 이름 필터 입력 하나 추가. 완료 조건:
   - D1. 입력한 글자가 이름에 들어간 항목만 보인다 — 브라우저로 확인
   - D2. 결과가 없으면 "찾는 이름이 없어요" 안내가 보인다 — 브라우저로 확인
   - D3. 390 폭에서 가로 스크롤이 없다 — `scripts/measure.py`
   - D4. 키보드로 입력에 포커스가 가고 포커스 표시가 보인다 — 브라우저로 확인
2. **짧은 리서치**: "Python 백테스트 라이브러리 3개 비교, 우리 퀀트 봇에 무엇을 쓸지" 결정 하나.

## 방법
- 과제마다 새 세션 두 개. 한쪽은 `/plugin disable my-skills`, 다른 쪽은 `/plugin disable superpowers`.
- 같은 첫 메시지로 시작하고, 사람 개입은 같은 질문에 같은 답만 해요.

## 기록할 것 (`evals/results/compare-<날짜>.md`)
| 항목 | 재는 법 |
|---|---|
| 끝까지 갔나 | O/X |
| 토큰 | `python3 scripts/session_tokens.py <세션 jsonl>` (입력, 출력, 캐시 읽기, 캐시 쓰기 따로) |
| 외부 호출 | `evals/results/ext-calls.jsonl`의 호출 수, 걸린 시간 |
| 되물은 횟수 | 사용자에게 질문한 메시지 수 |
| 남은 실수 | 끝난 뒤 완료 조건을 직접 확인해 실패한 개수 |

세션 jsonl은 `~/.claude/projects/<프로젝트 경로>/<세션 id>.jsonl`에 있어요. 하위 에이전트 기록(`<세션 id>/subagents/*.jsonl`)은 스크립트가 자동으로 합쳐요.

## Superpowers를 끄는 조건
my-skills가 두 과제 모두에서 토큰은 적고(캐시 포함 합계), 남은 실수는 같거나 적을 때.
