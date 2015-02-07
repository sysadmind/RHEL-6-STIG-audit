from utils import console, parsing
import operator


class auditd():

    def __init__(self):
        self.auditd_config_file = '/etc/audit/auditd.conf'
        self.auditd_config = parsing.parse_config_file(self.auditd_config_file, '=')
        console.heading("auditd config")
        return

    def check_value(self, key, value, operator_function):
        if (
            key not in self.auditd_config.keys() or
            not operator_function(self.auditd_config[key], value)
        ):
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

    def check_suspend_ignore(self, key):
        if (
            key not in self.auditd_config.keys() or
            self.auditd_config[key] == 'SUSPEND' or
            self.auditd_config[key] == 'IGNORE'
        ):
            console.error("Auditd %s improperly set!" % key)


def run_tests():

    audit = auditd()
    audit.check_value('admin_space_left_action', 'SINGLE', operator.eq)  # RHEL-06-000163
    audit.check_spece_left_action()
    audit.check_value('max_log_file_action', 'ROTATE', operator.eq)  # RHEL-06-000161
    audit.check_value('max_log_file', '6', operator.eq)  # RHEL-06-000160
    audit.check_value('num_logs', '5', operator.ge)  # RHEL-06-000159
    # The following check may need a preset config value instead of '1' because
    # the value is determined by the organization.
    audit.check_value('space_left', '1', operator.ge)  # RHEL-06-000311
    audit.check_value('action_mail_acct', 'root', operator.eq)  # RHEL-06-000313

    audit.check_suspend_ignore('disk_full_action')  # RHEL-06-000510
    audit.check_suspend_ignore('disk_error_action')  # RHEL-06-000511
