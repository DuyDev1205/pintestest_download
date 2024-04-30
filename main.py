from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
from time import sleep
import keyboard
import shutil
from PIL import Image
import pyautogui
from tabulate import tabulate
from termcolor import colored
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
def show_image(path_list):
    quit_signal = False

    def check_quit(event):
        nonlocal quit_signal
        if event.name == 'q':
            quit_signal = True
    keyboard.on_press(check_quit)
    for i in path_list:
        img = Image.open(i)
        img.show()
        while True:
            if quit_signal:
                pyautogui.hotkey('alt', 'f4')
                print("Thoát khỏi chương trình...")
                keyboard.unhook_all()  # Gỡ bỏ tất cả các hook
                raise SystemExit  # Thoát hoàn toàn khỏi chương trình
            break
        pyautogui.hotkey('alt', 'f4')

    # Gỡ bỏ hook khi hàm kết thúc
    keyboard.unhook_all()
def remove_image(path_list):
    for i in path_list:
        if os.path.exists(i):
            os.remove(i)
        else:
            pass
    open('image_paths.txt', 'w').close()
    print("Đã xóa thành công")
def display_menu():
    menu_items = [
        ["1", "Tải ảnh"],
        ["2", "Xem ảnh"],
        ["3", "Xóa ảnh"],
        ["0", "Thoát"]
    ]
    headers = ["Lựa chọn", "Chức năng"]
    menu = tabulate(menu_items, headers, tablefmt="fancy_outline",colalign=("center","center"))
    print(menu)
def load_image_paths():
    try:
        with open('image_paths.txt', 'r') as file:
            # Đọc mọi dòng từ file, mỗi dòng chứa một đường dẫn
            path_list = file.readlines()
            # Loại bỏ ký tự xuống dòng ở cuối mỗi đường dẫn
            path_list = [path.strip() for path in path_list]
            return path_list
    except FileNotFoundError:
        print("File 'image_paths.txt' không tồn tại.")
        return []
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return []
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
    try:
        with open('image_paths.txt', 'r') as file:
            existing_paths = {line.strip() for line in file.readlines()}
    except FileNotFoundError:
        existing_paths = set()
    while downloaded < num:
        images = wait_for_xpath_all(driver, '//img[@class="hCL kVc L4E MIw"]')
        for img in images[1:num+1]:
            src = img.get_attribute('src')
            file_name = os.path.join(os.getcwd(), f'images/image_{downloaded + 1}.jpg')
            if src and src not in images_processed and file_name not in existing_paths:
                if download_image(src, file_name):
                    downloaded += 1
                    images_processed.add(src)
                    if file_name not in existing_paths:
                        with open('image_paths.txt', 'a') as file:
                            file.write(file_name + '\n')
                            existing_paths.add(file_name)
                    if downloaded >= num:
                        break
            else:
                downloaded+=1
                num+=1
        if downloaded < num:  # Chỉ cuộn trang khi cần thêm ảnh
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)  # Đợi ảnh mới tải về
    driver.quit()
def output(): 
    cls=os.system('cls')
    print(Color.GREEN)
    display_menu()
    while True:
        path_list =load_image_paths()
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
                show_image(path_list)
            case 3:
                remove_image(path_list)

if __name__ == "__main__":
    path =os.path.join(os.getcwd(),f'ChromeProfile\\Default')
    clear_catche =os.path.join(os.getcwd(),f'ChromeProfile\\Default\\Cache')
    if os.path.exists(clear_catche):
        clear_chrome_profile_cache(path)
    output()