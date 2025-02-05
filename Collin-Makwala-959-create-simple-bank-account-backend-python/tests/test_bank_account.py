from decimal import Decimal
import pytest

from banking.bank_account import BankAccount


@pytest.fixture
def account():
    return BankAccount(12)


@pytest.fixture
def account_with_1000_as_balance(account):
    account.deposit(1000)
    return account


@pytest.fixture
def account_with_float_as_balance(account):
    account.deposit(100.50)
    return account


def test_bank_account_balance_after_instantiating(account):
    assert account.balance == 0


def test_bank_account_deposit(account):
    account.deposit(1500)
    assert account.balance == 1500


def test_bank_account_withdraw(account_with_1000_as_balance):
    account_with_1000_as_balance.withdraw(500)
    assert account_with_1000_as_balance.balance == 500


def test_bank_account_compound_interest(account_with_1000_as_balance):
    account_with_1000_as_balance.compound_interest()
    assert account_with_1000_as_balance.balance == 1010


def test_bank_account_multiple_compound_interest(account_with_1000_as_balance):
    account_with_1000_as_balance.compound_interest()
    account_with_1000_as_balance.compound_interest()
    assert account_with_1000_as_balance.balance == Decimal("1020.10")


def test_bank_account_round_half_up(account_with_float_as_balance):
    account_with_float_as_balance.compound_interest()
    assert account_with_float_as_balance.balance == Decimal("101.51")


def test_bank_account_negative_interest_rate(account):
    with pytest.raises(ValueError, match="The interest rate cannot be negative"):
        account.interest_rate = -12


def test_bank_account_deposit_negative_amount(account):
    with pytest.raises(ValueError, match="The deposit amount cannot be negative"):
        account.deposit(-1500)


def test_bank_account_withdraw_negative_amount(account):
    with pytest.raises(ValueError, match="The withdrawal amount cannot be negative"):
        account.withdraw(-500)


def test_bank_account_withdraw_more_than_balance(account_with_1000_as_balance):
    with pytest.raises(
        ValueError, match="Insufficient funds, cannot withdraw more than the balance"
    ):
        account_with_1000_as_balance.withdraw(2000)


def test_bank_account_non_number_interest_rate():
    with pytest.raises(TypeError, match="The interest rate must be a number"):
        BankAccount("twelve")


def test_bank_account_deposit_non_number(account):
    with pytest.raises(TypeError, match="The deposit amount must be a number"):
        account.deposit("five_hundred")


def test_bank_account_withdraw_non_number(account):
    with pytest.raises(TypeError, match="The withdrawal amount must be a number"):
        account.withdraw("five_hundred")


def test_bank_account_instantiation_with_non_number_balance():
    with pytest.raises(TypeError, match="The initial balance must be a number"):
        BankAccount(12, "Seven_hundred")


def test_bank_account_instantiation_with_negative_balance():
    with pytest.raises(ValueError, match="The initial balance cannot be negative"):
        BankAccount(12, -5)


@pytest.mark.parametrize(
    "transaction, error_message",
    [
        ("interest rate", "The interest rate cannot be negative"),
        ("deposit amount", "The deposit amount cannot be negative"),
        ("withdrawal amount", "The withdrawal amount cannot be negative"),
    ],
)
def test_validate_amount_value_error(account, transaction, error_message):
    with pytest.raises(ValueError, match=error_message):
        account.validate_amount(-1, transaction)


@pytest.mark.parametrize(
    "input, transaction, error_message",
    [
        ("four", "interest rate", "The interest rate must be a number"),
        ([4], "deposit amount", "The deposit amount must be a number"),
        ({4}, "withdrawal amount", "The withdrawal amount must be a number"),
    ],
)
def test_validate_amount_type_error(account, input, transaction, error_message):
    with pytest.raises(TypeError, match=error_message):
        account.validate_amount(input, transaction)
