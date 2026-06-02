"""LaWink MCP 서버 — 공식 mcp SDK(FastMCP) 기반. 한국 법률 온톨로지·판례를 AI에 노출.

ntriq-platform 백엔드(/lawink/api/v1/...)를 relay. 모든 경로 openapi 검증.
korean-law-mcp(키워드 검색=commodity) 대비 차별점: 온톨로지 그래프(2.3M 관계) + 시맨틱 검색.
FastMCP가 MCP 프로토콜(initialize/tools/list/tools/call, 2024-11-05+)을 표준대로 처리 →
Claude Desktop·ChatGPT·Gemini·Cursor 등 MCP 클라이언트와 호환.
"""
from mcp.server.fastmcp import FastMCP

from . import relay

mcp = FastMCP("lawink")


@mcp.tool(
    description="온톨로지 그래프 통계 (엔티티/관계 타입별 건수, 최근 동기 시각). "
    "한국 법률 지식그래프 전체 규모 현황 (entity_relations 230만+ 관계)."
)
async def lawink_ontology_stats() -> dict:
    return await relay.get("/ontology/stats")


@mcp.tool(
    description="지식그래프 조회: 판례·법령 등 엔티티 중심의 관계 이웃(노드+엣지). "
    "'이 판례가 인용한 법령', '유사 법령 조문', '이 법령을 다룬 판례' 등 추론에 사용. "
    "entity_type=precedent|statute|court|casetype|ministry|law, entity_id=UUID. "
    "공개 데이터만 노출 (의뢰인 사건 정보는 차단됨)."
)
async def lawink_ontology_graph(entity_type: str, entity_id: str, depth: int = 1) -> dict:
    return await relay.get(
        f"/ontology/graph/{entity_type}/{entity_id}", {"depth": depth}
    )


@mcp.tool(
    description="특정 판례의 모든 온톨로지 관계 (인용 법령 cites, 유사 판례 similar_to, "
    "참조 references, 사건유형 of_type, 법원 decided_by). precedent_id=판례 UUID."
)
async def lawink_precedent_relations(precedent_id: str) -> dict:
    return await relay.get(f"/ontology/precedent/{precedent_id}/relations")


@mcp.tool(
    description="특정 법령 조문을 인용한 판례 목록 ('이 법령을 적용한 판례들'). "
    "statute_id=법령 조문 UUID. 변호사 핵심 기능 — 법령→판례 추적."
)
async def lawink_statute_precedents(statute_id: str, skip: int = 0, limit: int = 50) -> dict:
    return await relay.get(
        f"/ontology/statute/{statute_id}/precedents", {"skip": skip, "limit": limit}
    )


@mcp.tool(
    description="판례 시맨틱(의미) 검색 — 임베딩 기반. 키워드가 아니라 사안의 의미로 "
    "유사 판례 검색 (16만 판례). query=자연어 사안/질의. (Pro: 인증 필요할 수 있음)"
)
async def lawink_precedent_semantic_search(query: str, limit: int = 10) -> dict:
    return await relay.post(
        "/connectors/kr-court-precedents/semantic-search", {"query": query, "limit": limit}
    )


@mcp.tool(
    description="법령 조문 시맨틱(의미) 검색 — 임베딩 기반. 사안 설명으로 관련 법령 조문 "
    "검색 (13만 조문). query=자연어 사안/질의. (Pro: 인증 필요할 수 있음)"
)
async def lawink_statute_semantic_search(query: str, limit: int = 10) -> dict:
    return await relay.post(
        "/connectors/kr-statute-law/semantic-search", {"query": query, "limit": limit}
    )


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
