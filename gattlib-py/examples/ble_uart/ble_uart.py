#!/usr/bin/env python3

import argparse
import threading

from gattlib import adapter

parser = argparse.ArgumentParser(description='NOA Uart Example')
args = parser.parse_args()

# We only use a lock to not mixed printing statements of various devices
lock = threading.Lock()


def connect_ble_device(device):
    print('device id: ', device.id)
    print('device name: ', str(device))
    if str(device).find('NOA_BLE_UART') > -1:
        print('Start connect')
        device.connect()
        lock.acquire()
        print('Start discover')
        device.discover()
        for key, val in device.characteristics.items():
            print("- GATTCharacteristic: 0x%x" % key)

        lock.release()
        device.disconnect()


def on_discovered_ble_device(device, user_data):
    threading.Thread(target=connect_ble_device, args=(device,)).start()


# Use default adapter
default_adapter = adapter.Adapter()

# Scan for 30 seconds
default_adapter.open()
default_adapter.scan_enable(on_discovered_ble_device, 10, rssi_threshold=-80)
print('finished')
default_adapter.close()