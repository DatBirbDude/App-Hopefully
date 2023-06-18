from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base62
from urllib.parse import urlparse
import os

import insta

hostName = "glitchtech.top"
serverPort = 6


def handleImage(img):
    outimage = open("upload.jpg", "wb")
    outimage.write(img)
    outimage.close()
    os.system('cp upload.jpg /var/www/isvincent.gay/public_html/upload.jpg')

def inIndex(list, target):
    for i in list:
        if i == target:
            return True
    return False

def de(input):
    return base62.decodebytes(input).decode("utf-8")

def jwrite(file, outjson):
    outfile = open(file, "w")
    json.dump(outjson, outfile, indent=2)
    outfile.close()

def jload(file):
    jfile = open(file)
    jdict = json.load(jfile)
    jfile.close()
    return jdict

def login(username, password):
    logins = jload("creds.json")
    ret = {"res": 0, "name": "noname"}
    if username in logins['users']:
        ret["res"] = 1
        if password == logins['users'][username]['Password']:
            ret["name"] = logins['users'][username]['Name']
            ret["res"] = 2
            if(logins['users'][username]['Admin']):
                ret["res"] = 3
    return ret

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
            output = login(username, password)
            self.wfile.write(bytes(json.dumps(output), "utf-8"))

        if (p[0] == "/signup"):
            username = de(query_components["username"])
            password = de(query_components["password"])
            newuser = {"Password": "NOT FOUND", "Name": "NOT FOUND", "Admin": False}

            if login(username, password)["res"] < 1:
                name = de(query_components["name"])
                logins = jload("creds.json")
                newuser = {"Password": password, "Name": name, "Admin": False}
                logins["users"][username] = newuser
                jwrite("creds.json", logins)
            self.wfile.write(bytes(json.dumps({"new user": newuser}), "utf-8"))

        if(p[0]=="/refresh"):
            insta.refresh()
            self.wfile.write(bytes(json.dumps({"refresh": 1}), "utf-8"))

        if (p[0] == "/bugs"):
            self.wfile.write(bytes(json.dumps(jload("bugs.json")), "utf-8"))

        if (p[0] == "/addbug"):
            name = de(query_components["name"])
            bug = de(query_components["bug"])
            bugjson = jload("bugs.json")
            newbug = {"Name": name, "Bug": bug}
            bugjson.append(newbug)
            jwrite("bugs.json", bugjson)
            self.wfile.write(bytes(json.dumps({"bug": newbug}), "utf-8"))

        if (p[0] == "/addnotice"):
            name = de(query_components["name"])
            noticetype = de(query_components["type"])
            date = de(query_components["date"])
            notes = de(query_components["notes"])
            noticejson = jload("notice.json")
            newnotice = {"Name": name, "Type": noticetype, "Date": date, "Notes": notes}
            noticejson.append(newnotice)
            jwrite("notice.json", noticejson)
            self.wfile.write(bytes(json.dumps({"notice": newnotice}), "utf-8"))
        if (p[0] == "/notices"):
            self.wfile.write(bytes(json.dumps(jload("notice.json")), "utf-8"))

        if(p[0]=="/addpost"):
            author = de(query_components["author"])
            name = de(query_components["title"])
            date = de(query_components["date"])
            desc = de(query_components["desc"])
            postfile = open("posts.json")
            postjson = json.load(postfile)
            postfile.close()
            newpost = {"num": len(postjson["posts"]), "url": "none", "name": name, "author": author, "date": date, "desc": desc}
            postjson["posts"].append(newpost)
            outjson = open("posts.json", "w")
            json.dump(postjson, outjson, indent=2)
            outjson.close()
            trypost = {"media": insta.add(desc), "post": newpost}
            self.wfile.write(bytes(json.dumps(trypost), "utf-8"))

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
