# Operator Overloading & Value Objects (Money class)

Successfully created a `Money` value object implementing operator overloading dunder methods (`__add__`, `__sub__`, `__eq__`, `__lt__`), string representations (`__repr__`, `__str__`), and currency checking.

Tackled the stretch goal: integrated `Money` directly into `projects/BankAccount.py` across `deposit()` and `withdraw()` in `BankAccount` and `CheckingAccount`.

Independently debugged and resolved runtime type mismatches between raw floats and `Money` instances during testing.

## Non-obvious nuances & review items
- **Value object immutability**: correctly returned new `Money` instances rather than mutating in place.
- **Type guards vs. Domain validation in `__sub__`**:
  - `__add__` correctly guarded with `isinstance` -> `return NotImplemented`, followed by currency check -> `raise ValueError`.
  - In `__sub__`, `if not isinstance(other, Money):` currently raises `ValueError` referencing `other.currency` (which would cause an `AttributeError` if `other` is not `Money`, and misses currency validation when `other` *is* a `Money` instance of a different currency). Cleaned up as part of the review feedback.

## Implications
- Solid grasp of operator overloading, dunder methods (`__add__`, `__sub__`, `__eq__`, `__lt__`), and value objects.
- Ready for Day 10: Custom Exceptions (`BankingError`, `InsufficientFundsError`, `InvalidAmountError`, `CurrencyMismatchError`) — moving away from `print()` warnings and generic `ValueError`s toward structured domain exception hierarchies.
