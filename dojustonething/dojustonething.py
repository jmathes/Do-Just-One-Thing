from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
# import cgi  # for cgi.escape(<user input>
import os
import urllib
# import logging
# logging.getLogger().setLevel(logging.DEBUG)
# logging.debug("Hello")


class Greeting(db.Model):
    """Models an individual Guestbook entry with an author, content, and date."""
    author = db.StringProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)


def guestbook_key(guestbook_name=None):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return db.Key.from_path('Butthole', guestbook_name or 'default_guestbook')


class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')
        guestbook_name = self.request.get('guestbook_name')

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
        greetings = Greeting.gql("WHERE ANCESTOR IS :ancestor "
                                "ORDER BY content DESC LIMIT 10",
                                ancestor=guestbook_key(guestbook_name))

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))


class Guestbook(webapp.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each greeting is in
        # the same entity group. Queries across the single entity group will be
        # consistent. However, the write rate to a single entity group should
        # be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name')
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()

        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))


if __name__ == "__main__":
    application = webapp.WSGIApplication(
         [('/', MainPage),
          ('/sign', Guestbook)],
         debug=True)
    run_wsgi_app(application)
