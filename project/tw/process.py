from twitter import *
from project.TextAnalyzer import TextAnalyzer
from project.fb.Entity import TwitterPost
from pymongo import MongoClient
import time
import re


class TwitterProcess:
    _twitter_api = None
    _auth = None
    _company_processed = ""
    _analyzer = None
    _db = None

    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''


    def __init__(self, analizer):
        self._twitter_api = Twitter(
            auth=OAuth(self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET, self.CONSUMER_KEY, self.CONSUMER_SECRET))
        self._analyzer = analizer
        client = MongoClient('localhost', 27017)
        self.db = client["socialinteraction"]

    def start_process(self, name_company):
        self._company_processed = name_company
        q = name_company
        count = 100
        search_results = self._twitter_api.search.tweets(q=q, count=count)
        statuses = search_results['statuses']

        # Iterate through 5 more batches of results by following the cursor

        for _ in range(5):
            print("Length of statuses", len(statuses))
            try:
                next_results = search_results['search_metadata']['next_results']
            except KeyError:
                break

            # Create a dictionary from next_results, which has the following form:
            # ?max_id=313519052523986943&q=NCAA&include_entities=1
            kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])

            search_results = self._twitter_api.search.tweets(**kwargs)
            statuses += search_results['statuses']

        for status in statuses:

            if self.check_analyzed(status['id']):
                tw_entity = TwitterPost(status['id'])
                status_text = status['text']
                tw_entity.set_comment(status_text)
                status_text = status_text.replace(".", "").replace("#", '')
                status_text = re.sub(r"http\S+", "", status_text)
                tw_entity.set_count_favorites(status['favorite_count'])
                tw_entity.set_count_retweet(status['retweet_count'])
                tw_entity.set_created(time.strptime(status['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
                self._analyzer.populate_twcomment(tw_entity, status_text)
                summary = tw_entity.summarize()
                self.db["tw_posts"].insert_one(summary)

    def check_analyzed(self, id):
        element = self.db["tw_posts"].find({"tw_id": id}).limit(1)
        return element.count() == 0


        # screen_names = [ user_mention['screen_name']
        # for user_mention in status['entities']['user_mentions'] ]
        #
        # hashtags = [ hashtag['text']
        #                  for hashtag in status['entities']['hashtags']]



