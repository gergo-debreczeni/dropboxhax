# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import cStringIO
import os
import select
import socket
import time
import warnings
import logging

import six

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import paramiko

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


class Client(object):

    def _get_config(self):
        ### should but don't work :(
        config = paramiko.SSHConfig()
        config_path = os.path.expanduser("~/.ssh/config")

        try:
            with open(config_path) as f:
                config.parse(f)
        except IOError:
            pass

        host_config = config.lookup(self.host)

        self.host = host_config.get('hostname', self.host)
        self.username = host_config.get('user', self.username)
        self.port = host_config.get('port', self.port)

        if 'proxycommand' in host_config:
            self.sock = paramiko.ProxyCommand(host_config['proxycommand'])

    def __init__(self, host, username, password=None, timeout=300, pkey=None,
                 channel_timeout=10, look_for_keys=False, key_filename=None):
        self.host = host
        self.port = 22
        self.username = username
        self.password = password
        if isinstance(pkey, six.string_types):
            pkey = paramiko.RSAKey.from_private_key(
                cStringIO.StringIO(str(pkey)))
        self.pkey = pkey
        self.look_for_keys = look_for_keys
        self.key_filename = key_filename
        self.timeout = int(timeout)
        self.channel_timeout = float(channel_timeout)
        self.buf_size = 1024
        get_lxc_ip = (' echo $(host $(echo %(container)s.lxc | sed "s/\\.lxc//g") 10.0.3.1 '
                      '| tail -1 | awk \'{print $NF}\')') % {'container': host}
        s_int, s_out, s_err = os.popen3(get_lxc_ip)
        container = s_out.read().strip()
        print "Container %(cont)s with %(ip)s " %{'cont':host,'ip':container}
        self.host = container

    def _get_ssh_connection(self, sleep=1.5, backoff=1):
        """Returns an ssh connection to the specified host."""
        bsleep = sleep
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())
        _start_time = time.time()
        if self.pkey is not None:
            LOG.info("Creating ssh connection to '%s' as '%s'"
                     " with public key authentication",
                     self.host, self.username)
        else:
            LOG.info("Creating ssh connection to '%s' as '%s'"
                     " with password %s",
                     self.host, self.username, str(self.password))
        attempts = 0
        while True:
            try:
                ssh.connect(self.host, username=self.username,
                            password=self.password,
                            look_for_keys=self.look_for_keys,
                            key_filename=self.key_filename,
                            timeout=self.channel_timeout, pkey=self.pkey)
                LOG.info("ssh connection to %s@%s successfuly created",
                         self.username, self.host)
                return ssh
            except (socket.error,
                    paramiko.SSHException) as e:
                if self._is_timed_out(_start_time):
                    LOG.exception("Failed to establish authenticated ssh"
                                  " connection to %s@%s after %d attempts",
                                  self.username, self.host, attempts)
                    raise exceptions.SSHTimeout(host=self.host,
                                                user=self.username,
                                                password=self.password)
                bsleep += backoff
                attempts += 1
                LOG.warning("Failed to establish authenticated ssh"
                            " connection to %s@%s (%s). Number attempts: %s."
                            " Retry after %d seconds.",
                            self.username, self.host, e, attempts, bsleep)
                time.sleep(bsleep)

    def _is_timed_out(self, start_time):
        return (time.time() - self.timeout) > start_time

    def sftp(self, source, destination):

        try:
            transport = paramiko.Transport((self.host, self.port))
            transport.start_client()
            self.agent_auth(transport, self.username)
            sftp = transport.open_session()
            sftp = paramiko.SFTPClient.from_transport(transport)
            is_up_to_date = False

            try:
                sftp.mkdir(destination)
            except IOError as e:
                LOG.exception(e)

            destination_file = destination + '/' + os.path.basename(source)
            try:
                if sftp.stat(destination):
                    source_data = open(source, "rb").read()
                    destination_data = sftp.open(destination_file).read()
                    md1 = md5.new(source_data).digest()
                    md2 = md5.new(destination_data).digest()
                    if md1 == md2:
                        is_up_to_date = True
            except:
                pass

            if not is_up_to_date:
                sftp.put(source, destination_file)
                LOG.info(
                    "Successfuly copied over %s to %s", source, destination)
        except Exception as e:
            raise Exception ('*** Failed to sftp: %s: %s' % (e.__class__, e))
            try:
                transport.close()
            except:
                pass

    def agent_auth(self, transport, username):

        agent = paramiko.Agent()
        agent_keys = agent.get_keys() + (self.pkey,)
        if len(agent_keys) == 0:
            return

        for key in agent_keys:
            try:
                transport.auth_publickey(username, key)
                return
            except paramiko.SSHException, e:
                raise e

    def exec_command(self, cmd):
        """
        Execute the specified command on the server.

        Note that this method is reading whole command outputs to memory, thus
        shouldn't be used for large outputs.

        :returns: data read from standard output of the command.
        :raises: SSHExecCommandFailed if command returns nonzero
                 status. The exception contains command status stderr content.
        """
        ssh = self._get_ssh_connection()
        transport = ssh.get_transport()
        channel = transport.open_session()
        channel.fileno()  # Register event pipe
        channel.exec_command(cmd)
        channel.shutdown_write()
        out_data = []
        err_data = []
        poll = select.poll()
        poll.register(channel, select.POLLIN)
        start_time = time.time()

        while True:
            ready = poll.poll(self.channel_timeout)
            if not any(ready):
                if not self._is_timed_out(start_time):
                    continue
                raise exceptions.TimeoutException(
                    "Command: '{0}' executed on host '{1}'.".format(
                        cmd, self.host))
            if not ready[0]:  # If there is nothing to read.
                continue
            out_chunk = err_chunk = None
            if channel.recv_ready():
                out_chunk = channel.recv(self.buf_size)
                out_data += out_chunk,
            if channel.recv_stderr_ready():
                err_chunk = channel.recv_stderr(self.buf_size)
                err_data += err_chunk,
            if channel.closed and not err_chunk and not out_chunk:
                break
        exit_status = channel.recv_exit_status()
        if 0 != exit_status:
            raise exceptions.SSHExecCommandFailed(
                command=cmd, exit_status=exit_status,
                strerror=''.join(err_data))
        return ''.join(out_data)

    def test_connection_auth(self):
        """Raises an exception when we can not connect to server via ssh."""
        connection = self._get_ssh_connection()
        connection.close()