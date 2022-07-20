import tweepy
from tweepy import OAuthHandler
from tweepy import Cursor
import time


class TwitterService:
    def __init__(self, cons_key, cons_secret, acc_token, acc_secret):
        super().__init__()
        self.url = None
        self.cons_key = cons_key
        self.cons_secret = cons_secret
        self.acc_token = acc_token
        self.acc_secret = acc_secret

    def get_twitter_auth(self, cons_key, cons_secret, acc_token, acc_secret):
        """
            This method is responsible to make the authentication with twitter
            after, you could use this connection for whatever you need
            :param string cons_key: your consumer key
            :param string cons_secret: your consumer_secret
            :param string acc_token: your access token
            :param string acc_secret: your access secret
            :return: auth - the authentication to twitter using tweepy
        """

        try:
            consumer_key = cons_key
            consumer_secret = cons_secret
            access_token = acc_token
            access_secret = acc_secret

        except KeyError:
            sys.stderr.write("Twitter Environment Variable not Set\n")
            sys.exit(1)

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        return auth

    def get_twitter_client(self):
        """
            This method is responsible to make the authentication with twitter
            and return the client to be used after
            :return: client - the client to access the twitter API
        """

        auth = self.get_twitter_auth(self.cons_key,
                                     self.cons_secret,
                                     self.acc_token,
                                     self.acc_secret
                                     )
        client = tweepy.API(auth, wait_on_rate_limit=True)
        return client

    def tweets_timeout(self):
        timeout = 30  # [seconds]
        timeout_start = time.time()
        while time.time() < timeout_start + timeout:
            time_counter = 0
            if time_counter == 5:
                break
            time_counter += 1

    def get_tweets_from_tag(self, search_tag, page_limit=1, count_tweet=100):
        """
            This method is responsible to make the authentication with twitter
            after, you could use this connection for whatever you need
            :param search_tag: the retrieved search tag
            :param string page_limit: the total number of pages
            :param string count_tweet: the maximum number of tweets to be retrieved from a page
            :return: all the tweets for the specified tag
        """
        client = self.get_twitter_client()

        timeout = 30
        timeout_start = time.time()
        all_tweets = []

        for page in Cursor(client.search_tweets,
                           q=search_tag,
                           count=count_tweet).pages(page_limit):
            for tweet in page:
                parsed_tweet = {'message_id': tweet.id,
                                'message_created_at': tweet.created_at,
                                'text': tweet.text,
                                'author': tweet.author.name,
                                'user_id': tweet.user.id,
                                'user_created_at': tweet.user.created_at,
                                'user_name': tweet.user.name,
                                'user_screen_name': tweet.user.screen_name
                                }

                all_tweets.append(parsed_tweet)
                if time.time() > timeout_start + timeout:
                    break

        return all_tweets

