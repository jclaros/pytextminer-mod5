import datetime

class FacebookFeed:

    entity_id = 0
    comment = ""
    distribution = []

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

    def summarize(self):
        return {
            "fb_id": self.get_id(),
            "count_likes": self.get_count_likes(),
            "count_comments": self.get_count_comments(),
            "comments": self.get_comments(),
            "distribution": self.get_distribution(),
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