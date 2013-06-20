import logging
import random

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
try:
    import json
except ImportError:
    try:
        from django.utils import simplejson as json
    except ImportError:
        import simplejson as json

from todolist import ToDoList, AmbiguousUrgencyExeption
from userinfo import UserInfo

api_funcs = {}


def api(func):
    global api_funcs
    api_funcs[func.__name__] = func


@api
def multiply(a, b):
    return a * b

@api
def did_task(item_id):
    user = users.get_current_user()
    users_list = ToDoList(user.nickname(), db)
    users_list.remove_item(item_id)
    user_info = UserIanfo.get(user)
    new_points = random.randint(0, 1)
    while random.randint(1, 5) > 3 and new_points < 20:
        new_points *= 2
        new_points += random.randint(0, 3)
    user_info.score += new_points
    user_info.save()
    return [users_list.get_top_item(), user_info.score]

@api
def delete_task(item_id):
    user = users.get_current_user()
    users_list = ToDoList(user.nickname(), db)
    users_list.remove_item(item_id)
    user_info = UserInfo.get(user)
    return [users_list.get_top_item(), user_info.score]

@api
def delay_task(item_id):
    user = users.get_current_user()
    users_list = ToDoList(user.nickname(), db)
    users_list.delay_item(item_id)
    return users_list.get_top_item()

@api
def get_score():
    user = users.get_current_user()
    user_info = UserInfo.get(user)
    return user_info.score

@api
def get_next_task():
    user = users.get_current_user()
    users_list = ToDoList(user.nickname(), db)
    return users_list.get_top_item()

@api
def get_next_task_and_score():
    user = users.get_current_user()
    user_info = UserInfo.get(user)
    users_list = ToDoList(user.nickname(), db)
    return [users_list.get_top_item(), user_info.score]

@api
def add_task(todo):
    user = users.get_current_user()
    users_list = ToDoList(user.nickname(), db)
    try:
        users_list.insert(todo)
    except AmbiguousUrgencyExeption, e:
        return {
            'success': False,
            'newthing': todo,
            'benchmark': {
                'task': e.benchmark.task,
                'urgency': e.benchmark.urgency,
            },
        }
    return {
        'success': True,
        'top_item': users_list.get_top_item(),
    }


class ApiRequestHandler(webapp.RequestHandler):
    def post(self, func=None):
        self.response.headers['Content-Type'] = "application/json; charset=utf-8"
        response = self.request.get('args', '[]')
        args = json.loads(response)
        if func in api_funcs:
            response = json.dumps(api_funcs[func](*args))
        # kwargs = self.request.get('kwargs')
        # self.response.out.write(json.dumps(args[0] * args[1]))
        self.response.out.write(response)

application = webapp.WSGIApplication(
    [('/api/([^/]+)', ApiRequestHandler), ], debug=True)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.WARNING)
    run_wsgi_app(application)
