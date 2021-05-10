from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)

from auth import Authenticate

# Create an Options object and pass headless argument
ch_ops = Options()
ch_ops.add_argument("--headless")

driver = webdriver.Chrome(options=ch_ops)
driver.implicitly_wait(10)
driver.get('https://teams.microsoft.com/')
assert "Sign in to your account" in driver.title

auth = Authenticate(driver)
driver = auth.login()
driver.quit()
