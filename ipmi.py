#/usr/bin/python3

import sys
import json
import time

import pyipmi
import pyipmi.interfaces
import paho.mqtt.publish as publish

def main():

    if len(sys.argv) < 4:
        print('<HOST> <USER> <PASSWORD>')
        sys.exit(1)

    host = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[3]

    interface = pyipmi.interfaces.create_interface('ipmitool',
                                                   interface_type='lanplus')
    ipmi = pyipmi.create_connection(interface)
    ipmi.session.set_session_type_rmcp(host, 623)
    ipmi.session.set_auth_type_user(user, password)
    ipmi.session.establish()
    ipmi.target = pyipmi.Target(ipmb_address=0x20)

    while True:
        rsp = ipmi.get_power_reading(1)

        power = {
            "power": rsp.current_power,
            "min_power": rsp.minimum_power,
            "max_power": rsp.maximum_power,
            "avg_power": rsp.average_power
        }

        publish.single("server/power", json.dumps(power), hostname=host)
        print(power)
        time.sleep(10)

        # print('Power Reading')
        # print('  current:   {}'.format(rsp.current_power))
        # print('  minimum:   {}'.format(rsp.minimum_power))
        # print('  maximum:   {}'.format(rsp.maximum_power))
        # print('  average:   {}'.format(rsp.average_power))
        # print('  timestamp: {}'.format(rsp.timestamp))
        # print('  period:    {}'.format(rsp.period))
        # print('  state:     {}'.format(rsp.reading_state))

if __name__ == '__main__':
    main()