# -*- coding: utf-8 -*-
"""CSM_Twitter Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vj8fHru4W-4FCEfWpD6CrPM8Jzy0Xcsu
"""

#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
# https://github.com/sixohsix/twitter/tree/master
# Python Twitter Tool (Version 1.18.0)
from twitter import *
from twitter.stream import TwitterStream, Timeout, HeartbeatTimeout, Hangup
import time
import pandas as pd

# Replace with your own key/secret
consumer_key ='insert your consumer key here'
consumer_secret ='insert your consumer secret here'
resource_owner_key ='insert your resource owner key here'
resource_owner_secret ='insert resource owner secret here'


#NA notes: Build lists of expected attributes (columns) you want to have on your dataframe
#full text
full_text = []
#tweet information, hashtag
url = []
retweet = []
loneliness = []
lonely = []
desolation = []
solitude = []
forlorn = []
lonesome = []
alone = []
#tweet content
langVal = []
hashtagsVal = []
screen_nameVal = []
retweetScreenNameVal = []

if __name__ == '__main__':
    while True:
        try:
            # When using twitter stream you must authorize.
            auth = OAuth(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                token=resource_owner_key,
                token_secret=resource_owner_secret
            )
            # Set location bounding box
            query_args = {'track': 'loneliness,lonely,desolation,solitude,forlorn,lonesome,alone', 'stall_warnings':True}
            # Start authorization and filtering tweets
            stream = TwitterStream(auth=auth)
            tweet_iter = stream.statuses.filter(**query_args)
            # Iterate over the sample stream.
            for tweet in tweet_iter:
                # We should check the type of tweet.
                # It might be  a delete or data message.
                if tweet is None:
                    print("-- None --")
                elif tweet is Timeout:
                    print("-- Timeout --")
                elif tweet is HeartbeatTimeout:
                    print("-- Heartbeat Timeout --")
                elif tweet is Hangup:
                    print("-- Hangup --")
                else:
                    #valid tweets come to this stage
                    print(tweet)
                    print('/n') #print tweets 
                    #clean data - put values of desired attributes into lists
                    if tweet['entities']['urls']==[]:
                        url.append(0)
                    else: url.append(1)
                    text = ''
                    if 'retweeted_status' in tweet:
                        retweet.append(1)
                        retweetScreenNameVal.append(tweet['retweeted_status']['user']['screen_name'])
                        if 'extended_tweet' in tweet['retweeted_status']: 
                            text = tweet['retweeted_status']['extended_tweet']['full_text']
                        else: 
                            text = tweet['retweeted_status']['text']
                        full_text.append(text)
                    else: 
                        retweet.append(0)
                        retweetScreenNameVal.append('')
                        if "extended_tweet" in tweet:
                            text = tweet['extended_tweet']['full_text']
                        else: 
                            text = tweet['text']
                        full_text.append(text)
                    
                    tags = ''
                    
                    for hashtag in tweet['entities']['hashtags']:
                        tags = tags + hashtag['text'] + ' '
                    #for example if it has key words
                    if 'loneliness' in text or 'loneliness' in tags:
                        loneliness.append(1)
                    else: loneliness.append(0)
                    if 'lonely' in text or 'lonely' in tags:
                        lonely.append(1)
                    else: lonely.append(0)
                    if 'desolation' in text or 'desolation' in tags:
                        desolation.append(1)
                    else: desolation.append(0)
                    if 'solitude' in text or 'solitude' in tags:
                        solitude.append(1)
                    else: solitude.append(0)
                    if 'forlorn' in text or 'forlorn' in tags:
                        forlorn.append(1)
                    else: forlorn.append(0)
                    if 'lonesome' in text or 'lonesome' in tags:
                        lonesome.append(1)
                    else: lonesome.append(0)
                    if 'alone' in text or 'alone' in tags:
                        alone.append(1)
                    else: alone.append(0)
                   #tweet content
                    langVal.append(tweet['lang'])

                    hashtagsVal.append(tags)
                    
                    screen_nameVal.append(tweet['user']['screen_name'])

                #form a dataframe from these lists above
                dictTweets = {"full_text": full_text, 'url': url, 'retweet': retweet, 
                              'loneliness': loneliness, 'lonely': lonely,
                              'desolation': desolation, 'solitude': solitude, 
                              'forlorn': forlorn, 'lonesome': lonesome, 
                              'alone': alone,
                              #Tweet content
                              'langVal': langVal, 'hashtagsVal': hashtagsVal,
                              'screen_nameVal': screen_nameVal,
                              'retweetScreennameVal': retweetScreenNameVal}
                

                df = pd.DataFrame(dictTweets) #no need to specify cols if all keys in dictTweets are included
                #save to local computer - replace "C:\Users\ADMIN\Downloads\samples.csv" with your own file path and file name 
                df.to_csv ('/Users/Lam/Documents/Project/Fall/CSM_Final/Reup/Data.csv', index = False, header=True)

        except Exception as e:
            print('error (Follow): ' + str(e))
            time.sleep(15)