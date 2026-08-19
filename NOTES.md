# Notes

## User preferences
- Comfortable with core Python (functions, loops, scripts) but new to classes/OOP.
- ~1-2 hrs/day, daily project cadence — wants one tangible project per day, difficulty increasing slowly.
- No strong preference on project theme (CLI/games/backend) — pick whatever best teaches the day's concept, but keep it portfolio-plausible.
- Job/career prep is the driver — don't shy away from interview-relevant material (SOLID, design patterns, being able to explain trade-offs) later in the path.
- No hard deadline.

## Curriculum roadmap (working plan, revise as we go)
Spine project: a bank-account system that grows in sophistication day over day (mirrors how OOP is actually taught/interviewed). Not every day has to use it, but default to extending it unless a fresh project teaches the concept better.

1. Classes & objects, `__init__`, methods, multiple instances — BankAccount v1
2. Class vs instance attributes, `@classmethod`/`@staticmethod` — BankAccount v2 (account counter, alt constructors)
3. Encapsulation — properties, private attrs, validation — BankAccount v3 (balance can't go negative)
4. Inheritance, `super()` — SavingsAccount / CheckingAccount subclasses
5. Polymorphism & method overriding — per-subclass interest/fee behavior
6. Dunder/magic methods — `__str__`, `__repr__`, `__eq__`, `__lt__`
7. Composition over inheritance — Bank + Customer classes composed of Accounts
8. Abstract base classes (`abc`) — enforce a shared interface
9. Operator overloading — custom Money or Vector-style class
10. Custom exceptions — `InsufficientFundsError` etc., exception hierarchies
11. SOLID: SRP & OCP — refactor the spine project
12. SOLID: LSP, ISP, DIP — refactor further
13. Design pattern: Factory
14. Design pattern: Strategy — interest/fee algorithms extracted from account subclasses; Notifiers already were Strategy-shaped DIP (name it on Day 14)
15. Design pattern: Observer
16. Testing OOP code — `pytest` with classes, mocking
17. Capstone — multi-file system tying it together, ready for GitHub

This is a plan, not a contract — check learning-records before each session and adjust pacing/order based on what's actually sticking.
