from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Dropbox(object):

    def __init__(self, refer_mail, mail, password):
        self.refer_mail = refer_mail
        self.mail = mail
        self.password = password

    def register(self):
        try:
            driver = webdriver.Firefox()
            driver.implicitly_wait(10)
            driver.get(self.refer_mail)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-input")))
            elem=driver.find_elements_by_class_name("text-input")
            elem[4].send_keys('Jonhatan')
            elem[5].send_keys('Doe')
            elem[6].send_keys(self.mail)
            elem[7].send_keys(self.password)
            tos=driver.find_elements_by_name('tos_agree')
            tos[1].send_keys(Keys.SPACE)
            elem[7].send_keys(Keys.RETURN)
        finally:
            driver.quit()
        pass

    def confirm(self, mail_link):
        try:
            driver = webdriver.Firefox()
            driver.implicitly_wait(10)
            driver.get(mail_link)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-input")))
            ea=driver.find_elements_by_name('login_email')
            ea[3].send_keys(self.mail)
            ee=driver.find_elements_by_class_name("password-input")
            ee[1].send_keys(self.password)
            ee[1].send_keys(Keys.RETURN)
        finally:
            driver.quit()