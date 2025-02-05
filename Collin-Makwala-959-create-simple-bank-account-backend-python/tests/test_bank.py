from decimal import Decimal
import pytest

from banking.bank import Bank


@pytest.fixture
def bank():
    return Bank()


@pytest.fixture
def bank_with_account_types(bank):
    bank.add_account_type("Savings", 5)
    bank.add_account_type("Current", 2.5)
    return bank


@pytest.fixture
def bank_accounts_with_deposits(bank_with_account_types):
    acc_num_1 = bank_with_account_types.open_bank_account("Savings")
    acc_num_2 = bank_with_account_types.open_bank_account("Current")
    bank_with_account_types.deposit(acc_num_1, 500)
    bank_with_account_types.deposit(acc_num_2, 1000)
    return acc_num_1, acc_num_2, bank_with_account_types


def test_add_account_type(bank):
    bank.add_account_type("Savings", 5)
    bank.add_account_type("Current", 2.5)
    assert bank.account_types == {"Savings": 5, "Current": 2.5}


def test_add_account_type_with_existing_account_type(bank_with_account_types):
    with pytest.raises(ValueError, match="Account type Savings already exists"):
        bank_with_account_types.add_account_type("Savings", 5)


def test_open_bank_account(bank_with_account_types):
    acc_num_1 = bank_with_account_types.open_bank_account("Savings")
    acc_num_2 = bank_with_account_types.open_bank_account("Current")
    assert (
        acc_num_1 in bank_with_account_types.bank_accounts
        and acc_num_2 in bank_with_account_types.bank_accounts
    )


def test_open_bank_account_with_non_existing_account_type(bank):
    with pytest.raises(ValueError, match="Account type Savings does not exist"):
        bank.open_bank_account("Savings")


def test_bank_deposit(bank_with_account_types):
    acc_num_1 = bank_with_account_types.open_bank_account("Savings")
    acc_num_2 = bank_with_account_types.open_bank_account("Current")
    bank_with_account_types.deposit(acc_num_1, 500)
    bank_with_account_types.deposit(acc_num_2, 1000)
    assert (
        bank_with_account_types.bank_accounts[acc_num_1].balance == 500
        and bank_with_account_types.bank_accounts[acc_num_2].balance == 1000
    )


def test_bank_withdraw(bank_accounts_with_deposits):
    acc_num_1, acc_num_2, bank = bank_accounts_with_deposits
    bank.withdraw(acc_num_1, 400)
    bank.withdraw(acc_num_2, 500)
    assert (
        bank.bank_accounts[acc_num_1].balance == 100
        and bank.bank_accounts[acc_num_2].balance == 500
    )


def test_bank_transfer(bank_accounts_with_deposits):
    acc_num_1, acc_num_2, bank = bank_accounts_with_deposits
    bank.transfer(acc_num_1, acc_num_2, 400)
    assert (
        bank.bank_accounts[acc_num_1].balance == 100
        and bank.bank_accounts[acc_num_2].balance == 1400
    )


def test_bank_compound_interest(bank_accounts_with_deposits):
    acc_num_1, acc_num_2, bank = bank_accounts_with_deposits
    bank.compound_interest()
    assert bank.bank_accounts[acc_num_1].balance == Decimal(
        "502.08"
    ) and bank.bank_accounts[acc_num_2].balance == Decimal("1002.08")


def test_bank_get_balance(bank_accounts_with_deposits):
    acc_num_1, acc_num_2, bank = bank_accounts_with_deposits
    assert bank.get_balance(acc_num_1) == 500 and bank.get_balance(acc_num_2) == 1000


def test_bank_get_interest_rate(bank_with_account_types):
    acc_num_1 = bank_with_account_types.open_bank_account("Savings")
    acc_num_2 = bank_with_account_types.open_bank_account("Current")
    assert (
        bank_with_account_types.get_interest_rate(acc_num_1) == 5
        and bank_with_account_types.get_interest_rate(acc_num_2) == 2.5
    )


def test_bank_account_exist(bank):
    with pytest.raises(ValueError, match="Account number 7133436283 does not exist"):
        bank.account_exists("7133436283")


def test_add_account_type_string(bank):
    with pytest.raises(TypeError, match="Account type must be a string"):
        bank.add_account_type(562, 5)


def test_bank_add_account_type_string(bank):
    with pytest.raises(TypeError, match="Account type must be a string"):
        bank.open_bank_account(3525)


def test_add_account_with_non_number(bank):
    with pytest.raises(TypeError, match="Interest rate must be a number"):
        bank.add_account_type("Savings", "2.5")