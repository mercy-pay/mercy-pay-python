    def mobile_money_number(self, provider: str, outcome: str = "succeeded") -> Optional[str]:
        """The sandbox number giving this outcome (succeeded, pending, payout_failed, or a failure_code such as insufficient_balance), or None."""
        from ._helpers import matches_outcome

        for number in self.mobile_money_numbers(provider=provider).data:
            if matches_outcome(number, outcome):
                return str(number["phone"])
        return None
