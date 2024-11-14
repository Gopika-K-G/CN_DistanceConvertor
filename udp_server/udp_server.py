# udp_server.py

import socket
import os

# Conversion factors
conversion_factors = {
    'cm': 1,
    'mm': 10,
    'inches': 0.393701,
    'km': 0.00001,
    'ft': 0.0328084,
    'm': 0.01,
    'yd': 0.0109361,
    'mile': 0.0000062137,
    'dm': 0.1
}

# Conversion logic
def convert_distance(value, from_unit, to_unit):
    if from_unit in conversion_factors and to_unit in conversion_factors:
        converted_value = value * (conversion_factors[to_unit] / conversion_factors[from_unit])
        return round(converted_value, 2)
    return None

def udp_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', port))

    print(f"UDP Server listening on port {port}")
    while True:
        data, addr = server_socket.recvfrom(1024)
        value, from_unit, to_unit = data.decode().split(',')
        converted_value = convert_distance(float(value), from_unit, to_unit)
        
        print(f"UDP Request from {addr[0]}: {value} {from_unit} to {to_unit}")
        server_socket.sendto(str(converted_value).encode(), addr)

if __name__ == '__main__':
    udp_port = int(os.environ.get("UDP_PORT", 5001))  # Use environment variable for UDP port
    udp_server(udp_port)
