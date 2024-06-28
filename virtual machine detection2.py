import subprocess
import platform

vm_os_model_list = [ 'VMware', 'VirtualBox', 'Hyper-V', 'KVM', 'Xen', 'Parallels', 'PowerVM', 'z/VM', 'EC2', 'Compute Engine', 'Nutanix AHV'
]
vm_manufacturer_list = [
    'VMware, Inc',
    'Oracle Corporation (VirtualBox)',
    'Microsoft Corporation (Hyper-V)',
    'Red Hat, Inc (Red Hat Virtualization, KVM)',
    'Citrix Systems, Inc (Citrix Hypervisor, formerly XenServer)',
    'Parallels, Inc (Parallels Desktop)',
    'IBM Corporation (IBM PowerVM, IBM z/VM)',
    'Amazon Web Services, Inc (AWS EC2)',
    'Google LLC (Google Compute Engine)',
    'Nutanix, Inc (Nutanix AHV)'
]

def get_property_value(line):
    line = line.replace('\n', '').replace('\r', '').replace('\t', ':')
    values = line.split(maxsplit=1)
    return values[1].strip() if len(values) > 1 else ""

def detect_windows_vm():
    os_model = subprocess.check_output('wmic COMPUTERSYSTEM GET Model', shell=True).decode().strip()
    os_manufacturer = subprocess.check_output('wmic COMPUTERSYSTEM GET MANUFACTURER', shell=True).decode().strip()
    os_serial_number = subprocess.check_output('WMIC BIOS GET SERIALNUMBER', shell=True).decode().strip()

    model = get_property_value(os_model)
    manufacturer = get_property_value(os_manufacturer)
    serial_number = get_property_value(os_serial_number)

    print("-------------")
    print('osModel:', model)
    print('osManufacturer:', manufacturer)
    print('osSerialNumber:', serial_number)
    print("-------------")

    if any(os_model.lower() in model.lower() for os_model in vm_os_model_list):
        print('Honeypot detected', model)
    elif any(manufacturer.lower() == vm.lower() for vm in vm_manufacturer_list):
        print('Honeypot detected', manufacturer.lower())
    elif 'vm' in serial_number.lower():
        print('Honeypot detected')
    else:
        print('Not a honeypot, go ahead and hack the world')

def detect_linux_vm():
    print("Linux VM detection not implemented")

def detect_mac_vm():
    print("Mac VM detection not implemented")

host_platform = platform.system()
print("Platform detected:", host_platform)

if host_platform == 'Linux':
    detect_linux_vm()
elif host_platform == 'Windows':
    detect_windows_vm()
else:
    detect_mac_vm()
