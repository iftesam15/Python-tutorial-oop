# Custom Exceptions & Error Hierarchies (BankingExceptions module)

Successfully separated exceptions into a dedicated domain module `projects/BankingExceptions.py` and integrated custom exceptions into `projects/BankAccount.py`.

Built an exception hierarchy rooted at `BankingError(Exception)`:
- `InvalidAmountError(BankingError)`
- `CurrencyMismatchError(BankingError)` with `currency1` and `currency2` attributes
- `InsufficientFundsError(BankingError)` with `amount`, `balance`, and computed `shortfall`
- `OverdraftLimitError(InsufficientFundsError)` (stretch goal) inheriting from `InsufficientFundsError` and correctly computing effective available balance (`balance - overdraft_limit`) via `super().__init__`.

Replaced silent `print()` and `return` failures in `withdraw`, `deposit`, and `is_valid_amount` with real exceptions. Swapped generic `ValueError` in `Money` for `CurrencyMismatchError`.

## Non-obvious nuances & review items
- **Exception Inheritance & Attribute Reuse**: `OverdraftLimitError` subclassing `InsufficientFundsError` allows calling code to either catch `OverdraftLimitError` specifically or catch `InsufficientFundsError` generically, while reusing the shortfall arithmetic.
- **Contract consistency in subclass deposit**: `SavingsAccount.deposit` passed `money.amount` into `super().deposit()`, but `BankAccount.deposit` now expects a `Money` instance. Noted for clean interface consistency.

## Implications
- Strong command of domain-specific exception modeling, payload encapsulation, and Python exception hierarchy mechanics.
- Ready for Day 11: **SOLID Principles (Part 1) — SRP & OCP**. Transitioning from adding class features to evaluating system architecture and modularity (e.g. separating account ledger/statement printing and transaction recording out of `BankAccount`).
