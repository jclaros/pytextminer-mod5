from facepy import GraphAPI
from pymongo import MongoClient
from time import strptime
import time
import sys


from .Entity import FacebookPost

class Facebook:
    db = None
    facebook_entities = []
    analyzer = None
    graphic_api_access = False

    def __init__(self, access_code, analyzer):
        self.graphic_api_access = GraphAPI(access_code)
        self.analyzer = analyzer
        client = MongoClient('localhost', 27017)
        self.db = client["socialinteraction"]

    def start_process(self, company_name):
        try:
            self.analyze_posts(company_name)
        except:
            print("error analyzing data", sys.exc_info()[0])

    def analyze_posts(self, company):
        url = "{}/posts?limit=10".format(company)
        results = self.graphic_api_access.get(url)
        if len(results['data']) > 0:
            self.parse_posts(results)

    def analyze_feeds(self, company):
        url = "{}/feed?limit=50".format(company)
        results = self.graphic_api_access.get(url)
        if len(results['data']) > 0:
            self.parse_feeds(results)

    def check_analyzed(self, type, result):
        element = self.db[type].find({"fb_id": result["id"]}).limit(1)
        return element.count() == 0


    def process_likes_count(self, ob_id, face_obj):
        #get likes
        response = self.graphic_api_access.get("{}/likes?summary=1".format(ob_id))
        if response["summary"] and response["summary"]["total_count"]:
            face_obj.set_count_likes(int(response["summary"]["total_count"]))

    def process_comments(self, ob_id, face_obj):
        comments = []
        response = self.graphic_api_access.get("{}/comments?limit=10&summary=1".format(ob_id))
        if response["summary"] and response["summary"]["total_count"]:
            face_obj.set_count_comments(int(response["summary"]["total_count"]))
        if len(response["data"]) > 0:
            for comment in response["data"]:
                com = comment["message"].lower().replace(".", "")
                comments.append(com)
        try:
            if len(response["data"]) > 0 and response["paging"] and response["paging"]["next"]:
                self.get_more_comments(ob_id, response["paging"]["cursors"]["after"], comments)
        except KeyError:
            pass

        face_obj.set_comments(comments)

    def get_more_comments(self, ob_id, token, comments):
        response = self.graphic_api_access.get("{}/comments?limit=10&after={}".format(ob_id, token))
        if len(response["data"]) > 0:
            for comment in response["data"]:
                com = comment["message"].lower().replace(".", "")
                comments.append(com)
            try:
                if len(response["data"]) > 0 and response["paging"] and response["paging"]["cursors"]:
                    self.get_more_comments(ob_id, response["paging"]["cursors"]["after"], comments)
            except KeyError:
                pass

    def process_post(self, post):
        object_id = post['id']
        face_post = FacebookPost(object_id)
        date_created = time.strptime(post["created_time"], '%Y-%m-%dT%H:%M:%S+0000')
        face_post.set_created(date_created)
        self.process_likes_count(object_id, face_post)
        self.process_comments(object_id, face_post)
        self.analyzer.populate_comments(face_post)
        # prepare post
        entity = face_post.summarize()
        self.db["fb_posts"].insert_one(entity)

    def parse_posts(self, results):
        for result in results['data']:
            if self.check_analyzed("fb_posts", result):
                self.process_post(result)
