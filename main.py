import json, os, glob, random, time
from unsplash.api import Api
from unsplash.auth import Auth
import tweepy
import urllib.request

credentials = json.loads(open("credentials.json").read())
TwitterAuth = tweepy.OAuthHandler(credentials["consumerKey"], credentials["consumerSecret"])
TwitterAuth.set_access_token(credentials["accessToken"], credentials["accessSecret"])
TwitterApi = tweepy.API(TwitterAuth)


client_id = credentials["unsplashID"]
client_secret = credentials["unsplashSecret"]
redirect_uri = credentials["callbackURL"]

UnsplashAuth = Auth(client_id, client_secret, redirect_uri)
UnsplashApi = Api(UnsplashAuth)

def getImage():

    image = UnsplashApi.photo.random(featured=True)
    
    # imgData = {
    #     "url": img["urls"]["regular"] + ".jpg",
    #     "credit": img["user"]["name"] or img["user"]["username"],
    #     "creditLink": (img["links"]["self"] or img["user"]["portfolio_url"] or img["user"]["links"]["portfolio"]).replace("api.","")
    # }

    return image


def downloadImage(imgURL):
    savePath = "/app/images/input/" + str(random.randint(1,1000)) + ".jpg"
    urllib.request.urlretrieve(imgURL, savePath)
    time.sleep(2)
    return savePath

def getArtStyle():
    availableStyles = glob.glob("ckpt_files/*")
    return random.choice(availableStyles)

def styleImage(imgPath, stylePath):
    script = str("python evaluate.py --checkpoint " + stylePath + " --in-path " + "/app/images/input/" + " --out-path " + "/app/images/output/" + " --allow-different-dimensions")
    os.system(script)

    return imgPath.replace("input","output")

def genDescription(data):
    return data["style"] + " applied to a photo by " + data["credit"] + ".\nOriginal: " + data["creditLink"]

def tweetArt(imgPath, post):
    time.sleep(3)
    TwitterApi.update_with_media(
        str(imgPath),
        status=post
    )

def genNewPost():
    image = getImage()
    print(image)

    # imgPath = downloadImage(image["url"])
    # artStylePath = getArtStyle()

    # image["style"] = "'" + artStylePath.split("/")[-1].replace(".ckpt","").replace("_"," ").title() + "' art style"

    # styledImgPath = styleImage(imgPath, artStylePath)
    # description = genDescription(image)

    # tweetArt(styledImgPath, description)
    # os.remove(imgPath)
    # os.remove(styledImgPath)


def main():
    #sleepTime = 60 * 60 *  4
    sleepTime = 3
    while True:
        try:
            genNewPost()
        except Exception as e:
            TwitterApi.send_direct_message(credentials["myTwitter"], text="New post failed: " + str(e))

        time.sleep(sleepTime)

if __name__ == "__main__":
    main()

