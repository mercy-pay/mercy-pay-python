    def wait_for_completion(self, id: str, *, timeout: float = 120.0, interval: float = 2.0) -> MercyPayObject:
        """Reads the session until it is completed, expired or cancelled, in seconds."""
        from ._helpers import FINAL_SESSION_STATUSES

        return self._poll(lambda: self.retrieve(id), FINAL_SESSION_STATUSES, timeout, interval, f"La session {id}")
