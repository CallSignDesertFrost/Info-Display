import os
import psutil
import clamd

def get_system_info():
    uname = os.uname()
    if uname.sysname == 'Linux':
        temperature = psutil.sensors_temperatures()['cpu_thermal'][0].current
    elif uname.sysname == 'Windows':
        battery = psutil.sensors_battery()
        temperature = None
    else:
        raise ValueError("Unsupported operating system")

    boot_time = psutil.boot_time()
    boot_time_datetime = datetime.datetime.fromtimestamp(boot_time)

    processes = psutil.process_iter()
    process_count = len(list(processes))

    cpu_count = psutil.cpu_count()
    cpu_logical = psutil.cpu_count(logical=True)

    memory = psutil.virtual_memory()
    memory_total = memory.total / (1024 * 1024)
    memory_used = memory.used / (1024 * 1024)

    disk_partitions = psutil.disk_partitions()
    disk_usage = psutil.disk_usage('/')
    disk_used = disk_usage.used / (1024 * 1024)
    disk_total = disk_usage.total / (1024 * 1024)

    users = psutil.users()

    return {
        'system': uname.sysname,
        'temperature': temperature,
        'battery': battery.percent if battery else None,
        'boot_time': boot_time_datetime.strftime('%Y-%m-%d %H:%M:%S'),
        'process_count': process_count,
        'cpu_count': cpu_count,
        'cpu_logical': cpu_logical,
        'memory_total': memory_total,
        'memory_used': memory_used,
        'disk_used': disk_used,
        'disk_total': disk_total,
        'users': users
    }

def scan_system(clamd_host='localhost', clamd_port=3310):
    clamd_socket = clamd.ClamdUnixSocket(clamd_host, clamd_port)
    scan_result = clamd_socket.scan(' /')
    return scan_result

if __name__ == '__main__':
    system_info = get_system_info()
    scan_result = scan_system()

    print("System information:")
    print(json.dumps(system_info, indent=2))
    print("Virus scan result:", scan_result['result'])