import re
import hashlib
import random

from getpass import getpass
def generate_account_number():
    return str(random.randint(10000000, 99999999))

def register():
    while True:
        fullname = input("Enter your Full name: ")
        if not fullname:
            print("Full name can't be blank")
            continue
        if len(fullname) < 4:
            print("Full name must not be less than 4 characters")
            continue
        elif len(fullname) > 255:
            print("Full name must not be more than 255 characters")
            continue
        break
    while True:
        username = input("Enter your user name: ")
        if not username:
            print("User name can't be blank")
            continue
        if len(username) < 3 or len(username) > 20:
            print("User name must be between 3 and 20 characters")
            continue
        pattern = r"^[a-zA-Z0-9_]*$"
        match = re.match(pattern, username)
        if not match:
            print("User name must contain only alphanumeric characters or underscores")
            continue
        break
    while True:
        password = input("Enter your password: ")
        if not password:
            print("Password can't be blank")
            continue
        if len(password) < 8:
            print("Password must be at least 8 characters")
            continue
        elif len(password) > 30:
            print("Password must not be more than 30 characters")
            continue
        pattern =r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$"
        match = re.match(pattern, password)
        if not match:
            print("Enter a valid password.")
            continue
        break
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    while True:
        initial_deposit = float(input("Enter your first deposit: "))
        if initial_deposit < 2000:
            print("Initial deposit must be at least 2000")
            continue
        break

        
    account_number = generate_account_number()
    print("Your new account number is:", account_number)


user_data = register()