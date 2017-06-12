import json, os, glob, random, time
from unsplash_python.unsplash import Unsplash
import tweepy
import urllib.request

credentials = json.loads(open('credentials.json').read())
auth = tweepy.OAuthHandler(credentials['consumerKey'], credentials['consumerSecret'])
auth.set_access_token(credentials['accessToken'], credentials['accessSecret'])
api = tweepy.API(auth)
cwd = str(os.getcwd())

def getImageURL():

    unsplash = Unsplash({
        'application_id': credentials['unsplashID'],
        'secret': credentials['unsplashSecret'],
        'callback_url': credentials['callbackURL']
    })

    img = unsplash.photos().get_random_photo(
        featured=True
    )[0]

    return img['urls']['regular'] + '.jpg'


def downloadImage(imgURL):
    savePath = "images/input/" + str(random.randint(1,10000)) + ".jpg"
    urllib.request.urlretrieve(imgURL,savePath)
    return savePath


def getArtStyle():
    availableStyles = glob.glob("ckpt_files/*")

    return random.choice(availableStyles)

def styleImage(imgPath, stylePath):

    script = str("python evaluate.py --checkpoint " + stylePath + " --in-path " + "images/input/" + " --out-path " + "images/output/" + " --allow-different-dimensions")
    os.system(script)


    return imgPath.replace("input","output")

def tweetArt(imgPath):
    api.update_with_media(str(imgPath))
    print("tweet sent")


def postNewArt():
    image = getImageURL()
    imgPath = downloadImage(image)
    artStylePath = getArtStyle()

    styledImgPath = styleImage(imgPath,artStylePath)

    tweetArt(imgPath)


def main():

    sleepTime = 60 * 60 *  6 # 6 hours

    sleepTime = 20 # five seconds


    while True:
        postNewArt()
        time.sleep(sleepTime)


main()

# python evaluate.py --checkpoint ckpt_files/" + fields['arttype'] +".ckpt --in-path uploads/ --out-path outputs/")
