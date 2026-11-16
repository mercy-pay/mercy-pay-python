import asyncio
import json
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote

import httpx

from ._errors import ApiError, ConnectionError
from ._version import VERSION

DEFAULT_BASE_URL = "https://mercy-pay.com"


def _query_pairs(params: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Nested parameters the way the API reads them: created[gte]=…, expand[]=…"""
    pairs: List[Tuple[str, str]] = []

    def add(key: str, value: Any) -> None:
        if value is None:
            return
        if isinstance(value, bool):
            pairs.append((key, "true" if value else "false"))
        elif isinstance(value, (list, tuple)):
            for item in value:
                add(f"{key}[]", item)
        elif isinstance(value, dict):
            for child, nested in value.items():
                add(f"{key}[{child}]", nested)
        else:
            pairs.append((key, str(value)))

    for key, value in params.items():
        add(key, value)
    return pairs


class _Base:
    def __init__(self, api_key: str, base_url: Optional[str], timeout: float, max_retries: int) -> None:
        if not api_key:
            raise ValueError("Clé API manquante : passez votre clé mp_sandbox_… ou mp_live_….")
        self._api_key = api_key
        self._base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self._timeout = timeout
        self._max_retries = max(0, max_retries)

    def _prepare(self, method: str, path: str, params: Dict[str, Any], idempotency_key: Optional[str]) -> Dict[str, Any]:
        verb = method.upper()
        clean = path.lstrip("/")
        for prefix in ("api/v1/", "v1/"):
            if clean.startswith(prefix):
                clean = clean[len(prefix):]
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json",
            "User-Agent": f"mercy-pay-python/{VERSION}",
        }
        request: Dict[str, Any] = {"method": verb, "url": f"{self._base_url}/api/v1/{clean}", "headers": headers}
        if verb in ("GET", "DELETE"):
            request["params"] = _query_pairs(params)
        else:
            headers["Content-Type"] = "application/json"
            request["content"] = json.dumps(params, ensure_ascii=False).encode("utf-8")
        if verb == "POST":
            headers["Idempotency-Key"] = idempotency_key or f"py_{uuid.uuid4().hex}"
        return request

    @staticmethod
    def _retryable(response: httpx.Response) -> bool:
        return response.status_code == 429 or response.status_code >= 500

    @staticmethod
    def _backoff(attempt: int, retry_after: Optional[str]) -> float:
        if retry_after is not None and retry_after.isdigit():
            return float(min(int(retry_after), 60))
        return 0.5 * (2 ** (attempt - 1))

    @staticmethod
    def _decode(response: httpx.Response) -> Dict[str, Any]:
        try:
            body = response.json() if response.content else {}
        except ValueError:
            body = {}
        if response.status_code >= 400:
            raise ApiError.from_response(response.status_code, body, response.headers.get("Request-Id"))
        return body if isinstance(body, dict) else {}


class SyncTransport(_Base):
    def __init__(self, api_key: str, base_url: Optional[str], timeout: float, max_retries: int, http_client: Optional[httpx.Client], sleep: Any) -> None:
        super().__init__(api_key, base_url, timeout, max_retries)
        self._http = http_client or httpx.Client(timeout=timeout)
        self._sleep = sleep or time.sleep

    def request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        prepared = self._prepare(method, path, params or {}, idempotency_key)
        attempt = 0
        while True:
            try:
                response = self._http.request(**prepared)
            except httpx.TransportError as error:
                if attempt >= self._max_retries:
                    raise ConnectionError(f"Mercy Pay n'a pas pu être joint : {error}") from error
                attempt += 1
                self._sleep(self._backoff(attempt, None))
                continue
            if self._retryable(response) and attempt < self._max_retries:
                attempt += 1
                self._sleep(self._backoff(attempt, response.headers.get("Retry-After")))
                continue
            return self._decode(response)


class AsyncTransport(_Base):
    def __init__(self, api_key: str, base_url: Optional[str], timeout: float, max_retries: int, http_client: Optional[httpx.AsyncClient], sleep: Any) -> None:
        super().__init__(api_key, base_url, timeout, max_retries)
        self._http = http_client or httpx.AsyncClient(timeout=timeout)
        self._sleep = sleep or asyncio.sleep

    async def request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        prepared = self._prepare(method, path, params or {}, idempotency_key)
        attempt = 0
        while True:
            try:
                response = await self._http.request(**prepared)
            except httpx.TransportError as error:
                if attempt >= self._max_retries:
                    raise ConnectionError(f"Mercy Pay n'a pas pu être joint : {error}") from error
                attempt += 1
                await self._sleep(self._backoff(attempt, None))
                continue
            if self._retryable(response) and attempt < self._max_retries:
                attempt += 1
                await self._sleep(self._backoff(attempt, response.headers.get("Retry-After")))
                continue
            return self._decode(response)

    async def aclose(self) -> None:
        await self._http.aclose()


def encode_id(value: str) -> str:
    return quote(str(value), safe="")
