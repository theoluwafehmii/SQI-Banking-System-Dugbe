import re
import hashlib
import random
import sqlite3

from getpass import getpass

conn = sqlite3.connect("SQI_BANK.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

def main():
    

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
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_type NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        amount REAL NOT NULL,
        user_id INTEGER ,
        FOREIGN KEY (user_id) REFERENCES users (id)
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
            log_in()

    def log_in():
        print("\n\n*************Log In****************")

        while True:
            username = input("Enter your username: ")
            if not username:
                print("Username can't be blank")
                continue
            break

        while True:
            password = getpass("Enter your password: ")
            if not password:
                print("Password can't be blank")
                continue
            break

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password)).fetchone()
        if user is not None:
            print("Logged in successfully")
            bank(user)
        else:
            
            print("Invalid username or password")


    main_menu = """
        1. Deposit Amount
        2. Withdrawal Amount
        3. Balance Inquiry
        4. Transaction History
        5. Transfer
        6. Acount Details
        7. Log out
    """
    def bank(user):
        def transaction_history(user_id):
            print("\n======= Transaction History =======")
            cursor.execute("""
                SELECT transaction_type, amount, timestamp 
                FROM transactions 
                WHERE user_id = ? 
                ORDER BY timestamp DESC
            """, (user_id,))
            transactions = cursor.fetchall()

            if not transactions:
                print("No transactions found.")
            else:
                for t_type, amount, timestamp in transactions:
                    print(f"{timestamp} - {t_type}: ₦{amount:.2f}")


        user_id, fullname, username, _, balance, account_number = user
        print("\n\n**********************Welcome to SQI Dugbe Ibadan*********************")
        print(f'Welcome, {username}')
        while True:
                print(main_menu)
                choice = input("Choose an option from the menu above: ")
                if choice == "1":
                    deposit_amount = (float(input("Enter amount to deposit: ")))
                    if deposit_amount <= 0:
                        print("Amount must be greater than 0.")
                        continue
                    balance += deposit_amount

                    cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (balance, user_id))
                    cursor.execute("INSERT INTO transactions(transaction_type, amount, user_id)VALUES (?,?,?)",('Deposit', deposit_amount, user_id))
                    conn.commit()
                    print(f"Deposit successful. New balance: ₦{balance}")

                elif choice == "2":
                    withdrawal_amount = float(input("Enter an amount to withdraw: "))
                    if withdrawal_amount <= 0:
                        print("Withdrawal amount must be greater than 0.")
                    elif withdrawal_amount > balance:
                        print(f"Insufficient funds. Your current balance is ₦{balance}")
                    else:
                        balance -= withdrawal_amount
                        cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (balance, user_id))
                        cursor.execute("INSERT INTO transactions(transaction_type, amount, user_id)VALUES (?,?,?)",('Withdraw', withdrawal_amount, user_id))

                        conn.commit()
                        print(f"₦{withdrawal_amount:.2f} withdrawn successfully.")

                        print(f"New balance: ₦{balance}")
                
                elif choice == "3":
                    print(f"Your available balance is ₦{balance}")
                elif choice == "4":
                    transaction_history(user_id)

                elif choice == "5":
                    account_number = input("Enter account number: ")
                    if account_number in user:
                        print("You can't send money to your self")
                        continue
                    recipient = cursor.execute("SELECT * FROM users WHERE account_number = ?", (account_number,)).fetchone()
                    if recipient:
                        amount = float(input("Enter amount: "))
                        if amount <= 0: 
                            print("Amount must be greater than 0.")
                        elif amount > balance:
                            print(f"Insufficient funds. Your current balance is ₦{balance:.2f}.")
                        else:
                            balance -= amount
                            cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (balance, user_id))
                            recipient_balance = recipient[4] + amount  
                            cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (recipient_balance, recipient[0])) 
                            cursor.execute("INSERT INTO transactions(transaction_type, amount, user_id)VALUES (?,?,?)",('Transfer', amount ,user_id))

                            conn.commit()
                            print(f"₦{amount:.2f} sent successfully.")
                            print(f"New balance: ₦{balance:.2f}")
                    else:
                        print("Account number does not exist")
                        continue
                elif choice == "6":
                    print(f"Fullname: {fullname}, Username: {username}, Balance: {balance}, Account number: {account_number} ")
                elif choice == "7":
                    print("Thank you for banking with us")
                    break
                else:
                    print("Invalid choice")
                    continue
    while True:

        print("\n--- WELCOME TO SQI BANK ---")

        print("1. Register")

        print("2. Login")

        print("3. Exit")

        option = input("Select an option: ")
        if option == "1":

            print(register())

        elif option == "2":

            print(log_in())

        elif option == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid input, try again.")

# test=cursor.execute("SELECT * FROM transactions WHERE user_id=?",(2,)).fetchall()
# print(test)
try:
    main()
except sqlite3.IntegrityError as e:
    print(e)
except sqlite3.OperationalError as e:
    print(e)
except Exception as e:
    print(f"Something went wrong: {e}")
finally:
    conn.close()

