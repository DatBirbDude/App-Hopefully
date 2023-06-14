import instagramapi

print("Instagram bot standing by")

def refresh() {
    posts = user_medias(user_id=55178546179, amount=20)
    print(posts)
}
