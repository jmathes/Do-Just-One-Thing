from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class API(object):
    pass


class ScriptRequestHandler(webapp.RequestHandler):
    def get(self, *args, **kwargs):
        self.response.headers['Content-Type'] = "text/javascript; charset=UTF-8"
        jsfile = open("script/%s.js" % args[0], 'rb')
        js = jsfile.read()
        jsfile.close()
        self.response.out.write(js)

application = webapp.WSGIApplication([
     ('/script/(.*)\.js', ScriptRequestHandler),
     ], debug=True)

if __name__ == "__main__":
    run_wsgi_app(application)
