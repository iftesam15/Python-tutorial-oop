class AccountEvent:
    def __init__(
        self, kind: str, account, amount: float | None = None, message: str = ""
    ):
        self.kind = kind
        self.account = account
        self.amount = amount
        self.message = message


from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, event: AccountEvent) -> None:
        """React to one published event. Do not return a value the account needs."""


class EventManager:
    def __init__(self):
        self._observers: dict[str, list[Observer]] = {}
