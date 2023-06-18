from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base62
from urllib.parse import urlparse
import os

import insta

hostName = "glitchtech.top"
serverPort = 6

def login(self, username, password):
    l = open('creds.json')
    logins = json.load(l)
    ret = {"res": 0, "name": "noname"}
    if username in logins['users']:
        if password == logins['users'][username]['Password']:
            ret["name"] = logins['users'][username]['Name']
            ret["res"] = 1
            if(logins['users'][username]['Admin']):
                ret["res"] = 2
    l.close()
    return ret
def handleImage(im_b62):
    #img_bytes = base62.decodebytes(im_b62)
    outimage = open("upload.jpg", "wb")
    outimage.write(im_b62)
    outimage.close()
    os.system('cp upload.jpg /var/www/isvincent.gay/public_html/upload.jpg')

def inIndex(list, target):
    for i in list:
        if i == target:
            return True
    return False

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
            output = login(self, username, password)
            self.wfile.write(bytes(json.dumps(output), "utf-8"))
        if(p[0]=="/addpost"):
            author = base62.decode(query_components["author"])
            name = base62.decode(query_components["title"])
            date = base62.decode(query_components["date"])
            desc = base62.decode(query_components["desc"])
            postfile = open("posts.json")
            postjson = json.load(postfile)
            postfile.close()
            newpost = {"num": len(postjson["posts"]), "url": "none", "name": name, "author": author, "date": date, "desc": desc}
            postjson["posts"].append(newpost)
            outjson = open("posts.json", "w")
            json.dump(postjson, outjson, indent=2)
            outjson.close()
            trypost = {"success": 1}
            self.wfile.write(bytes(json.dumps(newpost), "utf-8"))

        if(p[0]=="/posts"):
            postfile = open("posts.json")
            postjson = json.load(postfile)
            self.wfile.write(bytes(json.dumps(postjson), "utf-8"))
        if(p[0]=="/supersecret"):
            self.wfile.write(bytes("Nice work Vincent\n", "utf-8"))
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        #POST requests requiring decode should be put here
        decode = []
        if inIndex(decode, self.path):
            query = post_data.decode("utf-8")
            if (len(query) > 0):
                query_components = dict(qc.split("=") for qc in query.split("&"))
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        if self.path == "/addpost":
            handleImage(post_data)
            trypost = {"success": 1}
            self.wfile.write(bytes(json.dumps(trypost), "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), HopefullyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
