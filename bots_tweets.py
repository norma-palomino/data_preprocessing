from __future__ import print_function
import csv

from pymongo import MongoClient
client = MongoClient('localhost', 27017)



def get_tweets(db_name, collection_name):
    db = client[db_name]
    tweets_cursor = db[collection_name].find()

    tweets = []

    for tweet in tweets_cursor:
        tweets.append(tweet)

    #print(tweets)    
    return tweets

def get_sources(tweets):
    
    sources = []
    
    for tweet in tweets:
        bot = tweet['source'].find('bot')
        if bot > -1:            
            source = bot, tweet['id_str'], tweet['source'].encode('utf-8')
            sources.append(source)
    #print('this is sources: ', sources)
    return sources


def export_tweet_ids_sources(sources, file_name):      
    with open(file_name,'wb') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['bot_index','str_id', 'source_text'])
        for row in sources:
            csv_out.writerow(row)    
            
            

            
    #with open(file_name, 'w') as fp:
        #writer = csv.writer(f, delimiter='\t')
        #fp.write('\n'.join('{} {} {}'.format(x[0], '\t', x[1], '\t', x[2].encode('utf-8'), '\t') for x in sources))    
    
    
    #with open(file_name, 'wb') as f:
        #writer = csv.writer(f)
        
        # write headers
        #writer.writerow(['id_str', 'source'])
        #for counter, tweet in enumerate(tweets):
            #tweet_id = tweet['id_str']
            #source=tweet['source'].encode('utf-8')
            #writer.writerow([tweet_id,source])
            
            

if __name__ == '__main__':
    # Goal: help the user to input the database and file names    
    database_name =  'annotation_guidelines'
    collection_name = 'scarcely_tweets'
    #database_name = raw_input('enter database name: ')
    #collection_name = raw_input('enter collection name: ')
    tweets = get_tweets(database_name, collection_name)
    sources = get_sources(tweets)
    #print(sources)
    export_tweet_ids_sources(sources, '3_botindex_strid__sources_' + collection_name + '.csv')



