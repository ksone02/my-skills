# 시도 기록 형식

`docs/experiments/<주제>/decision.tsv`, 탭으로 나눠요. 첫 줄은 정확히 아래 머리줄이에요.

```
id	hypothesis	change	before	after	delta	tests	verdict	note
1	수수료를 넣으면 회전율 높은 전략이 떨어진다	cost=0.1%	1.42	1.10	-0.32	pass	되돌림	샤프 비율, 2020-2024 표본 밖
```

- before, after, delta는 같은 단위(지표 정의에 적은 단위)로 써요.
- verdict는 `남김` 또는 `되돌림`.
- note에 노이즈 크기와 평가 구간을 적어요.
