from utils.selenium_utils import Dropbox
from utils import ssh
from utils import powershell

import random
import time


class DropboxAwesome(object):


    def __init__(self, ref_url):
        self.ref_url = ref_url
        self.ps_script = 'C:\Users\Gergo\Dropbox\personal\Project\dropbox-hoax\utils\change_mac_start.ps1'
        self.ip_address ='192.168.0.100'
        self.user = 'root'
        self.password = 'Passw0rd'

    def generate_mac(self):
# The first line is defined for specified vendor
        mac = [ 0x00, 0x24, 0x81,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff) ]

        return ''.join(map(lambda x: "%02x" % x, mac))

    def do_magic(self, count):
        for _ in range(count):
           # mac = self.generate_mac()
           #self.configure_vm(mac)
            base_ = self.rand_name('lxc') + '@mailinator.com'
            self.create_account(base_)
            import pdb
            pdb.set_trace()
            #addr = self.get_address()
            addr = ''
            self.confirm_account(addr)
            time.sleep(5)

    def rand_name(self, name=''):
        randbits = str(random.randint(1, 0x7fffffff))
        if name:
            return name + '-' + randbits
        else:
            return randbits

    def configure_vm(self, mac):
        win_utils = powershell.WindowsUtils()
        win_utils.execute_powershell_script(self.ps_script, mac)

    def get_address(self):
        ssh_client = ssh.Client(self.ip_address, self.user, self.password, 30, channel_timeout=30)
        ssh_client.test_connection_auth()
        ssh_client.exec_command('rm -r .dropbox/')
        ssh_client.exec_command('~/.dropbox-dist/dropboxd > output.log &')
        output = ssh_client.exec_command('tail -n 2 output.log')
        while True:
            if not 'https' in output:
                time.sleep(3)
                output = ssh_client.exec_command('tail -n 2 output.log')
            else:
                break

        parts = output.split('visit')
        address = parts[1].split('to link')[0].strip()
        return address

    def create_account(self, mail):
        self.db = Dropbox(self.ref_url, mail, self.password)
        self.db.register()

    def confirm_account(self, address):
        self.db.confirm(address)

if __name__ == '__main__':
    #ref_url = 'https://db.tt/z79TgyBk' #inlove
    ref_url = 'https://db.tt/bS0ks7Nk' #gergo.debre
    win = DropboxAwesome(ref_url)
    win.do_magic(1)
