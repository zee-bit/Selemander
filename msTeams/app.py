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

from utils.auth import Authenticate
from styles.pretty_print import in_color, styled_error, styled_input, styled_success, styled_warning

# Create an Options object and pass headless argument
ch_ops = Options()
# ch_ops.add_argument("--headless")
ch_ops.add_argument("--use-fake-device-for-media-stream")
ch_ops.add_argument("--use-fake-ui-for-media-stream")

# Pass the argument 1 to allow and 2 to block
ch_ops.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1
  })

driver = webdriver.Chrome(options=ch_ops)
# driver = webdriver.Chrome()
# driver.implicitly_wait(20)
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

is_meeting_joined = False

def search_and_join_meetings():
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
        btn.click()

        # If the above click didnt work, then explicitly modify the attribute
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
            is_meetings_in_channel = False
            channel_name = channel.find_element_by_tag_name("span").get_attribute("innerText")

            styled_success(f'\t{channel_name}')

            # driver.implicitly_wait(0)
            active_call_marker = channel.find_elements_by_tag_name("active-calls-counter")
            # driver.implicitly_wait(20)
            if len(active_call_marker) == 0:
                styled_error("\tNo ongoing meetings in this channel. Skipping...")
            else:
                styled_warning("\tFound an ongoing meeting in this channel. Trying to join...")
                channel.find_element_by_xpath("//li/a").click()

                # time.sleep(5)
                message_container = driver.find_element_by_tag_name("message-list")
                # print(message_container.get_attribute("innerHTML"))

                # Reverse the message list array so that its easier to check from the last.
                message_list = WebDriverWait(message_container, 100).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ts-message-list-item")))
                # message_list = message_container.find_elements_by_xpath("//div[@class='ts-message-list-item']")[:-1]

                # test1, test2 = message_list[0], message_list[len(message_list) - 1]
                # print(len(message_list))
                # print(test1.tag_name, test2.tag_name)
                # print(test1.get_attribute("data-scroll-pos"), test2.get_attribute("data-scroll-pos"))

                for msg in message_list:
                    # Look for messages with ongoing meetings and click the join button
                    ongoing_call = msg.find_elements_by_class_name("ts-ongoing-call-header")
                    if(len(ongoing_call) != 0):
                        # join_btn = WebDriverWait(ongoing_call[0], 10).until(EC.element_to_be_clickable((By.XPATH, "//calling-join-button/button[@class='ts-calling-join-button']")))
                        # join_btn = ongoing_call[0].find_element_by_xpath("//calling-join-button/button[@class='ts-calling-join-button']")
                        join_btn_outer = ongoing_call[0].find_element_by_tag_name("calling-join-button")
                        join_btn = join_btn_outer.find_element_by_tag_name("button")
                        # print(join_btn.tag_name, join_btn.get_attribute("innerHTML"))
                        # join_btn.click()
                        driver.execute_script("arguments[0].click();", join_btn)
                        # webdriver.ActionChains(driver).move_to_element(element ).click(element ).perform()
                    else:
                        continue

                    # Configure presentation options from the meeting lobby. i.e.
                    # Switch off camera and microphone and join the meeting.
                    meeting_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "video-and-name-input")))
                    meeting_control_panel = meeting_container.find_element_by_xpath("//section[@class='controls-container']")
                    presentation_container = meeting_container.find_element_by_xpath("//div[@role='presentation']")

                    join_btn = meeting_control_panel.find_element_by_xpath("//button[contains(@class, 'join-btn')]")
                    camera_toggle = WebDriverWait(presentation_container, 10).until(EC.element_to_be_clickable((By.XPATH, "//toggle-button[@data-tid='toggle-video']/div/button")))
                    mic_toggle = WebDriverWait(presentation_container, 10).until(EC.element_to_be_clickable((By.XPATH, "//toggle-button[@data-tid='toggle-mute']/div/button")))

                    if(camera_toggle.get_attribute("aria-pressed") == 'true'):
                        # camera_toggle.click()
                        driver.execute_script("arguments[0].click();", camera_toggle)
                    if(mic_toggle.get_attribute("aria-pressed") == 'true'):
                        # mic_toggle.click()
                        driver.execute_script("arguments[0].click();", mic_toggle)
                    join_btn.click()
                    styled_success("Meeting joined successfully.")
                    is_meetings_in_channel = True
                    is_meeting_joined = True
                    # FIXME: Should we really break here and not search in further channels?
                    break
            # FIXME: Should we really break here and not search in further teams?
            if is_meetings_in_channel:
                break
        if is_meeting_joined:
            break
        print('\n')

# Run the search for the first time
search_and_join_meetings()

# If no ongoing meetings found, then re-search after 10 mins(?)
while not is_meeting_joined:
    styled_warning("No meetings were found. Re-searching in 600 secs")
    time.sleep(600)
    styled_warning("Initiating search...")
    search_and_join_meetings()

# print(teams_channel_mp)

# for team_info, channels in teams_channel_mp.items():
#     team_info[1].click()
#     for channel in channels:
#         print(channel.get_attribute("innerHTML"))
#         driver.quit()
#         channel_name = channel.find_element_by_tag_name("span").get_attribute("innerText")
#         styled_warning(f"➔ # {team_info[0]} ▶ {channel_name}")

# FIXME: We shouldn't quit the browser session. This will remove you from meeting as
# soon as you join.
# driver.quit()
