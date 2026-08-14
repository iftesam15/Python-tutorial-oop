from abc import ABC,abstractmethod


class Money:
    def __init__(self,amount,currency="USD"):
        self.amount = float(amount)
        self.currency= currency.upper()

    def __repr__(self):
        return f"Money({self.amount!r},{self.currency!r})"

    def __str__(self):
        return f"{self.amount:.2f} {self.currency}"     

    def __add__(self,other):
        if not isinstance(other,Money):
            return NotImplemented

        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency} ")
        return  Money(self.amount + other.amount,self.currency)

    def __sub__(self,other):
        if not isinstance(other,Money):
            raise ValueError(f"Cannot subtract {self.currency} from {other.currency} ")

        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract {self.currency} from {other.currency} ")    
        return  Money(self.amount - other.amount,self.currency)

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError(f"Cannot compare {self.currency} and {other.currency}")
        return self.amount < other.amount        




class BankAccount(ABC):
    minimum_balance = 0
    bank_name = "Python National Bank"
    account_count=0
    total_deposited = 0

    def __init__(self,owner,balance: Money ):
        self.owner = owner
        self.balance = balance
        BankAccount.account_count +=1

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self,value):
        if value <self.minimum_balance:
            raise ValueError("Balance cannot be negative")
        self._balance = value 

    @property
    def owner(self):
        return self._owner
    @owner.setter
    def owner(self,name):
        if not len(name):
            raise ValueError("Owner name cannot be empty")
        self._owner = name

    def deposit(self,money:Money):
        if(self.is_valid_amount(money.amount)):
            self.balance += money.amount
            BankAccount.total_deposited +=money.amount
            print( f"Deposited {money.amount} to your account")             

    def withdraw(self,money:Money):
        if  money.amount > self.balance:
            print('Amount Exceeds your balance')
            return 
        
        if(self.is_valid_amount(money.amount)):
            self.balance -=money.amount

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
            print('Entered Amount is invalid')
            return False 

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


class SavingsAccount(BankAccount):
    def __init__(self,owner,balance=0,interest_rate=0.02):
        super().__init__(owner,balance)
        self.interest_rate = interest_rate

    def deposit(self, amount):
        super().deposit(amount)
        if(self.balance >= 10000):
            print(f"Congratualtions {self.owner} , you are a platinum member")    

    def add_interest(self):
        interest = self.balance * self.interest_rate
        self.deposit(interest)
        print(f"Added {interest:.2f} interest")    

    def account_type(self):
       return 'Savings'

"""
 Checking account class 
"""        

class CheckingAccount(BankAccount):
    bank_name = "Python National Bank branch-1"

    def __init__(self, owner, balance=0,transaction_fee = 1.5,overdraft_value=300):
        super().__init__(owner, balance)
        self.transaction_fee= transaction_fee
        self.minimum_balance = -overdraft_value

    def withdraw(self, money:Money):                    # REPLACE override — different rule entirely
        total = money.amount + self.transaction_fee
     
        if self.balance - total < self.minimum_balance:
            print("Amount exceeds balance and overdraft limit")
            return
        self.balance -= total

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




account = CheckingAccount("Iftesam", 5000, overdraft_value=300)
account.deposit(Money(100, "USD"))
account.withdraw(Money(50, "USD"))
print(account)

m1 = Money(100, "USD")
m2 = Money(50, "USD")
m3 = Money(50, "EUR")

print(m1 + m2)
print(m1-m2)        # $150.00 USD
print(m1 > m2)        # True
# print(m1 + m3)      # Raises ValueError: Cannot add USD and EUR