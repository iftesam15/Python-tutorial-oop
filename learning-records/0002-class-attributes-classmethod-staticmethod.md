# Class attributes, @classmethod, @staticmethod — solid

Built `BankAccount` v2 correctly on the first pass: `bank_name`/`account_count`/`total_deposited` as class attributes, `account_count` mutated via `BankAccount.account_count += 1` (correctly avoided the `self.x += 1` shadowing gotcha from [[0001-classes-instances-init-self]] without being told twice), `from_string` as a working alternate constructor, `is_valid_amount` as a static validity check reused inside both `deposit` and `withdraw`. Confirmed verbally, unprompted from code, why the `self.` version would have shadowed rather than shared the attribute.

## Implications
- Class-level vs. instance-level state, and the purpose split between `@classmethod` (alternate constructors) and `@staticmethod` (related utility functions), are a solid floor. No need to re-teach.
- Ready for Day 3: encapsulation — properties, private-by-convention attributes, and validation on write (e.g. balance can never be set to something invalid, not just checked after the fact in `deposit`/`withdraw`). This is a natural next step since `is_valid_amount` is already validating amounts imperatively; properties will show a more Pythonic way to enforce invariants.
