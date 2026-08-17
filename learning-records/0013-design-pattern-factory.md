# Design Pattern: Factory (Registry-Based Object Creation)

Successfully built and integrated a registry-based Factory pattern in `projects/AccountFactory.py`.

## Accomplishments
- Extracted `Money` into its own domain value object module (`projects/Money.py`) to eliminate circular import coupling between `BankAccount.py` and `AccountFactory.py`.
- Created `projects/AccountFactory.py` with:
  - `_registry: dict[str, Type[Any]]` storing dynamic class mappings.
  - `@AccountFactory.register(account_type: str)` decorator to register subclasses dynamically without modifying the factory (adhering strictly to OCP).
  - `create(account_type, owner, balance, **kwargs)` looking up classes dynamically and forwarding parameters via `**kwargs`.
  - `create_from_dict(data: dict)` parsing configuration dictionaries, resolving currencies, and injecting concrete notifiers (`EmailNotifier`, `SMSNotifier`, `ConsoleNotifier`) according to the Dependency Inversion Principle (DIP).
- Registered all four account types (`"savings"`, `"checking"`, `"investment"`, `"vip"`) directly via decorators.
- Demonstrated end-to-end factory instantiation and dictionary payload parsing in `projects/BankAccount.py`.

## Non-obvious nuances & review items
- **Circular Imports in Factory Architectures**: When a factory needs to know about product classes and product classes register with the factory, placing domain value objects (like `Money`) in separate modules and using type guards / string keys avoids module duplication and runtime `TypeError` (`isinstance(Money, Money)`).
- **Extensibility**: Adding a 5th account type (e.g. `CryptoAccount`) requires zero edits to `AccountFactory.py` — decorating the new class registers it automatically.

## Implications
- Solid mastery of Creational Design Patterns in Python (Simple Factory, Factory Method, Registry Pattern with Decorators, and Payload Deserialization).
- Ready for Day 14: **Design Pattern: Strategy** — swapping algorithms and business rules at runtime (e.g. dynamic Interest Calculation Strategies and Fee Calculation Strategies).
