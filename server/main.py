# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from urllib.parse import urlparse

hostName = "glitchtech.top"
serverPort = 6

class HopefullyServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        p = self.path
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        c = query_components["username"]
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        if(p=="/supersecret"):
            self.wfile.write(bytes("Nice work Vincent\n", "utf-8"))
        self.wfile.write(bytes("Error 469: Ben detected! Request rejected. We apologize for the inconvenience. =" + p + "=!" + query + "!", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), HopefullyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")