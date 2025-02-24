from captchaImageGenerator import generate_captcha
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json


HOST = "localhost"
PORT = 8000

class CaptchaHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.serve_file("Captcha.html", "text/html")
        elif self.path == "/captcha.png":
            self.serve_file("captcha.png", "image/png", binary=True)
        elif self.path.startswith("/submit"):
            self.handle_captcha_submission()
        else:
            self.send_error(404, "File Not Found")

    def serve_file(self, filename, content_type, binary=False):
        """ Serves static files correctly with proper encoding. """
        try:
            if binary:
                with open(filename, "rb") as f:
                    content = f.read()
            else:
                with open(filename, "r", encoding="utf-8") as f:  # Force UTF-8 encoding
                    content = f.read().encode()

            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, f"File {filename} not found")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")

    def handle_captcha_submission(self):
        """ Handles CAPTCHA validation. """
        query = urlparse(self.path).query
        params = parse_qs(query)
        user_input = params.get("captchaInput", [""])[0].strip()

        try:
            with open("captcha_text.txt", "r") as f:
                correct_captcha = f.read().strip()
        except FileNotFoundError:
            self.send_json({"success": False, "message": "CAPTCHA not found. Please refresh."})
            return

        if user_input == correct_captcha:
            response = {"success": True, "message": "CAPTCHA is correct!"}
        else:
            new_captcha_text = generate_captcha()
            print(f"New CAPTCHA generated: {new_captcha_text}")
            response = {"success": False, "message": "Incorrect CAPTCHA. Try again!"}

        self.send_json(response)

    def send_json(self, data):
        """ Sends JSON response. """
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

if __name__ == "__main__":
    captcha_text = generate_captcha()
    print(f"Generated CAPTCHA: {captcha_text}")

    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, CaptchaHandler)

    webbrowser.open(f"http://{HOST}:{PORT}")
    print(f"Server started at http://{HOST}:{PORT}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
        httpd.server_close()

