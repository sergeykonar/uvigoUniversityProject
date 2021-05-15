from google.appengine.ext import ndb


class Article(ndb.Model):
    hours = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty(required=True)
    content = ndb.StringProperty(required=True)
    author = ndb.StringProperty(required=True)
    image = ndb.StringProperty()


class Comment(ndb.Model):
    hours = ndb.DateTimeProperty(auto_now_add=True)
    text = ndb.StringProperty(required=True)
    author = ndb.StringProperty()
    article = ndb.KeyProperty(kind=Article)
