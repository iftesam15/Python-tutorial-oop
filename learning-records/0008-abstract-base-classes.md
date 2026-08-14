# Abstract Base Classes — Interface Enforcement

Successfully implemented an abstract base class (`Account`) inheriting from `abc.ABC` and marked `account_type()` as an `@abstractmethod`. Created `SavingsAccount` concrete subclass providing the required implementation and instantiated it.

Understood the key distinction: a plain method with a `pass` or `...` body relies on developer convention and only fails if/when called, whereas `@abstractmethod` forces Python to raise a `TypeError` immediately at object instantiation if any subclass fails to fulfill the contract.

## Implications
- Solid understanding of enforcing interfaces in Python via `abc.ABC` and `@abstractmethod`.
- Ready for Day 9: Operator Overloading (`__add__`, `__sub__`, `__eq__`, `__gt__`, etc.) — introducing custom value objects (like a `Money` class) that support math operations and comparisons, tying naturally into `BankAccount` or standalone monetary operations.
