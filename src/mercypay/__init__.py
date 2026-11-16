"""La bibliothèque Python officielle de l'API Mercy Pay."""

from typing import Any, Dict, Optional

import httpx

from . import webhooks
from ._client import AsyncTransport, SyncTransport
from ._errors import (
    ApiError,
    ApiServerError,
    AuthenticationError,
    ConnectionError,
    IdempotencyError,
    InvalidRequestError,
    MercyPayError,
    PaymentError,
    RateLimitError,
    SignatureVerificationError,
)
from ._object import MercyPayObject
from ._page import AsyncPage, Page
from ._resources import (
    AccountResource, AsyncAccountResource, AsyncBillingPortalResource, AsyncCheckoutSessionsResource, AsyncCustomersResource, AsyncEventsResource, AsyncFeesResource, AsyncInvoicesResource, AsyncPaymentLinksResource, AsyncPaymentsResource, AsyncPayoutsResource, AsyncPlansResource, AsyncProviderStatusResource, AsyncRefundsResource, AsyncRequestLogsResource, AsyncSubscriptionsResource, AsyncTestHelpersResource, AsyncWalletTransfersResource, AsyncWalletsResource, AsyncWebhookEndpointsResource, BillingPortalResource, CheckoutSessionsResource, CustomersResource, EventsResource, FeesResource, InvoicesResource, PaymentLinksResource, PaymentsResource, PayoutsResource, PlansResource, ProviderStatusResource, RefundsResource, RequestLogsResource, SubscriptionsResource, TestHelpersResource, WalletTransfersResource, WalletsResource, WebhookEndpointsResource,
)
from ._version import VERSION
from .webhooks import construct_event, verify_signature

__all__ = [
    "VERSION",
    "ApiError",
    "ApiServerError",
    "AsyncMercyPay",
    "AsyncPage",
    "AuthenticationError",
    "ConnectionError",
    "IdempotencyError",
    "InvalidRequestError",
    "MercyPay",
    "MercyPayError",
    "MercyPayObject",
    "Page",
    "PaymentError",
    "RateLimitError",
    "SignatureVerificationError",
    "construct_event",
    "verify_signature",
    "webhooks",
]


class MercyPay:
    """One client per API key. Keep the key on your server.

    >>> mercy_pay = MercyPay("mp_sandbox_…")
    >>> session = mercy_pay.checkout_sessions.create(amount=15000, currency="XAF")

    A network error, a 429 or a 5xx is retried; a POST always carries an Idempotency-Key,
    the same on every attempt, so a retry never creates twice.
    """

    webhooks = webhooks

    def __init__(self, api_key: str, *, base_url: Optional[str] = None, timeout: float = 30.0, max_retries: int = 2, http_client: Optional[httpx.Client] = None, _sleep: Any = None) -> None:
        self._transport = SyncTransport(api_key, base_url, timeout, max_retries, http_client, _sleep)
        self.account = AccountResource(self._transport)
        self.fees = FeesResource(self._transport)
        self.provider_status = ProviderStatusResource(self._transport)
        self.checkout_sessions = CheckoutSessionsResource(self._transport)
        self.payments = PaymentsResource(self._transport)
        self.refunds = RefundsResource(self._transport)
        self.wallets = WalletsResource(self._transport)
        self.wallet_transfers = WalletTransfersResource(self._transport)
        self.payouts = PayoutsResource(self._transport)
        self.payment_links = PaymentLinksResource(self._transport)
        self.plans = PlansResource(self._transport)
        self.customers = CustomersResource(self._transport)
        self.subscriptions = SubscriptionsResource(self._transport)
        self.invoices = InvoicesResource(self._transport)
        self.billing_portal = BillingPortalResource(self._transport)
        self.events = EventsResource(self._transport)
        self.webhook_endpoints = WebhookEndpointsResource(self._transport)
        self.request_logs = RequestLogsResource(self._transport)
        self.test_helpers = TestHelpersResource(self._transport)

    def request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        """Any call, for an endpoint this version does not know yet."""
        return self._transport.request(method, path, params, idempotency_key)


class AsyncMercyPay:
    """The async client: the same resources, each method awaited.

    >>> async with AsyncMercyPay("mp_sandbox_…") as mercy_pay:
    ...     session = await mercy_pay.checkout_sessions.create(amount=15000, currency="XAF")
    """

    webhooks = webhooks

    def __init__(self, api_key: str, *, base_url: Optional[str] = None, timeout: float = 30.0, max_retries: int = 2, http_client: Optional[httpx.AsyncClient] = None, _sleep: Any = None) -> None:
        self._transport = AsyncTransport(api_key, base_url, timeout, max_retries, http_client, _sleep)
        self.account = AsyncAccountResource(self._transport)
        self.fees = AsyncFeesResource(self._transport)
        self.provider_status = AsyncProviderStatusResource(self._transport)
        self.checkout_sessions = AsyncCheckoutSessionsResource(self._transport)
        self.payments = AsyncPaymentsResource(self._transport)
        self.refunds = AsyncRefundsResource(self._transport)
        self.wallets = AsyncWalletsResource(self._transport)
        self.wallet_transfers = AsyncWalletTransfersResource(self._transport)
        self.payouts = AsyncPayoutsResource(self._transport)
        self.payment_links = AsyncPaymentLinksResource(self._transport)
        self.plans = AsyncPlansResource(self._transport)
        self.customers = AsyncCustomersResource(self._transport)
        self.subscriptions = AsyncSubscriptionsResource(self._transport)
        self.invoices = AsyncInvoicesResource(self._transport)
        self.billing_portal = AsyncBillingPortalResource(self._transport)
        self.events = AsyncEventsResource(self._transport)
        self.webhook_endpoints = AsyncWebhookEndpointsResource(self._transport)
        self.request_logs = AsyncRequestLogsResource(self._transport)
        self.test_helpers = AsyncTestHelpersResource(self._transport)

    async def request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        """Any call, for an endpoint this version does not know yet."""
        return await self._transport.request(method, path, params, idempotency_key)

    async def aclose(self) -> None:
        await self._transport.aclose()

    async def __aenter__(self) -> "AsyncMercyPay":
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.aclose()
