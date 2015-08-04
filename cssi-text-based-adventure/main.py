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
from google.appengine.ext import ndb

import random
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)





class Events(ndb.Model):
    encounter = ndb.StringProperty()
    outcome = ndb.StringProperty()

class Directional_events(ndb.Model):
    encounter = ndb.StringProperty()
    directional_limitation = ndb.StringProperty()

event_1 = Events(encounter = "Your bag caught on fire. Oops.", outcome = "All of your supplies are destroyed.")
event_2 = Events(encounter = "You saw a bus", outcome = "You know what a bus looks like")
event_3 = Events(encounter = "You see your brither get shot.", outcome = "You're sad.")
event_4 = Events(encounter = "You find a penny.", outcome = "Gain 1 cent.")

directional_event_1 = Directional_events(encounter = "A tree falls down!", directional_limitation= "You can only go North.")
event_list = [event_1, event_2]


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Welcome to our game! Click here to play!")

class GameHandler(webapp2.RequestHandler):
    def get(self):
        start_text = "Your identical twin has set you up. He told you to meet him downtown at the Board of Trade building, and when you arrive you realize that he has robbed the commissioners and is using you as a doppelganger. You don't realize this until you see the news in a store window nearby announcing the breaking news. Miraculously, you realize that you haven't been caught yet because the police think that the twin is still in the building and that he is wearing all black, but you are about a block away and wearing pastel colors. You have to get away from the scene quickly or you will have to pay a pretty bad price. Without a second thought, you decide you should run somewhere. To the north is Madison Street, to the west is a deserted alley, to the east is Wacker Drive, and to the south is Monroe Street."
        beginning = {"story_text": start_text}
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.out.write(template.render(beginning))

    def post(self):
        i = random.randint(0,1)
        user_direction = self.request.get('user_direction')
        story1 = "This is what happens when they go " + user_direction.lower() + ":"
        user_direction_template_vars = {"direction": user_direction, "story_text": story1, "event_encounter": event_list[i].encounter, "event_outcome": event_list[i].outcome }


        if user_direction.lower() == 'north' or user_direction.lower() == 'south' or user_direction.lower() == 'east' or user_direction.lower() == 'west':

            template = JINJA_ENVIRONMENT.get_template('templates/index.html')
            self.response.out.write(template.render(user_direction_template_vars))
            # self.response.out.write("You went: " + user_input_loc)
        else:
            self.response.out.write("Please enter a valid command")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/game', GameHandler)
], debug=True)
