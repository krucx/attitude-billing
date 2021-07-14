from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from configuration import username
from html_2_jpg import conversion

def send_image(phone_number, image_filename):
    try:
        link = f'https://web.whatsapp.com/send?phone=91{phone_number}&text&app_absent=0'
        options = webdriver.ChromeOptions()
        #options.add_argument(r"user-data-dir=./driver/data")
        options.add_argument(f"user-data-dir=C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        driver = webdriver.Chrome(
            executable_path=r'./driver/chromedriver', options=options)
        driver.get(link)
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')))

        attachbtn = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div')
        attachbtn.click()
        time.sleep(1)
        imagebtn = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div[1]/div/ul/li[1]/button/input')
        if conversion(image_filename):
            filepath = f'C:\\Users\\{username}\\Desktop\\attitude\\bills\\'+image_filename+'.jpg'
            imagebtn.send_keys(filepath)
            time.sleep(2)
            sendbtn = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/span/div/div')
            sendbtn.click()
            time.sleep(5)
        else:
            print('Conversion from html to jpg Failed')
    finally:
        driver.quit()

def send_text(phone_number, text):
    try:
        link = f'https://web.whatsapp.com/send?phone=91{phone_number}&text&app_absent=0'
        options = webdriver.ChromeOptions()
        #options.add_argument(r"user-data-dir=./driver/data")
        options.add_argument(f"user-data-dir=C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        driver = webdriver.Chrome(
            executable_path=r'./driver/chromedriver', options=options)
        driver.get(link)
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')))

        textbox = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[1]/div/div[2]')
        textbox.send_keys(text)
        time.sleep(1)

        sendbtn = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]/button')
        sendbtn.click()
        time.sleep(5)
    finally:
        driver.quit()

#send_text('9920816377', 'This is a test message')
