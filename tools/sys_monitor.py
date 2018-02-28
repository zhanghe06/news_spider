#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: sys_monitor.py
@time: 2018-02-10 17:43
"""


import psutil
import time


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9.8 K'
    >>> bytes2human(100001221)
    '95.4 M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f B' % n


def _format_info(k, v):
    if len(str(v)) <= 5:
        return '%-25s %5s' % (k, v)
    elif len(str(v)) <= 10:
        return '%-20s %10s' % (k, v)
    else:
        return '%-15s %15s' % (k, v)


def _print_info(contents, topic=''):
    if topic:
        print('\n[%s]' % topic)
    contents.insert(0, '-' * 31)
    contents.append('-' * 31)
    print('\n'.join(contents))


def _cpu():
    contents = [
        _format_info('cpu_count_logical', psutil.cpu_count()),
        _format_info('cpu_count_physical', psutil.cpu_count(logical=False)),
    ]
    _print_info(contents, 'CPU')


def _memory():
    mem_virtual = psutil.virtual_memory()
    mem_swap = psutil.swap_memory()

    contents = [_format_info('mem_virtual_total', bytes2human(mem_virtual.total)),
                _format_info('mem_virtual_free', bytes2human(mem_virtual.free)),
                _format_info('mem_virtual_percent', '%s %%' % mem_virtual.percent),
                _format_info('mem_swap_total', bytes2human(mem_swap.total)),
                _format_info('mem_swap_free', bytes2human(mem_swap.free)),
                _format_info('mem_swap_percent', '%s %%' % mem_swap.percent)]
    _print_info(contents, 'Memory')


def _disks():
    sdisk_part = psutil.disk_partitions()

    contents = []

    for i in sdisk_part:
        contents.append(_format_info(i.device, i.mountpoint))

        sdisk_usage = psutil.disk_usage(i.mountpoint)
        contents.append(_format_info('disk_usage_total', bytes2human(sdisk_usage.total)))
        contents.append(_format_info('disk_usage_free', bytes2human(sdisk_usage.free)))
        contents.append(_format_info('disk_usage_percent', '%s %%' % sdisk_usage.percent))

    _print_info(contents, 'Disks')


def _network(speed=True):
    snetio = psutil.net_io_counters()
    contents = [_format_info('bytes_sent', bytes2human(snetio.bytes_sent)),
                _format_info('bytes_recv', bytes2human(snetio.bytes_recv))]

    if speed:
        time.sleep(1)
        snetio_after = psutil.net_io_counters()
        contents.append(_format_info('speed_sent', '%s/S' % bytes2human(snetio_after.bytes_sent - snetio.bytes_sent)))
        contents.append(_format_info('speed_recv', '%s/S' % bytes2human(snetio_after.bytes_recv - snetio.bytes_recv)))
    _print_info(contents, 'Network')


def _sensors():

    contents = []

    if hasattr(psutil, "sensors_temperatures"):
        sensors_temperatures = psutil.sensors_temperatures()
        for name, entries in sensors_temperatures.items():
            for entry in entries:
                contents.append(
                    _format_info(entry.label or name, '%s °C' % entry.current))

    sbattery = psutil.sensors_battery()

    if sbattery:
        contents.append(_format_info('battery_percent', '%s %%' % sbattery.percent))
        contents.append(_format_info('secsleft', sbattery.secsleft))
        contents.append(_format_info('power_plugged', sbattery.power_plugged))
    _print_info(contents, 'Sensors')


def stats():
    _cpu()
    _memory()
    _disks()
    _network()
    _sensors()


if __name__ == '__main__':
    stats()
