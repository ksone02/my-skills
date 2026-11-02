---
name: design
description: 대시보드·도구·랜딩 화면을 새로 만들거나 크게 고쳐요. 실제 브라우저 세 폭으로 재고 스크린샷으로 비평해요. 화면 코드를 쓰기 전에, 다른 기능을 구현하는 도중이라도 사용자가 말하지 않아도 반드시 먼저 써요. 색 하나, 간격 하나 바꾸는 작은 수정에는 쓰지 않아요.
---

# design

## 목적
AI가 만든 티가 나지 않고, 실제로 쓰기 편한 화면을 만들어요. 눈대중 대신 측정과 스크린샷으로 확인해요.

## 입력
- 요청(만들 화면 또는 고칠 화면), 프로젝트.
- `--landing`: 랜딩·소개 페이지일 때.

## 산출물
- 화면 코드 수정.
- 측정 보고 `.measure/report.json`과 스크린샷 3장.
- 보고: 고친 1층 위반, 2층 질문 목록, 측정 `fail` 결과.

## 실행 순서
1. **화면 종류를 정해요.**
   - `--landing`이면 Skill 도구로 `taste-skill:design-taste-frontend`를 불러 그 절차를 따르고, 끝난 뒤 이 스킬의 4~6단계만 해요. 설치돼 있지 않으면 `/plugin marketplace add Leonxlnx/taste-skill` 뒤 `/plugin install taste-skill@taste-skill`을 안내하고 멈춰요.
   - 그 밖에는 대시보드·도구 방식([operate-mode.md](references/operate-mode.md)).
2. **프로젝트를 먼저 읽어요.** 이미 있는 토큰, 컴포넌트, `DESIGN.md`가 있으면 그걸 따라요. 처음 만드는 화면이면 시안 2~3개의 방향(정보 배치 위주)을 나란히 보여 주고 고르게 해요.
3. **만들어요.** [ui.md](../../rules/ui.md) 1층은 처음부터 지켜요. 장식을 뺀 자리는 실제 내용과 위계로 채워요. 문구는 [writing-ko.md](../../rules/writing-ko.md).
4. **재요.** `uv run --with playwright==1.49.1 python <이 스킬 폴더>/../../scripts/measure.py <url 또는 파일>`. 폭은 1440x900, 1366x768, 390x844. `fail`은 전부 1층이에요.
5. **스크린샷을 보고 비평해요.** 세 장을 Read로 열어 [critique.md](references/critique.md) 순서로 비평하고 가장 큰 문제 3개를 고쳐요. 4~5단계를 최대 3회 반복해요. 스크린샷에 보이는 문제는 코드가 뭐라 하든 진짜 문제예요.
6. **3층으로 정리해요.** 1층은 고친 내용을 보고하고, 2층(`UI-R`)은 한 번에 물어요([review-layers.md](../../rules/review-layers.md)).

## 하지 않는 것
- 화면 문구만 고치는 일(그건 `copy`).
- 기능·데이터 로직 바꾸기.

## 하지 말아야 할 것
- 측정 없이 "반응형 확인했어요"라고 쓰기.
- 이미 있는 디자인 체계를 무시하고 새 토큰 덮어쓰기.
- 3회를 넘겨 계속 고치기(남은 문제는 목록으로 보고).

출처: pbakaus/impeccable, leonxlnx/taste-skill, Nutlope/hallmark, toss/apps-in-toss-harness design.
