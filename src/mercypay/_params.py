"""Généré par scripts/generate.py depuis la référence de l'API. Ne pas modifier à la main.

What each operation accepts, for your editor and your type checker.
"""

from typing import Any, Dict, List, Literal, Optional, Union

from typing_extensions import Required, TypedDict


GetAccountParams = TypedDict("GetAccountParams", {}, total=False)

CreateFeeQuoteParams = TypedDict("CreateFeeQuoteParams", {"amount": Required[int], "currency": Required[str], "payment_method": Required[Literal["mobile_money", "card"]], "country": str}, total=False)

GetProviderStatusParams = TypedDict("GetProviderStatusParams", {}, total=False)

CreateCheckoutSessionParams = TypedDict("CreateCheckoutSessionParams", {"amount": Required[int], "currency": Required[str], "description": str, "payer_name": str, "payer_email": str, "payer_phone": str, "success_url": str, "cancel_url": str, "payment_method_types": List[Literal["mobile_money", "card"]], "allowed_countries": List[str], "ui_mode": Literal["hosted", "embedded"], "metadata": Dict[str, Any]}, total=False)

ListCheckoutSessionsParams = TypedDict("ListCheckoutSessionsParams", {"status": Literal["created", "pending_payment", "completed", "expired", "cancelled"], "from": str, "to": str, "limit": int, "starting_after": str, "ending_before": str, "created": Dict[str, str]}, total=False)

GetCheckoutSessionParams = TypedDict("GetCheckoutSessionParams", {}, total=False)

ExpireCheckoutSessionParams = TypedDict("ExpireCheckoutSessionParams", {}, total=False)

CreatePaymentParams = TypedDict("CreatePaymentParams", {"amount": Required[int], "currency": Required[str], "payment_method": Literal["mobile_money", "card"], "country": str, "provider": str, "phone": str, "payer_name": str, "payer_email": str, "description": str, "metadata": Dict[str, Any]}, total=False)

ListPaymentsParams = TypedDict("ListPaymentsParams", {"status": Literal["pending", "processing", "succeeded", "failed", "canceled", "expired", "refunded", "disputed"], "from": str, "to": str, "limit": int, "starting_after": str, "ending_before": str, "expand": List[str], "created": Dict[str, str]}, total=False)

GetPaymentParams = TypedDict("GetPaymentParams", {"expand": List[str]}, total=False)

CreateRefundParams = TypedDict("CreateRefundParams", {"amount": int, "reason": str}, total=False)

ListRefundsParams = TypedDict("ListRefundsParams", {"payment": str, "status": Literal["pending", "processing", "succeeded", "failed", "canceled"]}, total=False)

GetRefundParams = TypedDict("GetRefundParams", {}, total=False)

CancelRefundParams = TypedDict("CancelRefundParams", {}, total=False)

ListWalletsParams = TypedDict("ListWalletsParams", {"limit": int, "starting_after": str, "ending_before": str, "created": Dict[str, str]}, total=False)

ListWalletTransfersParams = TypedDict("ListWalletTransfersParams", {"limit": int, "starting_after": str, "ending_before": str, "created": Dict[str, str]}, total=False)

CreateWalletTransferParams = TypedDict("CreateWalletTransferParams", {"from_wallet": Required[str], "to_wallet": Required[str], "amount": Required[int]}, total=False)

CreatePayoutParams = TypedDict("CreatePayoutParams", {"amount": Required[int], "currency": Required[str], "destination_id": str, "destination": Dict[str, Any], "metadata": Dict[str, Any]}, total=False)

ListPayoutsParams = TypedDict("ListPayoutsParams", {"status": Literal["requested", "approved", "processing", "paid", "failed", "rejected", "canceled"], "currency": str, "from": str, "to": str, "limit": int, "starting_after": str, "ending_before": str, "created": Dict[str, str]}, total=False)

GetPayoutParams = TypedDict("GetPayoutParams", {}, total=False)

CreatePaymentLinkParams = TypedDict("CreatePaymentLinkParams", {"title": Required[str], "description": str, "pricing_mode": Literal["fixed", "flexible", "options", "cart"], "amount": int, "minimum_amount": int, "price_options": List[Dict[str, Any]], "items": List[Dict[str, Any]], "custom_fields_schema": List[Dict[str, Any]], "collect_phone": bool, "collect_address": bool, "after_payment_message": str, "max_uses": int, "expires_at": str, "success_url": str, "cancel_url": str, "active": bool, "metadata": Optional[Dict[str, Any]], "type": Literal["one_time", "recurring"], "currency": str, "plan": str}, total=False)

ListPaymentLinksParams = TypedDict("ListPaymentLinksParams", {"active": bool, "type": Literal["one_time", "recurring"], "archived": bool, "limit": int, "starting_after": str, "ending_before": str, "created": Dict[str, str]}, total=False)

GetPaymentLinkParams = TypedDict("GetPaymentLinkParams", {}, total=False)

UpdatePaymentLinkParams = TypedDict("UpdatePaymentLinkParams", {"title": str, "description": str, "pricing_mode": Literal["fixed", "flexible", "options", "cart"], "amount": int, "minimum_amount": int, "price_options": List[Dict[str, Any]], "items": List[Dict[str, Any]], "custom_fields_schema": List[Dict[str, Any]], "collect_phone": bool, "collect_address": bool, "after_payment_message": str, "max_uses": int, "expires_at": str, "success_url": str, "cancel_url": str, "active": bool, "metadata": Optional[Dict[str, Any]]}, total=False)

DeletePaymentLinkParams = TypedDict("DeletePaymentLinkParams", {}, total=False)

ArchivePaymentLinkParams = TypedDict("ArchivePaymentLinkParams", {}, total=False)

ListPaymentLinkPaymentsParams = TypedDict("ListPaymentLinkPaymentsParams", {"status": str, "limit": int, "starting_after": str, "ending_before": str, "created": Dict[str, str]}, total=False)

CreatePlanParams = TypedDict("CreatePlanParams", {"name": Required[str], "amount": Required[int], "currency": Required[str], "interval": Required[Literal["daily", "weekly", "monthly", "yearly"]], "interval_count": int, "trial_period_days": int, "description": str, "portal_switchable": bool, "metadata": Optional[Dict[str, Any]]}, total=False)

ListPlansParams = TypedDict("ListPlansParams", {"status": Literal["active", "archived"], "limit": int, "starting_after": str, "ending_before": str, "created": Dict[str, str]}, total=False)

GetPlanParams = TypedDict("GetPlanParams", {}, total=False)

UpdatePlanParams = TypedDict("UpdatePlanParams", {"name": str, "description": Optional[str], "portal_switchable": bool, "metadata": Optional[Dict[str, Any]]}, total=False)

DeletePlanParams = TypedDict("DeletePlanParams", {}, total=False)

ArchivePlanParams = TypedDict("ArchivePlanParams", {}, total=False)

RestorePlanParams = TypedDict("RestorePlanParams", {}, total=False)

CreateCustomerParams = TypedDict("CreateCustomerParams", {"email": Required[str], "name": Optional[str], "metadata": Dict[str, Any]}, total=False)

ListCustomersParams = TypedDict("ListCustomersParams", {"email": str, "limit": int, "starting_after": str, "ending_before": str, "created": Dict[str, str]}, total=False)

GetCustomerParams = TypedDict("GetCustomerParams", {}, total=False)

UpdateCustomerParams = TypedDict("UpdateCustomerParams", {"email": str, "name": Optional[str], "metadata": Dict[str, Any]}, total=False)

DeleteCustomerParams = TypedDict("DeleteCustomerParams", {}, total=False)

ListCustomerPaymentMethodsParams = TypedDict("ListCustomerPaymentMethodsParams", {"limit": int, "starting_after": str, "ending_before": str, "created": Dict[str, str]}, total=False)

SetDefaultPaymentMethodParams = TypedDict("SetDefaultPaymentMethodParams", {}, total=False)

RemovePaymentMethodParams = TypedDict("RemovePaymentMethodParams", {}, total=False)

CreateSubscriptionParams = TypedDict("CreateSubscriptionParams", {"customer_name": Required[str], "customer_email": Required[str], "payment_method": Literal["card", "mobile_money"], "customer_phone": str, "customer_country": str, "customer_provider": str, "max_cycles": int, "metadata": Optional[Dict[str, Any]], "plan": Required[str]}, total=False)

ListSubscriptionsParams = TypedDict("ListSubscriptionsParams", {"status": Literal["incomplete", "trialing", "active", "past_due", "unpaid", "paused", "canceled"], "customer_email": str, "plan": str, "limit": int, "starting_after": str, "ending_before": str, "expand": List[str], "created": Dict[str, str]}, total=False)

GetSubscriptionParams = TypedDict("GetSubscriptionParams", {"expand": List[str]}, total=False)

UpdateSubscriptionParams = TypedDict("UpdateSubscriptionParams", {"max_cycles": Optional[int], "customer_name": str, "customer_phone": str, "customer_country": str, "customer_provider": str, "metadata": Optional[Dict[str, Any]], "plan": str}, total=False)

CancelSubscriptionParams = TypedDict("CancelSubscriptionParams", {"at_period_end": bool}, total=False)

ReactivateSubscriptionParams = TypedDict("ReactivateSubscriptionParams", {}, total=False)

AdvanceSubscriptionParams = TypedDict("AdvanceSubscriptionParams", {}, total=False)

PauseSubscriptionParams = TypedDict("PauseSubscriptionParams", {"resumes_at": str}, total=False)

ResumeSubscriptionParams = TypedDict("ResumeSubscriptionParams", {}, total=False)

ListSubscriptionInvoicesParams = TypedDict("ListSubscriptionInvoicesParams", {"status": Literal["pending", "paid", "failed", "canceled"], "limit": int, "starting_after": str, "ending_before": str, "expand": List[str], "created": Dict[str, str]}, total=False)

ListInvoicesParams = TypedDict("ListInvoicesParams", {"status": Literal["pending", "paid", "failed", "canceled"], "subscription": str, "limit": int, "starting_after": str, "ending_before": str, "expand": List[str], "created": Dict[str, str]}, total=False)

GetInvoiceParams = TypedDict("GetInvoiceParams", {"expand": List[str]}, total=False)

PayInvoiceParams = TypedDict("PayInvoiceParams", {}, total=False)

SendInvoiceParams = TypedDict("SendInvoiceParams", {}, total=False)

CreateBillingPortalSessionParams = TypedDict("CreateBillingPortalSessionParams", {"customer_email": Required[str], "return_url": str}, total=False)

ListEventsParams = TypedDict("ListEventsParams", {"type": str, "limit": int, "starting_after": str, "ending_before": str}, total=False)

GetEventParams = TypedDict("GetEventParams", {}, total=False)

ListEventDeliveriesParams = TypedDict("ListEventDeliveriesParams", {"limit": int, "starting_after": str, "ending_before": str}, total=False)

ResendEventParams = TypedDict("ResendEventParams", {"webhook_endpoint": Required[str]}, total=False)

CreateWebhookEndpointParams = TypedDict("CreateWebhookEndpointParams", {"url": Required[str], "events": Required[List[str]], "environment": Optional[Literal["sandbox", "live"]]}, total=False)

ListWebhookEndpointsParams = TypedDict("ListWebhookEndpointsParams", {"limit": int, "starting_after": str, "ending_before": str}, total=False)

GetWebhookEndpointParams = TypedDict("GetWebhookEndpointParams", {}, total=False)

UpdateWebhookEndpointParams = TypedDict("UpdateWebhookEndpointParams", {"url": str, "events": List[str], "environment": Optional[Literal["sandbox", "live"]], "status": Literal["enabled", "disabled"]}, total=False)

DeleteWebhookEndpointParams = TypedDict("DeleteWebhookEndpointParams", {}, total=False)

RotateWebhookEndpointSecretParams = TypedDict("RotateWebhookEndpointSecretParams", {}, total=False)

TestWebhookEndpointParams = TypedDict("TestWebhookEndpointParams", {}, total=False)

ListRequestLogsParams = TypedDict("ListRequestLogsParams", {"status": Literal["success", "error"], "method": Literal["GET", "POST", "PATCH", "PUT", "DELETE"], "path": str, "limit": int, "starting_after": str, "ending_before": str}, total=False)

CreateTestEventParams = TypedDict("CreateTestEventParams", {"type": Required[Literal["payment.succeeded", "payment.failed", "payment.refunded", "payment.disputed", "payment.dispute_closed", "refund.succeeded", "refund.failed", "refund.canceled", "payout.paid", "payout.failed", "payout.canceled", "subscription.created", "subscription.updated", "subscription.past_due", "subscription.unpaid", "subscription.paused", "subscription.resumed", "subscription.canceled", "invoice.created", "invoice.upcoming", "invoice.paid", "invoice.canceled", "invoice.payment_failed", "checkout_session.completed", "provider_status.changed", "account.updated"]]}, total=False)

CreateEmbedDomainParams = TypedDict("CreateEmbedDomainParams", {"hostname": Required[str]}, total=False)

ListEmbedDomainsParams = TypedDict("ListEmbedDomainsParams", {"limit": int, "starting_after": str, "ending_before": str}, total=False)

GetEmbedDomainParams = TypedDict("GetEmbedDomainParams", {}, total=False)

DeleteEmbedDomainParams = TypedDict("DeleteEmbedDomainParams", {}, total=False)

VerifyEmbedDomainParams = TypedDict("VerifyEmbedDomainParams", {}, total=False)

ListTestMobileMoneyNumbersParams = TypedDict("ListTestMobileMoneyNumbersParams", {"country": str, "provider": str}, total=False)
