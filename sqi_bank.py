import re
import hashlib
import random
import sqlite3

from getpass import getpass

conn = sqlite3.connect("SQI_BANK.db")
def main():
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        balance NOT NULL,
        account_number Text UNIQUE NOT NULL
    )
    """)
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
            exists = cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone() == (1, )
            if exists:
                print("User with that username exists already")
                continue
            break
        while True:
            password = getpass("Enter your password: ")
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

        while True:
            account_number = generate_account_number()
            exists = cursor.execute("SELECT 1 FROM users WHERE account_number = ?", (account_number,)).fetchone()
            if not exists:
                break 
        print("Your new account number is:", account_number)

        try:
            cursor.execute("""
                INSERT INTO users (fullname, username, password, balance, account_number) VALUES
                (?, ?, ?, ?, ?)
            """, (fullname, username, hashed_password, initial_deposit, account_number))
        except sqlite3.IntegrityError as e:
            print(f"User with that username/ account number exists: {e}")
        else:
            conn.commit()
            print("Account created successfully.")

    