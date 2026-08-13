# Encapsulation via @property — solid

Built `BankAccount` v3 correctly: `balance` and `owner` both turned into properties with validating setters (`_balance`/`_owner` as backing storage), `deposit`/`withdraw` needed no changes since they write through `self.balance` and inherit validation automatically. Completed the stretch goal (owner property) unprompted. Proved the fix by showing `account.balance = -9999` now raises `ValueError` where it previously succeeded silently. Confirmed verbally, unprompted, why the setter must assign to `self._balance` rather than `self.balance` inside itself (infinite recursion otherwise) — same pattern as the [[0002-class-attributes-classmethod-staticmethod]] self-vs-class-attribute gotcha: a case of correctly avoiding a subtle Python trap without needing it pointed out twice.

## Implications
- `@property`/setter pattern, backing-attribute convention, and the recursion trap are a solid floor. No need to re-teach.
- Ready for Day 4: inheritance (`SavingsAccount`/`CheckingAccount` subclassing `BankAccount`, `super().__init__()`). The validated `balance`/`owner` properties will carry over "for free" to subclasses, which is a good moment to make the point that inheritance reuses behavior, not just structure.
- Minor, non-blocking style note observed: demo code doesn't wrap the balance=-9999 line in try/except, so the script crashes before printing the rest of the demo. Not a class defect — just something to mention if it recurs, not worth a dedicated lesson.
