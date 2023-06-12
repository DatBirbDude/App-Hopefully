import requests

#If you don't see this, everything went wrong!
print("The client helper is here!")

def login(username, password):
    res = requests.get("http://glitchtech.top:6/login", params = {"username": username, "password": password})
    print(res.text)
    return res.text
