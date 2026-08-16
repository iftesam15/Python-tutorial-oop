class BankingError(Exception):
    """Base exception for all banking domain errors."""
    pass

class InvalidAmountError(BankingError):
    """Raised when enter amount is invalid"""
    def __init__(self):
        
        super().__init__(
            f"Entered amount is invalid"
        )


class InsufficientFundsError(BankingError):
    """Raised when an account does not have enough balance for a withdrawal"""
    def __init__(self,amount,balance):
        self.amount = amount 
        self.balance= balance
        self.shortfall = amount - balance
        super().__init__(
            f"Cannot withdraw ${amount:.2f}: balance is ${balance:.2f} (short by ${self.shortfall:.2f})"
        )

class CurrencyMismatchError(BankingError):
    """Raised when operating on two incompatible currencies."""
    def __init__(self, currency1, currency2):
        self.currency1 = currency1
        self.currency2 = currency2
        super().__init__(f"Cannot operate between {currency1} and {currency2}")


class OverdraftLimitError(InsufficientFundsError):
    """Raised when a withdrawal exceeds the account's overdraft limit"""

    def __init__(self, amount, balance, overdraft_limit):
        self.overdraft_limit = overdraft_limit
        super().__init__(amount, balance - overdraft_limit)