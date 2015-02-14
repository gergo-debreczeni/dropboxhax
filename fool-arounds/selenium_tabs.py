from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Dropbox(object):

    def __init__(self, refer_mail, mail, password):
        self.refer_mail = refer_mail
        self.mail = mail
        self.password = password

    def register(self):
        try:
            driver = webdriver.Firefox()
            driver.implicitly_wait(10)
            for _ in xrange(100, 133):

                driver.implicitly_wait(5)
                driver.get(self.refer_mail)
                element = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "text-input")))
                elem=driver.find_elements_by_class_name("text-input")
                elem[4].send_keys('whiteman')
                elem[5].send_keys('Doe')
                elem[6].send_keys(self.mail%_)
                elem[7].send_keys(self.password)
                tos=driver.find_elements_by_name('tos_agree')
                tos[1].send_keys(Keys.SPACE)
                elem[7].send_keys(Keys.RETURN)
                time.sleep(1)
                driver.delete_all_cookies()
        finally:
            driver.quit()
        pass

if __name__ == "__main__":

    #ref_url = 'https://db.tt/bS0ks7Nk' #gergo.debre
    ref_url = 'https://db.tt/tr6esxYv' #gerry_dropbox1@mailinator.com Passw0rd
    mail = 'nobodynocryess_%i@mailinator.com'
    #for _ in xrange(4):
    db = Dropbox(ref_url, mail, 'Passw0rd')
    db.register()