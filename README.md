# Brutium

This script was written to automate the process of attempting logins on a given URL using a list of usernames and passwords. The primary motivation behind developing this script was to find a way to bypass anti-CSRF (Cross-Site Request Forgery) tokens that are often used to protect web forms from unauthorized actions. By using Selenium for browser automation, this script can efficiently perform login attempts and identify successful logins, even in the presence of anti-CSRF tokens. I know there are other ways to do this say in burp or caido or zap but doing it this way makes more sense to me. 

This script was only tested on RoundCube Email service 1.6.7 and worked great. I can not say it fully works for older versions but I dont see why not. https://github.com/roundcube/roundcubemail

## Disclaimer

**This script is intended for educational purposes only. The author does not condone or support any illegal or malicious activities. Use this script responsibly and only on systems you have explicit permission to test. The author is not responsible for any misuse or damage caused by this script.**

## Requirements

- Python 3.x
- Selenium
- webdriver_manager

## Installation

Install the required packages:

```bash
pip install selenium webdriver_manage
```
## Usage
`python brutium.py --url <login_url> --username_file <path_to_username_file> --password_file <path_to_password_file> --login_button <button_locator> --presence_of_element <success_element_locator> --error_message_locator <error_element_locator> --error_message_string <error_message> [--headless]`

### Threading

The script uses threading to perform multiple login attempts concurrently, which speeds up the process. The number of concurrent threads is limited to 10 to prevent overwhelming the server but you can set it to anything that suits your need.

## Arguments
- --url: The login URL.
- --username_file: Path to the file containing usernames.
- --password_file: Path to the file containing passwords.
- --login_button: The login button locator (e.g., id:rcmloginsubmit). Format is <locator_type>:<locator_value>.
- --presence_of_element: Locator for the element that confirms login (e.g., id:mailboxlist). Format is <locator_type>:<locator_value>.
- --error_message_locator: Locator for the error message element (e.g., class_name:alert-warning). Format is <locator_type>:<locator_value>.
- --error_message_string: String to look for in the error message to identify failed login attempts.
- --headless: (Optional) Run browser in headless mode.

## Locators
Locators are used to identify elements on the web page. Common locator types are:

- id
- name
- class_name
- tag_name
- css_selector
- xpath

# Example Usage
`python3 brutium.py --url "http://192.168.117.129/roundcubemail/" --username_file "users.txt" --password_file "pass.txt" --login_button "ID:rcmloginsubmit" --presence_of_element "ID:mailboxlist" --error_message_locator "class_name:alert-warning" --error_message_string "Login failed." --headless`

![brutium_example](https://github.com/user-attachments/assets/32f07bde-fb70-4d33-a764-53d5b4d255ca)

## Future Improvement Ideas

- Add proxy support for spoofing IP addresses

# RoundCube_Email_BruteForce.py

Created specifically for Bruteforcing Roundcube eamail service

## Usage

- Change URL to the desired roundcube URL you are trying to attack
- Change the the username and password files to whatever you desire
- Run the script
- You can also change the number of threads to run, default is set to 10
