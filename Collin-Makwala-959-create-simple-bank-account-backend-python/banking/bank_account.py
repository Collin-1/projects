from decimal import Decimal, ROUND_HALF_UP

decimal_precision = Decimal("0.01")


class BankAccount:
    def __init__(self, interest_rate, balance=Decimal("0.00")):
        self.validate_amount(interest_rate, "interest rate")
        self.validate_amount(balance, "initial balance")
        self._interest_rate = Decimal(interest_rate)
        self._balance = Decimal(balance)

    @property
    def balance(self):
        return self._balance

    @property
    def interest_rate(self):
        return self._interest_rate

    @interest_rate.setter
    def interest_rate(self, interest_rate):
        self.validate_amount(interest_rate, "interest rate")
        self._interest_rate = Decimal(interest_rate)

    def deposit(self, amount):
        self.validate_amount(amount, "deposit amount")
        self._balance += Decimal(amount)
        self._balance.quantize(decimal_precision)

    def withdraw(self, amount):
        self.validate_amount(amount, "withdrawal amount")
        if amount > self._balance:
            raise ValueError(
                "Insufficient funds, cannot withdraw more than the balance"
            )
        amount = Decimal(str(amount))
        self._balance -= amount.quantize(decimal_precision)

    def compound_interest(self):
        self._balance += (((self._balance / 100) * self.interest_rate) / 12).quantize(
            decimal_precision, rounding=ROUND_HALF_UP
        )

    def validate_amount(self, amount, transaction):
        if not isinstance(amount, (float, int, Decimal)):
            raise TypeError(f"The {transaction} must be a number")
        if amount < 0:
            raise ValueError(f"The {transaction} cannot be negative")
