from flask import Flask, render_template, request, jsonify
import socket

app = Flask(__name__)

# Route to render the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Function to send data to TCP server
def send_to_tcp_server(value, from_unit, to_unit):
    server_address = ('https://cn-distanceconvertor-1.onrender.com', 5002)  # Replace with server's IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.connect(server_address)
        tcp_socket.sendall(f"{value},{from_unit},{to_unit}".encode())
        result = tcp_socket.recv(1024).decode()
    return result

# Function to send data to UDP server
def send_to_udp_server(value, from_unit, to_unit):
    server_address = ('localhost', 5001)  # Replace with server's IP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.sendto(f"{value},{from_unit},{to_unit}".encode(), server_address)
        result, _ = udp_socket.recvfrom(1024)
    return result.decode()

# Route to handle the form submission and communicate with the server
@app.route('https://cn-distanceconvertor-1.onrender.com/convert', methods=['POST'])
def convert():
    value = request.form.get('value')
    from_unit = request.form.get('from_unit')
    to_unit = request.form.get('to_unit')
    protocol = request.form.get('protocol')

    if protocol == 'TCP':
        result = send_to_tcp_server(value, from_unit, to_unit)
    elif protocol == 'UDP':
        result = send_to_udp_server(value, from_unit, to_unit)
    else:
        return jsonify({"error": "Invalid protocol"}), 400

    return jsonify({"converted_value": result, "protocol": protocol})

if __name__ == '__main__':
    app.run(debug=True)
