# Simple HTTP Server

## Overview
This project implements a basic HTTP server in Python that serves static files and handles HTTP GET requests. The server also includes support for:

- HTTP status codes like `200 OK`, `404 Not Found`, `403 Forbidden`, and `302 Found`.
- Serving files of various types (`html`, `txt`, `jpg`, `js`, `css`) with appropriate `Content-Type` headers.
- Redirecting requests for certain resources.
- Handling forbidden files and internal server errors.

## Features
- **Handles HTTP GET requests**: Serves requested files or returns appropriate HTTP error responses.
- **Content-Type support**: Automatically determines and sets the `Content-Type` header based on the file extension.
- **Redirection**: Redirects certain URLs to new locations using `302 Found`.
- **Forbidden access**: Prevents access to specified files, returning `403 Forbidden`.

## Prerequisites
- Python 3.x

## Usage
1. Clone or download the project files.
2. Ensure that Python 3 is installed on your system.
3. Open a terminal and navigate to the project directory.
4. Run the server using the command:
   ```bash
   python HTTP_server_shell.py
   ```
5. Open a web browser or use an HTTP client (e.g., `curl`) to access the server at:
   ```
   http://127.0.0.1:54321
   ```

### Accessing Files
- To access the root directory (`/`), navigate to:
  ```
  http://127.0.0.1:54321/
  ```
  The server will serve the `index.html` file (ensure this file exists in the same directory as the server).

- To request specific files, append their paths to the URL. For example:
  ```
  http://127.0.0.1:54321/example.html
  ```

### Handling Errors
- If the requested file does not exist, the server will return a `404 Not Found` response.
- If access to the file is forbidden, the server will return a `403 Forbidden` response.
- If the server encounters an unknown error, it will return a `500 Internal Server Error` response.

## Notes
- The server listens on `127.0.0.1` (localhost) and port `54321` by default. Make sure this port is not in use by another application.
- For testing redirection, request `/html1.page` to be redirected to `/html2.page`.

## Customization
You can modify the following aspects in the `HTTP_server_shell.py` file:
- **Port**: Change the `PORT` constant to a different value if needed.
- **Redirections**: Add or modify entries in the `REDIRECTION_DICTIONARY`.
- **Forbidden Files**: Add filenames to the `FORBIDDEN_FILES` list to restrict access.
---

Enjoy using this simple HTTP server!

