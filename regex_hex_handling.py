
import re
import string
	# import nltk
	# from nltk.tokenize import TweetTokenizer

tweet_str = 'b"[/Very seldom~ will someone enter your life] to question\xc3\xa2\xe2\x82\xac\xc2\xa6 "'
print(type(tweet_str))
# ''' WORKS!!:
# tweet_regex = re.sub(r'\\x[a-f0-9]{2,}', '', tweet_str)'''
#eliminating the "b' " or 'b " ' charaters added by python after converting from bytes to strings:
tweet_nob = re.sub(r'^(b\'b\")', '', tweet_str)
#deleting final ' or ":
tweet_noendquot = re.sub(r'\'\"$', '', tweet_nob)
#deleting anything that hex representations ('\xc3', etc)
#print('this is tweet_noendquot: ', tweet_noendquot)
tweet_regex = re.sub(r'\\x[a-f0-9]{2,}', '', tweet_noendquot)
#tweet1.decode('ascii','ignore')
#print('this is tweet_regex: ', tweet_regex)
#print('this is tweet_regex type: ', type(tweet_regex))


#cleaning [] and /~
tweet_non_marks = re.sub(r'[\[\]~/]', '', tweet_str)
print('this is tweet non marks: ', tweet_non_marks)




##WORKS:
#clear_tweet =''.join([c for c in tweet if ord(c) < 128])
# print('this is clear_tweet: ', clear_tweet)


# print('this is tweet: ', tweet)
# print('this is tweet type: ', type(tweet))
# tweet_en = tweet.encode('utf8')
# print('this is tweet_en: ', tweet_en)
# print('this is tweet_en type: ', type(tweet_en))
# tweet_str = str(tweet_en)
# print('this is tweet_str: ', tweet_str)



