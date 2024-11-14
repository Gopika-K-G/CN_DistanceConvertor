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

def tcp_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)

    print(f"TCP Server listening on port {port}")
    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024).decode()
        parts = data.split(',')

        if len(parts) == 3:
            value, from_unit, to_unit = parts
            converted_value = convert_distance(float(value), from_unit, to_unit)
            print(f"TCP Request from {addr[0]}: {value} {from_unit} to {to_unit}")
        else:
            converted_value = "Invalid input format. Please provide: value,from_unit,to_unit"
            print(f"Received invalid input from {addr[0]}: {data}")

        client_socket.sendall(str(converted_value).encode())
        client_socket.close()

if __name__ == '__main__':
    tcp_port = int(os.environ.get("PORT", 5002))
    tcp_server(tcp_port)
