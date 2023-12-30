# Import necessary user-defined modules

from DatabaseConnection import DatabaseConnection
import UserInput3
import FINALPassGen2
from PrintStatements2 import print_Main_Menu
from getpass import getpass
from datetime import datetime
from FINALEncrypt import (
    encrypt_data,
    decrypt_data,
    generate_specific_key_from_passphrase,
    generate_key_from_passphrase,
)


def MainMenu(user_id):
    # -------------------------------------------------------------------------------------------------------------------------------- #
    # Establish connection with the database

    conn = DatabaseConnection.get_connection("accounts.db")
    cursor = conn.cursor()

    # -------------------------------------------------------------------------------------------------------------------------------- #
    # User-Interaction and execute CRUD operations

    # Define the escape sequence for bold text
    BOLD = "\033[1m"

    # Reset the formatting
    RESET = "\033[0m"

    while True:
        # --------------------------------------------------------------------------------------------------------- #
        # Print Main Menu and take user input

        print_Main_Menu()

        choice = UserInput3.input_choice()

        # --------------------------------------------------------------------------------------------------------- #
        # Create new password manually

        if choice == 1:
            i = 0
            while i <= 5:
                purpose_of_pass = input(
                    "Please enter the purpose of the password : "
                ).lower()
                cursor.execute(
                    "SELECT * FROM {} WHERE purpose = ?".format(user_id),
                    (purpose_of_pass,),
                )
                result = cursor.fetchone()
                if result is None:
                    password_to_add = getpass("Enter the password to set : ")

                    cursor.execute(
                        "SELECT * FROM passphrases WHERE user_id = ?", (user_id,)
                    )
                    passphrases_row = cursor.fetchone()
                    salt = passphrases_row[3]

                    passphrase = getpass(
                        "Please enter your secret passphrase to confirm: "
                    )
                    key = generate_specific_key_from_passphrase(passphrase, salt)

                    if passphrases_row[2] != key:
                        print("Action denied!")
                        break

                    password_to_add = encrypt_data(password_to_add, key)

                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    cursor.execute(
                        "INSERT INTO {} (purpose, password, timestamp) VALUES (?, ?, ?)".format(
                            user_id
                        ),
                        (purpose_of_pass, password_to_add, timestamp),
                    )
                    conn.commit()
                    print("Password added!")
                    break
                elif result is not None:
                    print("The mentioned purpose already exists in the database.")
                    i = i + 1
                    if i == 6:
                        print("Maximum attempts reached. Returning to menu.")
                    continue
            if i == 6:
                continue

        # --------------------------------------------------------------------------------------------------------- #
        # Retrieve already existing password

        elif choice == 2:
            i = 0
            retrieved_pass_row = None
            while i <= 5:
                purpose_of_pass = input(
                    "Please enter the purpose of the password : "
                ).lower()
                cursor.execute(
                    "SELECT * FROM {} WHERE purpose = ?".format(user_id),
                    (purpose_of_pass,),
                )
                retrieved_pass_row = cursor.fetchone()
                if retrieved_pass_row is None:
                    print(
                        "The password for your given purpose- "
                        + purpose_of_pass
                        + " is not in the database!"
                    )
                    i = i + 1
                    if i == 6:
                        print("Maximum attempts reached. Returning to menu.")
                    continue
                elif retrieved_pass_row is not None:
                    break
            if i == 6:
                continue

            cursor.execute("SELECT * FROM passphrases WHERE user_id = ?", (user_id,))
            passphrases_row = cursor.fetchone()
            salt = passphrases_row[3]

            passphrase = getpass("Please enter your secret passphrase to confirm: ")
            key = generate_specific_key_from_passphrase(passphrase, salt)

            if passphrases_row[2] != key:
                print("Action denied!")
                continue

            retrieved_pass = retrieved_pass_row[2]

            retrieved_pass = decrypt_data(retrieved_pass, key)

            print(
                "The password for "
                + purpose_of_pass
                + " is "
                + BOLD
                + retrieved_pass
                + RESET
            )

        # --------------------------------------------------------------------------------------------------------- #
        # Update already existing password

        elif choice == 3:
            i = 0
            while i <= 5:
                purpose_of_pass = input(
                    "Please enter the purpose of the password : "
                ).lower()
                cursor.execute(
                    "SELECT * FROM {} WHERE purpose = ?".format(user_id),
                    (purpose_of_pass,),
                )
                result = cursor.fetchone()
                if result is None:
                    print(
                        "The password for your given purpose- "
                        + purpose_of_pass
                        + " is not in the database!"
                    )
                    i = i + 1
                    if i == 6:
                        print("Maximum attempts reached. Returning to menu.")
                    continue
                elif result is not None:
                    break
            if i == 6:
                continue

            cursor.execute("SELECT * FROM passphrases WHERE user_id = ?", (user_id,))
            passphrases_row = cursor.fetchone()
            salt = passphrases_row[3]

            passphrase = getpass("Please enter your secret passphrase to confirm: ")
            key = generate_specific_key_from_passphrase(passphrase, salt)

            if passphrases_row[2] != key:
                print("Action denied!")
                continue

            updated_pass = getpass("Enter a strong replacement password : ")

            if updated_pass == decrypt_data(result[2], key):
                print("New password is same as the previous password.")
                continue

            updated_pass = encrypt_data(updated_pass, key)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                "UPDATE {} SET password = ?, timestamp = {} WHERE purpose = ?".format(
                    user_id, timestamp
                ),
                (updated_pass, purpose_of_pass),
            )
            conn.commit()
            print("Password updated!")

        # --------------------------------------------------------------------------------------------------------- #
        # Delete already existing password

        elif choice == 4:
            i = 0
            while i <= 5:
                purpose_of_pass = input(
                    "Please enter the purpose of the password : "
                ).lower()
                cursor.execute(
                    "SELECT * FROM {} WHERE purpose = ?".format(user_id),
                    (purpose_of_pass,),
                )
                result = cursor.fetchall()
                if result is None:
                    print(
                        "The password for your given purpose- "
                        + purpose_of_pass
                        + " is not in the database!"
                    )
                    i = i + 1
                    if i == 6:
                        print("Maximum attempts reached. Returning to menu.")
                    continue
                elif result is not None:
                    break
            if i == 6:
                continue

            cursor.execute("SELECT * FROM passphrases WHERE user_id = ?", (user_id,))
            passphrases_row = cursor.fetchone()
            salt = passphrases_row[3]

            passphrase = getpass("Please enter your secret passphrase to confirm: ")
            key = generate_specific_key_from_passphrase(passphrase, salt)

            if passphrases_row[2] != key:
                print("Action denied!")
                continue

            cursor.execute(
                "DELETE FROM {} WHERE purpose=?".format(user_id), (purpose_of_pass,)
            )
            conn.commit()
            print("Delete successful!")

        # --------------------------------------------------------------------------------------------------------- #
        # Change account passphrase

        elif choice == 5:
            cursor.execute("SELECT * FROM passphrases WHERE user_id = ?", (user_id,))
            passphrases_row = cursor.fetchone()
            salt = passphrases_row[3]

            passphrase = getpass(
                "Please enter your original secret passphrase to confirm: "
            )
            key = generate_specific_key_from_passphrase(passphrase, salt)

            if passphrases_row[2] != key:
                print("Action denied!")
                continue

            while True:
                new_passphrase = getpass("Enter a new strong passphrase: ")
                re_enter_new_passphrase = getpass(
                    "Please enter the same passphrase to confirm: "
                )
                if new_passphrase != re_enter_new_passphrase:
                    print("The passphrases do not match. Please try again.")
                    continue
                elif new_passphrase == re_enter_new_passphrase:
                    break

            passphrase_tuple = generate_key_from_passphrase(new_passphrase)
            passphrase = passphrase_tuple[0]
            salt = passphrase_tuple[1]

            cursor.execute(
                "UPDATE passphrases SET passphrase = ?, salt = ? WHERE user_id = ?",
                (passphrase, salt, user_id),
            )
            print("Updated passphrase succesfully. Please login again to continue.")
            break

        # --------------------------------------------------------------------------------------------------------- #
        # Show passwords table

        elif choice == 6:
            cursor.execute("SELECT * FROM {}".format(user_id))
            rows = cursor.fetchall()
            print("\nID \t Purpose \t Password \t\t Date-Added ")
            for row in rows:
                print(
                    "{:<1}\t{:<10}\t{:<20}\t{}".format(
                        row[0], row[1], "*****PASSWORD*****", row[3]
                    )
                )

        # --------------------------------------------------------------------------------------------------------- #
        # Initialise password generator

        elif choice == 7:
            FINALPassGen2.password_generator(user_id)

        # --------------------------------------------------------------------------------------------------------- #
        # Exit the program

        elif choice == 8:
            print("Logging out!")
            break

    # --------------------------------------------------------------------------------------------------------- #
