import webapp2
from webapp2_extras import jinja2

from webapp2_extras.users import users

from handlers.models import Comment


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        print ("NEWS")
        list_data = Comment.query().order(-Comment.hours)

        if user:
            login_logout_url = users.create_logout_url("/single")
        else:
            login_logout_url = users.create_login_url("/single")

        d = {
            'list_data': list_data,
            'login_logout_url' : login_logout_url,
            "user": user
        }
        jinja = jinja2.get_jinja2(app=self.app)

        self.response.write(jinja.render_template("single.html", **d))

    def post(self):
        comment = self.request.get("comment_text", "no data")
        user = users.get_current_user()

        nick = ""
        if user:
            nick = user.nickname()

        comment_data = Comment(text=comment, author=nick)
        comment_data.put()

        list_data = Comment.query().order(-Comment.hours)

        data = {
            'list_data': list_data
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("single.html", **data))


app = webapp2.WSGIApplication([
    ('/single', MainHandler)
], debug=True)
