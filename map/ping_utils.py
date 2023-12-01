import subprocess

def ping_device(device_ip):
    try:
        # Realiza el ping al dispositivo
        subprocess.run(["ping", "-c", "1", device_ip], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
