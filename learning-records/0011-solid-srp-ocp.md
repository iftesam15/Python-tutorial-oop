# SOLID Principles (Part 1) — SRP & OCP

Successfully refactored `projects/BankAccount.py` to adhere to the Single Responsibility Principle (SRP) and Open/Closed Principle (OCP).

## Accomplishments
- Extracted transaction recording into a separate `projects/TransactionClass.py` module with timestamping and string representations.
- Added audit trail logging (`self.transactions.append(Transaction(...))`) inside `deposit()` and `withdraw()`.
- Implemented a decoupled `StatementPrinter` class with:
  - `to_text(account)` for formatted ledger output.
  - `generate_csv_statement(account)` using Python's built-in `csv` and `io.StringIO` modules (stretch goal achieved!).
- Demonstrated OCP by introducing `VipAccount(SavingsAccount)` with an `interest_boost` attribute, extending bank features without altering base `BankAccount` or `SavingsAccount` logic.

## Non-obvious nuances & review items
- **Separation of presentation from domain**: Domain methods (`deposit`, `withdraw`) now focus purely on balance calculation, validation, and audit recording rather than console printing.
- **Subclass side-effects**: In `SavingsAccount.deposit`, there is still a console `print("Congratualtions...")` for platinum status; moving status checks to event handlers/notifiers in Day 12 (DIP) will keep domain logic 100% pure.
- **Currency typing in interest calculation**: In `VipAccount.add_interest()`, creating `Money(interest, "USD")` wraps interest cleanly into the value object before passing to `self.deposit()`.

## Implications
- Solid understanding of SRP (separating presentation/audit/formatting from domain rules) and OCP (extending behavior via inheritance/polymorphism without editing existing classes).
- Ready for Day 12: **SOLID: LSP, ISP, and DIP** — diving into substitutability contracts, modular interfaces (`Protocol`/ABCs), and dependency injection.
