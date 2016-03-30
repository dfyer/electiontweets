
# Author: Park, Han Gyu
# I wrote this code, but 
# Reference: https://gist.github.com/yanofsky/5436496

import tweepy
import csv

consumer_info = open("secrets/consumer-info.dat", "r")
consumer_lines = consumer_info.read().splitlines()
consumer_key = consumer_lines[0]
consumer_secret = consumer_lines[1]
consumer_info.close()

access_token_info = open("secrets/access-token-info.dat", "r")
access_token_lines = access_token_info.read().splitlines()
access_token = access_token_lines[0]
access_token_secret = access_token_lines[1]
access_token_info.close()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#api = tweepy.API(auth_handler = oAuth, api_root = '/1.1')
api = tweepy.API(auth)

if __name__ == "__main__":

    screen_name = "soilpower"

    alltweets = []

    # REQUEST FOR RECENT TWEETS (MAX:200)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1

    # tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "...%s tweets downloaded so far" % (len(alltweets))

    #transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8").replace("\n", " ")] for tweet in alltweets]

    #write the csv
    with open('%s_tweets.csv' % screen_name, 'wb') as newfile:
        writer = csv.writer(newfile, delimiter="|")
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
