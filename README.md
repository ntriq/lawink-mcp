# LaWink MCP — 한국 법률 지식그래프 MCP

> **변호사가 쓰던 AI(Claude·ChatGPT·Gemini·Cursor)에 그대로 붙이는 한국 법률 온톨로지 서버.**
> 판례 16만 · 법령 조문 13만 · **관계 그래프 234만 건**을 추론 시점에 탐색. 무료.

한국 판례·법령은 **검색**보다 **관계**가 핵심입니다. "이 판례가 인용한 조문", "이 조문을 적용한 판례", "유사 판례 묶음"을 따라가야 쟁점이 확장됩니다. LaWink MCP는 이 관계 그래프(`entity_relations` 234만)와 의미 검색을 **MCP 표준**으로 노출해, 변호사가 **새 앱을 배우지 않고** 이미 쓰는 AI에 붙여 쓰게 합니다.

## 왜 다른가

- **검색이 아니라 그래프**: 키워드 매칭(commodity)을 넘어, 판례–법령–법원–사건유형을 잇는 온톨로지. `precedent_relations` 한 번에 인용 법령·유사 판례·참조 판례를 끌어옴.
- **BYOAI (Bring Your Own AI)**: 자체 앱·UI를 강요하지 않음. Claude Desktop·Cursor·기타 MCP 클라이언트 어디든 연결.
- **추론 시점 통합**: AI가 답변을 만드는 중에 실시간으로 근거 판례·조문을 끌어와 환각을 줄임.

## 빠른 시작 (1분)

> 데모 영상: _(준비중 — 연결~첫 질의까지 30초 가이드)_

**Claude Desktop** — `claude_desktop_config.json`에 추가:
```json
{
  "mcpServers": {
    "lawink": {
      "command": "uvx",
      "args": ["lawink-mcp"],
      "env": { "LAWINK_API_BASE": "https://api.lawink.co.kr" }
    }
  }
}
```
> PyPI 배포 전이면 소스 설치: repo clone 후
> `command`: `/path/to/lawink-mcp/.venv/bin/python`, `args`: `["-m", "lawink_mcp.server"]`

**Cursor / 기타 MCP 클라이언트**: 동일하게 `lawink-mcp`를 stdio MCP 서버로 등록.

재시작하면 `lawink_*` 도구 6종이 뜹니다. 인증·API 키 없이 바로 사용.

## 도구 (6종, 무료·인증 불필요)

| 도구 | 하는 일 |
|------|---------|
| `lawink_ontology_stats` | 지식그래프 전체 규모(엔티티·관계 타입별 건수) |
| `lawink_ontology_graph` | 판례·법령 중심의 관계 이웃(노드+엣지) 탐색 |
| `lawink_precedent_relations` | **한 판례의 모든 관계** — 인용 법령(cites)·유사 판례·참조 판례·법원·사건유형 |
| `lawink_statute_precedents` | **이 법령 조문을 적용한 판례 목록** (법령→판례 추적) |
| `lawink_precedent_semantic_search` | 자연어 사안 → 유사 판례 (16만, 임베딩) |
| `lawink_statute_semantic_search` | 자연어 사안 → 관련 법령 조문 (13만, 임베딩) |

## 변호사 워크플로우 예시

> **사안**: "임대차 종료 후 임대인이 원상회복 비용으로 보증금 공제를 주장."

1. `precedent_semantic_search("임대차 보증금 반환 원상회복 비용 공제")`
   → 유사 판례 + 각 판례의 `precedent_id`
2. `precedent_relations(precedent_id)`
   → 그 판례가 **인용한 법령**(예: 민법 제615·618·654조) + 유사·참조 판례를 한 번에
3. 필요하면 `statute_precedents(statute_id)`로 "그 조문을 적용한 다른 판례들"까지 확장

> 💡 **팁**: 근거 **조문**이 필요할 때는 법령 직접검색보다 **판례 검색 → `precedent_relations`의 인용 법령**으로 도출하는 경로가 더 정확합니다. (법령 의미검색은 현재 어휘 편향이 있어 개선 중 — 유사도 점수를 신뢰지표로 쓰지 마세요.)

## 요금

| 플랜 | 대상 | 내용 | 가격 |
|------|------|------|------|
| **무료** | 누구나 | 위 6도구, 그래프·시맨틱 검색 | ₩0 |
| **Pro** _(출시 예정)_ | 개인 변호사 | 추가 데이터셋(경매·부동산·세무 등) + 우선 지원 | **월 ₩19,000~** (사전 문의 환영) |
| **로펌 맞춤** | 로펌·법무팀 | 사건 DB 연동·맞춤 온톨로지 구축·납품 | 견적 |

> 📈 **데이터·도구는 계속 추가됩니다** — 경매·부동산·세무·계약 등 LaWink 백엔드의 공개 데이터를 순차 노출 예정. 원하는 데이터·기능이 있으면 알려주세요.

## 문의 / 사업 제휴

- 이메일: **support@ntriq.co.kr**
- Pro 사전 신청, 로펌 맞춤 구축, 데이터 요청 모두 환영합니다.

## 데이터 출처 · 면책

- 판례·법령: 법제처 국가법령정보센터(law.go.kr) 등 공개 데이터 기반.
- 본 서비스는 **법률 정보 제공 도구**이며 법률 자문이 아닙니다. 시행일·개정·최신성은 원문 확인 필수.
- 의뢰인 사건 등 비공개 데이터는 노출되지 않습니다(공개 그래프만).

## 만든 사람

**김대환** — ntriq(엔트릭) 창업자
한국 법률 데이터를 AI에 연결합니다. 문의·제휴: support@ntriq.co.kr

## 라이선스

MIT © ntriq

---

_LaWink — by 김대환, ntriq(엔트릭). 한국 법률 데이터를 AI에 연결합니다._
