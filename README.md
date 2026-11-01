# my-skills

개발과 연구를 같이 하는 사람을 위한 Claude Code 스킬 묶음이에요. Superpowers를 대신하려고 만들었어요.

- 슬래시 없이 말로 해도 스킬이 떠요. 작은 수정에는 뜨지 않게 설명에 조건을 적었고, 비싼 `build`와 `review`는 시작 전에 확인받아요.
- 피드백은 두 종류예요. 싼 대조 검사는 자주, 비싼 전문가 검토는 기획 직후와 설계 직후에만 해요.
- 검색은 DeepSeek, 검증은 Codex에 맡기고, 안 되면 Claude로 넘어가요.

설계 문서: [docs/superpowers/specs/2026-11-01-skillset-design.md](docs/superpowers/specs/2026-11-01-skillset-design.md)

## 설치

```text
/plugin marketplace add ~/Desktop/develop/my-skills
/plugin install my-skills@my-skills
```

GitHub에 올린 뒤에는 `/plugin install my-skills --marketplace ksone02/my-skills` 한 줄로 설치할 수 있어요.

### 상시 원칙 (선택, 권장)

스킬을 부르지 않아도 지킬 원칙 7줄을 `~/.claude/CLAUDE.md`에 넣어요. 넣기 전에 [rules/always.md](rules/always.md)를 읽어 보세요.

```sh
python3 scripts/always.py install   # 넣기 (두 번 해도 하나만 남아요)
python3 scripts/always.py remove    # 빼기 (블록 바깥은 그대로)
```

## 스킬

| 스킬 | 하는 일 |
|---|---|
| `shape` | 흐릿한 아이디어를 질문으로 구체화해 완료 조건 목록이 있는 명세로 만들어요 |
| `plan` | 명세를 위험한 것부터 배치한 작업 단위로 나눠요 |
| `build` | 하위 에이전트로 구현하고 작업마다 검토해요 |
| `check` | 완료 조건을 대조하고 실행으로 증명해요 (Codex → Claude) |
| `review` | 분야 전문가 역할 여러 명이 한 번에 검토해요 (퀀트, 웹, 데이터 연구) |
| `finish` | 결과물을 다시 확인하고 정리해요 |
| `research` | 조사 계획 → 넓게 → 방향 고르기 → 깊게 → 파일 하나 |
| `experiment` | 지표 하나를 반복 실험으로 올려요. 시도마다 기록하고 남기거나 되돌려요 |
| `handoff` | 멈추기, 이어 가기, 결정 기록 |
| `guard` | 위험한 명령 앞에서 확인을 묻는 훅을 켜고 꺼요 (기본 꺼짐) |
| `diagnose` | 실패하는 확인 장치부터 만드는 버그 진단 |
| `design` | 대시보드·도구 화면을 세 폭으로 재며 만들어요. 랜딩은 taste-skill에 맡겨요 |
| `copy` | 화면 문구를 모아 점검하고 승인한 것만 고쳐요 |
| `docs` | 코드를 읽고 문서를 쓰거나, 문서와 코드가 어긋난 곳을 고쳐요 |
| `unslop` | 글의 AI 티를 지워요. 한국어 긴 글은 humanize-korean으로 마무리해요 |

부를 때는 `/my-skills:<스킬> <인자>`예요. 예: `/my-skills:research 파이썬 백테스트 라이브러리 비교`.

## 외부 도구

| 도구 | 쓰는 곳 | 없으면 |
|---|---|---|
| `codex` | `check`, `review`(선택) | Claude 하위 에이전트가 독립 조건을 지켜 검사하고, 결과 첫 줄에 "Codex 사용 불가, Claude로 검증"이라고 적어요 |
| `aside` (DeepSeek) | `research` | Claude haiku가 검색하고 "DeepSeek 사용 불가, Claude로 조사"라고 적어요 |
| Chrome + uv | `design`, `check`의 화면 측정 | 측정 스크립트가 설치 방법을 알려 줘요 |
| taste-skill | `design --landing` | 설치 명령을 알려 줘요 |
| humanize-korean | `unslop` | 그 단계를 건너뛰고 알려 줘요 |

외부로 보내는 파일은 [scripts/safe_files.py](scripts/safe_files.py)가 걸러요. 데이터 폴더, `.env`, 데이터 파일, 큰 파일, 키가 든 파일은 빠져요. 프로젝트 `CLAUDE.md`에 "외부 AI 금지" 같은 문구가 있으면 외부 모델을 쓰지 않아요.

## 개발

```sh
uv sync
uv run pytest                                       # 스크립트와 스킬 형식 시험
uv run --with playwright==1.49.1 pytest             # 화면 측정 시험까지
claude --plugin-dir . plugin details my-skills      # 스킬 목록과 토큰 비용
```

행동 시험은 [evals/](evals/README.md)에 있어요.

## 라이선스

MIT. 참고한 저장소와 저작권은 [NOTICE.md](NOTICE.md)에 있어요.
