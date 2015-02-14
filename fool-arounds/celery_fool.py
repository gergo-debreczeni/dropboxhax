from celery import Celery

app = Celery()
@app.task()
def register(refer_mail, mail, password):
    from selenium import webdriver
    driver = webdriver.Firefox()
    driver.get(refer_mail)
    driver.close()
