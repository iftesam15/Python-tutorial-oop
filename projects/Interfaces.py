from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

# =====================================================================
# Role Interfaces (Interface Segregation Principle - ISP)
# =====================================================================
# Rather than bloating the base BankAccount class with methods that only
# some accounts need (like add_interest), we define segregated role
# interfaces. Only account types that support the role implement them.
# =====================================================================


class InterestBearing(ABC):
    """
    Role interface for accounts that accrue and pay interest
    (e.g., SavingsAccount, InvestmentAccount, FixedDeposit).
    """

    @abstractmethod
    def add_interest(self) -> None:
        """Calculate and deposit earned interest into the account."""
        pass


class Depositable(ABC):
    """Role interface for accounts or instruments that accept deposits."""

    @abstractmethod
    def deposit(self, money) -> None:
        """Deposit money into the account."""
        pass


class Withdrawable(ABC):
    """Role interface for accounts or instruments that support withdrawals."""

    @abstractmethod
    def withdraw(self, money) -> None:
        """Withdraw money from the account."""
        pass


# =====================================================================
# Protocol-Based Alternatives (Structural Subtyping / Duck Typing)
# =====================================================================

@runtime_checkable
class InterestBearingProtocol(Protocol):
    """Structural protocol for interest-bearing entities."""

    def add_interest(self) -> None:
        ...


@runtime_checkable
class DepositableProtocol(Protocol):
    """Structural protocol for depositable entities."""

    def deposit(self, money) -> None:
        ...


@runtime_checkable
class WithdrawableProtocol(Protocol):
    """Structural protocol for withdrawable entities."""

    def withdraw(self, money) -> None:
        ...
