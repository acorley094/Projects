# Project Description: Password Generation Tool

## Overview

This simple Python script, **Password Generation Tool**, provides a secure way to generate random passwords and optionally encrypt them using the bcrypt hashing algorithm. The tool uses the `secrets` module for password generation and the `bcrypt` library for password hashing.

## Features

- **Random Password Generation:** Generates random passwords of specified length using a combination of letters, digits, and punctuation.
  
- **Bcrypt Password Hashing:** Utilizes the bcrypt library to securely hash passwords, ensuring a high level of security.

- **Optional Encryption:** Allows users to choose whether to encrypt the generated password using bcrypt. Note that bcrypt is a one-way hashing function; encrypted passwords cannot be decrypted.

- **Username Support:** Accommodates usernames associated with accounts.

- **Simple Command-line Interface:** Offers a straightforward command-line interface for ease of use.

## Usage

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/acorley094/password-generation-tool.git
   cd password-generation-tool
   ```

2. **Run the Script:**
   ```bash
   ./password_gen.py -h
   ```
   This command displays help information and the available command-line options.

3. **Generate a Password:**
   ```bash
   ./password_gen.py example_website -u example_username
   ```
   This command generates a random password for the specified website and username.

4. **Encrypt the Password (Optional):**
   ```bash
   ./password_gen.py example_website -u example_username -e
   ```
   This command encrypts the generated password using bcrypt. Note that encrypted passwords cannot be decrypted.

5. **Save the Password:**
   After generating a password, the tool prompts whether to save it. Choose 'Y' to save the password in the `passwords.txt` file.

## Important Notes

- **Security Precautions:** Ensure secure handling of generated passwords, especially when choosing to encrypt them. Mark down the generated password in a secure location if encrypted.

- **Encryption Warning:** Encrypted passwords cannot be decrypted. Carefully consider the implications before choosing to encrypt passwords.

- **Filename:** The script saves passwords in a file named `passwords.txt`. Ensure appropriate access controls on this file.

## Author

- **Author:** acorley094

## License

This tool is provided under the MIT License. See the [LICENSE](LICENSE) file for details.

Feel free to contribute, report issues, or suggest improvements!
