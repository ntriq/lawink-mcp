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
    description="판례 시맨틱(의미) 검색 — 임베딩 기반(공개, 인증 불필요). 사안의 의미로 "
    "유사 판례 검색 (16만 판례). 모든 분야에서 선도 판례를 상위에 올리는 검증된 강점 도구. "
    "query=자연어 사안/질의. "
    "결과의 precedent_id를 lawink_precedent_relations에 넣어 인용 법령·유사 판례로 확장. "
    "★근거 법령 조문이 필요할 때는 lawink_statute_semantic_search로 법령을 직접 찾기보다, "
    "이 도구로 유사 판례를 먼저 찾은 뒤 lawink_precedent_relations의 cites(인용 법령)에서 "
    "조문을 도출하는 경로가 더 정확하다(권장 워크플로우)."
)
async def lawink_precedent_semantic_search(query: str, limit: int = 10) -> dict:
    return await relay.post("/precedent-search/similar", {"query": query, "top_k": limit})


@mcp.tool(
    description="★★사안 → 근거 법령 도출 (변호사용 기본·1차 진입점). 근거 조문이 필요하면 이 도구를 "
    "먼저 쓴다. 자연어 사안을 넣으면 ① 유사 판례를 찾고 ② 그 판례들이 실제 인용한 법령(cites)을 "
    "빈도순으로 반환한다. 법령 직접 시맨틱 검색(lawink_statute_semantic_search)의 어휘 편향을 우회하므로 "
    "근거 조문 도출에는 이 도구가 더 정확하다(검증: 임대차 → 민법 제618·615·654조 정확 도출). "
    "각 법령에 출처 판례가 함께 붙는다. query=자연어 사안/질의."
)
async def lawink_statute_by_precedent(query: str, limit: int = 10) -> dict:
    return await relay.post("/precedent-search/statute-by-precedent", {"query": query, "top_k": limit})


@mcp.tool(
    description="⚠️[보조·실험적 — 변호사 업무용 1차 도구로 쓰지 말 것] 법령 조문 직접 시맨틱 검색 "
    "(임베딩, 13만 조문). 어휘 매칭 편향이 있어 1위 결과가 사안과 무관한 법령(예: 세법·절차규칙)일 "
    "수 있고, similarity_score(0.84~0.89 좁은 구간에 뭉침)는 신뢰도 지표가 아니다. "
    "★사안 → 근거 조문이 필요하면 반드시 lawink_statute_by_precedent를 먼저 쓸 것 "
    "(유사 판례가 실제 인용한 법령을 빈도순·출처판례와 함께 한 번에 반환 — 예: 임대차 → 민법 제618·615·654조). "
    "이 도구는 위 경로로 안 잡히는 조문을 보조 탐색할 때만 사용. query=자연어 사안/질의. "
    "결과의 statute_id는 lawink_statute_precedents에 넣어 '이 법령을 적용한 판례'로 확장 가능."
)
async def lawink_statute_semantic_search(query: str, limit: int = 10) -> dict:
    return await relay.post("/statute-search/similar", {"query": query, "top_k": limit})


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
