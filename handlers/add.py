import webapp2
from webapp2_extras import jinja2

from webapp2_extras.users import users

from handlers.models import Comment, Article


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        print ("NEWS")
        list_data = Comment.query().order(-Comment.hours)

        if user:
            login_logout_url = users.create_logout_url("/add")
        else:
            login_logout_url = users.create_login_url("/add")

        d = {
            'list_data': list_data,
            'login_logout_url': login_logout_url,
            "user": user
        }
        jinja = jinja2.get_jinja2(app=self.app)

        self.response.write(jinja.render_template("add.html", **d))

    def post(self):
        content = self.request.get("article_text", "no data")
        article_title = self.request.get("article_title", "no data")
        img_article = self.request.get("img_article", "")
        user = users.get_current_user()

        if user:
            login_logout_url = users.create_logout_url("/add")
        else:
            login_logout_url = users.create_login_url("/add")

        nick = ""
        if user:
            nick = user.nickname()

        article_data = Article(title=article_title, content=content, author=nick, image=img_article)
        article_data.put()

        list_data = Article.query().order(-Article.hours)

        data = {
            'list_data': list_data,
            'login_logout_url': login_logout_url,
            "user": user
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("add.html", **data))


app = webapp2.WSGIApplication([
    ('/add', MainHandler)
], debug=True)
