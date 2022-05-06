from asyncio import TimeoutError
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from config import *
import os

class Browser:
    def __init__(self):
        """
        Represents a Selenium browser object with added functions for Discord-specific purposes.
        No parameters; global settings are used from py.

        Methods
        -----------
        browser_login()
            Opens the browser to the Discord channel and logs in if necessary.
            Returns True if load successful.
            Raises TimeoutError if the page does not load.
            Raises ValueError if incorrect page loads.
        send_text(text)
            Send text to active channel.
        react_emoji(emoji, message_id)
            Searches and clicks an emoji button.
            Raises Exception if button was not found.
        roll(count)
            Sends the roll command for count number of times with 3 seconds between each roll.
        refresh()
            Refreshes the page.
        close()
            Closes the browser window.
        """
        # Selenium browser control here
        options = Options()
        options.add_argument("-headless")
        self.driver = webdriver.Firefox(
            executable_path=WEB_DRIVER_PATH,
            options=options,
            service_log_path=os.devnull,
        )
        self.actions = ActionChains(self.driver)

    # Initiate browser
    def browser_login(self, *args):
        self.driver.get(f"https://discord.com/channels/{SERVER_ID}/{CHANNEL_ID}")
        try:
            email = WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element(By.NAME, "email")
            )
        except TimeoutException:
            if f"{SERVER_ID}/{CHANNEL_ID}" not in self.driver.current_url:
                # No login screen, but wrong channel (some weird error)
                raise TimeoutError
        else:
            email.send_keys(LOGIN_INFO[0])
            self.driver.find_element(By.NAME, "password").send_keys(LOGIN_INFO[1])
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            try:
                # Wait for main screen
                WebDriverWait(self.driver, 30).until(
                    lambda x: x.find_element(By.CLASS_NAME, "slateTextArea-1Mkdgw")
                )
                if f"{SERVER_ID}/{CHANNEL_ID}" not in self.driver.current_url:
                    # Logged in, but wrong channel (some weird error)
                    raise ValueError
            except TimeoutException or NoSuchElementException:
                raise TimeoutError
            except ValueError:
                raise ValueError
            else:
                return True

    def send_text(self, text: str, *args):
        # For some reason, typing directly into the message box doesn't work
        # ActionChains must be used instead to type character by character
        self.actions = ActionChains(self.driver)

        try:
            message_box = WebDriverWait(self.driver, 1).until(
                lambda x: x.find_element(By.CLASS_NAME, "slateTextArea-1Mkdgw")
            )
        except TimeoutException:
            self.refresh()
            return self.send_text(text)
        self.actions.click(on_element=message_box)
        for char in text:
            self.actions.key_down(char)
            self.actions.key_up(char)
        self.actions.key_down(Keys.ENTER)
        self.actions.key_up(Keys.ENTER)
        self.actions.perform()

    def refresh(self):
        self.driver.refresh()
        WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element(By.CLASS_NAME, "slateTextArea-1Mkdgw")
        )

    def close(self):
        self.driver.close()
