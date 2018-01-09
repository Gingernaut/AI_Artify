import json, os, glob, random, time, requests
import tweepy
import urllib.request

credentials = json.loads(open("credentials.json").read())
TwitterAuth = tweepy.OAuthHandler(credentials["consumerKey"], credentials["consumerSecret"])
TwitterAuth.set_access_token(credentials["accessToken"], credentials["accessSecret"])
TwitterApi = tweepy.API(TwitterAuth)

def getImage():
    random_url = "https://api.unsplash.com/photos/random?featured=true"

    headers = {'Authorization': 'Client-ID ' + credentials["unsplashID"]}
    img = requests.get(random_url, headers=headers).json()

    creditName = img["user"]["name"] or img["user"]["username"]
    if img["user"].get("twitter_username", None):
        creditName = "@" + img["user"]["twitter_username"]

    imgData = {
        "url": img["urls"]["regular"] + ".jpg",
        "credit": creditName,
        "creditLink": img["links"]["self"].replace("api.", "")
    }

    return imgData

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
        status=post)

def genNewPost():
    image = getImage()

    imgPath = downloadImage(image["url"])
    artStylePath = getArtStyle()

    image["style"] = "'" + artStylePath.split("/")[-1].replace(".ckpt","").replace("_"," ").title() + "' art style"

    styledImgPath = styleImage(imgPath, artStylePath)
    description = genDescription(image)

    tweetArt(styledImgPath, description)
    os.remove(imgPath)
    os.remove(styledImgPath)


def main():
    sleepTime = 60 * 60 *  4
    while True:
        try:
            genNewPost()
        except Exception as e:
            TwitterApi.send_direct_message(credentials["myTwitter"], text="New post failed: " + str(e))
            print(e)
        time.sleep(sleepTime)

if __name__ == "__main__":
    main()

