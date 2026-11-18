"""Généré par scripts/generate.py depuis la référence de l'API. Ne pas modifier à la main."""

from typing import TYPE_CHECKING, Any, Optional

from typing_extensions import Unpack

from . import _params
from ._helpers import WaitMixin, AsyncWaitMixin
from ._client import encode_id
from ._object import MercyPayObject
from ._page import AsyncPage, Page

if TYPE_CHECKING:
    from ._client import AsyncTransport, SyncTransport


class AccountResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def retrieve(self, **params: Unpack[_params.GetAccountParams]) -> MercyPayObject:
        """Lire le compte. GET /api/v1/account"""
        body = self._transport.request("GET", "account", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})


class FeesResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def quote(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateFeeQuoteParams]) -> MercyPayObject:
        """Calculer les frais d'un paiement. POST /api/v1/fees/quote"""
        body = self._transport.request("POST", "fees/quote", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})


class ProviderStatusResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def retrieve(self, **params: Unpack[_params.GetProviderStatusParams]) -> MercyPayObject:
        """État des opérateurs. GET /api/v1/provider_status"""
        body = self._transport.request("GET", "provider_status", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})


class CheckoutSessionsResource(WaitMixin):
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateCheckoutSessionParams]) -> MercyPayObject:
        """Créer une session. POST /api/v1/checkout_sessions"""
        body = self._transport.request("POST", "checkout_sessions", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def list(self, **params: Unpack[_params.ListCheckoutSessionsParams]) -> Page:
        """Lister les sessions. GET /api/v1/checkout_sessions"""
        return self._list("checkout_sessions", params)

    def retrieve(self, id: str, **params: Unpack[_params.GetCheckoutSessionParams]) -> MercyPayObject:
        """Lire une session. GET /api/v1/checkout_sessions/{id}"""
        body = self._transport.request("GET", f"checkout_sessions/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def expire(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.ExpireCheckoutSessionParams]) -> MercyPayObject:
        """Expirer une session. POST /api/v1/checkout_sessions/{id}/expire"""
        body = self._transport.request("POST", f"checkout_sessions/{encode_id(id)}/expire", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def wait_for_completion(self, id: str, *, timeout: float = 120.0, interval: float = 2.0) -> MercyPayObject:
        """Reads the session until it is completed, expired or cancelled, in seconds."""
        from ._helpers import FINAL_SESSION_STATUSES

        return self._poll(lambda: self.retrieve(id), FINAL_SESSION_STATUSES, timeout, interval, f"La session {id}")

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class PaymentsResource(WaitMixin):
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreatePaymentParams]) -> MercyPayObject:
        """Encaisser un paiement. POST /api/v1/payments"""
        body = self._transport.request("POST", "payments", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def list(self, **params: Unpack[_params.ListPaymentsParams]) -> Page:
        """Lister les paiements. GET /api/v1/payments"""
        return self._list("payments", params)

    def retrieve(self, id: str, **params: Unpack[_params.GetPaymentParams]) -> MercyPayObject:
        """Lire un paiement. GET /api/v1/payments/{id}"""
        body = self._transport.request("GET", f"payments/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def refund(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateRefundParams]) -> MercyPayObject:
        """Rembourser un paiement. POST /api/v1/payments/{id}/refunds"""
        body = self._transport.request("POST", f"payments/{encode_id(id)}/refunds", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def wait_for_final_status(self, id: str, *, timeout: float = 120.0, interval: float = 2.0) -> MercyPayObject:
        """Reads the payment until it is final (succeeded, failed, canceled, expired…), in seconds. On a server, prefer the payment.succeeded webhook."""
        from ._helpers import FINAL_PAYMENT_STATUSES

        return self._poll(lambda: self.retrieve(id), FINAL_PAYMENT_STATUSES, timeout, interval, f"Le paiement {id}")

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class RefundsResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def list(self, **params: Unpack[_params.ListRefundsParams]) -> Page:
        """Lister les remboursements. GET /api/v1/refunds"""
        return self._list("refunds", params)

    def retrieve(self, id: str, **params: Unpack[_params.GetRefundParams]) -> MercyPayObject:
        """Lire un remboursement. GET /api/v1/refunds/{id}"""
        body = self._transport.request("GET", f"refunds/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def cancel(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CancelRefundParams]) -> MercyPayObject:
        """Annuler un remboursement retardé. POST /api/v1/refunds/{id}/cancel"""
        body = self._transport.request("POST", f"refunds/{encode_id(id)}/cancel", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class WalletsResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def list(self, **params: Unpack[_params.ListWalletsParams]) -> Page:
        """Lire les soldes. GET /api/v1/wallets"""
        return self._list("wallets", params)

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class WalletTransfersResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def list(self, **params: Unpack[_params.ListWalletTransfersParams]) -> Page:
        """Lister les virements entre soldes. GET /api/v1/wallet_transfers"""
        return self._list("wallet_transfers", params)

    def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateWalletTransferParams]) -> MercyPayObject:
        """Virer entre deux soldes. POST /api/v1/wallet_transfers"""
        body = self._transport.request("POST", "wallet_transfers", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class PayoutsResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreatePayoutParams]) -> MercyPayObject:
        """Demander un retrait. POST /api/v1/payouts"""
        body = self._transport.request("POST", "payouts", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def list(self, **params: Unpack[_params.ListPayoutsParams]) -> Page:
        """Lister les retraits. GET /api/v1/payouts"""
        return self._list("payouts", params)

    def retrieve(self, id: str, **params: Unpack[_params.GetPayoutParams]) -> MercyPayObject:
        """Lire un retrait. GET /api/v1/payouts/{id}"""
        body = self._transport.request("GET", f"payouts/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class PaymentLinksResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreatePaymentLinkParams]) -> MercyPayObject:
        """Créer un lien. POST /api/v1/payment_links"""
        body = self._transport.request("POST", "payment_links", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def list(self, **params: Unpack[_params.ListPaymentLinksParams]) -> Page:
        """Lister les liens. GET /api/v1/payment_links"""
        return self._list("payment_links", params)

    def retrieve(self, id: str, **params: Unpack[_params.GetPaymentLinkParams]) -> MercyPayObject:
        """Lire un lien. GET /api/v1/payment_links/{id}"""
        body = self._transport.request("GET", f"payment_links/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def update(self, id: str, **params: Unpack[_params.UpdatePaymentLinkParams]) -> MercyPayObject:
        """Modifier un lien. PATCH /api/v1/payment_links/{id}"""
        body = self._transport.request("PATCH", f"payment_links/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def delete(self, id: str, **params: Unpack[_params.DeletePaymentLinkParams]) -> MercyPayObject:
        """Supprimer un lien. DELETE /api/v1/payment_links/{id}"""
        body = self._transport.request("DELETE", f"payment_links/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def archive(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.ArchivePaymentLinkParams]) -> MercyPayObject:
        """Archiver un lien. POST /api/v1/payment_links/{id}/archive"""
        body = self._transport.request("POST", f"payment_links/{encode_id(id)}/archive", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def payments(self, id: str, **params: Unpack[_params.ListPaymentLinkPaymentsParams]) -> Page:
        """Paiements d'un lien. GET /api/v1/payment_links/{id}/payments"""
        return self._list(f"payment_links/{encode_id(id)}/payments", params)

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class PlansResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreatePlanParams]) -> MercyPayObject:
        """Créer un plan. POST /api/v1/plans"""
        body = self._transport.request("POST", "plans", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def list(self, **params: Unpack[_params.ListPlansParams]) -> Page:
        """Lister les plans. GET /api/v1/plans"""
        return self._list("plans", params)

    def retrieve(self, id: str, **params: Unpack[_params.GetPlanParams]) -> MercyPayObject:
        """Lire un plan. GET /api/v1/plans/{id}"""
        body = self._transport.request("GET", f"plans/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def update(self, id: str, **params: Unpack[_params.UpdatePlanParams]) -> MercyPayObject:
        """Modifier un plan. PATCH /api/v1/plans/{id}"""
        body = self._transport.request("PATCH", f"plans/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def delete(self, id: str, **params: Unpack[_params.DeletePlanParams]) -> MercyPayObject:
        """Supprimer un plan. DELETE /api/v1/plans/{id}"""
        body = self._transport.request("DELETE", f"plans/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def archive(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.ArchivePlanParams]) -> MercyPayObject:
        """Archiver un plan. POST /api/v1/plans/{id}/archive"""
        body = self._transport.request("POST", f"plans/{encode_id(id)}/archive", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def restore(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.RestorePlanParams]) -> MercyPayObject:
        """Réactiver un plan. POST /api/v1/plans/{id}/restore"""
        body = self._transport.request("POST", f"plans/{encode_id(id)}/restore", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class CustomersResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateCustomerParams]) -> MercyPayObject:
        """Créer un client. POST /api/v1/customers"""
        body = self._transport.request("POST", "customers", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def list(self, **params: Unpack[_params.ListCustomersParams]) -> Page:
        """Lister les clients. GET /api/v1/customers"""
        return self._list("customers", params)

    def retrieve(self, id: str, **params: Unpack[_params.GetCustomerParams]) -> MercyPayObject:
        """Lire un client. GET /api/v1/customers/{id}"""
        body = self._transport.request("GET", f"customers/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def update(self, id: str, **params: Unpack[_params.UpdateCustomerParams]) -> MercyPayObject:
        """Modifier un client. PATCH /api/v1/customers/{id}"""
        body = self._transport.request("PATCH", f"customers/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def delete(self, id: str, **params: Unpack[_params.DeleteCustomerParams]) -> MercyPayObject:
        """Supprimer un client. DELETE /api/v1/customers/{id}"""
        body = self._transport.request("DELETE", f"customers/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def payment_methods(self, customer_id: str, **params: Unpack[_params.ListCustomerPaymentMethodsParams]) -> Page:
        """Moyens de paiement d'un client. GET /api/v1/customers/{id}/payment_methods"""
        return self._list(f"customers/{encode_id(customer_id)}/payment_methods", params)

    def set_default_payment_method(self, customer_id: str, payment_method_id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.SetDefaultPaymentMethodParams]) -> MercyPayObject:
        """Choisir le moyen par défaut. POST /api/v1/customers/{id}/payment_methods/{id}/default"""
        body = self._transport.request("POST", f"customers/{encode_id(customer_id)}/payment_methods/{encode_id(payment_method_id)}/default", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def remove_payment_method(self, customer_id: str, payment_method_id: str, **params: Unpack[_params.RemovePaymentMethodParams]) -> MercyPayObject:
        """Retirer un moyen de paiement. DELETE /api/v1/customers/{id}/payment_methods/{id}"""
        body = self._transport.request("DELETE", f"customers/{encode_id(customer_id)}/payment_methods/{encode_id(payment_method_id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class SubscriptionsResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateSubscriptionParams]) -> MercyPayObject:
        """Créer un abonnement. POST /api/v1/subscriptions"""
        body = self._transport.request("POST", "subscriptions", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def list(self, **params: Unpack[_params.ListSubscriptionsParams]) -> Page:
        """Lister les abonnements. GET /api/v1/subscriptions"""
        return self._list("subscriptions", params)

    def retrieve(self, id: str, **params: Unpack[_params.GetSubscriptionParams]) -> MercyPayObject:
        """Lire un abonnement. GET /api/v1/subscriptions/{id}"""
        body = self._transport.request("GET", f"subscriptions/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def update(self, id: str, **params: Unpack[_params.UpdateSubscriptionParams]) -> MercyPayObject:
        """Modifier un abonnement. PATCH /api/v1/subscriptions/{id}"""
        body = self._transport.request("PATCH", f"subscriptions/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def cancel(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CancelSubscriptionParams]) -> MercyPayObject:
        """Annuler un abonnement. POST /api/v1/subscriptions/{id}/cancel"""
        body = self._transport.request("POST", f"subscriptions/{encode_id(id)}/cancel", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def reactivate(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.ReactivateSubscriptionParams]) -> MercyPayObject:
        """Retirer une annulation prévue. POST /api/v1/subscriptions/{id}/reactivate"""
        body = self._transport.request("POST", f"subscriptions/{encode_id(id)}/reactivate", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def advance(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.AdvanceSubscriptionParams]) -> MercyPayObject:
        """Passer à l'échéance (sandbox). POST /api/v1/subscriptions/{id}/advance"""
        body = self._transport.request("POST", f"subscriptions/{encode_id(id)}/advance", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def pause(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.PauseSubscriptionParams]) -> MercyPayObject:
        """Mettre en pause. POST /api/v1/subscriptions/{id}/pause"""
        body = self._transport.request("POST", f"subscriptions/{encode_id(id)}/pause", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def resume(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.ResumeSubscriptionParams]) -> MercyPayObject:
        """Reprendre. POST /api/v1/subscriptions/{id}/resume"""
        body = self._transport.request("POST", f"subscriptions/{encode_id(id)}/resume", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def invoices(self, id: str, **params: Unpack[_params.ListSubscriptionInvoicesParams]) -> Page:
        """Factures d'un abonnement. GET /api/v1/subscriptions/{id}/invoices"""
        return self._list(f"subscriptions/{encode_id(id)}/invoices", params)

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class InvoicesResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def list(self, **params: Unpack[_params.ListInvoicesParams]) -> Page:
        """Lister les factures. GET /api/v1/invoices"""
        return self._list("invoices", params)

    def retrieve(self, id: str, **params: Unpack[_params.GetInvoiceParams]) -> MercyPayObject:
        """Lire une facture. GET /api/v1/invoices/{id}"""
        body = self._transport.request("GET", f"invoices/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def pay(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.PayInvoiceParams]) -> MercyPayObject:
        """Encaisser une facture. POST /api/v1/invoices/{id}/pay"""
        body = self._transport.request("POST", f"invoices/{encode_id(id)}/pay", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def send(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.SendInvoiceParams]) -> MercyPayObject:
        """Envoyer la facture au client. POST /api/v1/invoices/{id}/send"""
        body = self._transport.request("POST", f"invoices/{encode_id(id)}/send", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class BillingPortalResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def create_session(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateBillingPortalSessionParams]) -> MercyPayObject:
        """Ouvrir l'espace client. POST /api/v1/billing_portal/sessions"""
        body = self._transport.request("POST", "billing_portal/sessions", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})


class EventsResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def list(self, **params: Unpack[_params.ListEventsParams]) -> Page:
        """Lister les événements. GET /api/v1/events"""
        return self._list("events", params)

    def retrieve(self, id: str, **params: Unpack[_params.GetEventParams]) -> MercyPayObject:
        """Lire un événement. GET /api/v1/events/{id}"""
        body = self._transport.request("GET", f"events/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def deliveries(self, id: str, **params: Unpack[_params.ListEventDeliveriesParams]) -> Page:
        """Lister les envois d'un événement. GET /api/v1/events/{id}/deliveries"""
        return self._list(f"events/{encode_id(id)}/deliveries", params)

    def resend(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.ResendEventParams]) -> MercyPayObject:
        """Renvoyer un événement. POST /api/v1/events/{id}/resend"""
        body = self._transport.request("POST", f"events/{encode_id(id)}/resend", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class WebhookEndpointsResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateWebhookEndpointParams]) -> MercyPayObject:
        """Créer un endpoint. POST /api/v1/webhook_endpoints"""
        body = self._transport.request("POST", "webhook_endpoints", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def list(self, **params: Unpack[_params.ListWebhookEndpointsParams]) -> Page:
        """Lister les endpoints. GET /api/v1/webhook_endpoints"""
        return self._list("webhook_endpoints", params)

    def retrieve(self, id: str, **params: Unpack[_params.GetWebhookEndpointParams]) -> MercyPayObject:
        """Lire un endpoint. GET /api/v1/webhook_endpoints/{id}"""
        body = self._transport.request("GET", f"webhook_endpoints/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def update(self, id: str, **params: Unpack[_params.UpdateWebhookEndpointParams]) -> MercyPayObject:
        """Modifier un endpoint. PATCH /api/v1/webhook_endpoints/{id}"""
        body = self._transport.request("PATCH", f"webhook_endpoints/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def delete(self, id: str, **params: Unpack[_params.DeleteWebhookEndpointParams]) -> MercyPayObject:
        """Supprimer un endpoint. DELETE /api/v1/webhook_endpoints/{id}"""
        body = self._transport.request("DELETE", f"webhook_endpoints/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def rotate_secret(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.RotateWebhookEndpointSecretParams]) -> MercyPayObject:
        """Changer le secret. POST /api/v1/webhook_endpoints/{id}/rotate_secret"""
        body = self._transport.request("POST", f"webhook_endpoints/{encode_id(id)}/rotate_secret", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def test(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.TestWebhookEndpointParams]) -> MercyPayObject:
        """Envoyer un test. POST /api/v1/webhook_endpoints/{id}/test"""
        body = self._transport.request("POST", f"webhook_endpoints/{encode_id(id)}/test", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class RequestLogsResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def list(self, **params: Unpack[_params.ListRequestLogsParams]) -> Page:
        """Lister les requêtes. GET /api/v1/request_logs"""
        return self._list("request_logs", params)

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class TestHelpersResource(WaitMixin):
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def trigger_event(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateTestEventParams]) -> MercyPayObject:
        """Déclencher un événement de test. POST /api/v1/test_helpers/events"""
        body = self._transport.request("POST", "test_helpers/events", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def mobile_money_numbers(self, **params: Unpack[_params.ListTestMobileMoneyNumbersParams]) -> Page:
        """Lister les numéros de test mobile money. GET /api/v1/test_helpers/mobile_money_numbers"""
        return self._list("test_helpers/mobile_money_numbers", params)

    def mobile_money_number(self, provider: str, outcome: str = "succeeded") -> Optional[str]:
        """The sandbox number giving this outcome (succeeded, pending, payout_failed, or a failure_code such as insufficient_balance), or None."""
        from ._helpers import matches_outcome

        for number in self.mobile_money_numbers(provider=provider).data:
            if matches_outcome(number, outcome):
                return str(number["phone"])
        return None

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class EmbedDomainsResource:
    def __init__(self, transport: "SyncTransport") -> None:
        self._transport = transport

    def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateEmbedDomainParams]) -> MercyPayObject:
        """Ajouter un site. POST /api/v1/embed_domains"""
        body = self._transport.request("POST", "embed_domains", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def list(self, **params: Unpack[_params.ListEmbedDomainsParams]) -> Page:
        """Lister les sites autorisés. GET /api/v1/embed_domains"""
        return self._list("embed_domains", params)

    def retrieve(self, id: str, **params: Unpack[_params.GetEmbedDomainParams]) -> MercyPayObject:
        """Lire un site autorisé. GET /api/v1/embed_domains/{id}"""
        body = self._transport.request("GET", f"embed_domains/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def delete(self, id: str, **params: Unpack[_params.DeleteEmbedDomainParams]) -> MercyPayObject:
        """Retirer un site. DELETE /api/v1/embed_domains/{id}"""
        body = self._transport.request("DELETE", f"embed_domains/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def verify(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.VerifyEmbedDomainParams]) -> MercyPayObject:
        """Vérifier un site maintenant. POST /api/v1/embed_domains/{id}/verify"""
        body = self._transport.request("POST", f"embed_domains/{encode_id(id)}/verify", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    def _list(self, path: str, params: Any) -> Page:
        body = self._transport.request("GET", path, params)
        return Page(body, lambda next_params: self._list(path, next_params), dict(params))


class AsyncAccountResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def retrieve(self, **params: Unpack[_params.GetAccountParams]) -> MercyPayObject:
        """Lire le compte. GET /api/v1/account"""
        body = await self._transport.request("GET", "account", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})


class AsyncFeesResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def quote(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateFeeQuoteParams]) -> MercyPayObject:
        """Calculer les frais d'un paiement. POST /api/v1/fees/quote"""
        body = await self._transport.request("POST", "fees/quote", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})


class AsyncProviderStatusResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def retrieve(self, **params: Unpack[_params.GetProviderStatusParams]) -> MercyPayObject:
        """État des opérateurs. GET /api/v1/provider_status"""
        body = await self._transport.request("GET", "provider_status", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})


class AsyncCheckoutSessionsResource(AsyncWaitMixin):
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateCheckoutSessionParams]) -> MercyPayObject:
        """Créer une session. POST /api/v1/checkout_sessions"""
        body = await self._transport.request("POST", "checkout_sessions", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def list(self, **params: Unpack[_params.ListCheckoutSessionsParams]) -> AsyncPage:
        """Lister les sessions. GET /api/v1/checkout_sessions"""
        return await self._list("checkout_sessions", params)

    async def retrieve(self, id: str, **params: Unpack[_params.GetCheckoutSessionParams]) -> MercyPayObject:
        """Lire une session. GET /api/v1/checkout_sessions/{id}"""
        body = await self._transport.request("GET", f"checkout_sessions/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def expire(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.ExpireCheckoutSessionParams]) -> MercyPayObject:
        """Expirer une session. POST /api/v1/checkout_sessions/{id}/expire"""
        body = await self._transport.request("POST", f"checkout_sessions/{encode_id(id)}/expire", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def wait_for_completion(self, id: str, *, timeout: float = 120.0, interval: float = 2.0) -> MercyPayObject:
        """Reads the session until it is completed, expired or cancelled, in seconds."""
        from ._helpers import FINAL_SESSION_STATUSES

        return await self._poll(lambda: self.retrieve(id), FINAL_SESSION_STATUSES, timeout, interval, f"La session {id}")

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))


class AsyncPaymentsResource(AsyncWaitMixin):
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreatePaymentParams]) -> MercyPayObject:
        """Encaisser un paiement. POST /api/v1/payments"""
        body = await self._transport.request("POST", "payments", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def list(self, **params: Unpack[_params.ListPaymentsParams]) -> AsyncPage:
        """Lister les paiements. GET /api/v1/payments"""
        return await self._list("payments", params)

    async def retrieve(self, id: str, **params: Unpack[_params.GetPaymentParams]) -> MercyPayObject:
        """Lire un paiement. GET /api/v1/payments/{id}"""
        body = await self._transport.request("GET", f"payments/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def refund(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateRefundParams]) -> MercyPayObject:
        """Rembourser un paiement. POST /api/v1/payments/{id}/refunds"""
        body = await self._transport.request("POST", f"payments/{encode_id(id)}/refunds", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def wait_for_final_status(self, id: str, *, timeout: float = 120.0, interval: float = 2.0) -> MercyPayObject:
        """Reads the payment until it is final (succeeded, failed, canceled, expired…), in seconds. On a server, prefer the payment.succeeded webhook."""
        from ._helpers import FINAL_PAYMENT_STATUSES

        return await self._poll(lambda: self.retrieve(id), FINAL_PAYMENT_STATUSES, timeout, interval, f"Le paiement {id}")

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))


class AsyncRefundsResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def list(self, **params: Unpack[_params.ListRefundsParams]) -> AsyncPage:
        """Lister les remboursements. GET /api/v1/refunds"""
        return await self._list("refunds", params)

    async def retrieve(self, id: str, **params: Unpack[_params.GetRefundParams]) -> MercyPayObject:
        """Lire un remboursement. GET /api/v1/refunds/{id}"""
        body = await self._transport.request("GET", f"refunds/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def cancel(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CancelRefundParams]) -> MercyPayObject:
        """Annuler un remboursement retardé. POST /api/v1/refunds/{id}/cancel"""
        body = await self._transport.request("POST", f"refunds/{encode_id(id)}/cancel", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))


class AsyncWalletsResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def list(self, **params: Unpack[_params.ListWalletsParams]) -> AsyncPage:
        """Lire les soldes. GET /api/v1/wallets"""
        return await self._list("wallets", params)

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))


class AsyncWalletTransfersResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def list(self, **params: Unpack[_params.ListWalletTransfersParams]) -> AsyncPage:
        """Lister les virements entre soldes. GET /api/v1/wallet_transfers"""
        return await self._list("wallet_transfers", params)

    async def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateWalletTransferParams]) -> MercyPayObject:
        """Virer entre deux soldes. POST /api/v1/wallet_transfers"""
        body = await self._transport.request("POST", "wallet_transfers", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))


class AsyncPayoutsResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreatePayoutParams]) -> MercyPayObject:
        """Demander un retrait. POST /api/v1/payouts"""
        body = await self._transport.request("POST", "payouts", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def list(self, **params: Unpack[_params.ListPayoutsParams]) -> AsyncPage:
        """Lister les retraits. GET /api/v1/payouts"""
        return await self._list("payouts", params)

    async def retrieve(self, id: str, **params: Unpack[_params.GetPayoutParams]) -> MercyPayObject:
        """Lire un retrait. GET /api/v1/payouts/{id}"""
        body = await self._transport.request("GET", f"payouts/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))


class AsyncPaymentLinksResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreatePaymentLinkParams]) -> MercyPayObject:
        """Créer un lien. POST /api/v1/payment_links"""
        body = await self._transport.request("POST", "payment_links", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def list(self, **params: Unpack[_params.ListPaymentLinksParams]) -> AsyncPage:
        """Lister les liens. GET /api/v1/payment_links"""
        return await self._list("payment_links", params)

    async def retrieve(self, id: str, **params: Unpack[_params.GetPaymentLinkParams]) -> MercyPayObject:
        """Lire un lien. GET /api/v1/payment_links/{id}"""
        body = await self._transport.request("GET", f"payment_links/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def update(self, id: str, **params: Unpack[_params.UpdatePaymentLinkParams]) -> MercyPayObject:
        """Modifier un lien. PATCH /api/v1/payment_links/{id}"""
        body = await self._transport.request("PATCH", f"payment_links/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def delete(self, id: str, **params: Unpack[_params.DeletePaymentLinkParams]) -> MercyPayObject:
        """Supprimer un lien. DELETE /api/v1/payment_links/{id}"""
        body = await self._transport.request("DELETE", f"payment_links/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def archive(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.ArchivePaymentLinkParams]) -> MercyPayObject:
        """Archiver un lien. POST /api/v1/payment_links/{id}/archive"""
        body = await self._transport.request("POST", f"payment_links/{encode_id(id)}/archive", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def payments(self, id: str, **params: Unpack[_params.ListPaymentLinkPaymentsParams]) -> AsyncPage:
        """Paiements d'un lien. GET /api/v1/payment_links/{id}/payments"""
        return await self._list(f"payment_links/{encode_id(id)}/payments", params)

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))


class AsyncPlansResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreatePlanParams]) -> MercyPayObject:
        """Créer un plan. POST /api/v1/plans"""
        body = await self._transport.request("POST", "plans", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def list(self, **params: Unpack[_params.ListPlansParams]) -> AsyncPage:
        """Lister les plans. GET /api/v1/plans"""
        return await self._list("plans", params)

    async def retrieve(self, id: str, **params: Unpack[_params.GetPlanParams]) -> MercyPayObject:
        """Lire un plan. GET /api/v1/plans/{id}"""
        body = await self._transport.request("GET", f"plans/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def update(self, id: str, **params: Unpack[_params.UpdatePlanParams]) -> MercyPayObject:
        """Modifier un plan. PATCH /api/v1/plans/{id}"""
        body = await self._transport.request("PATCH", f"plans/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def delete(self, id: str, **params: Unpack[_params.DeletePlanParams]) -> MercyPayObject:
        """Supprimer un plan. DELETE /api/v1/plans/{id}"""
        body = await self._transport.request("DELETE", f"plans/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def archive(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.ArchivePlanParams]) -> MercyPayObject:
        """Archiver un plan. POST /api/v1/plans/{id}/archive"""
        body = await self._transport.request("POST", f"plans/{encode_id(id)}/archive", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def restore(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.RestorePlanParams]) -> MercyPayObject:
        """Réactiver un plan. POST /api/v1/plans/{id}/restore"""
        body = await self._transport.request("POST", f"plans/{encode_id(id)}/restore", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))


class AsyncCustomersResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateCustomerParams]) -> MercyPayObject:
        """Créer un client. POST /api/v1/customers"""
        body = await self._transport.request("POST", "customers", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def list(self, **params: Unpack[_params.ListCustomersParams]) -> AsyncPage:
        """Lister les clients. GET /api/v1/customers"""
        return await self._list("customers", params)

    async def retrieve(self, id: str, **params: Unpack[_params.GetCustomerParams]) -> MercyPayObject:
        """Lire un client. GET /api/v1/customers/{id}"""
        body = await self._transport.request("GET", f"customers/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def update(self, id: str, **params: Unpack[_params.UpdateCustomerParams]) -> MercyPayObject:
        """Modifier un client. PATCH /api/v1/customers/{id}"""
        body = await self._transport.request("PATCH", f"customers/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def delete(self, id: str, **params: Unpack[_params.DeleteCustomerParams]) -> MercyPayObject:
        """Supprimer un client. DELETE /api/v1/customers/{id}"""
        body = await self._transport.request("DELETE", f"customers/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def payment_methods(self, customer_id: str, **params: Unpack[_params.ListCustomerPaymentMethodsParams]) -> AsyncPage:
        """Moyens de paiement d'un client. GET /api/v1/customers/{id}/payment_methods"""
        return await self._list(f"customers/{encode_id(customer_id)}/payment_methods", params)

    async def set_default_payment_method(self, customer_id: str, payment_method_id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.SetDefaultPaymentMethodParams]) -> MercyPayObject:
        """Choisir le moyen par défaut. POST /api/v1/customers/{id}/payment_methods/{id}/default"""
        body = await self._transport.request("POST", f"customers/{encode_id(customer_id)}/payment_methods/{encode_id(payment_method_id)}/default", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def remove_payment_method(self, customer_id: str, payment_method_id: str, **params: Unpack[_params.RemovePaymentMethodParams]) -> MercyPayObject:
        """Retirer un moyen de paiement. DELETE /api/v1/customers/{id}/payment_methods/{id}"""
        body = await self._transport.request("DELETE", f"customers/{encode_id(customer_id)}/payment_methods/{encode_id(payment_method_id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))


class AsyncSubscriptionsResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateSubscriptionParams]) -> MercyPayObject:
        """Créer un abonnement. POST /api/v1/subscriptions"""
        body = await self._transport.request("POST", "subscriptions", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def list(self, **params: Unpack[_params.ListSubscriptionsParams]) -> AsyncPage:
        """Lister les abonnements. GET /api/v1/subscriptions"""
        return await self._list("subscriptions", params)

    async def retrieve(self, id: str, **params: Unpack[_params.GetSubscriptionParams]) -> MercyPayObject:
        """Lire un abonnement. GET /api/v1/subscriptions/{id}"""
        body = await self._transport.request("GET", f"subscriptions/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def update(self, id: str, **params: Unpack[_params.UpdateSubscriptionParams]) -> MercyPayObject:
        """Modifier un abonnement. PATCH /api/v1/subscriptions/{id}"""
        body = await self._transport.request("PATCH", f"subscriptions/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def cancel(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CancelSubscriptionParams]) -> MercyPayObject:
        """Annuler un abonnement. POST /api/v1/subscriptions/{id}/cancel"""
        body = await self._transport.request("POST", f"subscriptions/{encode_id(id)}/cancel", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def reactivate(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.ReactivateSubscriptionParams]) -> MercyPayObject:
        """Retirer une annulation prévue. POST /api/v1/subscriptions/{id}/reactivate"""
        body = await self._transport.request("POST", f"subscriptions/{encode_id(id)}/reactivate", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def advance(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.AdvanceSubscriptionParams]) -> MercyPayObject:
        """Passer à l'échéance (sandbox). POST /api/v1/subscriptions/{id}/advance"""
        body = await self._transport.request("POST", f"subscriptions/{encode_id(id)}/advance", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def pause(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.PauseSubscriptionParams]) -> MercyPayObject:
        """Mettre en pause. POST /api/v1/subscriptions/{id}/pause"""
        body = await self._transport.request("POST", f"subscriptions/{encode_id(id)}/pause", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def resume(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.ResumeSubscriptionParams]) -> MercyPayObject:
        """Reprendre. POST /api/v1/subscriptions/{id}/resume"""
        body = await self._transport.request("POST", f"subscriptions/{encode_id(id)}/resume", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def invoices(self, id: str, **params: Unpack[_params.ListSubscriptionInvoicesParams]) -> AsyncPage:
        """Factures d'un abonnement. GET /api/v1/subscriptions/{id}/invoices"""
        return await self._list(f"subscriptions/{encode_id(id)}/invoices", params)

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))


class AsyncInvoicesResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def list(self, **params: Unpack[_params.ListInvoicesParams]) -> AsyncPage:
        """Lister les factures. GET /api/v1/invoices"""
        return await self._list("invoices", params)

    async def retrieve(self, id: str, **params: Unpack[_params.GetInvoiceParams]) -> MercyPayObject:
        """Lire une facture. GET /api/v1/invoices/{id}"""
        body = await self._transport.request("GET", f"invoices/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def pay(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.PayInvoiceParams]) -> MercyPayObject:
        """Encaisser une facture. POST /api/v1/invoices/{id}/pay"""
        body = await self._transport.request("POST", f"invoices/{encode_id(id)}/pay", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def send(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.SendInvoiceParams]) -> MercyPayObject:
        """Envoyer la facture au client. POST /api/v1/invoices/{id}/send"""
        body = await self._transport.request("POST", f"invoices/{encode_id(id)}/send", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))


class AsyncBillingPortalResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def create_session(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateBillingPortalSessionParams]) -> MercyPayObject:
        """Ouvrir l'espace client. POST /api/v1/billing_portal/sessions"""
        body = await self._transport.request("POST", "billing_portal/sessions", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})


class AsyncEventsResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def list(self, **params: Unpack[_params.ListEventsParams]) -> AsyncPage:
        """Lister les événements. GET /api/v1/events"""
        return await self._list("events", params)

    async def retrieve(self, id: str, **params: Unpack[_params.GetEventParams]) -> MercyPayObject:
        """Lire un événement. GET /api/v1/events/{id}"""
        body = await self._transport.request("GET", f"events/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def deliveries(self, id: str, **params: Unpack[_params.ListEventDeliveriesParams]) -> AsyncPage:
        """Lister les envois d'un événement. GET /api/v1/events/{id}/deliveries"""
        return await self._list(f"events/{encode_id(id)}/deliveries", params)

    async def resend(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.ResendEventParams]) -> MercyPayObject:
        """Renvoyer un événement. POST /api/v1/events/{id}/resend"""
        body = await self._transport.request("POST", f"events/{encode_id(id)}/resend", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))


class AsyncWebhookEndpointsResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateWebhookEndpointParams]) -> MercyPayObject:
        """Créer un endpoint. POST /api/v1/webhook_endpoints"""
        body = await self._transport.request("POST", "webhook_endpoints", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def list(self, **params: Unpack[_params.ListWebhookEndpointsParams]) -> AsyncPage:
        """Lister les endpoints. GET /api/v1/webhook_endpoints"""
        return await self._list("webhook_endpoints", params)

    async def retrieve(self, id: str, **params: Unpack[_params.GetWebhookEndpointParams]) -> MercyPayObject:
        """Lire un endpoint. GET /api/v1/webhook_endpoints/{id}"""
        body = await self._transport.request("GET", f"webhook_endpoints/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def update(self, id: str, **params: Unpack[_params.UpdateWebhookEndpointParams]) -> MercyPayObject:
        """Modifier un endpoint. PATCH /api/v1/webhook_endpoints/{id}"""
        body = await self._transport.request("PATCH", f"webhook_endpoints/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def delete(self, id: str, **params: Unpack[_params.DeleteWebhookEndpointParams]) -> MercyPayObject:
        """Supprimer un endpoint. DELETE /api/v1/webhook_endpoints/{id}"""
        body = await self._transport.request("DELETE", f"webhook_endpoints/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def rotate_secret(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.RotateWebhookEndpointSecretParams]) -> MercyPayObject:
        """Changer le secret. POST /api/v1/webhook_endpoints/{id}/rotate_secret"""
        body = await self._transport.request("POST", f"webhook_endpoints/{encode_id(id)}/rotate_secret", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def test(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.TestWebhookEndpointParams]) -> MercyPayObject:
        """Envoyer un test. POST /api/v1/webhook_endpoints/{id}/test"""
        body = await self._transport.request("POST", f"webhook_endpoints/{encode_id(id)}/test", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))


class AsyncRequestLogsResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def list(self, **params: Unpack[_params.ListRequestLogsParams]) -> AsyncPage:
        """Lister les requêtes. GET /api/v1/request_logs"""
        return await self._list("request_logs", params)

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))


class AsyncTestHelpersResource(AsyncWaitMixin):
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def trigger_event(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateTestEventParams]) -> MercyPayObject:
        """Déclencher un événement de test. POST /api/v1/test_helpers/events"""
        body = await self._transport.request("POST", "test_helpers/events", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def mobile_money_numbers(self, **params: Unpack[_params.ListTestMobileMoneyNumbersParams]) -> AsyncPage:
        """Lister les numéros de test mobile money. GET /api/v1/test_helpers/mobile_money_numbers"""
        return await self._list("test_helpers/mobile_money_numbers", params)

    async def mobile_money_number(self, provider: str, outcome: str = "succeeded") -> Optional[str]:
        """The sandbox number giving this outcome (succeeded, pending, payout_failed, or a failure_code such as insufficient_balance), or None."""
        from ._helpers import matches_outcome

        page = await self.mobile_money_numbers(provider=provider)
        for number in page.data:
            if matches_outcome(number, outcome):
                return str(number["phone"])
        return None

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))


class AsyncEmbedDomainsResource:
    def __init__(self, transport: "AsyncTransport") -> None:
        self._transport = transport

    async def create(self, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.CreateEmbedDomainParams]) -> MercyPayObject:
        """Ajouter un site. POST /api/v1/embed_domains"""
        body = await self._transport.request("POST", "embed_domains", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def list(self, **params: Unpack[_params.ListEmbedDomainsParams]) -> AsyncPage:
        """Lister les sites autorisés. GET /api/v1/embed_domains"""
        return await self._list("embed_domains", params)

    async def retrieve(self, id: str, **params: Unpack[_params.GetEmbedDomainParams]) -> MercyPayObject:
        """Lire un site autorisé. GET /api/v1/embed_domains/{id}"""
        body = await self._transport.request("GET", f"embed_domains/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def delete(self, id: str, **params: Unpack[_params.DeleteEmbedDomainParams]) -> MercyPayObject:
        """Retirer un site. DELETE /api/v1/embed_domains/{id}"""
        body = await self._transport.request("DELETE", f"embed_domains/{encode_id(id)}", params, None)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def verify(self, id: str, *, idempotency_key: Optional[str] = None, **params: Unpack[_params.VerifyEmbedDomainParams]) -> MercyPayObject:
        """Vérifier un site maintenant. POST /api/v1/embed_domains/{id}/verify"""
        body = await self._transport.request("POST", f"embed_domains/{encode_id(id)}/verify", params, idempotency_key)
        return MercyPayObject(body.get("data", body) if isinstance(body.get("data", body), dict) else {})

    async def _list(self, path: str, params: Any) -> AsyncPage:
        body = await self._transport.request("GET", path, params)

        async def fetch(next_params: Any) -> AsyncPage:
            return await self._list(path, next_params)

        return AsyncPage(body, fetch, dict(params))
