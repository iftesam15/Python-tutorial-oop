# Classes, instances, `__init__`, and `self` — solid

Built `BankAccount` v1 (`__init__`, `deposit`, `withdraw` with an overdraft guard) unprompted-correct on the first pass, including the balance-guard edge case from the brief. Confirmed verbally — without prompting from code — that `self` is why `accountA.balance` and `accountB.balance` stay independent despite sharing one class. Treat classes/instances/attributes/methods/`__init__`/`self` as a solid floor; no need to re-teach fundamentals, safe to move straight into class-level (shared) state next.

## Implications
- Ready for Day 2: class vs. instance attributes, `@classmethod`/`@staticmethod`, alternate constructors — this is where the "shared across every account" idea (e.g. an account counter, a fixed bank name) will land meaningfully now that instance-level state is solid.
- Stretch goal (`transfer` method) was skipped — not a gap, just optional; can revisit naturally once composition (Day 7, Bank owning many Accounts) makes multi-account methods more relevant.
