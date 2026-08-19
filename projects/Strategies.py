from abc import ABC, abstractmethod


class InterestStrategy(ABC):
    @abstractmethod
    def calculate(self, balance: float) -> float:
        """Return interest  (or return) to deposit,given current balance"""


class FixedRateInterest(InterestStrategy):
    def __init__(self, rate: float):
        self.rate = rate

    def calculate(self, balance: float):
        return balance * self.rate


class PromotionalInterest(InterestStrategy):
    def __init__(self, rate: float, boost: float):
        self.rate = rate
        self.boost = boost

    def calculate(self, balance, boost):
        return balance * self.rate + self.boost


class FeeStrategy(ABC):
    @abstractmethod
    def calculate(self, balance: float) -> float:
        """Return fee to charge,given current balance"""


class FixedFee(FeeStrategy):
    def __init__(self, fee: float):
        self.fee = fee

    def calculate(self, balance: float):
        return self.fee


class PercentageFee(FeeStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage

    def calculate(self, balance: float):
        return balance * self.percentage


class TransactionFee(FeeStrategy):
    def __init__(self, fee: float):
        self.fee = fee

    def calculate(self, balance: float):
        return self.fee
