from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
MAIL_LINK = "https://www.dropbox.com"
EMAIL = 'gerry_dropbox11@mailinator.com'
PASSWORD = 'Passw0rd'

if __name__ == '__main__':
	try:
		driver = webdriver.Firefox()
		driver.implicitly_wait(10)
		driver.get(MAIL_LINK)
		element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-input")))

		import pdb
		pdb.set_trace()
		ea=driver.find_elements_by_name('login_email')
		ea[3].send_keys(EMAIL)
		ee=driver.find_elements_by_class_name("password-input")
		ee[1].send_keys(PASSWORD)
		ee[1].send_keys(Keys.RETURN)
	finally:
	    driver.quit()