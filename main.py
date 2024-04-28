from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
from time import sleep
import shutil
def clear_chrome_profile_cache(profile_path):
    cache_paths = [
        os.path.join(profile_path, 'Cache'),  # Thư mục cache chính
        os.path.join(profile_path, 'Code Cache'),  # Cache cho code
        os.path.join(profile_path, 'GPUCache')  # GPU cache
    ]

    for path in cache_paths:
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"Deleted cache at: {path}")
        else:
            print(f"Cache path not found: {path}")
def download_image(image_url, file_name):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)

def wait_for_xpath_single(xpath):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

def wait_for_xpath_all(xpath):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath))
    )


options = Options()
options.add_argument("user-data-dir=D:\\VSCode\\Codeathon\\pintestest_download\\ChromeProfile")
num = int(input("Số lượng ảnh cần tải: "))
value = input("Nội dung cần tìm kiếm ")
driver = webdriver.Chrome(options=options)
driver.get("https://www.pinterest.com")
tim_kiem = wait_for_xpath_single("//input[@aria-label='Tìm kiếm']")
tim_kiem.click()
tim_kiem.send_keys(value)
tim_kiem.send_keys(Keys.ENTER)
sleep(2)
images = wait_for_xpath_all('//img[@class="hCL kVc L4E MIw"]')
for idx, img in enumerate(images[1:num+1],start=1):
    src = img.get_attribute('src')
    if src:
        file_name = os.path.join(os.getcwd(), f'images/image_{idx}.jpg')
        download_image(src, file_name)
profile_path = 'D:\\VSCode\\Codeathon\\pintestest_download\\ChromeProfile\\Default'
clear_chrome_profile_cache(profile_path)        
driver.quit()