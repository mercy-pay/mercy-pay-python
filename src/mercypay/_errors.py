from typing import Any, Dict, List, Optional


class MercyPayError(Exception):
    """Everything this library raises."""


class ApiError(MercyPayError):
    """An error answered by the API. Branch on ``code`` (stable), never on ``message``.
    Quote ``request_id`` to the Mercy Pay support."""

    def __init__(self, status: int, body: Dict[str, Any], request_id: Optional[str]) -> None:
        self.status = status
        self.type: Optional[str] = body.get("type")
        self.code: Optional[str] = body.get("code")
        self.param: Optional[str] = body.get("param")
        self.request_id: Optional[str] = body.get("request_id") or request_id
        self.errors: Dict[str, List[str]] = body.get("errors") or {}
        self.raw = body
        super().__init__(body.get("message") or f"Mercy Pay a répondu {status}.")

    @staticmethod
    def from_response(status: int, body: Any, request_id: Optional[str]) -> "ApiError":
        error = body.get("error") if isinstance(body, dict) else None
        error = error if isinstance(error, dict) else {}
        kind = error.get("type")
        if kind == "authentication_error" or status == 401:
            return AuthenticationError(status, error, request_id)
        if kind == "rate_limit_error" or status == 429:
            return RateLimitError(status, error, request_id)
        if kind == "idempotency_error":
            return IdempotencyError(status, error, request_id)
        if kind == "payment_error":
            return PaymentError(status, error, request_id)
        if status >= 500 or kind == "api_error":
            return ApiServerError(status, error, request_id)
        return InvalidRequestError(status, error, request_id)


class AuthenticationError(ApiError):
    """A missing, wrong or revoked key, or live mode before the account is verified."""


class InvalidRequestError(ApiError):
    """A refused parameter, an object not found, an action not allowed."""


class PaymentError(ApiError):
    """Refused by the operator or the bank, or a balance too low."""


class IdempotencyError(ApiError):
    """The idempotency key is missing, reused with other content, or still in use."""


class RateLimitError(ApiError):
    """Too many requests: slow down."""


class ApiServerError(ApiError):
    """A problem on Mercy Pay's side. Retry later with the same idempotency key."""


class ConnectionError(MercyPayError):  # noqa: A001 - the name users expect
    """No answer from Mercy Pay. Send the request again with the same idempotency key."""


class SignatureVerificationError(MercyPayError):
    """A webhook whose signature is missing, wrong or too old: answer 400 and ignore it."""
