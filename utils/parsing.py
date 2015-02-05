

def parse_rsyslog_config(location):

    with open(location, 'r') as infile:
        file_values = {}
        lines = infile.readlines()

        for line in lines:
            # Remove whitespace in line
            line = line.strip()

            # Remove empty lines and comments
            if not line or line.startswith("#"):
                continue

            # Split lines on whitespace
            k, v = line.split(' ', 1)
            k = k.strip()
            v = v.strip()

            file_values[k] = v.strip()

    return file_values
