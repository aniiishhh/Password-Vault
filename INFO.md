# Project Overview

Welcome to the Password Vault, a robust command-line application designed for secure and efficient password management. Here's an overview of the key functionalities and user experience:

## First-Time Setup

1. **Master Email and Password:**
   - On the first run, users are prompted to input a MASTER email ID and password.
   - This MASTER email serves as the primary channel for automated recovery and account verification emails.
   - **NOTE: Some devices may restrict Python from accessing email IDs using regular passwords. If you encounter issues, consider generating an app password for your email ID. Learn         more about creating app passwords [here](<https://support.google.com/accounts/answer/185833?hl=en#zippy=>).**

## Master Menu

The user is directed to the **MASTER MENU**, where they can choose from the following options:

1. **Access Existing Account (Login)**
2. **Create New Account (Sign up)**
3. **Delete Existing Account**
4. **Forgot Password (Receive a new password via email)**
5. **Quit the Application**

## Account Creation

When creating a new account, users are guided through the process, providing:

- Account details.
- A secure PASSPHRASE, which acts as the primary key to access the vault (irretrievable and crucial).
- Recovery email ID, which requires verification through an automated email.

## Main Menu

After logging in, users enter the **MAIN MENU**, offering a range of actions within their personal environment:

1. **Create a New Password**
2. **Retrieve Existing Password**
3. **Update Existing Password Manually**
4. **Delete Existing Password**
5. **Change Account Passphrase**
6. **Show the Password Table**
7. **Generate a Custom Password using Password Generator**
8. **Logout**

## Security Measures

- Account passphrase is repeatedly requested for security during account actions.
- Every password is associated with a purpose (e.g., "BANK ABC" or "SOCIAL MEDIA XYZ").

## Custom Password Generator

- The 7th option in the MAIN MENU leads users to a screen for generating custom passwords.
- Users respond to prompts, and 20 custom passwords are generated based on their inputs.
- Users can save one password or regenerate based on the same responses.

## Password Table

- Users can view their passwords table through the **MAIN MENU's 6th option**.
- The table is formatted, but passwords are hidden for added security.

## Logout and Termination

- After completing actions, users can log out, returning to the **MASTER MENU**.
- Choosing the last option in the **MASTER MENU** terminates the application.

**Important Note:**
The PASSPHRASE is the critical key to access the user's vault, while passwords are associated with specific purposes. Ensure the secure handling and remembrance of your PASSPHRASE.

Explore the Password Vault and manage your passwords with confidence and efficiency!
