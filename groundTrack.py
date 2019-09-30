import tweepy
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skyfield.api import Loader, Topos, EarthSatellite
import csv
import pandas
import math
import os


dirpath = os.getcwd()

today = date.today()

consumer_key= ''
consumer_secret=''
access_token= ''
access_token_secret= ''


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def getTLE():
    import requests
    import random
    import csv
    print('Requesting TLE')



    #print('Hello')


    random='https://www.space-track.org/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/'+str(random.randint(25545,44000))+' /orderby/ORDINAL asc/limit/1000/format/tle/emptyresult/show'



    data = {
      'identity': '',
      'password': '',
      'query': random
        }

    response = requests.post('https://www.space-track.org/ajaxauth/login', data=data)


    tempFile='..Data\tempCSV.csv'

    with open(tempFile, 'w') as f:
        writer = csv.writer(f)
        for line in response.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))

def generatePlot():
    print('Generating Plot')

    df = pandas.read_csv('../Data/tempCSV.csv')


    objectID = df.values[1][0][2:7]
    L1=df.values[1][0]
    L2=df.values[2][0]

    load = Loader('~/Documents/fishing/SkyData')  # avoids multiple copies of large files
    ts   = load.timescale()

    data    = load('de421.bsp')
    earth   = data['earth']
    ts      = load.timescale()

    minutes = np.arange(60. * 24 )         # seven days
    time    = ts.utc(today.year, today.month, today.day, 0, minutes)  # start June 1, 2018

    ISS     = EarthSatellite(L1, L2)

    subpoint = ISS.at(time).subpoint()

    lon      = subpoint.longitude.degrees
    lat      = subpoint.latitude.degrees
    breaks   = np.where(np.abs(lon[1:]-lon[:-1]) > 30)  #don't plot wrap-around

    lon, lat    = lon[:-1], lat[:-1]
    lon[breaks] = np.nan


    my_tweet='Ground Track of NORAD ID #'+str(objectID)+' for the next 24 hours'

    fig1, ax1 = plt.subplots()

    earth=mpimg.imread('../Figures/earth.tif')
    earth=mpimg.imread(earthImg)
    ax1.imshow(earth)

    ax1.plot(10800*(lon/360  +.5), 5400*(lat/180 + 0.5))
    plt.axis('off')
    imgFile="../Figures/latestGroundTrack.png"

    plt.savefig(imgFile,dpi=300, bbox_inches='tight', pad_inches = 0)

    fig2, ax2 = plt.subplots()
    ax2.plot(lon/360 +.5, lat/180 -.5)


    print(lat[0])
    if(math.isnan(lat[0])):
        exitFlag=False
    else:
        exitFlag=True


    return exitFlag,my_tweet

exitFlag=False
while(not(exitFlag)):
    print(dirpath)
    getTLE()
    exitFlag,my_tweet=generatePlot()
    if(exitFlag):
        print(exitFlag)
        imgFile="../Figures/latestGroundTrack.png"

        print('Sending To Twitter')
        public_tweets = api.update_with_media(imgFile,my_tweet)
    else:
        print(exitFlag)
        print('Trying Again')
        print('*************')
