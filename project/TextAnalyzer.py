__author__ = 'jonathan'

import nltk
from nltk.corpus import stopwords
from nltk import FreqDist


class TextAnalyzer:
    _instance = None

    stopwords = []
    cleaned = []

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TextAnalyzer, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.stopwords = stopwords.words('spanish')
        self.cleaned = []


    def populate_comments(self, face_post):
        comments_cleaned = []
        for comment in face_post.get_comments():
            tokens = nltk.word_tokenize(comment)
            base_cleaned = [w for w in tokens if w not in self.stopwords and len(w) > 1]
            comments_cleaned.extend(base_cleaned)
            self.cleaned.extend(base_cleaned)

        dist = FreqDist(comments_cleaned)
        distribution = dist.most_common(30)
        face_post.set_distribution(distribution)


    def calculate_total_distribution(self):
        dist = FreqDist(self.cleaned)
        return dist.most_common(20)






