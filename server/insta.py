from instagrapi import Client

#cl = Client()
#cl.login("AACPS.star.light", "vincentsucks")

print("Instagram bot standing by")

def refresh():
    posts = cl.user_medias(user_id=60300809689, amount=20)
    print(posts)

