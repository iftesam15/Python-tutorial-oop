from BankingExceptions import CurrencyMismatchError


class Money:
    """Value object representing a monetary amount and currency."""

    def __init__(self, amount: float, currency: str = "USD"):
        self.amount = float(amount)
        self.currency = currency.upper()

    def __repr__(self) -> str:
        return f"Money({self.amount!r}, {self.currency!r})"

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"     

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise CurrencyMismatchError(self.currency, other.currency)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise CurrencyMismatchError(self.currency, other.currency)
        return Money(self.amount - other.amount, self.currency)

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise CurrencyMismatchError(self.currency, other.currency)
        return self.amount < other.amount
