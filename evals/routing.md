# 부르기 시험

새 세션에서 한 줄씩 보내요. 왼쪽은 그 스킬이 떠야 하고, 오른쪽은 my-skills 스킬이 저절로 뜨면 안 돼요(`disable-model-invocation: true`).

결과는 `evals/results/routing-<날짜>.md`에 `스킬 | 이름으로 뜸(O/X) | 이름 없이 안 뜸(O/X)` 표로 남겨요.

| 스킬 | 이름으로 부르기(떠야 함) | 이름 없이(뜨면 안 됨) |
|---|---|---|
| shape | `/my-skills:shape 동네 산책 기록 앱` | 이런 앱 만들고 싶은데 뭐부터 정하지? |
| plan | `/my-skills:plan docs/specs/x.md` | 이 명세로 작업 나눠 줘 |
| build | `/my-skills:build docs/plans/x.md` | 이 계획대로 구현해 줘 |
| check | `/my-skills:check` | 다 됐는지 확인해 줘 |
| review | `/my-skills:review quant docs/plans/x.md` | 이 계획 검토해 줘 |
| finish | `/my-skills:finish` | 마무리하자 |
| research | `/my-skills:research 백테스트 라이브러리 비교` | 백테스트 라이브러리 좀 찾아봐 |
| experiment | `/my-skills:experiment 샤프 비율 1.5` | 샤프 비율 올려 봐 |
| handoff | `/my-skills:handoff pause` | 오늘은 여기까지 |
| guard | `/my-skills:guard status` | 위험한 명령 막아 줘 |
| diagnose | `/my-skills:diagnose 저장하면 500 에러` | 저장하면 500 에러 나 |
| design | `/my-skills:design 설정 화면` | 설정 화면 예쁘게 해 줘 |
| copy | `/my-skills:copy src/pages` | 문구 다듬어 줘 |
| docs | `/my-skills:docs --audit main` | 문서화해 줘 |
| unslop | `/my-skills:unslop README.md` | README AI 티 좀 빼 줘 |
