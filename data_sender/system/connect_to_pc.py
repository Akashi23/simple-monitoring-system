import datetime
import re
import psutil
import GPUtil
import platform

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return float(f"{bytes:.2f}")
        bytes /= factor

def save_to_influxdb_pc():
    uname = platform.uname()
    all_pc_stat = {
        'measurement' : 'pc',
        'tags' : {'system_name' : uname.system},
        'time' : datetime.datetime.now()
    }
    net_io = psutil.net_io_counters()
    fields = {
        'disk_usage_percent' : psutil.disk_usage('C:/').percent,
        'disk_usage_free' : int(psutil.disk_usage('C:/').free / 1024 / 1024 / 1024),
        'disk_usage_total' : int(psutil.disk_usage('C:/').total / 1024 / 1024 / 1024),
        
        'memory_free' : round(psutil.virtual_memory().available / 1024 / 1024 / 1024),
        'memory_total' : round(psutil.virtual_memory().total / 1024 / 1024 / 1024),
        'memory_usage_percent' : int(psutil.virtual_memory().percent),
        
        'gpu_name' : GPUtil.getGPUs()[0].name,
        'gpu_temp' : round(GPUtil.getGPUs()[0].temperature,2),
        'gpu_memory_total' : round(GPUtil.getGPUs()[0].memoryTotal),
        'gpu_memory_used' : round(GPUtil.getGPUs()[0].memoryUsed),
        'gpu_memory_free' : round(GPUtil.getGPUs()[0].memoryFree),
        'gpu_memory_util' : round(GPUtil.getGPUs()[0].memoryUtil*100, 2),
        'gpu_util' : round(GPUtil.getGPUs()[0].load*100, 2),
        
        'cpu_name' : uname.processor,
        'system_name' : uname.system,
        'system_version' : uname.version,
        
        'cpu_phys_core' : psutil.cpu_count(logical=False),
        'cpu_total_core': psutil.cpu_count(logical=True),
        'cpu_max_freq' : round(psutil.cpu_freq().max, 2),
        'cpu_min_freq' : round(psutil.cpu_freq().min, 2),
        'cpu_curr_freq' : round(psutil.cpu_freq().current, 2),
        'cpu_total_usage': psutil.cpu_percent()
    }

    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        fields[f'Core {i + 1}'] =  percentage

    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                fields[f'{interface_name}_ip'] = address.address
                fields[f'{interface_name}_ip_broadcast'] = address.broadcast
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                fields[f'{interface_name}_mac'] = address.address
                fields[f'{interface_name}_mac_broadcast'] = address.broadcast
    
    fields['total_bytes_sent'] = get_size(net_io.bytes_sent)
    fields['total_bytes_received'] = get_size(net_io.bytes_recv)
    all_pc_stat['fields'] = fields

    return all_pc_stat

if __name__ == "__main__":
    print(save_to_influxdb_pc())