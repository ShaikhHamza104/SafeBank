import re
import pymongo
from random import randint

import pymongo.errors

class Error(Exception):
    """Custom error class to handle validation errors."""
    def __init__(self, msg):
        self.ErrorMsg = msg

    def __str__(self):
        return self.ErrorMsg

class Bank:
    """Bank class for managing bank operations like account creation, validation, deposits, and withdrawals."""

    def __init__(self):
        """Initialize the Bank with default settings."""
        self.bank = 'SBI'
        self._pin = ''
        self._balance = 0

    def gender_validate(self, gender):
        """
        Validate the gender input.

        Args:
            gender (str): The gender of the customer.

        Raises:
            Error: If the gender is not 'Male', 'Female', or 'Other'.
        """
        allowed_genders = ["Male", "Female", "Other"]
        if gender not in allowed_genders:
            raise Error("Invalid gender. Please choose from Male, Female, or Other.")

    def validate_age(self, age):
        """
        Validate the age input.

        Args:
            age (int): The age of the customer.

        Raises:
            ValueError: If the age is not within the range 0 to 100.
        """
        if not isinstance(age, int) or age < 0 or age > 100:
            raise ValueError("Age is invalid. Please enter a valid age between 0 and 100.")

    def validate_name(self, name):
        """
        Validate the customer's name.

        Args:
            name (str): The name of the customer.

        Raises:
            Error: If the name contains non-alphabetic characters.
        """
        if not re.match("^[a-zA-Z\s]+$", name):
            raise Error(f"{name} should not contain special characters or numbers.")

    def validate_pin(self, pin):
        """
        Validate the customer's PIN.

        Args:
            pin (int): The PIN of the customer.

        Raises:
            Error: If the PIN is not exactly 10 digits.
        """
        if len(str(pin)) != 10:
            raise Error("PIN should be exactly 10 digits.")

    def validate_contact(self, contact):
        """
        Validate the customer's contact number.

        Args:
            contact (str): The contact number of the customer.

        Raises:
            Error: If the contact number is not exactly 10 digits.
        """
        if len(str(contact)) != 10 or not contact.isdigit():
            raise Error("Contact number should be exactly 10 digits and contain only numbers.")

    def create_pin(self):
        """
        Generate a new 10-digit PIN for the customer.

        Returns:
            int: A randomly generated 10-digit PIN.
        """
        self._pin = randint(1000000000, 9999999999)
        print(f"Your new PIN is: {self._pin}")

    def create_account(self):
        """Create a new account for the customer by collecting and validating the necessary information."""
        try:
            has_pin = input("Do you have a PIN? (yes or no): ").strip().lower()
            if has_pin == 'no':
                self.create_pin()  # Automatically generates and assigns a new PIN
            pin = int(input("Please enter your PIN: ").strip())
            self.validate_pin(pin)

            user_name = input("Enter your name: ").title().strip()
            self.validate_name(user_name)

            gender = input("Enter your gender (Male, Female, Other): ").capitalize().strip()
            self.gender_validate(gender)

            age = int(input("Enter your age: ").strip())
            self.validate_age(age)

            address = input("Enter your address: ").strip()

            contact = input("Enter your contact number: ").strip()
            self.validate_contact(contact)

            amount = int(input("Enter an initial deposit amount (must be greater than or equal to 500): ").strip())
            if amount < 500:
                print("Initial deposit amount must be greater than or equal to 500.")
                return
            
            user_data = {
                '_id': pin,
                'name': user_name,
                'age': age,
                'gender': gender,
                'address': address,
                'contact': contact,
                'amount': amount,
            }

            # Attempt to insert the data into the MongoDB collection
            result = collection.insert_one(user_data)
            if result.acknowledged:
                print(f"Account created successfully. Your PIN is: {pin}")
            else:
                print("An issue occurred while creating your account. Please try again.")

        except Error as e:
            print(f"Validation Error: {e}")
        except pymongo.errors.DuplicateKeyError:
            print("An account with this PIN already exists. Please try a different PIN.")
        except ValueError as ve:
            print(f"Input Error: {ve}")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def view_profile(self):
        """View the customer's profile using their PIN."""
        try:
            pin = int(input("Enter your PIN: ").strip())
            profile = collection.find_one({"_id": pin})

            if profile is None:
                print(f"No account found with PIN: {pin}")
            else:
                print("=== Profile Details ===")
                for key, value in profile.items():
                    print(f"{key.capitalize()}: {value}")
                print("========================")

        except ValueError:
            print("Invalid PIN format. Please enter a numeric PIN.")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def check_balance(self):
        """Check the customer's account balance."""
        try:
            pin = int(input("Enter your PIN: ").strip())
            profile = collection.find_one({'_id': pin})
            if profile is None:
                print(f"No account found with PIN: {pin}")
            else:
                balance = profile.get('amount', 0)
                print(f"Account Balance: {balance}")
        except ValueError:
            print("Invalid PIN format. Please enter a numeric PIN.")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def find_details(self):
        """Find details by customer's PIN or name."""
        while True:
            try:
                choice = int(input('''
    1. Find ID by NAME
    2. Find NAME by ID
    3. Exit
Choice: ''').strip())
                if choice == 1:
                    name = input("Enter your name: ").title().strip()
                    profile = collection.find_one({'name': name}, {'_id': 1})
                    if profile:
                        print(f"PIN for {name}: {profile['_id']}")
                    else:
                        print(f"Sorry, no account found for name: {name}")

                elif choice == 2:
                    pin = int(input("Enter your PIN: ").strip())
                    profile = collection.find_one({'_id': pin}, {'name': 1})
                    if profile:
                        print(f"Name for PIN {pin}: {profile['name']}")
                    else:
                        print(f"Sorry, no account found for PIN: {pin}")

                elif choice == 3:
                    print("Exiting search.")
                    break
                else:
                    print("Please choose a valid option (1, 2, or 3).")

            except ValueError:
                print("Invalid input. Please enter a numeric value.")
            except Exception as e:
                print(f"Something went wrong: {e}")

    def deposit(self):
        """Deposit money into the customer's account."""
        try:
            pin = int(input("Enter your PIN: ").strip())
            amount = int(input("Enter a deposit amount (must be greater than 500): ").strip())
            if amount <= 0:
                print("Deposit amount must be positive.")
                return 
            if amount < 500:
                print("Deposit amount must be greater than 500.")
                return 

            profile = collection.find_one({'_id': pin})
            if profile is None:  
                print(f"No account found with PIN: {pin}")
                return

            # Update the user's balance
            new_balance = profile.get('amount', 0) + amount
            collection.update_one({'_id': pin}, {'$set': {'amount': new_balance}})
            print(f"Deposited {amount}. New balance: {new_balance}")

        except ValueError:
            print("Invalid input. Please enter numeric values.")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def withdraw(self):
        """Withdraw money from user's account"""
        try:
            pin = int(input("Enter your PIN: ").strip())
            amount = int(input("Enter the amount to withdraw: "))
            if amount <= 0:
                print("Withdrawal amount must be positive.")
                return
            
            profile = collection.find_one({'_id': pin})
            if profile is None:
                print(f"No account found with PIN: {pin}")
                return
            
            current_balance = profile.get('amount', 0)
            if amount > current_balance:
                print("Insufficient funds.")
                return
            
            # Update the user's balance
            new_balance = current_balance - amount
            collection.update_one({'_id': pin}, {'$set': {'amount': new_balance}})
            print(f"Withdrew {amount}. New balance: {new_balance}")
        
        except ValueError:
            print("Invalid input. Please enter numeric values.")
        except Exception as e:
            print(f"Something went wrong: {e}")        

    def delete_details(self):
        """Delete details by customer's PIN or name."""
        try:
            while True:
                choice = int(input('''
    1. Delete account by PIN
    2. Delete account by name
    3. Exit
    Choice: ''').strip())

                if choice == 1:
                    pin = int(input("Enter the PIN of the account you want to delete: "))

                    # Find the account by PIN
                    result = collection.find_one({'_id': pin})

                    if result is None:
                        print(f"No account found with PIN: {pin}")
                    else:
                        # Confirm with the user before deleting
                        confirm = input(f"Are you sure you want to delete the account with PIN {pin}? (y/n): ").lower()
                        if confirm == 'y':
                            # Delete the account using the `delete_one` method
                            deleted_result = collection.delete_one({'_id': pin})
                            if deleted_result.deleted_count > 0:
                                print(f"Account with PIN {pin} deleted successfully.")
                            else:
                                print(f"An error occurred while deleting the account.")
                        else:
                            print("Deletion canceled.")

                elif choice == 2:
                    name=input("Enter your name: ").title()
                    result=collection.find_one({'name':name})
                    if result is None:
                        print(f"No account found with Name: {name}")
                    else:
                        # Confirm with the user before deleting
                        confirm = input(f"Are you sure you want to delete the account with PIN {pin}? (y/n): ").lower()
                        if confirm == 'y':
                            # Delete the account using the `delete_one` method
                            collection.delete_one({'name':name})
                            if deleted_result.deleted_count > 0:
                                print(f"Account with name {name} deleted successfully.")
                            else:
                                print(f"An error occurred while deleting the account.")

                elif choice == 3:

                    break

                else:
                    print("Invalid choice. Please select 1 or 2.")

        except ValueError:
            print("Invalid input. Please enter a numeric value.")
        except Exception as e:
            print(f"An error occurred: {e}")
    def main(self):
        """Main menu to interact with the bank system."""
        while True:
            try:
                user = int(input('''
1. Create a new account
2. Create a PIN
3. View profile
4. Check Balance
5. Deposit Money
6. withdraw Money 
7. Find details
8. Delete details
9. Exit
Choice: ''').strip())
                if user == 1:
                    self.create_account()
                elif user == 2:
                    self.create_pin()
                elif user == 3:
                    self.view_profile()
                elif user == 4:
                    self.check_balance()
                elif user == 5:
                    self.deposit()
                elif user == 6:
                    self.withdraw()
                elif user == 7:
                    self.find_details()
                elif user==8:
                    self.delete_details()
                elif user == 9:
                    print("Thank you for using the bank system. Goodbye!")
                    break
                else:
                    print("Invalid option. Please choose a number between 1 and 7.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
            except Exception as e:
                print(f"Something went wrong: {e}")

if __name__ == "__main__":
    try:
        # Initialize MongoDB client and connect to the database
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["safebank"]
        collection = db["account"]

        # Start the Bank system
        b = Bank()
        b.main()

    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Could not connect to MongoDB. Please ensure that MongoDB is running and accessible.")
        print(f"Error: {err}")