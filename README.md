# SafeBank

SafeBank is a Python-based banking management system that allows users to create accounts, view profiles, check balances, make deposits, and perform withdrawals. It uses MongoDB for data storage and provides various functionalities to manage bank accounts.

## Features

- **Create a New Account**: Users can create a new account by providing personal details and an initial deposit.
- **Generate PIN**: Automatically generate a 10-digit PIN if the user does not have one.
- **View Profile**: View account details based on PIN.
- **Check Balance**: Check the current account balance.
- **Deposit Money**: Deposit funds into the account.
- **Withdraw Money**: Withdraw funds from the account.
- **Find Details**: Find account details by name or PIN.
- **Delete Account**: Delete an account based on PIN or name.

## Requirements

- Python 3.x
- `pymongo` library for MongoDB interaction

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/ShaikhHamza104/SafeBank.git
    ```
2. **Navigate to the Project Directory**:
    ```bash
    cd SafeBank
    ```
3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Setup MongoDB**:
   - Ensure you have MongoDB installed and running on your local machine or configure it to connect to a remote MongoDB instance.
   - Create a database named `safebank` and a collection named `account` for storing account details.

## Usage

1. **Run the Application**:
    ```bash
    python safe_bank.py
    ```

2. **Follow the On-Screen Prompts**: The application will present a menu with options to create an account, check balances, deposit/withdraw money, and more.

## Example
  **When you run the application, you will see the following menu**:
- 1.Create a new account
- 2.Create a PIN
- 3.View profile
- 4.Check Balance
- 5.Deposit Money
- 6.Withdraw Money
- 7.Find details
- 8.Delete details
- 9.Exit Choice: 1


## Error Handling

- **Validation Errors**: Handled for inputs like PIN, age, contact number, etc.
- **Database Errors**: Handles duplicate PIN errors and connection issues.

## Contributing

Feel free to fork the repository and submit pull requests for any improvements or bug fixes. Ensure that your contributions follow the coding standards and include relevant tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact mailto: kmohdhamza10@gmail.com


