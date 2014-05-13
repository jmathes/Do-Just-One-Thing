# encoding: utf-8
from google.appengine.ext import db
import logging


class UserInfo(db.Model):
    """Models an individual User's do-just-one-thing info"""
    user_id = db.StringProperty()
    signup_date = db.DateTimeProperty(auto_now_add=True)
    score = db.IntegerProperty()
    daily_limit = db.IntegerProperty()

    @classmethod
    def get(cls, user_id):
        if not isinstance(user_id, basestring):
            user_id = user_id.user_id()
        user_infos = list(cls.gql("WHERE user_id = :1", user_id))
        if len(user_infos) == 0:
            user_info = UserInfo(user_id=user_id, score=0, daily_limit=3)
            user_info.save()
        else:
            user_info = user_infos[0]
        return user_info
