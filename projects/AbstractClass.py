from abc import ABC,abstractmethod

class Account(ABC):
    def __init__(self,owner,balance=0):
        self.owner = owner
        self.balance=balance

    @abstractmethod
    def account_type(self):
        ...


