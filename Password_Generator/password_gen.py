#! /usr/bin/python3
AUTHOR = 'acorley094'
PROJECT = 'Password Generation Tool'

import argparse
import secrets
import string
import bcrypt  # Import the bcrypt library

def generate_password(length):
    # Generate a random password
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def hash_password(password):
    #Hash the password using bcrypt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Decode to string for storage

def save_password(filename, website, username, password):
    # Save passwords and website names to a file
    with open(filename, 'a') as file:
        file.write(f"Website: {website}\n")
        if username:
            file.write(f"Username: {username}\n")
        file.write(f"Password: {password}\n")
        file.write("\n")

def main():
    # Configure command line argument parser
    parser = argparse.ArgumentParser(description=f"{PROJECT} written by {AUTHOR}", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('Website', help='website for the account')
    parser.add_argument('-u', '--username', help='username associated with the account. (username or email address)', default=' ')
    parser.add_argument('-e', '--encrypt', action='store_true', help='encrypt the generated password using bcrypt. *CANNOT BE DECRYPTED*. Suggested: Mark down the password generated in stdout in a secure location.')
    args = parser.parse_args()
    config = vars(args)

    website = config['Website']
    username = config['username']

    length = int(input("Enter the length of the password: "))
    password = generate_password(length)
    print("Generated Password:", password)

    if config['encrypt']:
        password_option = input("Do you want to save the encrypted password? (Y/n): ").lower()
        if password_option == 'y' or password_option == '':
            hashed_password = hash_password(password)
            filename = "./passwords.txt"
            save_password(filename, website, username, hashed_password)
            print("Password saved.")
    else:
        password_option = input("Do you want to save this password? (Y/n): ").lower()
        if password_option == 'y' or password_option == '':
            filename = "./passwords.txt"
            save_password(filename, website, username, password)
            print("Password saved.")

if __name__ == "__main__":
    main()
