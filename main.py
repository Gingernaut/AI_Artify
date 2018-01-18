import json, os, glob, random, time, requests
import tweepy
import urllib.request

credentials = json.loads(open('credentials.json').read())
TwitterAuth = tweepy.OAuthHandler(credentials['consumerKey'], credentials['consumerSecret'])
TwitterAuth.set_access_token(credentials['accessToken'], credentials['accessSecret'])
TwitterApi = tweepy.API(TwitterAuth)

def getQueryTerm():
    return "&query=" + random.choice(['mountains', 'nature', 'forest', 'jungle', 'beach', 'autumn', 'winter', 'summer', 'spring', 'waterfall', 'rain'])

def getImage():
    random_url = 'https://api.unsplash.com/photos/random?featured=true' + getQueryTerm()

    headers = {'Authorization': 'Client-ID ' + credentials['unsplashID']}
    img = requests.get(random_url, headers=headers).json()

    creditName = img['user'].get('name', img['user'].get('username', None))
    if img['user'].get('twitter_username', None):
        creditName = '@' + img['user']['twitter_username']

    return {
        'url': img['urls']['regular'] + '.jpg',
        'credit': creditName,
        'creditLink': img['links']['self'].replace('api.', '')
    }

def downloadImage(imgURL):
    try:
        savePath = '/app/images/input/' + str(random.randint(1,1000)) + '.jpg'
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
        script = str('python evaluate.py --checkpoint ' + stylePath + ' --in-path ' + '/app/images/input/' + ' --out-path ' + '/app/images/output/' + ' --allow-different-dimensions')
        os.system(script)
        return imgPath.replace('input','output')

    except Exception as e:
        TwitterApi.send_direct_message(credentials['myTwitter'], text='styling image failed: ' + str(e))

def genDescription(data):
    if data.get('credit', None):
        return '{} applied to a photo by {}. \nOriginal: {}'.format(data['style'], data['credit'], data['creditLink'])
    else:
        return '{} applied to an @unsplash featured photo. \nOriginal: {}'.format(data['style'], data['creditLink'])

def tweetArt(imgPath, post):
    try:
        time.sleep(3)
        TwitterApi.update_with_media(
            str(imgPath),
            status=post
        )
    except Exception as e:
        TwitterApi.send_direct_message(credentials['myTwitter'], text='Tweeting image failed: ' + str(e))

def genNewPost():
    image = getImage()

    imgPath = downloadImage(image['url'])
    artStylePath = getArtStyle()

    artStyleName = artStylePath.split("/")[-1].replace(".ckpt","").replace("_"," ").title()
    image['style'] = "'{}' art style".format(artStyleName)

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
            time.sleep(sleepTime)
        except Exception as e:
            TwitterApi.send_direct_message(credentials['myTwitter'], text='New post failed: ' + str(e))
            time.sleep(5)
            print(e)

if __name__ == '__main__':
    main()

