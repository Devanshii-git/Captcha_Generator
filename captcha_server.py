from captchaImageGenerator import *
import webbrowser
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

HOST = "localhost"
PORT = 8000
class CaptchaHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("Captcha.html", "r") as f:
                self.wfile.write(f.read().encode())

        elif self.path == "/captcha.png":
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            with open("captcha.png", "rb") as f:
                self.wfile.write(f.read())

        elif self.path.startswith("/submit"):
            query = urlparse(self.path).query
            params = parse_qs(query)
            user_input = params.get("captchaInput", [""])[0].strip()
            print(f"User entered: {user_input}")

            with open("captcha_text.txt", "r") as f:
                correct_captcha = f.read().strip()

            if user_input == correct_captcha:
                response = """
                <h1 style='text-align:center;font-family:sans-serif;color:green;'>CAPTCHA is correct!</h1>
                """
            else:
                # Generate a new CAPTCHA if the user gets it wrong
                new_captcha_text = generate_captcha()
                print(f"New CAPTCHA generated: {new_captcha_text}")

                response = """
                <h1 style='text-align:center;font-family:sans-serif;color:red;'>CAPTCHA is incorrect!</h1>
                <p style='text-align:center;'>Generating a new CAPTCHA...</p>
                <script>
                    setTimeout(function() {
                        window.location.href = "/";
                    }, 2000);
                </script>
                """

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(response.encode())


if __name__ == "__main__":
    # Generate the first CAPTCHA
    captcha_text = generate_captcha()
    print(f"Generated CAPTCHA: {captcha_text}")

    server_address = ("", 8000)
    httpd = HTTPServer(server_address, CaptchaHandler)

    webbrowser.open("http://localhost:8000")
    print("Server started at http://localhost:8000")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
        httpd.server_close()
