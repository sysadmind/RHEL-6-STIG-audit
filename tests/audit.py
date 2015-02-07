from utils import console, parsing
import operator


class auditd():

    def __init__(self):
        self.auditd_config_file = '/etc/audit/auditd.conf'
        self.auditd_config = parsing.parse_config_file(self.auditd_config_file, '=')
        console.heading("auditd config")
        return

    def check_value(self, key, value, operator_function):
        if not operator_function(self.auditd_config[key], value):
            console.error("Auditd %s is not set to %s!" % (key, value))

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


def run_tests():

    audit = auditd()
    audit.check_value('admin_space_left_action', 'SINGLE', operator.eq)  # RHEL-06-000163
    audit.check_spece_left_action()
    audit.check_value('max_log_file_action', 'ROTATE', operator.eq)  # RHEL-06-000161
    audit.check_value('max_log_file', '6', operator.eq)  # RHEL-06-000160
    audit.check_value('num_logs', '5', operator.ge)  # # RHEL-06-000159
