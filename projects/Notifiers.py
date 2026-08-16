from abc import ABC, abstractmethod


class Notifier(ABC):
    """
    Abstract Base Class for notification mechanisms (Dependency Inversion Principle - DIP).
    Domain classes like BankAccount depend on this abstraction rather than concrete I/O classes.
    """

    @abstractmethod
    def send(self, message: str) -> None:
        """Send a notification message to the user/destination."""
        pass


class ConsoleNotifier(Notifier):
    """Low-level concrete notifier that prints messages to the console."""

    def send(self, message: str) -> None:
        print(f"[CONSOLE NOTIFICATION] {message}")


class EmailNotifier(Notifier):
    """Low-level concrete notifier that formats and sends email alerts."""
     
    def __init__(self,user_email):
        self.user_email= user_email

    def send(self,message):
        return print(f"[EMAIL to {self.user_email}] Notification:{message}")    


class SMSNotifier(Notifier):
    """Low-level concrete notifier that formats and sends SMS text alerts."""

    def __init__(self, phone_number: str):
        self.phone_number = phone_number

    def send(self, message: str) -> None:
        print(f"[SMS to {self.phone_number}] Alert: {message}")
