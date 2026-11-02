# 부르기 시험

임시 저장소에서 새 세션에 한 줄씩 보내요. 왼쪽 말에는 그 스킬이 떠야 하고, 오른쪽 말에는 my-skills 스킬이 뜨면 안 돼요.

결과는 `evals/results/routing-<날짜>.md`에 남겨요.

| 스킬 | 떠야 하는 말 |
|---|---|
| shape | 동네 산책 기록 앱 만들고 싶은데 아직 아이디어가 흐릿해. 같이 구체화해줘 |
| plan | docs/spec.md 명세로 구현 계획 세워줘 |
| build | docs/plan.md 계획대로 구현해줘 |
| check | docs/spec.md 완료 조건대로 다 됐는지 검증해줘 |
| review | docs/spec.md 전문가 검토해줘 |
| finish | 이 작업 마무리해줘 |
| research | 파이썬 백테스트 라이브러리 비교 조사해줘 |
| experiment | calc.py 속도 지표 올려줘. 실험 돌려줘 |
| handoff | 여기까지 하고 멈출게. 다음 세션에서 이어가게 정리해줘 |
| guard | 위험한 명령 막아줘 |
| diagnose | calc.py add가 가끔 이상한 값을 내는데 원인을 모르겠어 |
| design | 설정 화면 대시보드 만들어줘 |
| copy | page.html 화면 문구 다듬어줘 |
| unslop | README AI 티 좀 빼줘 |
| docs | 이 프로젝트 문서화해줘 |

이어지는 대화(첫 말 다음에 같은 세션으로 둘째 말을 보내요):

| 떠야 하는 스킬 | 첫 말 | 둘째 말 |
|---|---|---|
| plan 또는 design | 기능 정리 끝났어. 명세는 docs/spec.md야. 읽어만 봐 | 다른 할 거 없으면 바로 구현 들어가 |
| handoff 또는 design | docs/progress/HANDOFF.md 읽어줘. 아직 아무것도 하지 마 | 이어서 진행해 |
| build | docs/plan.md 읽고 무슨 작업들인지 한 줄로 요약해줘. 아직 아무것도 만들지 마 | ㅇㅋ 만들자 |
| design | docs/spec.md에 있는 설정 화면을 어떤 느낌으로 할지 한 줄로 말해줘. 아직 만들지 마 | ㅇㅋ 그 화면 만들자 |
| research | 백테스트 라이브러리는 뭐가 좋을지 네 생각만 한 줄로 말해줘. 검색은 하지 마 | ㅇㅇ 근거 제대로 찾아봐 |
| check | calc.py에 add 있는지 봐줘 | ㅇㅋ 그럼 명세대로 다 된 거 맞아? |
| 없음 | calc.py가 뭐 하는 파일인지 한 줄로 말해줘 | ㅇㅋ add 이름을 plus로 바꿔 |
| 없음 | page.html 버튼 색이 뭐야? | ㅇㅇ 파랗게 바꿔 |

뜨면 안 되는 말:

- calc.py의 add 함수 이름을 plus로 바꿔줘
- calc.py에 subtract 함수 추가해줘
- calc.py 좀 봐줘
- add 함수가 뭐 하는 거야?
- page.html 버튼 색 파랗게 바꿔줘
- page.html 버튼 문구 확인을 저장으로 바꿔줘
- git status 보여줘
- python으로 add(1, 2) 결과 돌려봐
