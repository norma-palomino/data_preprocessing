from get_tweets_mongo import get_tweets
from export_tweets_csv import export_tweets
import re



# GOAL: to remove duplicates
# a duplicate is a tweet with the same string, ignoring "RT"
# and ignoring @mentions


def ignore_junk(string):
    # TO DO: ignore @mentions as well
    string_without_rt = re.sub(r'^RT', '', string, flags=re.IGNORECASE)
    string_without_at = re.sub(r'@[\w\-0-9]+', '', string_without_rt,
                               flags=re.IGNORECASE)
    string_single_spaces = re.sub('\s+', ' ', string_without_at)
    string_without_urls = re.sub('http[^\s]+', '', string_single_spaces)
    string_trimming = string_without_urls.strip()
    return string_trimming


def is_duplicate(tweet1, tweet2):##duplicate should handle str_id
    # returns True if tweets match, otherwise return false
    tweet1_text = tweet1['tweet_text']
    tweet2_text = tweet2['tweet_text']

    return ignore_junk(tweet1_text) == ignore_junk(tweet2_text)


def tweet_is_in_list(tweet1, unique_tweets):
    '''returns True if the tweet1 is in unique_tweets
            returns False if the tweet is not in unique_tweets
    '''
    for tweet2 in unique_tweets:
        if is_duplicate(tweet1, tweet2):
            return True

    return False


def without_duplicate_strId(tweets):#
    # takes a list of tweets
    # returns a NEW list without duplicates
    # for each tweets,
        # compare it to ALL the other tweets
        # to see if `compare_tweets`
    unique_tweets = []
    for tweet in tweets:
        if not tweet_is_in_list(tweet, unique_tweets):##compares tweets
            unique_tweets.append(tweet)
    return unique_tweets


if __name__ == '__main__':
    database_name = raw_input('enter database name: ') # open files
    collection_name = raw_input('enter collection name: ')
    tweets = get_tweets(database_name, collection_name)
    print len(tweets)
    unique_tweets = without_duplicate_text(tweets[1:1000])
    print len(unique_tweets)
    export_tweets(unique_tweets, 'unique_' + collection_name + '.csv')
