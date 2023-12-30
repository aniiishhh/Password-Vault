from DatabaseConnection import DatabaseConnection
from FINALMainMenu import MainMenu
from FINALEncrypt import (
    generate_key_from_passphrase,
    generate_specific_key_from_passphrase,
)
from getpass import getpass
from PrintStatements2 import print_Master_Menu
from EmailValidation import validate_email_id
from RecoveryEmail import send_recovery_email

# Connect to database
conn = DatabaseConnection.get_connection("accounts.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute(
    """CREATE TABLE IF NOT EXISTS passphrases
             (user_id TEXT PRIMARY KEY, email_id TEXT NOT NULL, passphrase TEXT NOT NULL, salt TEXT NOT NULL)"""
)
conn.commit()

# Master menu loop
while True:
    print_Master_Menu()

    choice = input("Enter your choice (1/2/3/4/5): ")

    if choice == "1":
        # Access existing account
        user_id = input("Enter your user ID: ")
        cursor.execute("SELECT * FROM passphrases WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if result is None:
            print("User does not exist. Please create a new account.")
            continue

        passphrase = getpass("Enter your passphrase: ")
        salt = result[3]
        key = generate_specific_key_from_passphrase(passphrase, salt)

        # Check if user ID and passphrase match

        if result[2] == key:
            print("Access granted.")
            MainMenu(user_id)

        else:
            print("Access denied.")

    elif choice == "2":
        # Create new account
        user_id = input("Enter your user ID: ")
        cursor.execute("SELECT * FROM passphrases WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        if result is not None:
            print(
                "{} already exists. Please login or enter new user id.".format(user_id)
            )
            continue

        while True:
            passphrase = getpass("Enter your passphrase: ")
            re_enter_passphrase = getpass("Please enter passphrase again to confirm: ")
            if passphrase != re_enter_passphrase:
                print("The passphrases do not match. Please try again.")
                continue
            elif passphrase == re_enter_passphrase:
                break

        valid_email = False
        while not valid_email:
            email_id = input("Enter your email id for password recovery: ")
            valid_email = validate_email_id(email_id)

        passphrase_tuple = generate_key_from_passphrase(passphrase)
        passphrase = passphrase_tuple[0]
        salt = passphrase_tuple[1]

        # Insert user ID and passphrase into passphrases table
        cursor.execute(
            "INSERT INTO passphrases (user_id, email_id, passphrase, salt) VALUES (?, ?, ?, ?)",
            (user_id, email_id, passphrase, salt),
        )

        # Create a new table with user ID as table name
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS {} (ID INTEGER PRIMARY KEY AUTOINCREMENT, purpose TEXT NOT NULL, password TEXT NOT NULL, timestamp DATETIME)".format(
                user_id
            )
        )

        print("Account created successfully.")
        conn.commit()

    elif choice == "3":
        user_id = input("Enter your user ID: ")
        cursor.execute("SELECT * FROM passphrases WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if result is None:
            print("User does not exist. Please create a new account.")
            continue

        passphrase = getpass("Enter your passphrase: ")
        salt = result[3]
        key = generate_specific_key_from_passphrase(passphrase, salt)

        if result[2] != key:
            print("Action denied!")
            continue

        with conn:
            cursor.execute("BEGIN TRANSACTION")
            try:
                cursor.execute("DELETE FROM passphrases WHERE user_id = ?", (user_id,))
                cursor.execute("DROP TABLE IF EXISTS {}".format(user_id))
                print("Account deleted!")
            except Exception as e:
                print("Error deleting account:", e)
                cursor.execute("ROLLBACK")
            else:
                cursor.execute("COMMIT")

    elif choice == "4":
        user_id = input("Enter your user ID: ")
        cursor.execute("SELECT * FROM passphrases WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if result is None:
            print("User does not exist. Please create a new account.")
            continue

        email_id = result[1]

        send_recovery_email(email_id, user_id)

    elif choice == "5":
        # Quit
        print("Connection terminated!")
        break

    else:
        print("Please enter a valid Integer.")

# Close database connection
cursor.close()
conn.close()
