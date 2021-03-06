#!/usr/bin/python
# -*- coding: utf-8 -*-


import csv
import sys
import couchdb
from twitter_DB import load_from_DB

# this program contains a function to return lists of tweets' text using the 'text' entity in the tweet's metadata

# for each tweet, this function returns the text of that tweet
# Parameter:  a tweet (as a Twitter json object)
# Result:  A list of the text of first xx tweets
def get_entities(tweet):
    # get the tweet's text
    if 'text' in tweet.keys():
        twit=[tweet['text']]
        return twit
    else:
        # if no entities key, return empty lists
        return [],

# the main program tests this function by loading all tweets from a search database
#   and printing the entities from the first XX tweets
if __name__ == '__main__':
    # this should be the name of a DB with tweets
    DBname = 'a-few-081015'
    
    # open the database directly from CouchDB so that we can delete items as necessary
    # connect to database on couchdb server
    search_results = load_from_DB(DBname)    
    
    # open the database directly from CouchDB so that we can delete items as necessary
     # connect to database on couchdb server
    server = couchdb.Server('http://localhost:5984')
    try:
        db = server[DBname]
        print "Connected to DB named", DBname
    except couchdb.http.PreconditionFailed, e:
        db = server[DB]
        print "Could not find DB named", DBname
        sys.exit(0)
    except ValueError, e:
        print "Invalid DB name"
        sys.exit(0)    
    
    print 'number tweets loaded', len(search_results)  

    # initialize a dictionary of tweet ids
    # the first time an id is found, put it into the dict as a key (with value 1 (not used))          
    uniqueIDs = {}    
    numtweets = len(search_results)
    numdeleted = 0       
    
    for tweet in search_results:  
        # find the retweeted_status field
        if 'retweeted_status' in tweet.keys():   
            #get retweeted_status id
            if 'id' in tweet['retweeted_status']:
                retweetID = tweet['retweeted_status']['id']
                #print for verification
                #print "retweeted_status ID found: ", retweetID
                #check if the retweeted_status id is already in the dictionary                
                if retweetID in uniqueIDs.keys():
                    #if it's there, delete the tweet
                    db.delete(tweet)
                    #add "1" to the count of deleted tweets
                    numdeleted += 1
                  # otherwise add it to the unique ids
                else:
                    uniqueIDs[retweetID] = 1
            else:
                # reduce the count if we skipped one
                numtweets -= 1

    
    print "Number of tweets at beginning = ", numtweets
    print "Number of tweets deleted = ", numdeleted
    #print "Unique Retweet IDs = ", uniqueIDs    
    
    search_results = load_from_DB(DBname)
    
    # go through the first XX tweets and print the tweet text    
    for tweet in search_results[:200]:
        twit = get_entities(tweet)
        print 'Tweet text:', twit
        
  