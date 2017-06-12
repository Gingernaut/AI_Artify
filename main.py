import json, os, glob, random, time
from unsplash_python.unsplash import Unsplash
import tweepy
import urllib.request

credentials = json.loads(open('credentials.json').read())
auth = tweepy.OAuthHandler(credentials['consumerKey'], credentials['consumerSecret'])
auth.set_access_token(credentials['accessToken'], credentials['accessSecret'])
api = tweepy.API(auth)
cwd = str(os.getcwd())

def getImage():
    unsplash = Unsplash({
        'application_id': credentials['unsplashID'],
        'secret': credentials['unsplashSecret'],
        'callback_url': credentials['callbackURL']
    })

    img = unsplash.photos().get_random_photo(
        featured=True
    )[0]

    imgData = {
        'url': img['urls']['regular'] + '.jpg',
        'credit': img['user']['name'] or img['user']['username'],
        'creditLink': (img['links']['self'] or img['user']['portfolio_url'] or img['user']['links']['portfolio']).replace("api.","")
    }

    return imgData


def downloadImage(imgURL):
    savePath = "images/input/" + str(random.randint(1,10000)) + ".jpg"
    urllib.request.urlretrieve(imgURL, savePath)
    return savePath


def getArtStyle():
    availableStyles = glob.glob("ckpt_files/*")
    return random.choice(availableStyles)

def styleImage(imgPath, stylePath):
    script = str("python evaluate.py --checkpoint " + stylePath + " --in-path " + "images/input/" + " --out-path " + "images/output/" + " --allow-different-dimensions")
    os.system(script)

    return imgPath.replace("input","output")


def genDescription(data):

    return data['style'] + " applied to a photograph by " + data['credit'] + '.\nOriginal photo: ' + data['creditLink']

def tweetArt(imgPath, post):
    time.sleep(1)
    api.update_with_media(
        str(imgPath),
        status=post
    )

 
def genNewPost():
    image = getImage()
    imgPath = downloadImage(image['url'])
    artStylePath = getArtStyle()

    image['style'] = "'" + artStylePath.split("/")[-1].replace(".ckpt","").replace("_"," ").title() + "' art style"

    styledImgPath = styleImage(imgPath, artStylePath)

    description = genDescription(image)
    print(description)

    tweetArt(styledImgPath, description)

    os.remove(imgPath)
    os.remove(styledImgPath)


def main():

    sleepTime = 60 * 60 *  6 # 6 hours

    sleepTime = 10 # five seconds


    while True:
        try:
            genNewPost()
        except Exception as e:
            print("Error: " + str(e))

        time.sleep(sleepTime)


main()
