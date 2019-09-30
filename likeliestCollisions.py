import tweepy
from datetime import date
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

consumer_key= ''
consumer_secret=''
access_token= ''
access_token_secret= ''


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

response = requests.get('https://www.celestrak.com/SOCRATES/search-results.php?IDENT=NAME&NAME_TEXT1=&NAME_TEXT2=&ORDER=MAXPROB&MAX=20')
tree=html.fromstring(response.content)
conj=[]
for c in range(20):#go through all 20 just in case

    name1 = tree.xpath('/html/body/table[4]/form['+str(c+1)+']/tr[1]/td/text()')[1]
    id1= tree.xpath('/html/body/table[4]/form['+str(c+1)+']/tr[1]/td/text()')[0]
    name2 = tree.xpath('/html/body/table[4]/form['+str(c+1)+']/tr[2]/td/text()')[1]
    id2= tree.xpath('/html/body/table[4]/form['+str(c+1)+']/tr[2]/td/text()')[0]
    tca = tree.xpath('/html/body/table[4]/form['+str(c+1)+']/tr[2]/td/text()')[4]
    relVel=float(tree.xpath('/html/body/table[4]/form['+str(c+1)+']/tr[1]/td/text()')[6])

    if(relVel>0.001): #To ensure that it isnt two objects docked together
        conj.append([name1,id1,name2,id2,tca])

print(conj[0:5])
my_tweet = 'The two objects with the highest collision probability today are: \n\nObject 1 - '+conj[0][0] +' ('+conj[0][1]+')'+' \nObject 2 - '+conj[0][2] +' ('+conj[0][3]+')\n\nTheir time of closest approach is: '+tca+'\n\nThis data collected from https://www.celestrak.com/SOCRATES/'


public_tweets = api.update_status(my_tweet)
print('Sending To Twitter')
