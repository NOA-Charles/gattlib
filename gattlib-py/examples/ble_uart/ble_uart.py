#!/usr/bin/env python3

import argparse
import threading

from gattlib import adapter, uuid

parser = argparse.ArgumentParser(description='NOA Uart Example')
args = parser.parse_args()
lock = threading.Lock()

def connect_ble_device(device):
    print('found device: ', str(device))

    if str(device).find('NOA_BLE_UART') > -1:
        lock.acquire()
        print('Start connect')
        device.connect()
        print('Start discover')
        device.discover()
        for key, val in device.characteristics.items():
            print("- GATTCharacteristic: 0x%x" % key)

        write_uuid = uuid.gattlib_uuid_str_to_int('6e400002b5a3f393e0a9e50e24dcca9e')
        write_characteristic = device.characteristics[write_uuid]

        notify_uuid = uuid.gattlib_uuid_str_to_int('6e400003b5a3f393e0a9e50e24dcca9e')
        notify_characteristic = device.characteristics[notify_uuid]
        notify_characteristic.register_notification(notify_progress)
        notify_characteristic.notification_start()

        while True:
            content = input("Please input content\n")
            if content == 'disconnect':
                device.disconnect()
                break
            else:
                write_characteristic.write(content.encode())
                print('write success: ', content)

        print("Quit success")
        default_adapter.scan_disable()
        default_adapter.close()
        lock.release()


def notify_progress(value, user_data):
    print("notify value: ", value.decode(), "  user_data: ", user_data)


def on_discovered_ble_device(device, user_data):
    threading.Thread(target=connect_ble_device, args=(device,)).start()


# Use default adapter
default_adapter = adapter.Adapter()

# Scan for 30 seconds
default_adapter.open()
default_adapter.scan_enable(on_discovered_ble_device, 0, rssi_threshold=-45)
print('finished')
