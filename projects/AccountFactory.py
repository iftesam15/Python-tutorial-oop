from __future__ import annotations
from typing import TYPE_CHECKING, Type, Any, Dict
from Notifiers import ConsoleNotifier, EmailNotifier, SMSNotifier

from Money import Money

if TYPE_CHECKING:
    from BankAccount import BankAccount


class AccountFactory:
    """
    Registry-based factory for creating BankAccount instances dynamically.
    Adheres to the Open/Closed Principle (OCP) and Dependency Inversion Principle (DIP).
    """
    _registry: Dict[str, Type[Any]] = {}

    @classmethod
    def register(cls, account_type: str):
        """
        Decorator to register an account class with the factory under a type name.
        Example:
            @AccountFactory.register("savings")
            class SavingsAccount(BankAccount):
                ...
        """
        def decorator(subclass: Type[Any]) -> Type[Any]:
            cls._registry[account_type.lower()] = subclass
            return subclass
        return decorator

    @classmethod
    def get_registered_types(cls) -> list[str]:
        """Returns a list of all currently registered account type names."""
        return sorted(list(cls._registry.keys()))

    @classmethod
    def create(cls, account_type: str, owner: str, balance: Any, **kwargs) -> Any:
        """
        Instantiate an account of the given type with the provided owner, balance, and keyword arguments.
        """
        key = account_type.lower()
        if key not in cls._registry:
            valid_types = ", ".join(cls.get_registered_types())
            raise ValueError(f"Unknown account type '{account_type}'. Available types: [{valid_types}]")

        target_class = cls._registry[key]
        return target_class(owner, balance, **kwargs)

    @classmethod
    def create_from_dict(cls, data: dict) -> Any:
        account_type = data.get("type")
        if not account_type:
            raise ValueError("Configuration dictionary must include a 'type' field.")

        owner = data.get("owner")
        if not owner:
            raise ValueError("Configuration dictionary must include an 'owner' field.")

        raw_balance = data.get("balance", 0.0)
        currency = data.get("currency", "USD")
        money = raw_balance if isinstance(raw_balance, Money) else Money(raw_balance, currency)

        # Wire up notifier based on config
        notifier_type = data.get("notifier", "console").lower()
        if notifier_type == "email":
            email_addr = data.get("email") or data.get("user_email")
            if not email_addr:
                raise ValueError("EmailNotifier requires an 'email' field in payload.")
            notifier = EmailNotifier(email_addr)
        elif notifier_type == "sms":
            phone = data.get("phone") or data.get("phone_number")
            if not phone:
                raise ValueError("SMSNotifier requires a 'phone' or 'phone_number' field in payload.")
            notifier = SMSNotifier(phone)
        else:
            notifier = ConsoleNotifier()

        # Gather remaining extra arguments (e.g. interest_rate, overdraft_value, interest_boost)
        reserved_keys = {"type", "owner", "balance", "currency", "notifier", "email", "user_email", "phone", "phone_number"}
        extra_kwargs = {k: v for k, v in data.items() if k not in reserved_keys}

        return cls.create(account_type, owner, money, notifier=notifier, **extra_kwargs)
