import httpx
import pytest

from mercypay import AsyncMercyPay, MercyPay, WaitTimeoutError, catalog

from test_client import Recorder, client


def payment(status):
    return httpx.Response(200, json={"data": {"id": "pay_1", "object": "payment", "status": status}})


NUMBERS = {
    "object": "list",
    "has_more": False,
    "data": [
        {"provider": "ORANGE_CMR", "phone": "237693456789", "applies_to": "payment", "outcome": "succeeded", "failure_code": None},
        {"provider": "ORANGE_CMR", "phone": "237693456049", "applies_to": "payment", "outcome": "failed", "failure_code": "insufficient_balance"},
        {"provider": "ORANGE_CMR", "phone": "237693456119", "applies_to": "payout", "outcome": "failed", "failure_code": None},
    ],
}


def test_waits_until_the_payment_status_is_final():
    mercy_pay, recorder = client(payment("pending"), payment("processing"), payment("succeeded"))

    assert mercy_pay.payments.wait_for_final_status("pay_1")["status"] == "succeeded"
    assert len(recorder.requests) == 3


def test_gives_up_after_the_timeout_with_the_last_state():
    mercy_pay, _ = client(payment("pending"), payment("pending"), payment("pending"))

    with pytest.raises(WaitTimeoutError) as raised:
        mercy_pay.payments.wait_for_final_status("pay_1", timeout=1.0, interval=0.6)

    assert raised.value.last["status"] == "pending"


def test_picks_the_sandbox_number_for_an_outcome_or_a_failure_code():
    mercy_pay, recorder = client(*[httpx.Response(200, json=NUMBERS) for _ in range(4)])

    assert mercy_pay.test_helpers.mobile_money_number(catalog.ORANGE_CMR) == "237693456789"
    assert mercy_pay.test_helpers.mobile_money_number("ORANGE_CMR", "insufficient_balance") == "237693456049"
    assert mercy_pay.test_helpers.mobile_money_number("ORANGE_CMR", "payout_failed") == "237693456119"
    assert mercy_pay.test_helpers.mobile_money_number("ORANGE_CMR", "payer_not_found") is None
    assert str(recorder.requests[0].url) == "https://api.test/api/v1/test_helpers/mobile_money_numbers?provider=ORANGE_CMR"


@pytest.mark.asyncio
async def test_the_async_client_waits_for_a_session_too():
    recorder = Recorder(
        httpx.Response(200, json={"data": {"id": "cs_1", "status": "pending_payment"}}),
        httpx.Response(200, json={"data": {"id": "cs_1", "status": "completed"}}),
    )

    async def no_sleep(seconds):
        return None

    async with AsyncMercyPay("mp_sandbox_test", base_url="https://api.test", http_client=httpx.AsyncClient(transport=httpx.MockTransport(recorder)), _sleep=no_sleep) as mercy_pay:
        session = await mercy_pay.checkout_sessions.wait_for_completion("cs_1")

    assert session["status"] == "completed"


def test_the_catalog_lists_countries_operators_and_event_types():
    assert "MTN_MOMO_CMR" in catalog.COUNTRIES["CMR"]["providers"]
    assert "payment.succeeded" in catalog.EVENT_TYPES
