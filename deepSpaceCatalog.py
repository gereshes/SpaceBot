import tweepy
from datetime import date
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skyfield.api import Loader, Topos, EarthSatellite
import csv
import pandas
import pandas as pd
import math
import os
import pickle
import requests
import random
import csv
from lxml import html
import re
from numpy import genfromtxt
import pandas as pd

fileName='pathToData'
df=pd.read_csv(fileName, sep=',',header=None)


dirpath = os.getcwd()

today = date.today()

consumer_key= ''
consumer_secret=''
access_token= ''
access_token_secret= ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

monthNum=today.month
dayNum=today.day
yearNum=today.year

entries=np.shape(df.values)

vectorRand=np.argsort(np.random.rand(entries[0]))
content = "Today, {} years ago, something happened in deep-space.\n\n What happened, I dont know. \n\n ¯\_(ツ)_/¯ ".format(random.randint(1, 100))
for c in range(entries[0]):
        dateStr=df.values[vectorRand[c]][4][0:11]
        try:
                dateOfEvent=datetime.datetime.strptime(dateStr, '%Y %b %d')
                if(dateOfEvent.month==monthNum and dateOfEvent.day==dayNum):
                        yearsPast=yearNum-dateOfEvent.year
                        indexForEntry=vectorRand[c]
                        idNum=df.values[indexForEntry][0]
                        name=df.values[indexForEntry][1]
                        task=df.values[indexForEntry][-1]
                        content = "Today, {} years ago, {} ({}) {} \n\nThis data collected from www.planet4589.org/space/deepcat/".format(yearsPast,name,idNum,task)
                        break
        except:
                print('err')

print(dateOfEvent)
print(yearsPast)
print(df.values[indexForEntry])

print(content)
public_tweets = api.update_status(content)
