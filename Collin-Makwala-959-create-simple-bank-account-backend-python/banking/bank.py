import random
from decimal import Decimal

from banking.bank_account import BankAccount


class Bank:

    def __init__(self) -> None:
        self.account_types = {}
        self.bank_accounts = {}

    def add_account_type(self, account_type: str, interest_rate) -> None:
        self.validate_account_type(account_type)
        if not isinstance(interest_rate, (float, int, Decimal)):
            raise TypeError("Interest rate must be a number")
        if account_type in self.account_types:
            raise ValueError(f"Account type {account_type} already exists")
        self.account_types[account_type] = interest_rate

    def open_bank_account(self, account_type_name: str) -> str:
        self.validate_account_type(account_type_name)
        if account_type_name not in self.account_types:
            raise ValueError(f"Account type {account_type_name} does not exist")
        while True:
            account_number = f"{random.randint(0, 9999999999):010}"
            if account_number not in self.bank_accounts:
                break
        self.bank_accounts[account_number] = BankAccount(
            self.account_types[account_type_name]
        )
        return account_number

    def deposit(self, bank_account_number, amount):
        self.account_exists(bank_account_number)
        self.bank_accounts[bank_account_number].deposit(amount)

    def withdraw(self, bank_account_number, amount):
        self.account_exists(bank_account_number)
        self.bank_accounts[bank_account_number].withdraw(amount)

    def transfer(self, from_account_number, to_account_number, amount):
        self.account_exists(from_account_number, to_account_number)
        self.bank_accounts[from_account_number].withdraw(amount)
        self.bank_accounts[to_account_number].deposit(amount)

    def compound_interest(self):
        for account in self.bank_accounts.values():
            account.compound_interest()

    def get_balance(self, from_account_number):
        self.account_exists(from_account_number)
        return self.bank_accounts[from_account_number].balance

    def get_interest_rate(self, from_account_number):
        self.account_exists(from_account_number)
        return self.bank_accounts[from_account_number].interest_rate

    def account_exists(self, *account_numbers):
        for account_number in account_numbers:
            if account_number not in self.bank_accounts:
                raise ValueError(f"Account number {account_number} does not exist")

    def validate_account_type(self, account_type):
        if not isinstance(account_type, str):
            raise TypeError("Account type must be a string")
