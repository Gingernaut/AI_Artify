from unsplash.api import Api
from unsplash.auth import Auth
import json, os, glob, random, time

credentials = json.loads(open("credentials.json").read())


unsplashAuth = Auth(credentials['unsplashAccessId'],
            credentials['unsplashSecretId'], 
            credentials['callbackURL'])

unsplashApi = Api(unsplashAuth)

randId = unsplashApi.photo.random(featured=True)[0]

print(randId)