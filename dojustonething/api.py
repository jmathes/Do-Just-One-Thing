from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson


class AddThing(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "application/json; charset=utf-8"
        some_dict = {
            "foo": 1,
            "bar": 2,
        }
        self.response.out.write(simplejson.dumps(some_dict))

application = webapp.WSGIApplication([
     ('/api/add', AddThing),
     ], debug=True)

if __name__ == "__main__":
    run_wsgi_app(application)
