import requests
import base62
import datetime

# If you don't see this, everything went wrong!
print("The client helper is here!")
# Makes a request to our server. Response will be 0, 1 or 2
# 0 = Failed to find credentials, 1 = Found user credentials, 2 = Found admin credentials

def en(input):
    return base62.encodebytes(bytes(input, "utf-8"))


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

def addPost(title, author, desc, path ="sample_image.jpg", date ="auto"):
    image_file = path
    with open(image_file, 'rb') as f:
         r = requests.post('http://glitchtech.top:6/addpost', data=f)
    req = r.json()
    print(str(req))

    if date == "auto":
        today = datetime.date.today()
        year = today.year
        month = today.month
        day = today.day
        if day < 10:
            day = "0" + str(day)
        if month < 10:
            month = "0" + str(month)
        date = str(month) + "-" + str(day) + "-" + str(year)
        print(date)

    r = requests.get("http://glitchtech.top:6/addpost", params={
        "title": en(title),
        "author": en(author),
        "desc": en(desc),
        "date": en(date)})

    req = r.json()
    print(str(req))
    return req
