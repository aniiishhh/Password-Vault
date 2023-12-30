import random


def keyword_questions():
    print("🔑🔑🔑 Welcome! Get ready to generate keywords by answering some secret questions!🔑🔑🔑")
    print("(YES/NO): ")

    while True:
        reply1 = input("Your choice : ")

        if reply1.lower() == "no":
            print("")
            return {}
        elif reply1.lower() == "yes":
            print("🔒🔒🔒 Get ready to answer 5 random questions! 🔒🔒🔒")
            print("📝 Please provide short answers for accurate keywords. 📝")

            questions = {
                1: "What is the name of your first pet?",
                2: "What is the make and model of your first car?",
                3: "What is the name of your favorite childhood teacher?",
                4: "What is the name of the street you grew up on?",
                5: "What is your favorite childhood memory?",
                6: "What is the name of your childhood best friend?",
                7: "What is the name of your favorite fictional character?",
                8: "What is your favorite book?",
                9: "What is the name of your favorite childhood toy?",
                10: "What is the name of the first concert you attended?",
                11: "What is your favorite vacation destination?",
                12: "What is the name of your favorite restaurant?",
                13: "What is your favorite hobby?",
                14: "What is the name of your favorite sports team?",
                15: "What is your favorite type of food?",
                16: "What is your favorite movie?",
                17: "What is your favorite TV show?",
                18: "What is your favorite color?",
                19: "What is your favorite season of the year?",
                20: "What is your favorite animal?",
            }

            question_numbers = random.sample(list(questions.keys()), 5)

            answers = dict()

            for i in range(1, 6):
                question_number = question_numbers[i - 1]
                question = questions[question_number]

                while True:
                    answer = input(f"⭐ Question {i}: {question}\n🔍 Your Answer (or type 'skip' to skip): ")
                    if answer.lower() == "skip":
                        question_number = random.choice(
                            list(set(questions.keys()) - set(question_numbers))
                        )
                        question = questions[question_number]
                        continue
                    else:
                        answer = "".join(answer.split())
                        answers[question_number] = answer
                        break

            print("🎉 Thank you for your patience!")
            print(
                "\n# -------------------------------------------------------------------------------------------------------------------------------- #\n"
            )

            return answers
        else:
            print("Please enter either (YES/NO)")
            continue


# -------------------------------------------------------------------------------------------------------------------------------- #


def keywords_to_include():
    keywords = list()

    while True:
        reply1 = input("🔑 Would you like to customize your password with unique keywords? (YES/NO): ")

        if reply1.lower() == "no":
            print("")
            return []
        elif reply1.lower() == "yes":
            print("🔍 Enter any keywords you can recall and want to include in your password.")
            print("    NOTE: Enter only unique keywords (Enter DONE to exit!): ")

            while True:
                keyword = input("=> ")

                if keyword.lower() == "done":
                    break

                if not keyword.isalpha():
                    print("🔤 Please enter a valid one-word containing only alphabets.")
                    continue

                keywords.append(keyword)

            print(
                "\n# -------------------------------------------------------------------------------------------------------------------------------- #\n"
            )

            return keywords
        else:
            print("Please enter either (YES/NO)")
            continue


# -------------------------------------------------------------------------------------------------------------------------------- #


def min_length():
    while True:
        min_length = input("🔒 **Enter the minimum length of the password: ")

        try:
            min_length = int(min_length)

            if min_length < 10 or min_length > 25:
                print(
                    "⚠️ The password's minimum length should be between 10 and 25 characters. Please try again."
                )
                continue

        except:
            print("❌ Invalid inputs. Please try again.")
            continue

        break

    print(
        "\n# -------------------------------------------------------------------------------------------------------------------------------- #\n"
    )

    return min_length


# -------------------------------------------------------------------------------------------------------------------------------- #


def purpose_of_pass():
    while True:
        purpose = input("💼 **Mention the purpose of generating this password (e.g. website or app name) : ")
        if len(purpose) < 5:
            print("Input must be at least 5 characters long.")
            continue

        break

    return purpose.lower()


# -------------------------------------------------------------------------------------------------------------------------------- #


def special_char_list():
    all_special_char = [
        "!",
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*",
        "-",
        "_",
        "+",
        "=",
        "|",
        "\\",
        "/",
        "{",
        "}",
        "[",
        "]",
        "(",
        ")",
        ":",
        ";",
        '"',
        "'",
        "<",
        ">",
        ",",
        ".",
        "?",
        "`",
    ]
    allowed_special_char = list()

    while True:
        reply = input("🔒 Are there any limitations on using special characters in your password? (YES/NO): ")

        if reply.lower() == "no":
            print("")
            return all_special_char
        elif reply.lower() == "yes":
            print(
                "⚡️ Enter a special character that can be included in a password (Enter DONE to exit!) ⚡️"
            )

            while True:
                special_char = input("=> ")

                if special_char.lower() == "done":
                    break

                if special_char in all_special_char:
                    allowed_special_char.append(special_char)
                    continue
                else:
                    print(
                        "❌ That is not a valid special character. Please try again. ❌"
                    )
                    continue

            print(
                "\n# -------------------------------------------------------------------------------------------------------------------------------- #\n"
            )

            return allowed_special_char
        else:
            print("Please enter either (YES/NO)")
            continue


# -------------------------------------------------------------------------------------------------------------------------------- #


def keynumbers_to_include():
    keynumbers = list()

    while True:
        reply1 = input("💫 Would you like to specify any lucky numbers to include in your password? (YES/NO) : ")

        if reply1.lower() == "no":
            print("")
            return []
        elif reply1.lower() == "yes":
            print("🔢 Enter any key numbers you can remember and would like to include in your password. NOTE: Enter only unique numbers (Enter DONE to exit!): ")

            while True:
                keynumber = input("=> ")

                if keynumber.lower() == "done":
                    break

                if len(keynumber) > 4:
                    print("🍀 Please enter a lucky number with a maximum of 4 characters: ")
                    continue

                try:
                    keynumber = int(keynumber)
                except:
                    print("❌ Please enter a valid integer.")
                    continue

                keynumbers.append(keynumber)

            print(
                "\n# -------------------------------------------------------------------------------------------------------------------------------- #"
            )

            return keynumbers
        else:
            print("Please enter either (YES/NO)")
            continue


# -------------------------------------------------------------------------------------------------------------------------------- #


def input_menu_choice():
    while True:
        menu_choice = input("Enter your choice : ")

        try:
            menu_choice = int(menu_choice)
        except:
            print("❌ Please enter a valid integer.")
            continue

        if menu_choice not in range(1, 4):
            print("❌ Please enter a valid menu choice.")
            continue
        else:
            return menu_choice


# -------------------------------------------------------------------------------------------------------------------------------- #


def input_pass_id():
    while True:
        pass_id = input("\nEnter the password number you would like to store (1-20) : ")

        try:
            pass_id = int(pass_id)
        except:
            print("❌ Please enter a valid integer.")
            continue

        if pass_id not in range(1, 21):
            print("❌ Please enter a valid password number.")
            continue
        else:
            return pass_id


# -------------------------------------------------------------------------------------------------------------------------------- #


def input_choice():
    while True:
        choice = input("Enter your choice : ")

        try:
            choice = int(choice)
        except:
            print("❌ Please enter a valid integer.")
            continue

        if choice not in range(1, 9):
            print("❌ Please enter a valid menu choice.")
            continue
        else:
            return choice


# -------------------------------------------------------------------------------------------------------------------------------- #
