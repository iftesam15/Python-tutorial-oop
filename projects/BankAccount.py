from abc import ABC, abstractmethod
from BankingExceptions import CurrencyMismatchError, InsufficientFundsError, InvalidAmountError, OverdraftLimitError
from TransactionClass import Transaction
from Interfaces import InterestBearing, Depositable, Withdrawable
from Notifiers import Notifier, ConsoleNotifier, EmailNotifier, SMSNotifier
from AccountFactory import AccountFactory
from Money import Money
class BankAccount(ABC):
    minimum_balance = 0
    bank_name = "Python National Bank"
    account_count=0
    total_deposited = 0
    

    def __init__(self, owner, balance: Money, notifier: Notifier = None):
        self.owner = owner
        self.balance = balance
        self.transactions = []
        self.notifier = notifier if notifier is not None else ConsoleNotifier()
        
        BankAccount.account_count += 1
        

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        amount = value.amount if isinstance(value, Money) else float(value)
        if amount < self.minimum_balance:
            raise ValueError("Balance cannot be negative")
        self._balance = amount 

    @property
    def owner(self):
        return self._owner
    @owner.setter
    def owner(self,name):
        if not len(name):
            raise ValueError("Owner name cannot be empty")
        self._owner = name

    def deposit(self, money: Money) -> None:
        if not isinstance(money, Money):
            raise TypeError(f"Expected Money instance, got {type(money).__name__}")
        if self.is_valid_amount(money.amount):
            self.balance += money.amount
            BankAccount.total_deposited += money.amount
            self.transactions.append(Transaction('DEPOSIT', money))
            self.notifier.send(f"Deposited {money} into {self.owner}'s account. New balance: ${self.balance:.2f}")

    def withdraw(self, money: Money) -> None:
        if not isinstance(money, Money):
            raise TypeError(f"Expected Money instance, got {type(money).__name__}")
        if money.amount > self.balance:
            raise InsufficientFundsError(money.amount, self.balance)
        
        if self.is_valid_amount(money.amount):
            self.balance -= money.amount

        self.transactions.append(Transaction("WITHDRAWAL", money))
        self.notifier.send(f"Withdrew {money} from {self.owner}'s account. New balance: ${self.balance:.2f}")

    @abstractmethod
    def account_type(self):
        return 'Savings'        
          
        
    
    @classmethod
    def from_string(cls,data_string):
        owner,balance = data_string.split(",")
        return cls(owner,float(balance))

    @staticmethod
    def is_valid_amount(amount:float):
        if(amount > 0):
            return True
        else:
           raise InvalidAmountError()

           

    """Four dunder methods Example"""
    def __str__(self):
        return f"{self.owner}'s {self.account_type()} account: ${self.balance:.2f}"

    def __repr__(self):
        return f"BankAccount(owner={self.owner!r}, balance={self.balance!r})"   

    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.owner == other.owner and self.balance == other.balance

    def __lt__(self, other):
        if not isinstance(other,BankAccount):
            return NotImplemented
        return self.balance < other.balance

"""
 Savings account class 
"""

@AccountFactory.register("savings")
class SavingsAccount(BankAccount, InterestBearing):
    def __init__(self, owner, balance=0, interest_rate=0.02, notifier: Notifier = None):
        super().__init__(owner, balance, notifier=notifier)
        self.interest_rate = interest_rate

    def deposit(self, money: Money) -> None:
        if not isinstance(money, Money):
            raise TypeError(f"Expected Money instance, got {type(money).__name__}")
        super().deposit(money)
        if(self.balance >= 10000):
            self.notifier.send(f"Congratulations {self.owner}, you are a platinum member")    

    def add_interest(self):
        interest = self.balance * self.interest_rate
        self.deposit(Money(interest, "USD"))

    def account_type(self):
       return 'Savings'

"""
 Investment account class (Implements InterestBearing)
"""

@AccountFactory.register("investment")
class InvestmentAccount(BankAccount, InterestBearing):
    def __init__(self, owner, balance=0, return_rate=0.07, notifier: Notifier = None):
        super().__init__(owner, balance, notifier=notifier)
        self.return_rate = return_rate

    def add_interest(self):
        returns = self.balance * self.return_rate
        self.deposit(Money(returns, "USD"))

    def account_type(self):
        return 'Investment'

"""
 Checking account class 
"""        

@AccountFactory.register("checking")
class CheckingAccount(BankAccount):
    bank_name = "Python National Bank branch-1"

    def __init__(self, owner, balance=0, transaction_fee = 1.5, overdraft_value=300, notifier: Notifier = None):
        super().__init__(owner, balance, notifier=notifier)
        self.transaction_fee= transaction_fee
        self.minimum_balance = -overdraft_value

    def withdraw(self, money: Money) -> None:                    # REPLACE override — different rule entirely
        if not isinstance(money, Money):
            raise TypeError(f"Expected Money instance, got {type(money).__name__}")
        if self.is_valid_amount(money.amount):
            total = money.amount + self.transaction_fee
            fee = Money(self.transaction_fee, money.currency)
            if self.balance - total < self.minimum_balance:
                raise OverdraftLimitError(total,self.balance,self.minimum_balance)
            self.balance -= total

            self.transactions.append(
            Transaction("WITHDRAWAL", money)
        )

            self.transactions.append(
             Transaction("FEE", fee)
        )
            self.notifier.send(f"Withdrew {money} (fee: {fee}) from {self.owner}'s account. New balance: ${self.balance:.2f}")

    def account_type(self):
       return 'Checking'     


class Customer:
    def __init__(self,name,email):
        self.name=name
        self.email=email
        self.accounts=[]

    def open_account(self,account):
        self.accounts.append(account)

    def total_balance(self):
        return sum(account.balance for account in self.accounts)        

class Bank:
    def __init__(self,name):
        self.name = name
        self.customers=[]

    def add_customers(self,customer):
        self.customers.append(customer)
    def total_assets(self):
        return sum(customer.total_balance() for customer in self.customers)

    def find_customer(self,name):
        for customer in self.customers:
            if customer.name.lower() == name.lower():
                return customer
        return None         


import csv
import io

class StatementPrinter:
    
    @staticmethod
    def to_text(account:BankAccount) -> str:
        lines = [f"=== Statment:{account.owner}==="] 
        for tx in account.transactions:
            lines.append(f"{tx.timestamp:%Y-%m-%d %H:%M} | {tx.tx_type:10} | {tx.money}")    
        lines.append(f"Final Balance: ${account.balance:.2f}")
        return "\n".join(lines)

    @staticmethod
    def generate_csv_statement(account: BankAccount) -> str:
        output = io.StringIO()

        writer = csv.writer(output)

        writer.writerow(["Timestamp", "Type", "Amount", "Currency"])

        for tx in account.transactions:
            writer.writerow([
                tx.timestamp.strftime("%Y-%m-%d %H:%M"),
                tx.tx_type,
                tx.money.amount,
                tx.money.currency
            ])

        writer.writerow([])
        writer.writerow(["Final Balance", account.balance])

        return output.getvalue()    



@AccountFactory.register("vip")
class VipAccount(SavingsAccount):
     def __init__(self, owner, balance, interest_boost, notifier: Notifier = None):
        super().__init__(owner, balance, notifier=notifier)
        self.interest_boost = interest_boost

     def add_interest(self):
        interest = self.balance * self.interest_rate+self.interest_boost 
        self.deposit(Money(interest,"USD"))

account = CheckingAccount("Iftesam", 5000, overdraft_value=300)
account.deposit(Money(100, "USD"))
account.withdraw(Money(2000, "USD"))
print(account)
print(StatementPrinter.to_text(account))
print(StatementPrinter.generate_csv_statement(account))

account2 = VipAccount('Bill', 10000, interest_boost=5)

account2.deposit(Money(250, "USD"))
account2.add_interest()
print('Hello World', account2)


m1 = Money(100, "USD")
m2 = Money(50, "USD")
m3 = Money(50, "EUR")

depositAccount = SavingsAccount("iftesam2", 4000)

depositAccount.deposit(m1)

print(m1 - m2)
print(m1 - m2)        # $150.00 USD
print(m1 > m2)        # True
# print(m1 + m3)      # Raises ValueError: Cannot add USD and EUR

def apply_all_interest(accounts: list[BankAccount]) -> None:
    """
    Interface Segregation Principle (ISP) demonstration:
    Only accounts that implement InterestBearing have add_interest() called.
    Checking accounts are not forced to implement a dummy add_interest method.
    """
    print("\n--- Applying Interest (ISP Demonstration) ---")
    for acc in accounts:
        if isinstance(acc, InterestBearing):
            acc.add_interest()
            print(f"[ISP - Interest Applied] {acc.owner}'s {acc.account_type()} account: new balance is ${acc.balance:.2f}")
        else:
            print(f"[ISP - Skipped] {acc.owner}'s {acc.account_type()} account is not InterestBearing.")


# Demonstration of Interface Segregation
savings = SavingsAccount("Alice", 2000, interest_rate=0.03)
checking = CheckingAccount("Bob", 1500)
investment = InvestmentAccount("Charlie", 10000, return_rate=0.08)

all_accounts = [savings, checking, investment]
apply_all_interest(all_accounts)

# Demonstration of Dependency Inversion Principle (DIP)
print("\n--- Dependency Inversion (DIP Demonstration) ---")
email_account = SavingsAccount("Dana", 3000, notifier=EmailNotifier("dana@example.com"))
sms_account = CheckingAccount("Evan", 1200, notifier=SMSNotifier("+1-555-0199"))

email_account.deposit(Money(500, "USD"))
email_account.withdraw(Money(200, "USD"))

sms_account.deposit(Money(300, "USD"))
sms_account.withdraw(Money(100, "USD"))


# Demonstration of Liskov Substitution Principle (LSP)
def process_payroll(accounts: list[BankAccount], bonus: Money) -> None:
    """
    Liskov Substitution Principle (LSP) demonstration:
    Subclasses (SavingsAccount, CheckingAccount, VipAccount, InvestmentAccount)
    can substitute BankAccount without breaking client code or checking type(acc).
    """
    print(f"\n--- Processing Payroll ({bonus}) [LSP Demonstration] ---")
    for acc in accounts:
        acc.deposit(bonus)


payroll_accounts = [
    SavingsAccount("Grace", 1000),
    CheckingAccount("Henry", 800),
    VipAccount("Ivy", 5000, interest_boost=10),
    InvestmentAccount("Jack", 12000),
]

process_payroll(payroll_accounts,bonus=Money(250,"USD"))



from typing import Callable

class UserService:
    def __init__(self,logger:Callable[[str],None]):
        self.logger=logger  #self.logger is console_logger

    def create_user(self):
        self.logger('user created')   #here calling console_logger
                                      #parameter being passed to logger is 'user created'
    def delete_user(self):
        self.logger('user deleted')   #here calling console_logger
                                      #parameter being passed to logger is 'user deleted'

def console_logger(message:str):
    print(f'LOG:{message}')

def file_logger(message:str):
    with open("log.txt", "a") as f:
        f.write(message + "\n")    


user1 = UserService(console_logger)            
user1.create_user()
user1.delete_user()

# =====================================================================
# Demonstration of Factory Pattern (Lesson 13)
# =====================================================================
print("\n--- Factory Pattern Demonstration (Lesson 13) ---")
print("Registered Account Types in Factory:", AccountFactory.get_registered_types())

# 1. Creating via AccountFactory.create()
fact_savings = AccountFactory.create("savings", "Maya", Money(3000, "USD"), interest_rate=0.04)
fact_checking = AccountFactory.create("checking", "Liam", Money(1500, "USD"), overdraft_value=400)
fact_vip = AccountFactory.create("vip", "Sophia", Money(8000, "USD"), interest_boost=8)

print(f"Factory created: {fact_savings}")
print(f"Factory created: {fact_checking}")
print(f"Factory created: {fact_vip}")

# 2. Creating via AccountFactory.create_from_dict() with Dependency Injection
payload_email_account = {
    "type": "savings",
    "owner": "Olivia",
    "balance": 4500.0,
    "currency": "USD",
    "interest_rate": 0.05,
    "notifier": "email",
    "email": "olivia@example.com"
}

payload_sms_account = {
    "type": "checking",
    "owner": "Noah",
    "balance": 2200.0,
    "currency": "USD",
    "overdraft_value": 500,
    "notifier": "sms",
    "phone": "+1-800-555-0144"
}

dict_acc1 = AccountFactory.create_from_dict(payload_email_account)
dict_acc2 = AccountFactory.create_from_dict(payload_sms_account)

print("\n--- Operations on Dict-Configured Accounts ---")
dict_acc1.deposit(Money(500, "USD"))
dict_acc2.withdraw(Money(300, "USD"))

print(AccountFactory._registry)