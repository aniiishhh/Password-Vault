from validate_email_address import validate_email
import dns.resolver
from RecoveryEmail import generate_random_string, send_verification_email


def validate_email_id(email_id):
    # Call the function to validate the entered email with DNS verification
    valid_email = validate_email(
        email_id, verify=False
    )  # Set verify=False to skip MX record check

    if valid_email:
        try:
            # Check MX record using dnspython resolver
            domain = email_id.split("@")[1]
            mx_records = dns.resolver.resolve(domain, "MX")
            if mx_records:
                print("Email is valid and MX record exists.")

                verification_token = generate_random_string(20)
                send_verification_email(email_id, verification_token)
                user_entered_token = input(
                    "Please verify account by entering the verification token: "
                )

                if verification_token != user_entered_token:
                    print("Invalid token. Returning to previous step.")
                    return False

                return True
            else:
                print("Email is valid but MX record does not exist.")
                return False
        except dns.resolver.NXDOMAIN:
            print("Email is valid but domain does not exist.")
            return False
        except Exception as e:
            print("Error checking MX record:", e)
            return False
    else:
        print("Email is not valid.")
        return False
