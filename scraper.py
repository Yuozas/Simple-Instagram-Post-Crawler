import os
import random
import sys
import time
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Post link for bot
post_id = input("Instagram Post ID:")
post_link = "https://www.instagram.com/p/" + post_id + "/"
# Everything related to posts comments saves to the lists, sets.
unique_user_set = set()
user_list = []
comment_list = []
# Variables to set outside done now for testing
unique = False
posers_ig_name = 'whatever'
button_xpath = '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li/div/button'


def get_all_user_indexes(element):
    index_pos_list = []
    index_pos = 0
    while True:
        try:
            # Search for item in list from index_pos to the end of list
            index_pos = user_list.index(element, index_pos)
            # Add the index position in list
            index_pos_list.append(index_pos)
            index_pos += 1
        except ValueError as e:
            break
    return index_pos_list


def get_all_user_comments(indexes):
    user_comments = []
    for x in indexes:
        user_comments.append(comment_list[x])
    return user_comments


def check_for_button_on_start(driver):
    while True:
        try:
            driver.find_element_by_xpath(button_xpath)
            break
        except StaleElementReferenceException:
            # Ignore Stale elements exception. That's when bot is not allowed to click for some reason.
            pass
        except NoSuchElementException:
            return


def clicker(driver):
    while True:
        try:
            button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, button_xpath)))
            button.click()
        except TimeoutException:
            break
        # Finish when no more buttons


"""
def get_all_user_data_from_elements_old_version_use_if_slow_device(driver):
    comment = driver.find_elements_by_css_selector('div.C4VMK')  # Get all comments
    for c in comment:
        # Append user data from all comments
        while True:
            try:
                user = c.find_element_by_css_selector('a.TlrDj')
                user = user.get_attribute("title")
                comment = c.find_element_by_css_selector('span')
                comment = comment.get_attribute('innerHTML')
                break
            except StaleElementReferenceException:
                # In case StaleElementReferenceException
                # print("StaleElementReferenceException")
                WebDriverWait(driver, 5).until(EC.staleness_of((By.CSS_SELECTOR, 'a.TlrDj')))
                WebDriverWait(driver, 5).until(EC.staleness_of((By.CSS_SELECTOR, 'span')))
        # Skip post description
        if user == posers_ig_name:
            continue
        if unique:
            unique_user_set.update(user)  # Save unique user
        user_list.append(user)  # Save none unique user
        comment_list.append(comment)  # Save none unique comment
"""


def get_all_user_data_from_elements(driver):
    comment = driver.find_elements_by_css_selector('div.C4VMK')  # Get all comments
    for c in comment:
        # Append user data from all comments
        user = c.find_element_by_css_selector('a.TlrDj')
        user = user.get_attribute("title")
        comment = c.find_element_by_css_selector('span')
        comment = comment.get_attribute('innerHTML')
        # Skip post description
        if user == posers_ig_name:
            continue
        if unique:
            unique_user_set.update(user)  # Save unique user
        user_list.append(user)  # Save none unique user
        comment_list.append(comment)  # Save none unique comment


def pick_a_winner():
    if unique:
        unique_user_list = list(unique_user_set)
        unique_user_amount = len(unique_user_list) - 1
        print(unique_user_amount)
        winner_index = random.randint(0, unique_user_amount)
        print("Winner is:", unique_user_list[winner_index])
        print(unique_user_list[winner_index], "comments:\n")
        comments = get_all_user_comments(get_all_user_indexes(unique_user_list[winner_index]))
        print(comments)
    else:
        user_amount = len(user_list) - 1
        print("User amount", user_amount)
        winner_index = random.randint(0, user_amount)
        print("Winner is:", user_list[winner_index], "Comment number:", winner_index)
        print(user_list[winner_index], "comments:\n")
        comments = get_all_user_comments(get_all_user_indexes(user_list[winner_index]))
        print(comments, sep="\n")


def bot(driver):
    # Get button procedure
    print("Check for valid page in progress")
    check_for_button_on_start(driver)

    # Load all elements procedure
    start_time = time.time()
    print("Clicker in progress")
    clicker(driver)
    end_time = time.time()
    print("Time elapsed:", end_time - start_time, "s")

    # Get all user data from elements
    start_time = time.time()
    print("Getting users in progress")
    get_all_user_data_from_elements(driver)
    end_time = time.time()
    print("Time elapsed:", end_time - start_time, "s")


def start():
    options = Options()
    options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    driver = webdriver.Chrome(chrome_options=options,
                              executable_path=os.path.abspath(os.path.dirname(sys.argv[0])) + "/chromedriver.exe", )
    driver.get(post_link)
    # bot code
    bot(driver)
    # Pick a winner
    pick_a_winner()


if post_id != "":
    start()

