import datetime

class TwitterPost:

    entity_id = 0
    count_favorites = 0
    count_retweet = 0
    entity_id = 0
    comment = ""
    created = None
    distribution = []

    def __init__(self, entity_id):
        self.entity_id = entity_id

    def get_id(self):
        return self.entity_id

    def set_count_favorites(self, count_favorites):
        self.count_favorites = count_favorites

    def set_count_retweet(self, count_retweet):
        self.count_retweet = count_retweet

    def set_comment(self, comment):
        self.comment = comment

    def get_comment(self):
        return self.comment

    def get_count_favorites(self):
        return self.count_favorites

    def get_count_retweet(self):
        return self.count_retweet

    def set_distribution(self, distribution):
        self.distribution = distribution

    def get_distribution(self):
        return self.distribution

    def set_created(self, created):
        self.created = created

    def get_created(self):
        return self.created

    def summarize(self):
        return {
            "tw_id": self.get_id(),
            "count_favorites": self.get_count_favorites(),
            "count_retweet": self.get_count_retweet(),
            "comment": self.get_comment(),
            "distribution": self.get_distribution(),
            "created": self.get_created(),
            "date": datetime.datetime.utcnow()
        }


class FacebookPost:

    entity_id = 0
    count_likes = ""
    count_comments = ""
    comments = []
    distribution = []
    created = None


    def __init__(self, entity_id):
        self.entity_id = entity_id

    def get_id(self):
        return self.entity_id

    def set_count_likes(self, count_likes):
        self.count_likes = count_likes

    def set_count_comments(self, count_comments):
        self.count_comments = count_comments

    def set_comments(self, comments):
        self.comments = comments

    def get_comments(self):
        return self.comments

    def get_count_likes(self):
        return self.count_likes

    def get_count_comments(self):
        return self.count_comments

    def set_distribution(self, distribution):
        self.distribution = distribution

    def get_distribution(self):
        return self.distribution

    def set_created(self, created):
        self.created = created

    def get_created(self):
        return self.created

    def summarize(self):
        return {
            "fb_id": self.get_id(),
            "count_likes": self.get_count_likes(),
            "count_comments": self.get_count_comments(),
            "comments": self.get_comments(),
            "distribution": self.get_distribution(),
            "created": self.get_created(),
            "date": datetime.datetime.utcnow()
        }