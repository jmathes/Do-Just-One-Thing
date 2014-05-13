import logging
import os

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

from userinfo import UserInfo


class MainPage(webapp.RequestHandler):

    def render(self, filename, template_values):
        path = os.path.join(os.path.dirname(__file__), filename)
        self.response.out.write(template.render(path, template_values))

    def get(self):
        user = users.get_current_user()
        user_info = UserInfo.get(user)

        if user is None:
            return self.redirect(users.create_login_url(self.request.uri))
        username = user.nickname()
        logout_url = users.create_logout_url(self.request.uri)

        self.render('index.html', {
            'logout_url': logout_url,
            'username': username,
            'daily_limit': user_info.daily_limit if user_info.daily_limit is not None else "Infinity",
        })


application = webapp.WSGIApplication(
    [
        ('/', MainPage),
    ], debug=True)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)
