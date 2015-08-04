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

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)




class UserModel(ndb.Model):
    currentUser = ndb.StringProperty(required= True)
    text = ndb.TextProperty()


class Events(ndb.Model):
    encounter = ndb.StringProperty()
    outcome = ndb.StringProperty()



event_1 = Events(encounter = "Your bag caught on fire. Oops.", outcome = "All of your supplies are destroyed.")
event_2 = Events(encounter = "You saw a bus", outcome = "You know what a bus looks like")
event_3 = Events(encounter = "You see your brither get shot.", outcome = "You are sad.")
event_4 = Events(encounter = "You find a penny.", outcome = "Gain 1 cent.")
event_5 = Events(encounter = "The cops found and surrounded you.", outcome = "GAME OVER")
event_6 = Events(encounter = "You found a cute kitty!", outcome = "You realize you are allergic.")
event_7 = Events(encounter = "You find a cat!", outcome = "Now you look like the Joker. Congrats..")
event_8 = Events(encounter = "You run into your old friend Riccardo!", outcome = "Lose twenty dollars.")
event_9 = Events(encounter = "Hey look, it is Manny! He has got a riddle for you.", outcome = "Too bad you SUCK at riddles.")
event_10 = Events(encounter = "You find a ping pong paddle. ", outcome = "The air reeks of Liam...")
event_11 = Events(encounter = "You see your brother on the run from the police! ", outcome = "You immediately run the opposite direction in fear of being mistaken for him")
event_12 = Events(encounter = "A tree falls down!", outcome= "You can only go North.")
event_list = [event_1, event_2, event_3, event_9]
ending_events = [event_4, event_5]
directional_events = [event_12]

class MainHandler(webapp2.RequestHandler):
    def get(self):
        login_template = JINJA_ENVIRONMENT.get_template('templates/login.html')
        user = users.get_current_user()
        welcome = { "greeting": "Hey welcome to the game of life.", "state_user":"Your username is: ","user": user}
        if user:
            self.response.write(login_template.render(welcome))
            user = UserModel(currentUser=user.user_id(), text="HEYO")
            user.put()
        else:
            self.redirect(users.create_login_url(self.request.uri))


class GameHandler(webapp2.RequestHandler):
    def get(self):
        start_text = "Your identical twin has set you up. He told you to meet him downtown at the Board of Trade building, and when you arrive you realize that he has robbed the commissioners and is using you as a doppelganger. You don't realize this until you see the news in a store window nearby announcing the breaking news. Miraculously, you realize that you haven't been caught yet because the police think that the twin is still in the building and that he is wearing all black, but you are about a block away and wearing pastel colors. You have to get away from the scene quickly or you will have to pay a pretty bad price. Without a second thought, you decide you should run somewhere. To the north is Madison Street, to the west is a deserted alley, to the east is Wacker Drive, and to the south is Monroe Street."
        beginning = {"story_text": start_text}
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.out.write(template.render(beginning))

    def post(self):
        if len(event_list) == 0:
            i = random.randint(0,(len(ending_events)-1))

            user_direction = self.request.get('user_direction')
            story1 = "This is what happens when you go " + user_direction.lower() + ":"
            user_direction_template_vars = {"direction": user_direction, "story_text": story1, "event_encounter": ending_events[i].encounter, "event_outcome": ending_events[i].outcome }
            template = JINJA_ENVIRONMENT.get_template('templates/index.html')
            self.response.out.write(template.render(user_direction_template_vars))
        else:

            i = random.randint(0,(len(event_list)-1))
            user_direction = self.request.get('user_direction')
            story1 = "This is what happens when they go " + user_direction.lower() + ":"
            if event_list[i]==event_9:
                user_direction_template_vars= {"direction": user_direction, "story_text": story1, "event_encounter": event_list[i].encounter, "event_outcome": event_list[i].outcome }
                template = JINJA_ENVIRONMENT.get_template('templates/barricade.html')
                self.response.out.write(template.render(user_direction_template_vars))
            else:
                user_direction_template_vars = {"direction": user_direction, "story_text": story1, "event_encounter": event_list[i].encounter, "event_outcome": event_list[i].outcome }
                event_list.remove(event_list[i])
                template = JINJA_ENVIRONMENT.get_template('templates/index.html')
                self.response.out.write(template.render(user_direction_template_vars))
                # self.response.out.write("You went: " + user_input_loc)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/game', GameHandler)
], debug=True)
