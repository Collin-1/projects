The `BankAccount` class represents a bank account with basic functionalities such as depositing, withdrawing, and calculating compound interest.

## Features

- **Balance**: The balance of the bank account. It can only be modified by depositing or withdrawing.
- **Interest Rate**: The interest rate for the bank account. It must be a non-negative number.
- **Deposit**: Deposit a certain amount into the bank account.
- **Withdraw**: Withdraw a certain amount from the bank account. The amount must not exceed the current balance.
- **Compound Interest**: Calculate the compound interest for the current balance and add it to the balance.


## Project Setup

### 1. Environment Setup:
In the instructions below, information is provided on how to install the necessary tools and dependencies needed to run project on any capable machine:
- Use the following command in Windows Terminal or Command Prompt to create a virtual environment:
  1. Create a new virtual environment to run the tests in by using the following command in the terminal window: 
  ~~~
  python -m venv <virtual_environment_name>
  ~~~
  2. Activate the new virtual environment that you just created using the following command:
  ~~~
    source <virtual_environment_name>/bin/activate   # for Unix/Linux

    .\<virtual_environment_name>\Scripts\activate    # for Windows  
  ~~~
  
### 2. Cloning the Repository:
In the instructions below, information is provided to clone the repository of the project. Cloning the repository pulls down a full copy of all the repository data associated with the GitHub.com uploads:
- Use the following command in Windows Terminal or Command Prompt to clone the repository: 
~~~
   git clone https://github.com/Collin-1/projects.git
   cd projects/Collin-Makwala-959-simple-bank-account-backend-python/
~~~
  
### 3. Installing the Required Python Packages:
Once the repository has been cloned and the virtual environment has been set up:
1. Navigate to the project directory by using the following command in the virtual environment Command Terminal or Windows Terminal:
~~~
cd Collin-Makwala-959-contentitem-python/

~~~
- Once the virtual environment has been set up and activated, you will need to install all the relevant packages for the project
2. In the Windows Terminal or Command Prompt of the virtual environment, type in the following command to install the dependencies required to run the files for the project:
~~~
pip install -r requirements.txt
~~~

3. Once dependencies have been installed on your machine, the packages will need to be installed  by running the following command in the Windows Terminal or Command Prompt:
~~~
pip install .
~~~

### 4. Running the project and its test cases:
- After installing the required packages, run the tests/test cases of the project, use the following command in the virtual environment Command Terminal or Windows Terminal:
~~~
python -m pytest
~~~

### 5. Deactivating environment setup:
Once the necessary tasks have been completed, deactivate the virtual environment that was set up to run the tasks by typing the following command in the Windows Terminal or Command Prompt:
~~~
deactivate
~~~

## Usage

This example demonstrates the basic usage of the `BankAccount` class. You can create a new bank account with an initial balance and interest rate, deposit and withdraw money, calculate compound interest, and handle exceptions when trying to withdraw more than the current balance.

~~~
from banking.bank_account import BankAccount

# Create a new BankAccount object with an interest rate of 5% and initial balance of $100
account = BankAccount(5, 100)

# Check the current balance
print(account.balance)  # Output: 100.00

# Deposit $500 into the account
account.deposit(500)
print(account.balance)  # Output: 600.00

# Withdraw $200 from the account
account.withdraw(200)
print(account.balance)  # Output: 400.00

# Calculate compound interest for the current balance
account.compound_interest()
print(account.balance)  # Output: 401.67

# Try to withdraw more than the current balance
try:
    account.withdraw(2000)
except ValueError as e:
    print(e)  # Output: Insufficient funds, cannot withdraw more than the balance
~~~