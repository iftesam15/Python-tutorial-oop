from __future__ import annotations
from typing import TYPE_CHECKING, Type, Any, Dict
from Notifiers import ConsoleNotifier, EmailNotifier, SMSNotifier
from Strategies import (
    FixedRateInterest,
    PromotionalInterest,
    ZeroInterest,
    FixedFee,
    PercentageFee,
    NoFee,
    InterestStrategy,
    FeeStrategy,
)

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
            raise ValueError(
                f"Unknown account type '{account_type}'. Available types: [{valid_types}]"
            )

        target_class = cls._registry[key]
        return target_class(owner, balance, **kwargs)

    @classmethod
    def _build_interest_strategy(cls, data: dict) -> InterestStrategy | None:
        """
        Resolve an InterestStrategy from payload keys.
        Accepts a string name (like notifier) or an already-built strategy object.
        """
        raw = data.get("interest", data.get("interest_strategy"))
        if raw is None:
            return None
        if isinstance(raw, InterestStrategy):
            return raw
        if not isinstance(raw, str):
            raise TypeError(
                f"interest must be a strategy name (str) or InterestStrategy, got {type(raw).__name__}"
            )

        name = raw.lower()
        rate = float(data.get("interest_rate", data.get("rate", 0.02)))
        boost = float(data.get("boost", data.get("interest_boost", 0.0)))

        if name in ("fixed", "fixed_rate"):
            return FixedRateInterest(rate)
        if name in ("promo", "promotional"):
            return PromotionalInterest(rate, boost)
        if name in ("zero", "none", "no_interest"):
            return ZeroInterest()

        raise ValueError(
            f"Unknown interest strategy '{raw}'. " "Supported: fixed, promotional, zero"
        )

    @classmethod
    def _build_fee_strategy(cls, data: dict) -> FeeStrategy | None:
        """
        Resolve a FeeStrategy from payload keys.
        Accepts a string name (like notifier) or an already-built strategy object.
        """
        if "fee" in data:
            raw = data["fee"]
        elif "fee_strategy" in data:
            raw = data["fee_strategy"]
        elif "transaction_strategy" in data:
            raw = data["transaction_strategy"]
        else:
            return None
        if isinstance(raw, FeeStrategy):
            return raw
        if not isinstance(raw, str):
            raise TypeError(
                f"fee must be a strategy name (str) or FeeStrategy, got {type(raw).__name__}"
            )

        name = raw.lower()
        fee_amount = float(data.get("fee_amount", data.get("transaction_fee", 1.5)))
        percentage = float(data.get("fee_percentage", data.get("percentage", 0.02)))

        if name in ("fixed", "flat", "transaction"):
            return FixedFee(fee_amount)
        if name in ("percentage", "percent"):
            return PercentageFee(percentage)
        if name in ("none", "no_fee", "zero"):
            return NoFee()

        raise ValueError(
            f"Unknown fee strategy '{raw}'. " "Supported: fixed, percentage, none"
        )

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
        money = (
            raw_balance
            if isinstance(raw_balance, Money)
            else Money(raw_balance, currency)
        )

        # Wire up notifier based on config (string name → concrete notifier)
        notifier_type = data.get("notifier", "console").lower()
        if notifier_type == "email":
            email_addr = data.get("email") or data.get("user_email")
            if not email_addr:
                raise ValueError("EmailNotifier requires an 'email' field in payload.")
            notifier = EmailNotifier(email_addr)
        elif notifier_type == "sms":
            phone = data.get("phone") or data.get("phone_number")
            if not phone:
                raise ValueError(
                    "SMSNotifier requires a 'phone' or 'phone_number' field in payload."
                )
            notifier = SMSNotifier(phone)
        else:
            notifier = ConsoleNotifier()

        # Wire up interest / fee strategies (string name → concrete strategy)
        interest = cls._build_interest_strategy(data)
        fee_strategy = cls._build_fee_strategy(data)

        reserved_keys = {
            "type",
            "owner",
            "balance",
            "currency",
            "notifier",
            "email",
            "user_email",
            "phone",
            "phone_number",
            "interest",
            "interest_strategy",
            "interest_rate",
            "rate",
            "boost",
            "interest_boost",
            "fee",
            "fee_strategy",
            "transaction_strategy",
            "fee_amount",
            "transaction_fee",
            "fee_percentage",
            "percentage",
        }
        extra_kwargs = {k: v for k, v in data.items() if k not in reserved_keys}

        if interest is not None:
            extra_kwargs["interest"] = interest
        if fee_strategy is not None:
            # CheckingAccount constructor parameter name
            extra_kwargs["transaction_strategy"] = fee_strategy

        return cls.create(account_type, owner, money, notifier=notifier, **extra_kwargs)
