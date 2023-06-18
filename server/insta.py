from instagrapi import Client
import json
from instagrapi.exceptions import LoginRequired
import logging

logger = logging.getLogger()
cl = Client()

cl.delay_range = [1, 3]

USERNAME = "aacps.star.light"
PASSWORD = "vincentsucks"

def login_user():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    session = cl.load_settings("session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")


login_user()
print("Instagram bot standing by")

# These flags correspond to preference for checking Instagram over local, True=Local | False=Instagram,
# only use for emergency data correction please
def refresh(num =True, url =True, name =True, author =True, date =True, desc =True):
    posts = cl.user_medias(user_id=60300809689, amount=50)
    postfile = open("posts.json")
    postjson = json.load(postfile)
    oldposts = postjson["posts"]
    newposts = []
    postfile.close()
    c = 0
    for item in posts:
        m = item.dict()
        l = len(oldposts) > c
        if l:
            o = oldposts[c]
        n = {}

        if l and num:
            n["num"] = o["num"]
        else:
            n["num"] = c
        if l and url and (o["url"] != "none"):
            n["url"] = o["url"]
        else:
            n["url"] = m["thumbnail_url"]
        if l and name:
            n["name"] = o["name"]
        else:
            n["name"] = "Unnamed"
        if l and author:
            n["author"] = o["author"]
        else:
            n["author"] = "aacps.star.light"
        # Instagram uses YYYY-MM-DD format, so let us do the same for clarity's sake
        if l and date:
            n["date"] = o["date"]
        else:
            n["date"] = str(m["taken_at"])[:10]
        if l and desc:
            n["desc"] = o["desc"]
        else:
            n["desc"] = m["caption_text"]
        c = c + 1
        newposts.append(n)
    outjson = open("posts.json", "w")
    postsdict = {"posts": newposts}
    json.dump(postsdict, outjson, indent=2)
    outjson.close()


def add(desc):
    media = cl.photo_upload("upload.jpg", desc)
    refresh()
    return str(media)


''' Instagram user_medias() format breakdown
[
    Media(
        pk='3125309052166860228', 
        id='3125309052166860228_60300809689', 
        code='CtfVAY7t-3E', 
        taken_at=datetime.datetime(
            2023, 6, 14, 23, 38, 13, 
            tzinfo=datetime.timezone.utc
            ), 
        media_type=1, 
        image_versions2={}, 
        product_type='', 
        thumbnail_url=HttpUrl('https://scontent-iad3-2.cdninstagram.com/v/t51.2885-15/353778885_1227100771140408_8889196121969248234_n.jpg?stp=dst-jpg_e15&_nc_ht=scontent-iad3-2.cdninstagram.com&_nc_cat=100&_nc_ohc=_YSc9uSRNDEAX-eS7Pm&edm=APU89FABAAAA&ccb=7-5&oh=00_AfC72Y9YZFPn3mVAH46zn1BCjg39HK5GEgeYTQcdZekmTA&oe=6490C11C&_nc_sid=f4eaf9', ), 
        location=None, 
        user=UserShort(pk='60300809689', 
                       username='aacps.star.light', 
                       full_name='', 
                       profile_pic_url=None, 
                       profile_pic_url_hd=None, 
                       is_private=None, 
                       stories=[]
                       ), 
        comment_count=0, 
        comments_disabled=False, 
        commenting_disabled_for_viewer=False, 
        like_count=0, 
        play_count=None, 
        has_liked=None, 
        caption_text='So glad to be on Star Light, the new school event management program. Follow us for important updates from AACPS.', 
        accessibility_caption=None, 
        usertags=[], 
        sponsor_tags=[], 
        video_url=None, 
        view_count=0, 
        video_duration=0.0, 
        title='', 
        resources=[], 
        clips_metadata={}
    )
]
'''

