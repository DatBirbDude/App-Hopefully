# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse

hostName = "glitchtech.top"
serverPort = 6

def login(self, username, password):
    l = open('creds.json')
    logins = json.load(l)
    ret = {"res": 0}
    if username in logins['users']:
        if password == logins['users'][username]['Password']:
            name = logins['users'][username]['Name']
            #self.wfile.write(bytes("Name: " + name + "\n", "utf-8"))
            ret["res"] = 1
            if(logins['users'][username]['Admin']):
                #self.wfile.write(bytes("You are an admin!\n", "utf-8"))
                ret["res"] = 2
    self.wfile.write(bytes(json.dumps(ret)))
    l.close()
    return

class HopefullyServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        p = self.path.split("?")
        #Refer to p[0] for get path
        query = urlparse(self.path).query
        if(len(query)>0):
            query_components = dict(qc.split("=") for qc in query.split("&"))
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        if(p[0]=="/login"):
            username = query_components["username"]
            password = query_components["password"]
            login(self, username, password)
            #self.wfile.write(bytes("Lol your login is " + username + ":" +  password + "\n", "utf-8"))
        if(p[0]=="/supersecret"):
            self.wfile.write(bytes("Nice work Vincent\n", "utf-8"))
        self.wfile.write(bytes("Error 469: Ben detected! Request rejected. We apologize for the inconvenience. =" + p[0] + "=!" + query + "!", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), HopefullyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
