import ssh
import time

class Executor():

    def __init__(self, host, user='ubuntu', password='ubuntu'):
        self.host = host
        self.user =user
        self.password = password
        self.ssh_client = ssh.Client(self.host, self.user, self.password, 30, channel_timeout=30)

    def exec_command(self, command):
        output = self.ssh_client.exec_command(command)
        return output

    def clean_dropbox(self):
        kill_dropboxd = ("dropbox_daemons=`ps aux | grep dropbox | grep -v grep | wc -l`; "
                        "if [[ $dropbox_daemons > 0 ]]; then "
                            "kill $(ps aux | grep 'dropbox' | grep -v grep | awk '{print $2}'); "
                        "fi")
        self.ssh_client.exec_command(kill_dropboxd)
        self.ssh_client.exec_command('rm -rf .dropbox/; rm -f output.log')

    def get_address(self):
        self.clean_dropbox()
        self.ssh_client.exec_command('~/.dropbox-dist/dropboxd > output.log &')
        while True:
            output = self.ssh_client.exec_command('tail -n 2 output.log')
            if 'https' in output:
                break
            else:
                time.sleep(3)

        parts = output.split('visit')
        address = parts[1].split('to link')[0].strip()
        return address

    def wait_confirmation(self):
        count = 0
        while True:
            output = self.ssh_client.exec_command('tail -n 2 output.log')
            count += 1
            if 'is now linked' in output:
                self.clean_dropbox()
                break
            elif count > 10:
                raise Exception("timeout for %s with \n output: %s", self.host, self.output)
            else:
                time.sleep(2)
