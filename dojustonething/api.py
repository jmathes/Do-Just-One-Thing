from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from django.utils import simplejson as json
from todolist import ToDoList, AmbiguousUrgencyExeption
import logging


api_funcs = {}


def api(func):
    global api_funcs
    api_funcs[func.__name__] = func


@api
def multiply(a, b):
    return a * b


@api
def addtask(task):
    user = users.get_current_user()
    users_list = ToDoList(user.nickname(), db)
    try:
        users_list.insert(task)
    except AmbiguousUrgencyExeption as e:
        logging.debug(e)
        return {
            'success': False,
            'compare_to': [e.benchmark.task, e.benchmark.urgency],
        }
    logging.debug(users_list)
    return {
        'success': True,
        'top_item': users_list.get_top_item(),
        }


class ApiRequestHandler(webapp.RequestHandler):
    def post(self, func=None):
        self.response.headers['Content-Type'] = "application/json; charset=utf-8"
        args = json.loads(self.request.get('args', '[]'))
        if func in api_funcs:
            response = json.dumps(api_funcs[func](*args))
        # kwargs = self.request.get('kwargs')
        # self.response.out.write(json.dumps(args[0] * args[1]))
        self.response.out.write(response)

application = webapp.WSGIApplication([
     ('/api/([^/]+)', ApiRequestHandler),
     ], debug=True)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)
