    async def wait_for_final_status(self, id: str, *, timeout: float = 120.0, interval: float = 2.0) -> MercyPayObject:
        """Reads the payment until it is final (succeeded, failed, canceled, expired…), in seconds. On a server, prefer the payment.succeeded webhook."""
        from ._helpers import FINAL_PAYMENT_STATUSES

        return await self._poll(lambda: self.retrieve(id), FINAL_PAYMENT_STATUSES, timeout, interval, f"Le paiement {id}")
