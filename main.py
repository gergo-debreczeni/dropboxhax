from utils.selenium_utils import Dropbox
from utils import ssh
from utils import powershell
from utils.lxc_executor import Executor
import random
import time


class DropboxAwesome(object):


    def __init__(self, ref_url, base_fake_mail, desired_count):
        self.ref_url = ref_url
        self.base_fake_mail = base_fake_mail
        self.desired_count = desired_count
        self.mails = []
        self.user = 'root'
        self.password = 'Passw0rd'
        self.lxc_workers = ['test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9', 'test10', 'test11',
                            'test12', 'test13', 'test14', 'test15', 'test16', 'test17', 'test18', 'test19', 'test20', 'test21',
                            'test22', 'test23','test24', 'test25', 'test26', 'test27', 'test28', 'test29', 'test30', 'test31', 'test32']

    def do_magic(self):
        confirm_urls = []
        self.create_accounts()
        for lxc in self.lxc_workers[:self.desired_count]:
            exc = Executor(lxc)
            confirm_url = exc.get_address()
            confirm_urls.append(confirm_url)
        self.confirm_accounts(confirm_urls)
        for lxc in self.lxc_workers[:self.desired_count]:
            exc = Executor(lxc)
            exc.wait_confirmation()

    def rand_name(self, name=''):
        randbits = str(random.randint(1, 0x7fffffff))
        if name:
            return name + '-' + randbits
        else:
            return randbits

    def create_accounts(self):
        base_mail = self.rand_name(self.base_fake_mail) + '@mailinator.com'
        for _ in xrange(self.desired_count):
            self.mails.append(base_mail % _)
        self.db = Dropbox(self.ref_url, self.mails, self.password)
        self.db.register()

    def confirm_accounts(self, confirm_urls):
        self.db.confirm(confirm_urls)

if __name__ == '__main__':
    ref_url = 'https://db.tt/EDiAOZdg' #bob_ref
    base_fake_mail = 'linux_valentin_%i_'
    win = DropboxAwesome(ref_url, base_fake_mail, 13)
    win.do_magic()
