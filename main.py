import json, os, glob, random, time, requests
import tweepy
import urllib.request

credentials = json.loads(open('credentials.json').read())
TwitterAuth = tweepy.OAuthHandler(credentials['twitterConsumerKey'], credentials['twitterConsumerSecret'])
TwitterAuth.set_access_token(credentials['twitterAccessToken'], credentials['twitterAccessSecret'])
TwitterApi = tweepy.API(TwitterAuth)

def getQueryTerm():
    return "&query=" + random.choice(['mountains', 'nature', 'forest', 'jungle', 'beach', 'autumn', 'winter', 'summer', 'spring', 'waterfall', 'rain'])

def getImage():
    random_url = 'https://api.unsplash.com/photos/random?featured=true'

    headers = {'Authorization': 'Client-ID ' + credentials['unsplashAccessId']}
    img = requests.get(random_url, headers=headers).json()
    creditName = img['user'].get('name', img['user'].get('username'))
    if img['user'].get('twitter_username'):
        creditName = '@' + img['user']['twitter_username']

    return {
        'url': img['urls']['regular'] + '.jpg',
        'credit': creditName,
        'creditLink': img['links']['self'].replace('api.', '')
    }

def downloadImage(imgURL):
    print(imgURL)
    try:
        savePath = './images/input/' + str(random.randint(1,1000)) + '.jpg'
        urllib.request.urlretrieve(imgURL, savePath)
        time.sleep(5)
        return savePath
    except Exception as e:
        TwitterApi.send_direct_message(credentials['myTwitter'], text='download image failed: ' + str(e))


def getArtStyle():
    availableStyles = glob.glob('ckpt_files/*')
    return random.choice(availableStyles)

def styleImage(imgPath, stylePath):
    try:
        script = str('python evaluate.py --checkpoint ' + stylePath + ' --in-path ' + './images/input/' + ' --out-path ' + './images/output/' + ' --allow-different-dimensions')
        os.system(script)
        return imgPath.replace('input','output')

    except Exception as e:
        TwitterApi.send_direct_message(credentials['myTwitter'], text='styling image failed: ' + str(e))

def genDescription(data):
    if data.get('credit'):
        return '{} applied to a photo by {}. \nOriginal: {} \n #tensorflow #styletransfer'.format(data['style'], data['credit'], data['creditLink'])
    else:
        return '{} applied to an @unsplash featured photo. \nOriginal: {} \n #tensorflow #styletransfer'.format(data['style'], data['creditLink'])

def tweetArt(imgPath, post):
    try:
        time.sleep(3)
        TwitterApi.update_with_media(
            str(imgPath),
            status=post
        )
    except Exception as e:
        TwitterApi.send_direct_message(credentials['myTwitter'], text='Tweeting image failed: ' + str(e))


def removeImages():
    outputs = glob.glob('./images/output/*')
    for f in outputs:
        os.remove(f)

    inputs = glob.glob('./images/input/*')
    for f in inputs:
        os.remove(f)

def genNewPost():
    image = getImage()

    imgPath = downloadImage(image['url'])
    artStylePath = getArtStyle()

    artStyleName = artStylePath.split("/")[-1].replace(".ckpt","").replace("_"," ").title()
    image['style'] = "'{}' art style".format(artStyleName)

    styledImgPath = styleImage(imgPath, artStylePath)
    description = genDescription(image)

    tweetArt(styledImgPath, description)
    removeImages()

def main():
    sleepTime = 60 * 60 * 4
    while True:
        try:
            genNewPost()
            time.sleep(sleepTime)
        except Exception as e:
            TwitterApi.send_direct_message(credentials['myTwitter'], text='New post failed: ' + str(e))
            time.sleep(5)
            print(e)

    TwitterApi.send_direct_message(credentials['myTwitter'], text='AI_Artify is shutting down')

if __name__ == '__main__':
    main()

