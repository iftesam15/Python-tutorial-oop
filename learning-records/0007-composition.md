# Composition vs inheritance — correct choice, needed one nudge on the *why*

Built `Customer` and `Bank` via composition (accounts/customers lists), correctly avoiding `class Bank(Customer)`. First attempt at explaining *why* named a symptom ("BankAccount has no meaningful attributes Customer can use") rather than the underlying is-a/has-a test. Supplied the sharper framing — inheritance can only express "this object IS one of those," never "this object holds many of those" — and it landed immediately.

Also fixed two real bugs unprompted once pointed out, no fix spelled out for either: `find_customer` returning `customer.name` (str) instead of `customer` (a type mismatch that would break any chained call like `.total_balance()`), and a second customer left with zero accounts despite the brief requiring two per customer.

## Implications
- The is-a/has-a *test itself* — not just "does subclassing feel weird" — is the piece to check for retention next time inheritance-vs-composition comes up. First-pass intuition was correct but shallow; needed the explicit reframe once.
- Comfortable fixing bugs from a description of the symptom alone (no fix spelled out either time) — future code-review feedback can stay as pointers, not solutions.
- Ready for Day 8: Abstract Base Classes (`abc`) — enforcing that every account type implements a shared interface, building directly on [[0004-inheritance-super]] and [[0005-polymorphism-method-overriding]].
