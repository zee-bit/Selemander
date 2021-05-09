import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from styles import styled_input

# Create an Options object and pass headless argument
ch_ops = Options()
ch_ops.add_argument("--headless")

# Instantiate a Chrome driver and pass the URL
driver = webdriver.Chrome(options=ch_ops)
driver.get('https://teams.microsoft.com/')
assert "Sign in to your account" in driver.title

# Find and store the required tags
sign_in_form = driver.find_element_by_xpath("//form [1]")
email_field = driver.find_element_by_xpath("//input[@name='loginfmt']")
next_button = driver.find_element_by_id("idSIButton9")
# print(sign_in_form.get_attribute('innerHTML'))

email = styled_input("EMAIL, PHONE OR SKYPE: ")

email_field.clear()
email_field.send_keys(email, Keys.RETURN)



time.sleep(10)
driver.quit()