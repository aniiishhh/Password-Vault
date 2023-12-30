# Import user-defined modules and sqlite3
import UserInput3
from PrintStatements2 import print_Welcome, print_Menu
from PassGenerator2 import PassGenerator
from DatabaseConnection import DatabaseConnection
from datetime import datetime
from getpass import getpass
from FINALEncrypt import generate_specific_key_from_passphrase, encrypt_data


def password_generator(user_id):
    # -------------------------------------------------------------------------------------------------------------------------------- #
    # Connect to a database

    conn = DatabaseConnection.get_connection("accounts.db")
    cursor = conn.cursor()

    # -------------------------------------------------------------------------------------------------------------------------------- #
    # Print welcome statements

    print_Welcome()

    # -------------------------------------------------------------------------------------------------------------------------------- #
    # Assign function values (user inputs) to local variables

    while True:
        pass_purpose = UserInput3.purpose_of_pass()  # returns a string
        cursor.execute(
            "SELECT * FROM {} WHERE purpose = ?".format(user_id), (pass_purpose,)
        )
        result = cursor.fetchone()

        if result is None:
            PURPOSE_IN_TABLE = False
            break
        else:
            PURPOSE_IN_TABLE = True
            print('Password for "' + pass_purpose + '" already exists in database.')
            print(
                "Type 'YES' if you wish to update the password with the password generator. Type 'NO' to rewrite the purpose."
            )
            continue_option = input("Your reply : ").lower()

            if continue_option == "no":
                continue
            elif continue_option == "yes":
                UPDATE_PASSWORD = True
                break
            else:
                print("Invalid input. Please try again.")
                continue

    pass_minimum_length = UserInput3.min_length()  # returns an int
    pass_special_char = (
        UserInput3.special_char_list()
    )  # returns a user defined list() or default list()
    pass_keywords = UserInput3.keywords_to_include()  # returns a list() or []
    pass_keywords_questions = (
        UserInput3.keyword_questions()
    )  # returns a dict() as (QID, Ans) or {}
    pass_keynumbers = UserInput3.keynumbers_to_include()  # returns a list() or []

    # -------------------------------------------------------------------------------------------------------------------------------- #
    # Convert dictionary values to list

    pass_keywords_questions_list = list(pass_keywords_questions.values())

    # -------------------------------------------------------------------------------------------------------------------------------- #
    # Password generation algorithm and User-Interaction

    # --------------------------------------------------------------------------------------------------------- #
    # Define a password dictionary to store generated passwords

    pass_dictionary = dict()

    # --------------------------------------------------------------------------------------------------------- #
    # Main password generation algorithm

    while True:
        # --------------------------------------------------------------------------------------------------------- #
        # Clear the dictionary while regenerating passwords

        pass_dictionary.clear()

        # --------------------------------------------------------------------------------------------------------- #
        # Generate passwords using algorithm

        for i in range(20):
            password = PassGenerator()
            password.keyword_selection(
                pass_keywords, pass_keywords_questions_list, pass_minimum_length
            )
            password.keynumber_selection(pass_keynumbers)
            password.minimum_characters_remaining(pass_minimum_length)
            password.choose_remaining_random_char(
                pass_minimum_length, pass_special_char
            )
            password.shuffle()
            password.random_caps_pass()

            # ----------------------------------------------------------------------------------------- #
            # Store passwords in dictionary and print generated password over each iteartion of loop

            pass_dictionary[i + 1] = str(password)

            print(f"{i + 1}) {password}")

        # --------------------------------------------------------------------------------------------------------- #
        # User-interaction part, print menu and input user choice

        print_Menu()

        menu_choice = UserInput3.input_menu_choice()

        # --------------------------------------------------------------------------------------------------------- #
        # Insert the desired password in the database

        if menu_choice == 1:
            pass_id = UserInput3.input_pass_id()
            pass_to_store = pass_dictionary[pass_id]

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if not PURPOSE_IN_TABLE:
                cursor.execute(
                    "SELECT * FROM passphrases WHERE user_id = ?", (user_id,)
                )
                passphrases_row = cursor.fetchone()
                salt = passphrases_row[3]

                passphrase = getpass("Please enter your secret passphrase to confirm: ")
                key = generate_specific_key_from_passphrase(passphrase, salt)

                if passphrases_row[2] != key:
                    print("Action denied!")
                    continue

                pass_to_store = encrypt_data(pass_to_store, key)

                cursor.execute(
                    "INSERT INTO {} (password, purpose, timestamp) VALUES (?, ?, ?)".format(
                        user_id
                    ),
                    (pass_to_store, pass_purpose, timestamp),
                )
                conn.commit()
                print("Password added!")

            if PURPOSE_IN_TABLE and UPDATE_PASSWORD:
                cursor.execute(
                    "SELECT * FROM passphrases WHERE user_id = ?", (user_id,)
                )
                passphrases_row = cursor.fetchone()
                salt = passphrases_row[3]

                passphrase = getpass("Please enter your secret passphrase to confirm: ")
                key = generate_specific_key_from_passphrase(passphrase, salt)

                if passphrases_row[2] != key:
                    print("Action denied!")
                    continue

                pass_to_store = encrypt_data(pass_to_store, key)

                cursor.execute(
                    "UPDATE {} SET password = ?, timestamp = ? WHERE purpose = ?".format(
                        user_id
                    ),
                    (pass_to_store, timestamp, pass_purpose),
                )
                conn.commit()
                print("Password updated!")

            break

        # --------------------------------------------------------------------------------------------------------- #
        # Regenerate passwords

        elif menu_choice == 2:
            print("Regenerating passwords...\n")
            continue

        # --------------------------------------------------------------------------------------------------------- #
        # Break and return to the original Main Menu

        elif menu_choice == 3:
            break

        # --------------------------------------------------------------------------------------------------------- #
        # Print Error message

        else:
            print("Invalid choice! Please choose again.")


# -------------------------------------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    password_generator()

# -------------------------------------------------------------------------------------------------------------------------------- #
