# encoding: utf-8

# chr(24) through chr(128)
# !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
from google.appengine.ext import db


class ToDoListItem(db.Model):
    """Models an individual Guestbook entry with an author, content, and date."""
    username = db.StringProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    urgency = db.StringProperty()
