from utils import console


def run_tests():

    # RHEL-06-000005
    with open("/etc/audit/auditd.conf") as audit_config_file:
        audit_config = audit_config_file.readlines()
        for line in audit_config:

            line.strip()
            if not line.startswith("#"):

                if line.startswith("space_left_action"):
                    key, value = line.split(" = ")

                    if value == "EMAIL":
                        console.ok("Free space warning enabled in auditd")
                        return None

                    elif value == "SYSLOG":
                        console.warning("Free space warning is set to SYSLOG. Make sure this notifies the necessary individuals in a timely manner")

                    else:
                        console.error("Free space warning not enabled in auditd")
                        return None

        console.error("Free space warning not enabled in auditd")
        return None
