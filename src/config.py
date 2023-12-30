import configparser
import getpass
import os

config_file = "config.ini"


def create_config():
    config = configparser.ConfigParser()
    config.add_section("Email")
    config.set(
        "Email",
        "sender_email",
        input("Enter email address (through which automated emails are sent): "),
    )

    # Securely prompt for the password
    password = getpass.getpass("Enter your email password: ")
    config.set("Email", "password_email", password)

    with open(config_file, "w") as configfile:
        config.write(configfile)


def read_config():
    config = configparser.ConfigParser()
    config.read(config_file)
    sender_email = config.get("Email", "sender_email")
    password_email = config.get("Email", "password_email")

    return sender_email, password_email


if not os.path.exists(config_file):
    create_config()

sender_email, password_email = read_config()

if __name__ == "__main__":
    print("Master Email:", sender_email)
