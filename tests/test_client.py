import json

import httpx
import pytest

from mercypay import (
    ApiServerError,
    AsyncMercyPay,
    ConnectionError,
    InvalidRequestError,
    MercyPay,
    PaymentError,
)


class Recorder:
    """Answers from a queue and remembers every request: no network in the tests."""

    def __init__(self, *answers):
        self.answers = list(answers)
        self.requests = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        answer = self.answers.pop(0) if self.answers else httpx.Response(200, json={"data": {}})
        if isinstance(answer, Exception):
            raise answer
        return answer


def client(*answers):
    recorder = Recorder(*answers)
    http = httpx.Client(transport=httpx.MockTransport(recorder))
    return MercyPay("mp_sandbox_test", base_url="https://api.test", http_client=http, _sleep=lambda seconds: None), recorder


def test_sends_the_key_and_unwraps_the_object():
    mercy_pay, recorder = client(httpx.Response(200, json={"data": {"id": "pay_1", "status": "succeeded", "payer": {"name": "Awa"}}}))

    payment = mercy_pay.payments.retrieve("pay_1", expand=["checkout_session"])

    assert payment.status == "succeeded"
    assert payment.payer.name == "Awa"
    assert payment["payer"]["name"] == "Awa"
    assert payment.to_dict() == {"id": "pay_1", "status": "succeeded", "payer": {"name": "Awa"}}
    request = recorder.requests[0]
    assert request.method == "GET"
    assert str(request.url) == "https://api.test/api/v1/payments/pay_1?expand%5B%5D=checkout_session"
    assert request.headers["Authorization"] == "Bearer mp_sandbox_test"
    assert request.headers["User-Agent"].startswith("mercy-pay-python/")


def test_a_post_sends_json_with_an_idempotency_key():
    mercy_pay, recorder = client()

    mercy_pay.checkout_sessions.create(amount=15000, currency="XAF", metadata={"order": "é"}, idempotency_key="order-4821")
    mercy_pay.refunds.cancel("re_1")

    assert json.loads(recorder.requests[0].content) == {"amount": 15000, "currency": "XAF", "metadata": {"order": "é"}}
    assert recorder.requests[0].headers["Idempotency-Key"] == "order-4821"
    assert recorder.requests[1].content == b"{}"
    assert recorder.requests[1].headers["Idempotency-Key"].startswith("py_")


def test_a_retry_reuses_the_same_idempotency_key():
    mercy_pay, recorder = client(httpx.ConnectError("down"), httpx.Response(502), httpx.Response(201, json={"data": {"id": "po_1"}}))

    assert mercy_pay.payouts.create(amount=4000).id == "po_1"
    assert len(recorder.requests) == 3
    assert len({request.headers["Idempotency-Key"] for request in recorder.requests}) == 1


def test_gives_up_after_the_retries():
    mercy_pay, recorder = client(httpx.Response(500), httpx.Response(500), httpx.Response(500, json={"error": {"type": "api_error"}}))
    with pytest.raises(ApiServerError):
        mercy_pay.account.retrieve()
    assert len(recorder.requests) == 3

    offline, _ = client(httpx.ConnectError("down"), httpx.ConnectError("down"), httpx.ConnectError("down"))
    with pytest.raises(ConnectionError):
        offline.account.retrieve()


def test_typed_errors_carry_what_the_api_said():
    body = {"error": {"type": "invalid_request_error", "code": "validation_failed", "message": "Montant invalide.", "param": "amount", "request_id": "req_9", "errors": {"amount": ["Montant invalide."]}}}
    mercy_pay, recorder = client(httpx.Response(422, json=body), httpx.Response(402, json={"error": {"type": "payment_error", "code": "payment_declined"}}))

    with pytest.raises(InvalidRequestError) as caught:
        mercy_pay.payments.create(amount=-1)
    assert (caught.value.status, caught.value.code, caught.value.param, caught.value.request_id) == (422, "validation_failed", "amount", "req_9")
    assert caught.value.errors == {"amount": ["Montant invalide."]}
    assert len(recorder.requests) == 1

    with pytest.raises(PaymentError):
        mercy_pay.payments.create(amount=1)


def test_iterates_through_every_page():
    mercy_pay, recorder = client(
        httpx.Response(200, json={"object": "list", "has_more": True, "next_cursor": "pay_2", "data": [{"id": "pay_1"}, {"id": "pay_2"}]}),
        httpx.Response(200, json={"object": "list", "has_more": False, "next_cursor": None, "data": [{"id": "pay_3"}]}),
    )

    page = mercy_pay.payments.list(limit=2, created={"gte": "2026-11-01"})

    assert len(page) == 2
    assert [payment.id for payment in page.auto_paging_iter()] == ["pay_1", "pay_2", "pay_3"]
    assert str(recorder.requests[1].url) == "https://api.test/api/v1/payments?limit=2&created%5Bgte%5D=2026-11-01&starting_after=pay_2"


def test_ids_are_escaped_in_the_path():
    mercy_pay, recorder = client()
    mercy_pay.customers.retrieve("cus_1/../x")
    assert recorder.requests[0].url.raw_path == b"/api/v1/customers/cus_1%2F..%2Fx"


async def test_the_async_client_works_the_same():
    recorder = Recorder(
        httpx.Response(502),
        httpx.Response(200, json={"object": "list", "has_more": True, "next_cursor": "pay_1", "data": [{"id": "pay_1"}]}),
        httpx.Response(200, json={"object": "list", "has_more": False, "data": [{"id": "pay_2"}]}),
    )

    async def no_sleep(seconds):
        return None

    async with AsyncMercyPay("mp_sandbox_test", base_url="https://api.test", http_client=httpx.AsyncClient(transport=httpx.MockTransport(recorder)), _sleep=no_sleep) as mercy_pay:
        page = await mercy_pay.payments.list(limit=1)
        assert [payment.id async for payment in page.auto_paging_iter()] == ["pay_1", "pay_2"]
    assert len(recorder.requests) == 3
