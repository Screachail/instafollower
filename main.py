import os
import time
from random import choice
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

CHROME_DRIVER_PATH = "/home/user/Downloads/chromedriver"
SIMILAR_ACCOUNT = ""
USERNAME = ""
PASSWORD = ""


def wait():
    random_times = [3, 2, 3, 1, 4]
    time.sleep(choice(random_times))


class InstaFollower:
    def __init__(self, account: str):
        self.account_following = account
        self.follower_count = 0
        self.service = Service(CHROME_DRIVER_PATH)
        self.service.start()
        self.driver = webdriver.Remote(self.service.service_url)
        self.driver.maximize_window()

    def click_tag_with_text_in(self, tag: str, text: str):
        wait()
        index = 0
        tags = self.driver.find_elements(by=By.TAG_NAME, value=tag)
        wait()
        for tag in tags:
            if text in tag.text:
                wait()
                tags[index].click()
                break
            else:
                index += 1

    def click_tag_exact(self, tag: str, text: str):
        index = 0
        tags = self.driver.find_elements(by=By.TAG_NAME, value=tag)
        wait()
        for tag in tags:
            if text == tag.text:
                wait()
                tags[index].click()
                return
            else:
                index += 1
        return -1

    def scroll_followers(self):
        wait()
        scrollable = self.driver.find_element(by=By.CLASS_NAME, value="_aano")
        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable)

    def login(self):
        url = "https://www.instagram.com/accounts/login/"
        self.driver.get(url)
        wait()
        self.driver.find_element(By.XPATH, '//button[normalize-space()="Allow essential and optional cookies"]').click()
        inputs = self.driver.find_elements(by=By.TAG_NAME, value="input")
        inputs[0].send_keys(USERNAME)
        inputs[1].send_keys(PASSWORD)
        self.click_tag_with_text_in("button", "Log in")
        self.click_tag_with_text_in("button", "Not Now")
        self.click_tag_with_text_in("button", "Not Now")
        wait()

    def find_followers(self):
        url = f"https://www.instagram.com/{self.account_following}/"
        self.driver.get(url)
        wait()
        self.click_tag_exact("button", "Follow")
        list_items = self.driver.find_elements(by=By.TAG_NAME, value="li")
        self.follower_count = int(list_items[1].text.replace(',', '').split(' ')[0])
        print(f"{SIMILAR_ACCOUNT} has {self.follower_count} followers")
        wait()

    def follow_followers(self):
        self.click_tag_with_text_in("li", "followers")
        time.sleep(3)
        for i in range(self.follower_count):
            print(f"Round ({i})")
            if self.click_tag_exact("button", "Follow") == -1:
                print("Checking for cancel button")
                if self.click_tag_exact("button", "Cancel") == -1:
                    print("Scrolling!")
                    self.scroll_followers()
                elif self.click_tag_exact("button", "Requested") == -1:
                    print("Scrolling!")
                    self.scroll_followers()

    def quit(self):
        self.driver.quit()


bot = InstaFollower(SIMILAR_ACCOUNT)
bot.login()
bot.find_followers()
bot.follow_followers()
bot.quit()
