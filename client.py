import requests
import base62

# If you don't see this, everything went wrong!
print("The client helper is here!")
# Makes a request to our server. Response will be 0, 1 or 2
# 0 = Failed to find credentials, 1 = Found user credentials, 2 = Found admin credentials
def login(username, password):
    r = requests.get("http://glitchtech.top:6/login", params={"username": username, "password": password})
    req = r.json()
    print("Login response: " + str(req))
    return req

def getPosts():
    r = requests.get("http://glitchtech.top:6/posts")
    req = r.json()
    return req

def signup(username, password, name):
    r = requests.get("http://glitchtech.top:6/signup", params={"username": username, "password": password, "name": name})
    req = r.json()
    print("Signup response: " + str(req))
    return req

def addPost():
    image_file = 'sample_image.jpg'
    with open(image_file, "rb") as f:
        im_bytes = f.read()
    im_b62 = base62.encodebytes(im_bytes)
    print(im_b62)

    r = requests.get("http://glitchtech.top:6/addpost", params={"img": im_b62})
    req = r.json()
    print(str(req))
    return req
