tasks = []
from celery_fool import register

for i in xrange(4):
    tasks.append(register.delay('www.google.com','aa','bb'))
