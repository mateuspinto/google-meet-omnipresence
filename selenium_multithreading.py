# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
import threading

from constants import *
from credentials import *


def open_meet(email: str, passwd: str, meet_url: str):

    profile = webdriver.FirefoxProfile()
    profile.set_preference('media.navigator.permission.disabled', True)
    profile.update_preferences()

    driver = webdriver.Firefox(profile)

    driver.get(LOGIN_URL)
    sleep(3)

    try:
        email_elem = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, LOGIN_XPATH)))
        email_elem.send_keys(email)
        email_elem.send_keys(Keys.RETURN)
        sleep(3)

        passwd_elem = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, LOGIN_XPATH)))
        passwd_elem.send_keys(passwd)
        passwd_elem.send_keys(Keys.RETURN)
        sleep(3)
    except:
        print("[Login error] -- aborting")
        driver.quit()
        exit(1)

    driver.get(meet_url)
    sleep(3)

    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, MIC_XPATH))).click()
    sleep(3)

    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, JOIN_XPATH))).click()
    sleep(3)

    max_users = -1

    while True:
        current_users: int = int(WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, USERS_XPATH))).text)

        if current_users > max_users:
            max_users = current_users
        elif current_users <= (max_users/2):
            driver.quit()
            exit(1)

        print("[" + meet_url + "]\nCurrent users = " +
              str(current_users) + "\nMax users = " + str(max_users) + "\n")
        sleep(5)


threading.Thread(target=open_meet, args=(MAIL, PASSWD, MEET1)).start()

while True:
    sleep(60)
    pass
