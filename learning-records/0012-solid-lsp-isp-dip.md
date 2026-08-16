# SOLID Principles (Part 2) — LSP, ISP & DIP

Successfully refactored the banking system to implement Liskov Substitution Principle (LSP), Interface Segregation Principle (ISP), and Dependency Inversion Principle (DIP).

## Accomplishments
- **Dependency Inversion (DIP)**:
  - Created `projects/Notifiers.py` with an abstract base class `Notifier(ABC)` and three concrete implementations: `ConsoleNotifier`, `EmailNotifier`, and `SMSNotifier`.
  - Injected `Notifier` into `BankAccount.__init__`, defaulting to `ConsoleNotifier()`.
  - Replaced hardcoded `print()` statements across domain operations (`deposit`, `withdraw`, platinum tier upgrade) with `self.notifier.send(...)`.
- **Interface Segregation (ISP)**:
  - Created `projects/Interfaces.py` defining role-focused ABCs (`InterestBearing`, `Depositable`, `Withdrawable`) and runtime-checkable `@runtime_checkable` `typing.Protocol` alternatives.
  - Subclassed `InterestBearing` specifically in `SavingsAccount` and `InvestmentAccount`, avoiding forcing `CheckingAccount` to implement empty/bogus interest methods.
  - Implemented `apply_all_interest()` to safely process interest only on accounts implementing the `InterestBearing` role.
- **Liskov Substitution (LSP)**:
  - Harmonized `deposit()` and `withdraw()` type signatures across `BankAccount`, `SavingsAccount`, `CheckingAccount`, `VipAccount`, and `InvestmentAccount`.
  - Created and ran `process_payroll()` to verify polymorphic substitutability across mixed account lists without type-checking branches.

## Non-obvious nuances & review items
- **Constructor Injection vs Default Dependencies**: `BankAccount(..., notifier=None)` defaults cleanly to `ConsoleNotifier()` while allowing callers or unit test runners to pass mock/spy notifiers.
- **Protocol vs ABC**: Included both traditional ABCs and `typing.Protocol` with `@runtime_checkable`, giving flexibility between nominal inheritance and structural subtyping.
- **LSP Type Consistency**: Added type verification (`isinstance(money, Money)`) in method entries, ensuring consistent contracts across all subclass tiers.

## Implications
- Complete mastery of the five SOLID principles (SRP, OCP, LSP, ISP, DIP).
- Ready for Day 13: **Design Pattern: Factory & Factory Method** — centralizing and decoupling complex object creation (e.g. creating different account types and configurations from raw payloads or account creation requests).
