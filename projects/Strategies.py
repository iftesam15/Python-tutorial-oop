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
