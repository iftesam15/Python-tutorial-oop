from abc import ABC,abstractmethod

class BankAccount(ABC):
    minimum_balance = 0
    bank_name = "Python National Bank"
    account_count=0
    total_deposited = 0

    def __init__(self,owner,balance=0):
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

    def deposit(self,amount):
        if(self.is_valid_amount(amount)):
         self.balance += amount
         BankAccount.total_deposited +=amount
         print( f"Deposited {amount} to your account")             

    def withdraw(self,amount):
        if amount > self.balance:
            print('Amount Exceeds your balance')
            return 
        
        if(self.is_valid_amount(amount)):
            self.balance -=amount

    @abstractmethod
    def account_type(self):
            return 'Savings'        
          
        
    
    @classmethod
    def from_string(cls,data_string):
        owner,balance = data_string.split(",")
        return cls(owner,float(balance))

    @staticmethod
    def is_valid_amount(amount):
        if(amount > 0):
            return True
        else:
            print('Entered Amount is invalid')
            return False 

    """Four dunder methods Example"""
    def __str__(self):
        return f"{self.owner}'s account: ${self.balance:.2f}"

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

    def withdraw(self, amount):                    # REPLACE override — different rule entirely
        total = amount + self.transaction_fee
     
        if self.balance - total < self.minimum_balance:
            print("Amount exceeds balance and overdraft limit")
            return
        self.balance -= total
          


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


bank = Bank("Python National Bank")


dhrubo = Customer("Dhrubo", "dhrubo@example.com")
dhrubo.open_account(BankAccount("Dhrubo", 1000))
dhrubo.open_account(SavingsAccount("Dhrubo", 5000, interest_rate=0.03))

iftesam = Customer("Iftesam", "iftesam@example.com")
iftesam.open_account(BankAccount(iftesam.name, 1000))
iftesam.open_account(CheckingAccount(iftesam.name, 5000, overdraft_value=300))

bank.add_customers(dhrubo)
bank.add_customers(iftesam)

print(f"customer:{bank.find_customer('iftesam')}")

print(dhrubo.total_balance())   # 6000.0 — Customer doesn't care which Account subclass
print(bank.total_assets())      # 6000.0 — Bank doesn't care which Customer, either
