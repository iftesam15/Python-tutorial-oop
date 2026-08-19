from abc import ABC, abstractmethod


class InterestStrategy(ABC):
    @abstractmethod
    def calculate(self, balance: float) -> float:
        """Return interest  (or return) to deposit,given current balance"""


class FixedRateInterest(InterestStrategy):
    def __init__(self, rate: float):
        self.rate = rate

    def calculate(self, balance: float) -> float:
        return balance * self.rate


class PromotionalInterest(InterestStrategy):
    def __init__(self, rate: float, boost: float):
        self.rate = rate
        self.boost = boost

    def calculate(self, balance: float, boost: float | None = None) -> float:
        b = self.boost if boost is None else boost
        return balance * self.rate + b


class ZeroInterest(InterestStrategy):
    def calculate(self, balance: float) -> float:
        return 0.0


class FeeStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float:
        """Return fee to charge, given transaction amount"""


class FixedFee(FeeStrategy):
    def __init__(self, fee: float):
        self.fee = fee

    def calculate(self, amount: float) -> float:
        return self.fee


class PercentageFee(FeeStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage

    def calculate(self, amount: float) -> float:
        return amount * self.percentage


class TransactionFee(FeeStrategy):
    def __init__(self, fee: float):
        self.fee = fee

    def calculate(self, amount: float) -> float:
        return self.fee


class NoFee(FeeStrategy):
    def calculate(self, amount: float) -> float:
        return 0.0
