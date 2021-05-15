import time

import webapp2
from webapp2_extras import jinja2

from webapp2_extras.users import users
from google.appengine.ext import ndb
from handlers.models import Article, Comment


class MainHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        print ("NEWS")
        txt_article_key = self.request.GET["id"]
        article_key = ndb.Key(urlsafe=txt_article_key)
        article = article_key.get()
        comments_list = Comment.query(Comment.article == article_key).order(-Comment.hours)

        if user:
            login_logout_url = users.create_logout_url("/single")
        else:
            login_logout_url = users.create_login_url("/single")

        d = {
            'list_data': comments_list,
            'login_logout_url': login_logout_url,
            "user": user,
            "article_data": article

        }
        jinja = jinja2.get_jinja2(app=self.app)

        self.response.write(jinja.render_template("single.html", **d))

    def post(self):
        comment = self.request.get("comment_text", "no data")
        user = users.get_current_user()

        if user:
            login_logout_url = users.create_logout_url("/single")
        else:
            login_logout_url = users.create_login_url("/single")

        nick = ""
        if user:
            nick = user.nickname()

        txt_article_key = self.request.GET["id"]
        article_key = ndb.Key(urlsafe=txt_article_key)
        article = article_key.get()

        comment_data = Comment(text=comment, author=nick, article=article_key)
        comment_data.put()

        time.sleep(0.1)

        list_data = Comment.query(Comment.article == article_key).order(-Comment.hours)

        data = {
            'list_data': list_data,
            'login_logout_url': login_logout_url,
            "user": user,
            "article_data": article
        }
        print (article_key)

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("single.html", **data))


app = webapp2.WSGIApplication([
    ('/single', MainHandler)
], debug=True)
