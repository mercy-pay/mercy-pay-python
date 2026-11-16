"""Every operation of the API reference (tests/openapi.json, a copy of
docs.mercy-pay.com/openapi.json) has a method calling the right verb and path."""

import json
import re
from pathlib import Path

import httpx
import pytest

from mercypay import MercyPay

HERE = Path(__file__).parent
SPEC = json.loads((HERE / "openapi.json").read_text())
OPERATIONS = {op["operationId"]: op for op in json.loads((HERE.parent / "scripts/operations.json").read_text())}
CASES = [(path, verb, d["operationId"]) for path, methods in SPEC["paths"].items() for verb, d in methods.items()]


def snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def attribute(service):
    return snake(service if service in ("Account", "ProviderStatus", "BillingPortal") else service + "s")


@pytest.mark.parametrize("path,verb,operation_id", CASES, ids=[case[2] for case in CASES])
def test_operation_has_a_method(path, verb, operation_id):
    assert operation_id in OPERATIONS, f"aucune méthode pour {operation_id}"
    operation = OPERATIONS[operation_id]
    requests = []
    http = httpx.Client(transport=httpx.MockTransport(lambda request: requests.append(request) or httpx.Response(200, json={"data": {}})))
    mercy_pay = MercyPay("mp_sandbox_test", base_url="https://api.test", http_client=http)

    ids = [f"id_{name}" for name in operation["ids"]]
    method = "list" if operation["method"] == "all" else snake(operation["method"])
    getattr(getattr(mercy_pay, attribute(operation["service"])), method)(*ids)

    remaining = list(ids)
    expected = re.sub(r"\{[^}]+\}", lambda match: remaining.pop(0), path)
    assert requests[0].method == verb.upper()
    assert requests[0].url.path == expected


def test_no_extra_operation():
    assert len(OPERATIONS) == len(CASES)
