---
name: review
description: 분야 전문가 역할 여러 명이 기획이나 설계를 한 번에 검토하고, 지적을 3층으로 나눠 처리해요. "/my-skills:review [역할] [대상 경로]"로 불러요.
disable-model-invocation: true
---

# review

## 목적
그 분야 전문가여야 떠올릴 수 있는 지적을 받아요. 비싼 검토라서 기획 직후와 설계 직후, 만들기 전 두 자리에서만 써요. 개발 뒤에는 결과가 기대와 다를 때만 다시 불러요.

## 입력
- 역할 이름(선택): `quant`, `web`, `data-research` 또는 새 분야 이름.
- 대상: 명세나 계획 경로. 없으면 `docs/plans/` → `docs/specs/` 순으로 가장 최근 파일.

## 산출물
- 보고(채팅): 첫 줄에 고른 역할, 1층 지적과 고친 내용, 2층 질문 목록(번호, 근거, 비용).
- 고친 명세나 계획.

## 실행 순서
1. **역할을 골라요.** 이름을 받았으면 [roles/](references/roles/) 아래 그 파일. 없으면 대상을 보고 골라 보고 첫 줄에 적어요(사용자가 바로 바꿀 수 있게). 맞는 파일이 없으면 그 자리에서 역할 3개와 꼭 보는 항목을 만들어 쓰고, 끝에 저장할지 한 줄로 물어요.
2. **역할마다 하위 에이전트를 한 라운드에 병렬로 띄워요.** 모델은 sonnet, 되돌리기 어려운 구조 결정이면 opus([models.md](../../rules/models.md)). 프롬프트는 [reviewer-prompt.md](references/reviewer-prompt.md)에 역할 절과 대상 경로를 넣어요. 필요하면 같은 프롬프트로 Codex 한 명을 더해요(`scripts/ext.py codex`).
3. **지적을 모아 걸러요.** 근거 없는 지적, 3층(취향) 지적은 버려요. 겹치는 지적은 합쳐요.
4. **지적이 맞는지 확인해요.** 코드·자료·계산으로 확인하고, 틀린 지적은 근거와 함께 버려요.
5. **3층으로 처리해요**([review-layers.md](../../rules/review-layers.md)). 1층은 대상 문서를 바로 고치고, 2층은 한 메시지로 묻고, 답이 없으면 고치지 않아요.
6. 다음 단계 한 줄(명세 검토 뒤면 `plan`, 계획 검토 뒤면 `build`).

## 하지 않는 것
- 구현 코드 고치기(문서만 고쳐요).
- 매 단계마다 검토하기.

## 하지 말아야 할 것
- 역할 프롬프트에 "이건 지적하지 마"처럼 미리 판단 넣기.
- 2층 지적을 하나씩 따로 묻기.
- 확인하지 않은 지적을 사실처럼 반영하기.

출처: garrytan/gstack plan reviews, EveryInc/compound-engineering-plugin, pstack interrogate, toss/apps-in-toss-harness render-rules.
