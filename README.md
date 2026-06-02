# LaWink MCP

한국 법률 **온톨로지·판례 지식그래프**를 Claude Desktop(및 MCP 호환 AI)에 붙이는 MCP 서버.

류승인 `korean-law-mcp`(법령 키워드 검색 = commodity) 위에, **entity_relations 2.3M+ 관계 그래프**와 **임베딩 시맨틱 검색**으로 차별화. 변호사가 자기 AI에 붙여 판례-법령-사건 관계를 추론 시점에 탐색.

## MVP 도구 (공개, 인증 불필요)

| 도구 | 설명 | 백엔드 |
|------|------|--------|
| `lawink_ontology_stats` | 그래프 통계 (엔티티·관계 건수) | GET /ontology/stats |
| `lawink_ontology_graph` | 엔티티 중심 관계 이웃(노드+엣지) | GET /ontology/graph/{type}/{id} |
| `lawink_precedent_relations` | 판례의 모든 관계(인용법령·유사판례·법원·사건유형) | GET /ontology/precedent/{id}/relations |
| `lawink_statute_precedents` | 법령을 인용한 판례 목록(cited_by) | GET /ontology/statute/{id}/precedents |
| `lawink_precedent_semantic_search` | 판례 의미 검색 (166K, 임베딩) | POST /connectors/kr-court-precedents/semantic-search |
| `lawink_statute_semantic_search` | 법령 조문 의미 검색 (132K, 임베딩) | POST /connectors/kr-statute-law/semantic-search |

> 모든 경로는 ntriq-platform openapi로 검증됨. Pro 도구(등기·경매·CRM)는 후속 버전.

## 설치 (uvx)

```bash
uvx lawink-mcp   # PyPI 배포 후
```

Claude Desktop `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "lawink": {
      "command": "uvx",
      "args": ["lawink-mcp"],
      "env": { "LAWINK_API_BASE": "https://api.ntriq.co.kr" }
    }
  }
}
```

## 로컬 개발

```bash
cd lawink-mcp
pip install -e .
LAWINK_API_BASE=http://localhost:8080 python -m lawink_mcp.server
```

## 면책

본 MCP는 **정보 제공**용이며 법률 자문이 아닙니다. 검색·관계 결과는 참고 자료이고 최종 판단은 변호사 책임입니다.

## 라이선스

MIT © ntriq
