import os
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from secret import account,password
def wait_for_xpad(path):
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, path))
)
# val=input("Nhập dữ liệu ")
options = Options()
options.add_argument("secret.py")
driver = webdriver.Chrome(options=options)
driver.get(f'https://www.pinterest.com')
# sleep(3)
# login=driver.find_element(By.XPATH,'//*[@id="mweb-unauth-container"]/div/div/div[1]/div/div[2]/div[2]/button/div/div')
# login.click()
# sleep(3)
# email=driver.find_element(By.XPATH,'//*[@id="email"]')
# email.click()
# email.send_keys('tnhgenshin5@gmail.com')
# password=driver.find_element(By.XPATH,'//*[@id="password"]')
# password.click()
# password.send_keys('phamhuynhquyan')
# button=driver.find_element(By.XPATH,'(//div[text()="Log in"])[2]')
# button.click()
# sleep(5)
# tim_kiem = driver.find_element(By.XPATH, "//input[@aria-label='Tìm kiếm']")
# tim_kiem.click()
# tim_kiem.send_keys('baby')
# tim_kiem.send_keys(Keys.ENTER)
# sleep(50)
