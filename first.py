import re
import sqlite3
import hashlib

from getpass import getpass


# 1. Build sign up feature
# 2. Build log in feature
# 3. Protect the main menu so that only logged in users can access it
# 4. Input validation

conn = sqlite3.connect("bestbuydb.db")
def main():
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    def sign_up():
        while True:
            first_name = input("Enter your first name: ").strip()
            if not first_name:
                print("First name cannot be blank")
                continue
            break

        while True:
            last_name = input("Enter your last name: ").strip()
            if not last_name:
                print("Last name cannot be blank")
                continue
            break

        while True:
            username = input("Enter your username: ").strip()
            if not username:
                print("Username cannot be blank")
                continue
            
            exists = cursor.execute("SELECT 1 FROM customers WHERE username = ?", (username,)).fetchone() == (1, )
            if exists:
                print("User with that Username already exists")
                continue
            break


        while True:
            email = input("Enter your email address: ").strip()
            if not email:
                print("Email cannot be blank")
                continue
            
            pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            match = re.match(pattern, email)
            if not match:
                print("Enter a valid email address.")
                continue
            break

        while True:
            password = getpass("Enter your password: ").strip()
            if not password:
                print("Password cannot be blank")
                continue

            confirm_password = getpass("Confirm your password: ").strip()

            if not confirm_password:
                print("Confirm Password field cannot be blank")
                continue

            if password != confirm_password:
                print("Passwords don't match")
                continue
            break


        hashed_password = hashlib.sha256(password.encode()).hexdigest()



        try:
            cursor.execute("""
                INSERT INTO customers (first_name, last_name, username, email, password) VALUES 
                (?, ?, ?, ?, ?)
            """, (first_name, last_name, username, email, hashed_password))
        except sqlite3.IntegrityError as e:
            print(f"User with that username already exists: {e}")
        else:
            conn.commit()
            print("Account created successfully.")
            log_in()


    def log_in():
        print("\n\n**********************Log In**********************")

        while True:
            username = input("Enter your username: ").strip()
            if not username:
                print("Username field is required.")
                continue
            break

        while True:
            password = getpass("Enter your password: ").strip()
            if not password:
                print("Password field is required.")
                continue
            break
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = cursor.execute("SELECT * FROM customers WHERE username = ? AND password = ?", (username, hashed_password)).fetchone()
        if user is not None:
            print("Logged in successfully")
            ecommerce(user)
        else:
            print("Invalid username or password")


    main_menu = """
    1. View products.
    2. Return to the auth menu.
    """

    products = ["watch", "TV", "camera", "iPhone", "Dell Convertible", "Smart Fridge"]

    def ecommerce(user):
        user_id, username, first_name, last_name, email, _ = user
        print("\n\n**********************BestBuy**********************")
        print(f"Welcome, {username}")
        while True:
            print(main_menu)
            choice = input("Choose an option from the menu above: ").strip()
            if choice == "1":
                print("OUR PRODUCTS:")
                for idx, product in enumerate(products, start=1):
                    print(f"{idx}. {product}")
            elif choice == "2":
                break
            else:
                print("Invalid choice.")



    auth_menu = """
    1. Sign Up.
    2. Log In.
    3. Quit
    """



    while True:
        print("\n\n**********************Auth Menu**********************")
        print("Welcome to BestBuy Store.")
        print(auth_menu)
        choice = input("Choose an option from the menu above: ").strip()
        
        if choice == "1":
            print(sign_up())
        elif choice == "2":
            log_in()
        elif choice == "3":
            print("Hope to see you soon 👋.")
            break
        else:
            print("Invalid choice.")
            continue
            


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