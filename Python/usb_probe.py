# Probe for RoboMagellan USB devices
import subprocess, re

installed_devices = {
    '95437313334351516052': 'chias-test',
    '95437313335351514292': 'speedometer-test',
    'A6008iFZ':             'atmega-328-test',
    '95437313335351D0F171': 'chias',
    #'9543731333435141F0B2': 'compasswitch',
    '9543731333435141E082': 'compasswitch',
    '95437313035351412061': 'speedometer',
    #'9543731333435141F0B2': 'killswitch',
    '0000:00:14.0':         'gps',
    '95437313335351514292': 'lcd-display'
    }
port_families = ['/dev/ttyACM', '/dev/ttyUSB']

def probe():
    ports = {}
    for port_family in port_families:
        for index in range(10):
            port = '%s%s' % (port_family, index)
            command = 'udevadm info -a -n %s' % port
            try:
                out = subprocess.check_output(command.split(),
                                            stderr=subprocess.STDOUT)

                regex = re.compile("{serial}==\"([\w\.:]+)\"")
                match = regex.search(out)
                if match:
                    serial_num = match.group(1)
                    if serial_num in installed_devices:
                        ports[installed_devices[serial_num]] = port
            except:
                pass

    return ports
