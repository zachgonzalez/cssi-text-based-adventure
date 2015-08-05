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

event_2 = Events(encounter = "You saw a bus.", outcome = "CONGRATULATIONS!! You know what a bus looks like")
event_3 = Events(encounter = "You see your brother get shot.", outcome = "You're sad.")

event_4 = Events(encounter = "You find a penny.", outcome = "Gain 1 cent.")
event_5 = Events(encounter = "The cops found and surrounded you.", outcome = "GAME OVER")

event_6 = Events(encounter = "You found a cute kitty!", outcome = "You realize you are allergic.")

event_7 = Events(encounter = "You find a cat!", outcome = "Now you look like the Joker. Congrats..")
event_8 = Events(encounter = "You run into your old friend Riccardo!", outcome = "Lose twenty dollars.")
event_9 = Events(encounter = "You look up to see that the cops have barricaded the street.", outcome = "What would you like to do?")
event_10 = Events(encounter = "You find a ping pong paddle. ", outcome = "The air reeks of Liam...")
event_11 = Events(encounter = "You see your brother on the run from the police! ", outcome = "You immediately run the opposite direction in fear of being mistaken for him")
event_12 = Events(encounter = "A tree falls down!", outcome= "You can only go North.")

event_13 = Events(encounter = "You loook up to see that the cops have barricaded the street. What would you like to do?")
event_list = [event_1, event_2, event_3, event_13, event_9]

ending_events = [event_4, event_5]
directional_events = [event_12]


class MainHandler(webapp2.RequestHandler):
      def get(self):
        user = users.get_current_user()
        if user:
            username = user.nickname()
            signoutlink = users.create_logout_url('/')
            signout = ('(<a href="%s">sign out</a>)' %(signoutlink))
            #Damerrick's additional code. Needed?
            home_page = JINJA_ENVIRONMENT.get_template('templates/login.html')
            start= {"username": user.nickname(), "signoutlink": users.create_logout_url('/'),
            "greeting2":'Welcome!', "state_user": "Your username is: "}
            self.response.out.write(home_page.render(start))
            #End of additional code.
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %(users.create_login_url('/')))

            self.response.out.write('<html><body>%s</body></html>' %(greeting))

class GameHandler(webapp2.RequestHandler):

    def get(self):
        start_text = "Your identical twin has set you up. He told you to meet him downtown at the Board of Trade building, and as you are arriving you realize that he has robbed the commissioners and is using you as a doppelganger. You don't realize this until you see the news in a store window nearby announcing the breaking news. Miraculously, you realize that you haven't been caught yet because the police think that the twin is still in the building and that he is wearing all black, but you are about a block away and wearing pastel colors. You have to get away from the scene quickly or you will have to pay a pretty bad price. Without a second thought, you decide you should run somewhere. To the north is Madison Street, to the west is a deserted alley, to the east is Wacker Drive, and to the south is Monroe Street."
        beginning = {"story_text": start_text}
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.out.write(template.render(beginning))

    def post(self):

        if len(event_list) == 0:
            i = random.randint(0,(len(ending_events)-1))

            user_direction = self.request.get('user_direction')
            story1 = "This is what happens when you go " + user_direction.lower() + ":"
            user_direction_template_vars = {"direction": user_direction, "story_text": story1, "event_encounter": ending_events[i].encounter, "event_outcome": ending_events[i].outcome }
            template = JINJA_ENVIRONMENT.get_template('templates/death.html')
            self.response.out.write(template.render(user_direction_template_vars))
        else:
            i = random.randint(0,(len(event_list)-1))
            user_direction = self.request.get('user_direction')
            story1 = "You went " + user_direction.lower() + ":"

            if event_list[i] == event_13:
                user_direction_template_vars = {"direction": user_direction, "story_text": story1, "event_encounter": event_list[i].encounter, "event_outcome": event_list[i].outcome }
                event_list.remove(event_list[i])
                template = JINJA_ENVIRONMENT.get_template('templates/barricade.html')
                self.response.out.write(template.render(user_direction_template_vars))

            elif event_list[i]==event_9:
                user_direction_template_vars= {"direction": user_direction, "story_text": story1, "event_encounter": event_list[i].encounter, "event_outcome": event_list[i].outcome }
                event_list.remove(event_list[i])
                template = JINJA_ENVIRONMENT.get_template('templates/barricade.html')
                self.response.out.write(template.render(user_direction_template_vars))
            else:
                user_direction_template_vars = {"direction": user_direction, "story_text": story1, "event_encounter": event_list[i].encounter, "event_outcome": event_list[i].outcome }
                event_list.remove(event_list[i])
                template = JINJA_ENVIRONMENT.get_template('templates/index.html')
                self.response.out.write(template.render(user_direction_template_vars))
                # self.response.out.write("You went: " + user_input_loc)

class BarricadeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('STOP TRYING TO SKIP AHEAD!!')
    def post(self):
        # if len(event_list) == 0:
        #     i = random.randint(0,(len(ending_events)-1))
        #
        #     user_direction = self.request.get('user_direction')
        #     story1 = "This is what happens when you go " + user_direction.lower() + ":"
        #     user_direction_template_vars = {"direction": user_direction, "story_text": story1, "event_encounter": ending_events[i].encounter, "event_outcome": ending_events[i].outcome }
        #     template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        #     self.response.out.write(template.render(user_direction_template_vars))
        start_text = "You chose to hide in the dumpster and, luckily, the store owner moved it to the other side of the street. You made it past the cops and into a safe alley, but you cannot stay for long. Where would you like to go from here."
        beginning = {"story_text": start_text}
        template = JINJA_ENVIRONMENT.get_template('templates/barricade_results.html')
        self.response.out.write(template.render(beginning))

class DeathHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/death.html')
        self.response.out.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/game', GameHandler),
    ('/barricade-results', BarricadeHandler),
    ('/death', DeathHandler)
], debug=True)
