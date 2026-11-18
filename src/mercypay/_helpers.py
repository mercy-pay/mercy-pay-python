"""Written by hand: what the wait helpers share."""

import time
from typing import Any, Awaitable, Callable, List

from ._errors import MercyPayError
from ._object import MercyPayObject

FINAL_PAYMENT_STATUSES = ["succeeded", "failed", "canceled", "expired", "refunded", "disputed"]
FINAL_SESSION_STATUSES = ["completed", "expired", "cancelled"]


class WaitTimeoutError(MercyPayError):
    """The wait ended before the object reached a final status. Its last state is in ``last``."""

    def __init__(self, message: str, last: MercyPayObject) -> None:
        super().__init__(message)
        self.last = last


def _too_late(what: str, current: MercyPayObject) -> WaitTimeoutError:
    return WaitTimeoutError(f"{what} n'a pas atteint de statut final à temps (statut : {current.get('status')}).", current)


def matches_outcome(number: Any, outcome: str) -> bool:
    if outcome == "payout_failed":
        return bool(number.get("applies_to") == "payout")
    return bool(number.get("applies_to") == "payment" and outcome in (number.get("outcome"), number.get("failure_code")))


class WaitMixin:
    _transport: Any

    def _poll(self, read: Callable[[], MercyPayObject], final: List[str], timeout: float, interval: float, what: str) -> MercyPayObject:
        deadline = time.monotonic() + timeout
        delay = interval
        current = read()
        while current.get("status") not in final:
            if time.monotonic() + delay > deadline:
                raise _too_late(what, current)
            self._transport._sleep(delay)
            delay = min(delay * 1.5, 10.0)
            current = read()
        return current


class AsyncWaitMixin:
    _transport: Any

    async def _poll(self, read: Callable[[], Awaitable[MercyPayObject]], final: List[str], timeout: float, interval: float, what: str) -> MercyPayObject:
        deadline = time.monotonic() + timeout
        delay = interval
        current = await read()
        while current.get("status") not in final:
            if time.monotonic() + delay > deadline:
                raise _too_late(what, current)
            await self._transport._sleep(delay)
            delay = min(delay * 1.5, 10.0)
            current = await read()
        return current
