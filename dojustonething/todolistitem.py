# encoding: utf-8
from google.appengine.ext import db


class ToDoListItem(db.Model):
    """Models an individual Guestbook entry with an author, task, and date."""
    username = db.StringProperty()
    task = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    urgency = db.FloatProperty()

    def __repr__(self):
        return "%s-%s-%s: %s" % (
            self.username,
            self.date,
            self.urgency,
            self.task)
