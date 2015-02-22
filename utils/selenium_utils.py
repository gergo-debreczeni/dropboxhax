from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Dropbox(object):

    def __init__(self, refer_url, mails, password):
        self.refer_url = refer_url
        self.mails = mails
        self.password = password

    def register(self):
        try:
            driver = webdriver.Firefox()
            driver.implicitly_wait(10)
            for mail in self.mails:
                driver.get(self.refer_url)
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-input")))
                elem=driver.find_elements_by_class_name("text-input")
                elem[4].send_keys('Jonhatan')
                elem[5].send_keys('Doe')
                elem[6].send_keys(mail)
                elem[7].send_keys(self.password)
                tos=driver.find_elements_by_name('tos_agree')
                tos[1].send_keys(Keys.SPACE)
                elem[7].send_keys(Keys.RETURN)
                time.sleep(1)
                driver.delete_all_cookies()
        except Exception:
            raise
        finally:
            driver.quit()
        pass

    def confirm(self, confirm_urls):
        try:
            driver = webdriver.Firefox()
            driver.implicitly_wait(10)
            for pos, mail in enumerate(self.mails):
                confirm_url = confirm_urls[pos]
                driver.get(confirm_url)
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-input")))
                ea=driver.find_elements_by_name('login_email')
                ea[3].send_keys(mail)
                ee=driver.find_elements_by_class_name("password-input")
                ee[1].send_keys(self.password)
                ee[1].send_keys(Keys.RETURN)
                time.sleep(1)
                driver.delete_all_cookies()
        finally:
            driver.quit()
