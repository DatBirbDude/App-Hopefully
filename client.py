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
    r = requests.get("http://glitchtech.top:6/login", params={"username": en(username), "password": en(password)})
    req = r.json()
    print("Login response: " + str(req))
    return req

def signup(username, password, name):
    r = requests.get("http://glitchtech.top:6/signup", params={"username": en(username),
                                                               "password": en(password),
                                                               "name": en(name)})
    req = r.json()
    print("Signup response: " + str(req))
    return req

def getDate():
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    if day < 10:
        day = "0" + str(day)
    if month < 10:
        month = "0" + str(month)
    date = str(month) + "-" + str(day) + "-" + str(year)
    return date

def getPosts():
    r = requests.get("http://glitchtech.top:6/posts")
    req = r.json()
    return req

#Only send .jpg please or the server will not work.
def addPost(title, author, desc, path, date ="auto"):
    image_file = path
    with open(image_file, 'rb') as f:
         r = requests.post('http://glitchtech.top:6/addpost', data=f)
    req = r.json()
    print(str(req))

    if date == "auto":
        date = getDate()

    r = requests.get("http://glitchtech.top:6/addpost", params={
        "title": en(title),
        "author": en(author),
        "desc": en(desc),
        "date": en(date)})

    req = r.json()
    print(str(req))
    return req


def getNotices():
    r = requests.get("http://glitchtech.top:6/notices")
    req = r.json()
    return req


def addNotice(name, noticeType, notes, date="auto"):
    if date == "auto":
        date = getDate()

    r = requests.get("http://glitchtech.top:6/addnotice", params={
        "name": en(name),
        "type": en(noticeType),
        "date": en(date),
        "notes": en(notes)})

    req = r.json()
    print(str(req))
    return req

def getBugs():
    r = requests.get("http://glitchtech.top:6/bugs")
    req = r.json()
    return req


def addBug(name, bug):
    r = requests.get("http://glitchtech.top:6/addbug", params={
        "name": en(name),
        "bug": en(bug)})

    req = r.json()
    print(str(req))
    return req