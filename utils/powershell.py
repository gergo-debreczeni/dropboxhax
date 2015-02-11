import base64
import os
import re
import struct
import time

import six
import sys
import subprocess


class WindowsUtils(object):

    def execute_process(self, args, shell=True, decode_output=False):
        p = subprocess.Popen(args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=shell)
        (out, err) = p.communicate()

        if decode_output and sys.version_info < (3, 0):
            out = out.decode(sys.stdout.encoding)
            err = err.decode(sys.stdout.encoding)

        return (out, err, p.returncode)

    def get_system32_dir(self):
        return os.path.expandvars('%windir%\\system32')

    def get_sysnative_dir(self):
        return os.path.expandvars('%windir%\\sysnative')

    def check_sysnative_dir_exists(self):
        sysnative_dir_exists = os.path.isdir(self.get_sysnative_dir())
        return sysnative_dir_exists

    def _get_system_dir(self, sysnative=True):
        if sysnative and self.check_sysnative_dir_exists():
            return self.get_sysnative_dir()
        else:
            return self.get_system32_dir()

    def execute_powershell_script(self, script_path, args, sysnative=True):
        base_dir = self._get_system_dir(sysnative)
        powershell_path = os.path.join(base_dir,
                                       'WindowsPowerShell\\v1.0\\'
                                       'powershell.exe')

        args = [powershell_path, '-ExecutionPolicy', 'RemoteSigned',
                '-NonInteractive', '-File', script_path , args]

        return self.execute_process(args, shell=False)

    def execute_powershell_cmd(self, script_path, sysnative=True):
        base_dir = self._get_system_dir(sysnative)
        powershell_path = os.path.join(base_dir,
                                       'WindowsPowerShell\\v1.0\\'
                                       'powershell.exe')

        args = [powershell_path, '-ExecutionPolicy', 'RemoteSigned',
                '-NonInteractive', script_path]

        return self.execute_process(args, shell=False)

    def execute_system32_process(self, args, shell=True, decode_output=False,
                                 sysnative=True):
        base_dir = self._get_system_dir(sysnative)
        process_path = os.path.join(base_dir, args[0])
        return self.execute_process([process_path] + args[1:],
                                    decode_output=decode_output, shell=shell)