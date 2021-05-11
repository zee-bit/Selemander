import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)

from auth import Authenticate
from styles import in_color, styled_error, styled_input, styled_success, styled_warning

# Create an Options object and pass headless argument
ch_ops = Options()
ch_ops.add_argument("--headless")

driver = webdriver.Chrome(options=ch_ops)
# driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('https://teams.microsoft.com/')
assert "Sign in to your account" in driver.title

auth = Authenticate(driver)
driver = auth.login()

styled_warning("Control regained by app.py")
try:
    title_has_teams = WebDriverWait(driver, 20).until(EC.title_contains('Microsoft Teams'))
    person_drop_present = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'personDropdown')))
except TimeoutException as ex:
    styled_error("Timeout Error: Sorry Teams is taking too long to respond. Exiting...")
    driver.quit()

is_teams_clickable = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'app-bar-2a84919f-59d8-4441-a975-2a8c2643b741')))
is_teams_clickable.click()

styled_success('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
styled_success('\t\tLIST OF TEAMS')
styled_success('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

channels_container = driver.find_element_by_tag_name("channel-list")
channels_list = channels_container.find_elements_by_class_name('team')

# channel-list is polluted with few channels having 'data-tid' attr as None
channels_list = [ch for ch in channels_list if ch.get_attribute('data-tid') is not None]

for channel in channels_list:
    channel_name = channel.find_element_by_class_name("header-text").get_attribute('innerText')
    # print(channel_name, channel.find_element_by_class_name("header-text"))
    styled_success(f'  ▶ {channel_name}')

styled_warning("\nSearching for ongoing meetings...")

driver.quit()
