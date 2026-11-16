import hashlib
import hmac

import pytest

from mercypay import MercyPay, SignatureVerificationError, construct_event

# The same vector as the Mercy Pay servers and every other official library.
SECRET = "whsec_test"
PAYLOAD = '{"id":"evt_test","object":"event"}'
TIMESTAMP = 1791022800
SIGNATURE = "52dafa4217ab4708f69eaeecb1f77e14f6405da36a477620c75328c30567e13b"


def test_a_valid_signature_gives_the_event():
    assert construct_event(PAYLOAD, f"t={TIMESTAMP},v1={SIGNATURE}", SECRET, now=TIMESTAMP + 60).id == "evt_test"
    rotated = MercyPay.webhooks.construct_event(PAYLOAD.encode(), f"t={TIMESTAMP},v1=deadbeef,v1={SIGNATURE}", SECRET, now=TIMESTAMP)
    assert rotated.object == "event"


@pytest.mark.parametrize(
    "payload,header,now",
    [
        (PAYLOAD + " ", f"t={TIMESTAMP},v1={SIGNATURE}", TIMESTAMP),
        (PAYLOAD, f"t={TIMESTAMP},v1={SIGNATURE}", TIMESTAMP + 301),
        (PAYLOAD, None, TIMESTAMP),
        (PAYLOAD, f"t={TIMESTAMP}", TIMESTAMP),
        (PAYLOAD, f"t={TIMESTAMP},v1=" + hmac.new(b"whsec_other", f"{TIMESTAMP}.{PAYLOAD}".encode(), hashlib.sha256).hexdigest(), TIMESTAMP),
    ],
    ids=["changed body", "too old", "missing header", "no v1", "wrong secret"],
)
def test_a_bad_webhook_is_refused(payload, header, now):
    with pytest.raises(SignatureVerificationError):
        construct_event(payload, header, SECRET, now=now)
