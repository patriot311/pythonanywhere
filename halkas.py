import praw
import os
import sys
import requests
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
last_post_url=0
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
options = webdriver.ChromeOptions()
# options.add_argument("headless")
# mobile_emulation = { "deviceName": "iPhone 12 Pro" }
# options.add_experimental_option("mobileEmulation", mobile_emulation)
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def arca():
    id ="polandpoland"
    pw = 'polandpoland'
    URL =   'http://arca.live/u/login'
    GALL = 'http://arca.live/b/countryball/write'
    #options = webdriver.ChromeOptions() 
    
    #headless 모드
    #options.add_argument("disable-gpu")

    #user-agent 변경
    #options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")

    #크롬 드라이버 로드
    #driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    #driver.implicitly_wait(3)

    #로그인 구간
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')

    driver.get(URL)
    time.sleep(5)
    try:
        driver.find_element(By.ID, 'idInput').send_keys(id)
        time.sleep(2)
    except:
        pass
    try:
        driver.find_element(By.ID, 'submitBtn').click()
    except:
        pass
    time.sleep(5)
    try:
        driver.find_element(By.ID, 'idPassword').send_keys(pw)
        time.sleep(2)
    except:
        pass
    try:
        driver.find_element(By.ID, 'idPassword').send_keys(Keys.ENTER)
    except:
        pass
    time.sleep(10)

    ########################
    #e9393daa-0c80-4518-b7f8-54d0562e85ea  사이트키
    ##############################

    #글작성 페이지 로드
    driver.get(GALL)

    #글작성 구간
    time.sleep(5)
    driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/article/div/form/div[2]/span[14]/label').click()
    driver.find_element(By.ID, 'inputTitle').click()
    driver.find_element(By.ID, 'inputTitle').send_keys(u'New Reddit Post Upload!')
    #본문입력
    driver.find_element(By.CLASS_NAME,'fr-element.fr-view').click()
    driver.find_element(By.CLASS_NAME,'fr-element.fr-view').send_keys(last_post_url)
    driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/article/div/form/div[7]/button').click()
    time.sleep(5)

    print(f"Uploading to Arca Live with title: {last_post_url}")




# Reddit API credentials
reddit_client_id = 'oBz712llurry6lrZo1WVGQ'
reddit_client_secret = 'ELuKNoe1WkWbQesA6Z2q0151MtDKmQ'
reddit_user_agent = 'yeastking0'
subreddit_name = 'Arca_countryball'

# Reddit instance
reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_user_agent
)

# Initialize the last post URL
last_post_url = None

while True:
    try:
        # Get the most recent submission in the subreddit
        subreddit = reddit.subreddit(subreddit_name)
        submission = next(subreddit.new(limit=1))

        # Check if the current post URL is different from the previous one
        if submission.url != last_post_url:
            # Print the URL of the most recent post
            print(f"New post detected in r/{subreddit_name}: {submission.url}")

            # Perform your desired action with the post URL
            last_post_url=submission.url
            print(f"Processing post URL: {last_post_url}")
            arca()
            

        # Wait for 60 seconds before checking for new posts again
        time.sleep(60)

    except praw.exceptions.PRAWException as e:
        print(f"Error: {e}")

