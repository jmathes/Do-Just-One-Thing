import logging
import os

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users


def todolist_key(username=None):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return db.Key.from_path('ToDoList', username)


class MainPage(webapp.RequestHandler):

    def render(self, filename, template_values):
        path = os.path.join(os.path.dirname(__file__), filename)
        self.response.out.write(template.render(path, template_values))

    def get(self):

        # Ancestor Queries, as shown here, are strongly consistent with the High
        # Replication Datastore. Queries that span entity groups are eventually
        # consistent. If we omitted the ancestor from this query there would be a
        # slight chance that Greeting that had just been written would not show up
        # in a query.
        # greetings = db.GqlQuery("SELECT * "
        #                         "FROM Greeting "
        #                         "WHERE ANCESTOR IS :1 "
        #                         "ORDER BY content DESC LIMIT 10",
        #                         guestbook_key(guestbook_name))
        user = users.get_current_user()

        if user is None:
            return self.redirect(users.create_login_url(self.request.uri))
        username = user.nickname()
        logout_url = users.create_logout_url(self.request.uri)

        self.render('index.html', {
            'logout_url': logout_url,
            'username': username,
            })


application = webapp.WSGIApplication([
     ('/', MainPage),
     ], debug=True)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)
