import smtplib
from email.message import EmailMessage
from email.utils import formataddr
import string
import random
from DatabaseConnection import DatabaseConnection
from FINALEncrypt import generate_key_from_passphrase
from config import read_config

conn = DatabaseConnection.get_connection("accounts.db")
cursor = conn.cursor()

PORT = 587
EMAIL_SERVER = "smtp.gmail.com"

# sender_email = "noreply.passvault1@gmail.com"
# password_email = "mdybfcplkymtwlyb"

sender_email, password_email = read_config()


def send_recovery_email(receiver_email, user_id):
    new_passphrase = generate_random_string(25)
    passphrase_tuple = generate_key_from_passphrase(new_passphrase)
    passphrase = passphrase_tuple[0]
    salt = passphrase_tuple[1]

    cursor.execute(
        "UPDATE passphrases SET passphrase = ?, salt = ? WHERE user_id = ?",
        (passphrase, salt, user_id),
    )

    # Create the base text message.
    msg = EmailMessage()
    msg["Subject"] = "Recovery Email-Pass Vault"
    msg["From"] = formataddr(("Password Vault", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    msg.set_content(
        f"""\
    Hello {user_id},

    We received a request for password recovery for your account. As per your request, we have generated a new password for you. Please find the details below:

    Recovery Password: {new_passphrase}

    Please use this password to log in to your account and reset your password as soon as possible for security reasons.

    If you did not request for a password recovery or have any concerns, please contact our customer support immediately.

    Thank you,
    Team Password Vault
    """
    )

    msg.add_alternative(
        f"""\
    <html>
      <body>
        <p>Hello {user_id},</p>

        <p>We received a request for password recovery for your account. As per your request, we have generated a new password for you. Please find the details below:</p>

        <p>Recovery Password: <strong>{new_passphrase}<strong></p>

        <p>Please use this password to log in to your account and reset your password as soon as possible for security reasons.</p>

        <p>If you did not request for a password recovery or have any concerns, please contact our customer support immediately.</p>

        <p>Thank you,<br>
        Team Password Vault</p>
        
      </body>
    </html>
    """,
        subtype="html",
    )

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("Password recovery email sent!")


def generate_random_string(length):
    """Generate a random string of specified length."""
    letters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(letters) for _ in range(length))


def send_verification_email(receiver_email, verification_token):
    msg = EmailMessage()
    msg["Subject"] = "Account Verification Email-Pass Vault"
    msg["From"] = formataddr(("Password Vault", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    msg.set_content(
        f"""\
    Hello user,

    Thank you for signing up for an account with our service. To complete your registration, please verify your email address using the token provided below:

    Verification Token: {verification_token}

    Please enter this token on the verification page to confirm your email address. If you did not sign up for an account or have any concerns, please contact our customer support immediately.

    Thank you for choosing our service.

    Best regards,
    Team Password Vault
    """
    )

    msg.add_alternative(
        f"""\
    <html>
      <body>
        <p>Hello user,</p>

        <p>Thank you for signing up for an account with our service. To complete your registration, please verify your email address using the token provided below:</p>

        <p>Verification Token: <strong>{verification_token}</strong></p>

        <p>Please enter this token on the verification page to confirm your email address. If you did not sign up for an account or have any concerns, please contact our customer support immediately.</p>

        <p>Thank you for choosing our service.</p>

        <p>Best regards,<br>
        Team Password Vault</p>
        
      </body>
    </html>
    """,
        subtype="html",
    )

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("Account verification email sent!")


if __name__ == "__main__":
    send_recovery_email(receiver_email="kulkarnianish63@gmail.com", user_id="AnishK")
