from utils import console, parsing


class sshd():

    def __init__(self):
        self.sshd_config_file = '/etc/ssh/sshd_config'
        self.sshd_config = parsing.parse_config_file(self.sshd_config_file)
        console.heading("SSHd config")
        return

    def check_value(self, key, value):
        if (
            key not in self.sshd_config.keys() or
            self.sshd_config[key] != value
        ):
            console.error("SSHd %s is not set to %s!" % (key, value))


def run_tests():
    ssh = sshd()
    ssh.check_value('Protocol', '2')  # RHEL-06-000227
    ssh.check_value('ClientAliveInterval', '900')  # RHEL-06-000230
    ssh.check_value('ClientAliveCountMax', '0')  # RHEL-06-000231
    ssh.check_value('IgnoreRhosts', 'yes')  # RHEL-06-000231
    ssh.check_value('HostbasedAuthentication', 'no')  # RHEL-06-000236
    ssh.check_value('PermitRootLogin', 'no')  # RHEL-06-000237
    ssh.check_value('PermitEmptyPasswords', 'no')  # RHEL-06-000239
    ssh.check_value('Banner', '/etc/issue')  # RHEL-06-000240
    ssh.check_value('PermitUserEnvironment', 'no')  # RHEL-06-000241
    ssh.check_value('Ciphers', 'aes128-ctr,aes192-ctr,aes256-ctr,aes128-cbc,3des-cbc,aes192-cbc,aes256-cbc')  # RHEL-06-000243

    # ssh.check_value('', '')  #
