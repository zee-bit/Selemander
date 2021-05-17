import time
import stdiomask

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

from typing import Any
from styles.pretty_print import (
    in_color, styled_input, styled_error, styled_warning, styled_success)
from utils.config import _is_initialized, _write_selemrc, _parse_selemrc


class element_has_css_class(object):
    """
    An expectation for checking that an element has a particular css class.

    locator - used to find the element
    returns the WebElement once it has the particular css class
    """
    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(*self.locator)   # Finding the referenced element
        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False


class Authenticate:
    def __init__(self, driver):
        self.driver = driver
        self.email = ''
        self.passwd = ''

    def login(self):
        # Find and store the required sign-in form tag
        sign_in_form = self.driver.find_element_by_xpath("//form [1]")
        email_field = self.driver.find_element_by_xpath("//input[@name='loginfmt']")
        passwd_field = self.driver.find_element_by_xpath("//input[@name='passwd']")
        next_btn = self.driver.find_element_by_xpath("//input[@id='idSIButton9']")

        if _is_initialized():
            styled_warning(".selemrc located at /home. Parsing credentials...")
            self.email, self.passwd = list(_parse_selemrc().values())
            email_field.clear()
            email_field.send_keys(self.email, Keys.RETURN)
            passwd_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@name='passwd']"))
            )
            passwd_field.clear()
            passwd_field.send_keys(self.passwd, Keys.RETURN)
        else:
            styled_error("No .selemrc found in /home. Creating one...")
            styled_warning("This is a one-time setup. Please enter your credentials.\n")
            self.email = self.verify_input("EMAIL, PHONE OR SKYPE: ", email_field, "//input[@name='loginfmt']")
            # next_btn = WebDriverWait(driver, 10).until(
            #         EC.element_to_be_clickable((By.XPATH, "//input[@id='idSIButton9']")))
            passwd_field = WebDriverWait(self.driver, 10).until(
                        element_has_css_class((By.XPATH, "//input[@name='passwd']"), 'input'))
            passwd_field = self.driver.find_element_by_xpath("//input[@name='passwd']")
            self.passwd = self.verify_input("PASSWORD: ", passwd_field, "//input[@name='passwd']")

            # print(email, passwd)
            is_creds_stored = '\n' + _write_selemrc(self.email, self.passwd)
            styled_warning(is_creds_stored)

        styled_success("\nAuthentication successful. You are now logged in!!")
        styled_warning("Waiting for control to be passed to app...\n")

        no_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "idBtn_Back"))
        )
        # print(no_btn.get_attribute('value'))
        no_btn_click = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "idBtn_Back"))
        ).click()

        # self.driver.quit()
        return self.driver

    def verify_input(self, prompt: str, field: Any, xpath: str) -> str:
        if 'PASSWORD' in prompt:
            user_input = stdiomask.getpass(in_color('blue', prompt))
        else:
            user_input = styled_input(prompt)
        field.clear()
        field.send_keys(user_input, Keys.RETURN)
        try:
            next_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='idSIButton9']")))
        except StaleElementReferenceException as ex:
            return user_input
        except NoSuchElementException as ex:
            return user_input
        try:
            field = self.driver.find_element_by_xpath(xpath)
            # print(field)
            attrs = field.get_attribute("class")
            # print(attrs)
            if "has-error" in attrs:
                if "email" in field.get_attribute("type"):
                    styled_error('ERROR: No account with that username found.')
                else:
                    styled_error('ERROR: Invalid password. Try again.')
                return self.verify_input(prompt, field, xpath)
        except StaleElementReferenceException as ex:
            pass
        except NoSuchElementException as ex:
            pass
        return user_input