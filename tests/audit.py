from utils import console, parsing


class auditd():

    def __init__(self):
        self.auditd_config_file = '/etc/audit/auditd.conf'
        self.auditd_config = parsing.parse_auditd_config(self.auditd_config_file)
        return

    def check_admin_space_left_action(self):
        # RHEL-06-000163
        if self.auditd_config['admin_space_left_action'].upper() != "SINGLE":
            console.error("Auditd admin_space_left_action is not set to 'SINGLE'!")
            return None

    def check_spece_left_action(self):
        # RHEL-06-000005
        if self.auditd_config['space_left_action'] == "EMAIL":
            console.ok("Free space warning enabled in auditd")
            return None
        elif self.auditd_config['space_left_action'] == "SYSLOG":
            console.warning("Free space warning is set to SYSLOG. Make sure this notifies the necessary individuals in a timely manner")
            return None
        else:
            console.error("Free space warning not enabled in auditd")
            return None

    def check_max_log_file_action(self):
        # RHEL-06-000161
        if self.auditd_config['max_log_file_action'].upper() != "ROTATE":
            console.error("Auditd max_log_file_actoin not set to 'ROTATE'!")

    def check_max_log_file(self):
        # RHEL-06-000160
        #  This rule may need to be altered because the STIG only defines this
        #  must be set large enough to meet the retention period required.
        if not int(self.auditd_config['max_log_file']) >= 6:
            console.error("Auditd max_log_file not set to at least 6!")

    def check_num_logs(self):
        # RHEL-06-000159
        #  This rule may need to be altered because the STIG only defines this
        #  must be set large enough to meet the retention period required.
        if not int(self.auditd_config['num_logs']) >= 5:
            console.error("Auditd num_logs not set to at least 5!")


def run_tests():

    audit = auditd()
    audit.check_admin_space_left_action()
    audit.check_spece_left_action()
    audit.check_max_log_file_action()
    audit.check_max_log_file()
    audit.check_num_logs()
