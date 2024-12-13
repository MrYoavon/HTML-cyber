import os
import socket

# Constants
IP = '0.0.0.0'
PORT = 54321
SOCKET_TIMEOUT = 10
DEFAULT_URL = '/index.html'
REDIRECTION_DICTIONARY = {
    '/page1.html': '/page2.html'
}
FORBIDDEN_FILES = ['forbidden.html']

CONTENT_TYPES = {
    'html': 'text/html; charset=utf-8',
    'txt': 'text/html; charset=utf-8',
    'jpg': 'image/jpeg',
    'js': 'text/javascript; charset=UTF-8',
    'css': 'text/css'
}

def get_file_data(filename):
    """ Get data from file """
    if not os.path.isfile(filename):
        return None
    with open(filename, 'rb') as f:
        return f.read()

def generate_http_header(status_code, content_type=None, content_length=None, location=None):
    """ Generate HTTP header based on the status code and additional parameters """
    header = f"HTTP/1.0 {status_code} \r\n"
    if content_type:
        header += f"Content-Type: {content_type}\r\n"
    if content_length:
        header += f"Content-Length: {content_length}\r\n"
    if location:
        header += f"Location: {location}\r\n"
    header += "\r\n"
    return header

def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client """
    if resource == '/':
        resource = DEFAULT_URL

    if resource in REDIRECTION_DICTIONARY:
        new_location = REDIRECTION_DICTIONARY[resource]
        http_header = generate_http_header('302 Found', location=new_location)
        client_socket.send(http_header.encode())
        return

    if resource.lstrip('/') in FORBIDDEN_FILES:
        http_header = generate_http_header('403 Forbidden')
        client_socket.send(http_header.encode())
        return

    filepath = resource.lstrip('/')
    file_data = get_file_data(filepath)

    if file_data is None:
        http_header = generate_http_header('404 Not Found')
        client_socket.send(http_header.encode())
        return

    file_extension = filepath.split('.')[-1]
    content_type = CONTENT_TYPES.get(file_extension, 'application/octet-stream')
    content_length = len(file_data)
    http_header = generate_http_header('200 OK', content_type=content_type, content_length=content_length)
    client_socket.send(http_header.encode() + file_data)

def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    try:
        lines = request.split('\r\n')
        request_line = lines[0]
        method, url, version = request_line.split(' ')
        if method == 'GET' and version.startswith('HTTP/'):
            return True, url
    except Exception:
        pass
    return False, None

def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    try:
        client_request = client_socket.recv(1024).decode()
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print(f'Got a valid HTTP request, {resource}')
            handle_client_request(resource, client_socket)
        else:
            print(f'Error: Not a valid HTTP request, {resource}')
            http_header = generate_http_header('500 Internal Server Error')
            client_socket.send(http_header.encode())
    except Exception as e:
        print(f'Error handling client: {e}')
    finally:
        print('Closing connection')
        client_socket.close()

def main():
    """ Main server loop """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    print(f"Listening for connections on port {PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)

if __name__ == "__main__":
    main()
