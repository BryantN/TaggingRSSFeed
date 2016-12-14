import TwitterSearch
import feedparser
import json
import sys, traceback
import time
from datetime import datetime
"""
Bryant Nielson
Long Script Built to Gather Data From multiple news Sources.
feedlist, holds  the sources, with thier respective autotags
"""

feedlist = {}

feedlist['WashingtonPost'] = {
    'feeds': ['http://feeds.washingtonpost.com/rss/politics',
    'http://feeds.washingtonpost.com/rss/sports',
    'http://feeds.washingtonpost.com/rss/rss_speaking-of-science',
    'http://feeds.washingtonpost.com/rss/rss_innovations',
    'http://feeds.washingtonpost.com/rss/world',
    'http://feeds.washingtonpost.com/rss/business',
    'http://feeds.washingtonpost.com/rss/entertainment'],
    'autoTags' : ['politics', 'sports', 'science','technology','international','business','entertainment']
}

feedlist['LATimes']={

    'feeds':['http://www.latimes.com/world/europe/rss2.0.xml',
    'http://www.latimes.com/sports/rss2.0.xml',
    'http://www.latimes.com/entertainment/rss2.0.xml',
    'http://www.latimes.com/nation/politics/rss2.0.xml',
    'http://www.latimes.com/science/rss2.0.xml',
    'http://www.latimes.com/business/rss2.0.xml'],
'autoTags' :['europe', 'sports', 'entertainment','politics','science','buisness']
}

feedlist['ESPN']={

    'feeds':['http://www.espn.com/espn/rss/nfl/news',
    'http://www.espn.com/espn/rss/mlb/news',
    'http://www.espn.com/espn/rss/nba/news',
    'http://www.espn.com/espn/rss/nhl/news',
    'http://soccernet.espn.com/rss/news',
    'http://www.espn.com/espn/rss/news'],
'autoTags' :['sports', 'sports', 'sports','sports','sports','sports']
}


feedlist['NYTimes']={

    'feeds':['http://feeds.nytimes.com/nyt/rss/Technology',
    'http://www.nytimes.com/services/xml/rss/nyt/Soccer.xml',
    'http://www.nytimes.com/services/xml/rss/nyt/Sports.xml',
    'http://www.nytimes.com/services/xml/rss/nyt/ProBasketball.xml',
    'http://www.nytimes.com/services/xml/rss/nyt/Science.xml',
    'http://www.nytimes.com/services/xml/rss/nyt/Environment.xml',
    'http://www.nytimes.com/services/xml/rss/nyt/Politics.xml',
             'http://feeds.nytimes.com/nyt/rss/Business'],
'autoTags' :['science', 'sports', 'sports','sports','science','science','politics','Business']
}

# your twitter tokens go here
ts = TwitterSearch.TwitterSearch(
    consumer_key='ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ',
    consumer_secret='BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    access_token='ccccccccccccccccccccccccccccccccccccccccccccccccccc',
    access_token_secret='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
)
Mapping = []
count = 0
try:
    for selectedFeed, blah in feedlist.items():
        try:
            for j in xrange(len(feedlist[selectedFeed]['feeds'])):
                d = feedparser.parse(feedlist[selectedFeed]['feeds'][j])
                print d
                for i in d['entries']:
                    try:
                        print "hit"
                        print i['title']
                        tso = TwitterSearch.TwitterSearchOrder()
                        tso.set_keywords([i['link']])
                        AllTags = []
                        limit = 40
                        for tweet in ts.search_tweets_iterable(tso):
                            limit -= 1
                            if 0 < len(tweet['entities']['hashtags']):
                                AllTags.append(tweet['entities']['hashtags'][0]['text'])
                            if limit < 0:
                                break
                        AllTags.append(feedlist[selectedFeed]['autoTags'][j])
                        AllTagSet = set(AllTags)
                        if len(AllTagSet) >= 2:
                            count += 1
                        Mapping.append({'title': i['title'], 'links': list(AllTagSet)})
                    except TwitterSearch.TwitterSearchException as e:
                        print e
                        traceback.print_exc()
                        # pause if twitter is getting tired of the amount of requests I have made
                        if e.code == 429:
                            time.sleep(15*60)
        except Exception as e:
            # Forgive me general exception handling, can't let a 2 hour run fail for a bad single character encode.
            print e
            traceback.print_exc()

except Exception as e:
    # Forgive me again, occaisionly the feed doens't like to be parsed.
    print e
    traceback.print_exc()

# Little timestamp function from stack overflow
def timeStamp(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
    return datetime.now().strftime(fmt).format(fname=fname)

f = open('./InputData/' + timeStamp("AllFeeds") + '.txt', 'w')
json.dump(Mapping, f)
#Counts the Number of 'Good' Datapoints, Data, that has two or more tags, averages around 360 a run
# mainly for my point of view.
print count
