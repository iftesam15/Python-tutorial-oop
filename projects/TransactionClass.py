from datetime import datetime

class Transaction:
    def __init__(self, tx_type, money, timestamp=None):
        self.timestamp = timestamp or datetime.now()
        self.tx_type = tx_type
        self.money = money

    def __repr__(self):
        return (
            f"Transaction("
            f"timestamp={self.timestamp!r}, "
            f"tx_type={self.tx_type!r}, "
            f"money={self.money!r})"
        )
    def __str__(self):
        return f"{self.timestamp}, {self.tx_type}, {self.money}"


class Action:
    action_name= 'KiCK the ball'
    
    @classmethod
    def change_name(cls,name:str):
        cls.action_name = name

    def do_action(self):
        print(f"doing {self.action_name}")
        


print(Action.action_name)
action = Action()
action.do_action()
Action.change_name("Dunk the ball")
action.do_action()
print(Action.action_name)