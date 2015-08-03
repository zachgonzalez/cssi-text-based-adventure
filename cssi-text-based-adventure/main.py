#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

user_input_loc= "North"

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Welcome to our game! Click here to play!")

class GameHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.out.write(template.render())
    def post(self):
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.out.write(template.render(user_input_loc))
        # self.response.out.write("You went: " + user_input_loc)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/game', GameHandler)
], debug=True)
