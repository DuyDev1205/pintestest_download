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
from PIL import Image
import pyautogui
from tabulate import tabulate
from termcolor import colored
import json
class Color:
    GREEN = '\033[92m'
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
def wait_for_xpath_single(driver, xpath):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

def wait_for_xpath_all(driver, xpath):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath))
    )

def download_image(image_url, file_name):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        return True
    return False
def show_image():
    global path_list
    for i in path_list:
        img=Image.open(i)
        img.show() 
        pyautogui.hotkey('alt', 'f4')
def remove_image():
    for i in path_list:
        os.remove(i)
def display_menu():
    menu_items = [
        ["1", "Tải ảnh"],
        ["2", "Xem ảnh"],
        ["3", "Xóa ảnh"],
        ["0", "Thoát"],
    ]
    headers = ["Lựa chọn", "Chức năng"]
    menu = tabulate(menu_items, headers, tablefmt="fancy_outline",colalign=("center","center"))
    print(menu)
def final():
    options = Options()
    options.add_argument("user-data-dir="+os.path.join(os.getcwd(),f'ChromeProfile'))
    num = int(input("Số lượng ảnh cần tải: "))
    value = input("Nội dung cần tìm kiếm ")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.pinterest.com")
    tim_kiem = wait_for_xpath_single(driver, "//input[@aria-label='Tìm kiếm']")
    tim_kiem.click()
    tim_kiem.send_keys(value)
    tim_kiem.send_keys(Keys.ENTER)
    sleep(2)

    downloaded = 0
    images_processed = set()
    global path_list
    path_list =[]
    while downloaded < num:
        images = wait_for_xpath_all(driver, '//img[@class="hCL kVc L4E MIw"]')
        for img in images[1:num+1]:
            src = img.get_attribute('src')
            if src and src not in images_processed:
                file_name = os.path.join(os.getcwd(), f'images/image_{downloaded + 1}.jpg')
                if download_image(src, file_name):
                    downloaded += 1
                    images_processed.add(src)
                    if downloaded >= num:
                        break
        if downloaded < num:  # Chỉ cuộn trang khi cần thêm ảnh
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)  # Đợi ảnh mới tải về
    driver.quit()
def output():
    cls=os.system('cls')
    print(Color.GREEN)
    display_menu()
    while True:
        try:
                choice = int(input("Nhập lựa chọn: "))
        except ValueError:
            print("Vui lòng nhập một số hợp lệ.")
            continue
        match choice:
            case 0:
                print("Đang thoát chương trình...")
                break
            case 1:
                final()
            case 2:
                show_image()
            case 3:
                remove_image()
if __name__ == "__main__":
    path =os.path.join(os.getcwd(),f'ChromeProfile\\Default')
    clear_catche =os.path.join(os.getcwd(),f'ChromeProfile\\Default\\Cache')
    if os.path.exists(clear_catche):
        clear_chrome_profile_cache(path)
    # final()
    # show_image()
    # remove_image()
    output()