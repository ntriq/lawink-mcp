"""환경설정 — ntriq-platform 백엔드 relay 대상."""
import os

# 백엔드 base URL.
# - 로컬 개발: http://localhost:8080 (ntriq-gateway) 또는 :8000 (platform 직접)
# - 프로덕션:  https://api.ntriq.co.kr (gateway, Cloudflare)
API_BASE = os.getenv("LAWINK_API_BASE", "http://localhost:8080").rstrip("/")

# LaWink REST prefix (openapi 검증: /lawink/api/v1/...)
API_PREFIX = "/lawink/api/v1"

# 인증 (Pro 도구용. 공개 도구는 없어도 동작). gateway 외부 호출 시 X-API-Key.
API_KEY = os.getenv("LAWINK_API_KEY", "")

# HTTP 타임아웃 (초). 온톨로지 그래프/시맨틱검색은 다소 길 수 있음.
TIMEOUT = float(os.getenv("LAWINK_TIMEOUT", "60"))

SERVER_NAME = "lawink"
SERVER_VERSION = "0.1.0"
PROTOCOL_VERSION = "2024-11-05"
