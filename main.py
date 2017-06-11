"""
import credentials and tweepy client
def sendTweet
def downloadImage
def styleImage
def deleteImg
def getArtStyle
def main
"""
import tweepy
import json
import glob
import random
from unsplash_python.unsplash import Unsplash

import urllib.request

credentials = json.loads(open('credentials.json').read())
auth = tweepy.OAuthHandler(credentials['consumerKey'], credentials['consumerSecret'])
auth.set_access_token(credentials['accessToken'], credentials['accessSecret'])
api = tweepy.API(auth)

def getImageURL():

    unsplash = Unsplash({
        'application_id': credentials['unsplashID'],
        'secret': credentials['unsplashSecret'],
        'callback_url': credentials['callbackURL']
    })

    img = unsplash.photos().get_random_photo(
        featured=True
    )[0]

    return img['urls']['full'] + '.jpg'


def downloadImage(imgURL):
    imgPath = "images/unsplashPhoto" + str(random.randint(1,1000)) + ".jpg"
    urllib.request.urlretrieve(imgURL,imgPath)
    return imgPath


def getArtStyle():
    availableStyles = glob.glob("ckpt_files/*")

    return random.choice(availableStyles)




def tweetArt():
    api.update_with_media()



def main():
    image = getImageURL()
    imgPath = downloadImage(image)

    artStylePath = getArtStyle()



main()

# python evaluate.py --checkpoint ckpt_files/" + fields['arttype'] +".ckpt --in-path uploads/ --out-path outputs/")
