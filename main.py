#!/usr/bin/env python

import os
import jinja2
import webapp2
import random


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
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

    def post(self):
        convert_from = float(self.request.get("convert"))
        operation = self.request.get("operation")
        result = 0

        if operation == "miles to kilometers":
            result = convert_from * 1.609344
            resultlong = str(convert_from)+" miles is "+str(result)+" kilometers"
        elif operation == "kilometers to miles":
            result = convert_from * 0.621371192
            resultlong = str(convert_from)+" kilometers is "+str(result)+" miles"

        params = {"result": result, "resultlong": resultlong}

        return self.render_template("index.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
