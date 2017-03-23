# -*- coding: utf-8 -*-

from google.appengine.ext import ndb

class Message(ndb.Model):
    content = ndb.StringProperty()
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)