#!/usr/bin/env python
import os
import jinja2
import webapp2
import cgi
from models import Message


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")


class GuestbookHandler(BaseHandler):
    def get(self):
        return self.render_template("guestbook.html")


class MessageHandler(BaseHandler):
    def post(self):
        msg = cgi.escape(self.request.get("content"))
        name = cgi.escape(self.request.get("name"))
        email = cgi.escape(self.request.get("email"))
        msg_save = Message(content=msg, name=name, email=email)
        msg_save.put()
        return self.render_template("sent.html")


class MessagesHandler(BaseHandler):
    def get(self):
        messages = Message.query(Message.deleted == False).fetch()
        params = {
            "messages": messages
        }
        return self.render_template("messages.html", params)


class MessageSingleHandler(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))
        params = {
            "message": message
        }
        return self.render_template("message_single.html", params)


class MessageEditHandler(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))
        params = {
            "message": message
        }
        return self.render_template("message_edit.html", params)

    def post(self, message_id):
        message = Message.get_by_id(int(message_id))
        message.name = cgi.escape(self.request.get("name"))
        message.email = cgi.escape(self.request.get("email"))
        message.content = cgi.escape(self.request.get("content"))
        message.put()
        return self.redirect("/messages")


class MessageDeleteHandler(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))
        params = {
            "message": message
        }
        return self.render_template("delete_message.html", params)

    def post(self, message_id):
        message = Message.get_by_id(int(message_id))
        message.deleted = True
        message.put()
        return self.render_template("message_deleted.html")


class DeletedMessagesHandler(BaseHandler):
    def get(self):
        messages = Message.query(Message.deleted == True).fetch()
        params = {
            "messages": messages
        }
        return self.render_template("deletedmessages.html", params)




app = webapp2.WSGIApplication([
        webapp2.Route('/', MainHandler),
        webapp2.Route('/guestbook', GuestbookHandler),
        webapp2.Route('/message-sent', MessageHandler),
        webapp2.Route('/messages', MessagesHandler),
        webapp2.Route('/<message_id:\d+>', MessageSingleHandler),
        webapp2.Route('/message-edit-<message_id:\d+>', MessageEditHandler),
        webapp2.Route('/message-delete-<message_id:\d+>', MessageDeleteHandler),
        webapp2.Route('/deleted-messages', DeletedMessagesHandler),
], debug=True)
