import re
import pymongo
from random import randint

class Error(Exception):
    """Custom error class to handle validation errors."""
    def __init__(self, msg):
        self.ErrorMsg = msg
    def __str__(self):
        return self.ErrorMsg

class Bank:
    def __init__(self):
        self.bank = 'SBI'
        self._pin = ''
        self._balance=0

    def gender_validate(self, gender)->Error:
        """
        Validate the gender input.
        
        Args:
            gender (str): Gender of the student.
            
        Raises:
            Error: If the gender is not in the allowed list.
        """

        allowed_genders = ["Male", "Female", "Other"]
        if gender not in allowed_genders:
            raise Error("Invalid gender. Please choose from Male, Female, or Other.")

    def validate_age(self, age):
        """
        Validate the age input.
        
        Args:
            age (int): Age of the student.
            
        Raises:
            ValueError: If the age is not a valid integer or not within the allowed range.
        """

        if not isinstance(age, int) or age < 0 or age > 100:
            raise ValueError("Age is invalid. Please enter a valid age between 0 and 100.")

    def validate_name(self, name)->Error:
        """
        Validate the student's name.
        
        Args:
            name (str): Name of the student.
            
        Raises:
            Error: If the name contains non-alphabetic characters.
        """

        if not re.match("^[a-zA-Z\s]+$", name):
            raise Error(f"{name} should not contain special characters or numbers.")

    def validate_pin(self, pin)->Error:
        """
        Validate the pin .
        
        Args:
            pin (int): pin of customer.
            
        Raises:
            Error: If the pin is less then 10 digit.
        """

        if len(str(pin)) != 10:
            raise Error("Pin should be exactly 10 digits.")

    def validate_contact(self, contact)->Error:
        """
        Validate the contact number .
        
        Args:
            contact (int): contact number of customer.
            
        Raises:
            Error: If the contact number is less then 10 digit.
        """

        if len(str(contact)) != 10:
            raise Error("Contact number should be exactly 10 digits.")

    def create_pin(self)->int:
        """Creating a 10 digit pin"""
        self._pin = randint(1000000000, 9999999999)
        print(self._pin)

    def create_account(self):
        """Creates an account for the user."""
        
        try:
            has_pin = input("Do you have a PIN? (yes or no): ").strip().lower()
            if has_pin == 'no':
                self.create_pin()  # Automatically generates and assigns a new PIN
            pin = int(input("Enter your PIN: "))
            self.validate_pin(pin)

            user_name = input("What is your name? ").title().strip()
            self.validate_name(user_name)

            gender = input("Enter your gender (Male, Female, Other): ").capitalize().strip()
            self.gender_validate(gender)

            age = int(input("Enter your age: ").strip())
            self.validate_age(age)

            address = input("What is your address? ").strip()
            
            contact = input("Please enter your contact number: ").strip()
            self.validate_contact(contact)

            amout = int(input("Enter a amount (its must be grater than or equal to 500): "))
            if amout<500:
                return f"amount should be grater then or equal to 500"
            
            user_data = {
                '_id': pin,
                'name': user_name,
                'age': age,
                'gender': gender,
                'address': address,
                'contact': contact,
                'amount' : amout,
            }

            # Attempt to insert the data into the MongoDB collection
            result = collection.insert_one(user_data)

            if result.acknowledged:
                print(f"Account has been created successfully. Your PIN is: {pin}")
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
        """Allows the user to view their profile based on their PIN."""
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
        """Check user's account balance"""
        try:
            pin = int(input("Enter your PIN: ").strip())  # Ensure PIN is integer
            profile = collection.find_one({'_id': pin})
            if profile is None:
                print(f"No account found with PIN: {pin}")
            else:
                # Assuming the balance is stored under the key 'amount'
                balance = profile.get('amount', 0)
                print(f"Account Balance: {balance}")
        except ValueError:
            print("Invalid PIN format. Please enter a numeric PIN.")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def find_details(self):
        while True:
            try:
                choice = int(input('''
    1. Find ID by NAME
    2. Find NAME by ID
    3. Exit
        '''))
                if choice==1:
                    pin=int(input("Enter your pin: ".strip()))
                    profile=collection.find_one({'_id':pin},{"_id":0,'name':1})
                    if profile:
                        print(profile)
                    else:
                        print(f"sorry this pin:{pin} is not in this bank")

                elif choice==2:
                    name=input("Enter your name: ".strip()).title()
                    profile=collection.find_one({'name':name},{'_id':1})
                    if profile is None:
                        print(f"sorry this name:{name} is not in this bank")
                    else:
                        print(profile)
                elif choice == 3:
                    break
            except ValueError:
                print("Invalid input. Please enter numeric values.")
            except Exception as e:
                print(f"Something went wrong: {e}")
            

    def deposit(self):
        """Deposit money into user's account"""
        try:
            pin = int(input("Enter your PIN: ").strip())
            amount = int(input("Enter a deposit amount : ").strip())
            if amount <= 0:
                print("Deposit amount must be positive.")
                return 
            if amount <= 500:
                print("Deposit amount must be grater then 500")
                return 
            profile=collection.find_one({'_id':pin})
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
            """Withdraw money into user's account"""
            try:
                pin=int(input("Enter your pin"))
                amount = int(input("Enter a deposit amount (its must be grater than or equal to 500): ").strip())
                if amount <= 0:
                    print("Withdrawal amount must be positive.")
                    return
                profile=collection.find_one({'_id':pin})
                
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
                print(f"Withdraw {amount}. New balance: {new_balance}")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
            except Exception as e:
                print(f"Something went wrong: {e}")
            
    def main(self):
        """Main menu to interact with the Bank."""
        while True:
            user=int(input('''
1. Create a new account

2. Create a pin

3. View profile

4. Check Balance

5. Deposit Money

6. Withdraw Money
7. Exit 
'''))
            t=(1,2,3,4,5,6,7)
            if user not in t:
                print("You can choose either 1,2,3,4,5 or 6")
            else:
                if user==1:
                    self.create_account()
                elif user==2:
                    self.create_pin()
                elif user==3:
                    self.view_profile()
                elif user==4:
                    self.check_balance()
                elif user==5:
                    self.deposit()
                if user==6:
                    self.find_details()
                elif user==7:
                    break
if __name__ == "__main__":
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["safebank"]
        collection = db["account"]
        b = Bank()
        b.main()
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Could not connect to MongoDB: ", err)