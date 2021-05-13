import time
from collections import OrderedDict

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
driver.implicitly_wait(20)
driver.get('https://teams.microsoft.com/')
assert "Sign in to your account" in driver.title

auth = Authenticate(driver)
driver = auth.login()

styled_warning("Control regained by app.py. Loading your teams...")
try:
    title_has_teams = WebDriverWait(driver, 20).until(EC.title_contains('Microsoft Teams'))
    person_drop_present = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'personDropdown')))
except TimeoutException as ex:
    styled_error("Timeout Error: Sorry Teams is taking too long to respond. Exiting...")
    driver.quit()

is_teams_clickable = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'app-bar-2a84919f-59d8-4441-a975-2a8c2643b741')))
is_teams_clickable.click()

styled_success('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
styled_success('\t\tYOUR TEAMS')
styled_success('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

teams_container = driver.find_element_by_tag_name("channel-list")
teams_list = teams_container.find_elements_by_class_name('team')
# print(teams_list)

# team-list is polluted with few teams having 'data-tid' attr as None
teams_list = [tm for tm in teams_list if tm.tag_name == 'li']
# print(teams_list[0].tag_name, teams_list[1].tag_name)
teams_channel_mp = OrderedDict()

for team in teams_list:
    # driver.execute_script("arguments[0].setAttribute('aria-expanded', true)", team)
    # time.sleep(1)
    # btn = WebDriverWait(team, 10).until(EC.element_to_be_clickable((By.XPATH, "//h3/a[@data-tid]")))
    btn = team.find_element_by_tag_name("a")
    # print(btn.tag_name, btn.get_attribute('data-tid'), team.get_attribute("aria-expanded"))
    btn.click()
    if team.get_attribute('aria-expanded') == 'false':
        driver.execute_script("arguments[0].click()", btn)
    team_header = team.find_element_by_class_name("header-text")
    team_name = team_header.get_attribute('innerText')

    styled_success(f' ▶ {team_name}')

    try:
        channel_container = team.find_element_by_class_name('channels')
    except NoSuchElementException as ex:
        driver.execute_script("arguments[0].setAttribute('aria-expanded', true)", team)
        channel_container = team.find_element_by_class_name('channels')
    channel_list = channel_container.find_elements_by_tag_name('li')
    for channel in channel_list:
        channel_name = channel.find_element_by_tag_name("span").get_attribute("innerText")

        styled_success(f'     {channel_name}')

        try:
            active_call_marker = channel.find_element_by_tag_name("active-calls-counter")
            styled_warning("     Found an ongoing meeting in this channel. Trying to join...")
            channel.click()
        except NoSuchElementException as ex:
            # channel.click()
            styled_error("     No ongoing meetings in this channel. Skipping...")
    print('\n')

# print(teams_channel_mp)

# for team_info, channels in teams_channel_mp.items():
#     team_info[1].click()
#     for channel in channels:
#         print(channel.get_attribute("innerHTML"))
#         driver.quit()
#         channel_name = channel.find_element_by_tag_name("span").get_attribute("innerText")
#         styled_warning(f"➔ # {team_info[0]} ▶ {channel_name}")

driver.quit()
