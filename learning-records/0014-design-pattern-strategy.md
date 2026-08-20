# Design Pattern: Strategy (runtime algorithm swap)

Implemented Strategy on the spine project: interest and fee formulas live in `projects/Strategies.py`, accounts delegate, and a client can replace the algorithm after construction.

## Evidence
- `InterestStrategy` / `FeeStrategy` ABCs with several concretes (`FixedRateInterest`, `PromotionalInterest`, `ZeroInterest`, `FixedFee`, `PercentageFee`, `NoFee`).
- `SavingsAccount` / `InvestmentAccount` / `VipAccount` call `self.interest.calculate(...)`; VIP’s boost lives in `PromotionalInterest`, not a unique override of the math. `CheckingAccount.withdraw` asks `self.transaction_strategy.calculate(...)`.
- Runtime swap demo in `BankAccount.py`: apply `FixedRateInterest(0.02)`, then `set_interest_strategy(PromotionalInterest(0.05, 50))` and apply again.
- Factory wiring: `AccountFactory.create_from_dict` maps payload strings (`"interest": "fixed"`, `"fee_strategy": "percentage"`) to strategy objects the same way it maps `"notifier": "email"`.

## Implications
- Factory vs Strategy is now a lived distinction: factory builds the graph; strategy is a plug the graph holds. Do not re-teach that contrast as new material.
- Ready for Day 15: **Observer** — the remaining notifier pain is *who listens* (one `self.notifier`, hardcoded platinum print), not *how to send*.
