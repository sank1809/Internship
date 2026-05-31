import socket

target = input("Enter Target IP or Website: ")

# Remove https:// or http://
target = target.replace("https://", "")
target = target.replace("http://", "")
target = target.strip("/")

print(f"\nScanning {target}...\n")

ports = [21, 22, 23, 25, 53, 80, 443, 8080]

try:
    ip = socket.gethostbyname(target)

    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        result = s.connect_ex((ip, port))

        if result == 0:
            print(f"Port {port} is OPEN")
        else:
            print(f"Port {port} is CLOSED")

        s.close()

    print("\nScan Completed")

except socket.gaierror:
    print("Invalid website or unable to resolve hostname")
