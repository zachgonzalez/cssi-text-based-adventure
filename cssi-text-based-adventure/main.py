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



event_1 = Events(encounter = "A creepy guy catcalls you.", outcome = "How rude.")

event_2 = Events(encounter = "You saw a bus.", outcome = "CONGRATULATIONS!! You know what a bus looks like.")
event_3 = Events(encounter = "A taxi comes by and splashes mud on your clothes, ruining the pastel look.", outcome = "You now look even more like your brother!")

event_4 = Events(encounter = "Your mom comes and picks you up.", outcome = "Nap time!")
event_5 = Events(encounter = "The cops found and surrounded you.", outcome = "")

event_6 = Events(encounter = "A fire alarm goes off in a nearby building, occupying some of the police looking for your brother.", outcome = "Your journey is safe... for now.")

event_7 = Events(encounter = "Traffic signals are out all throughout the city.", outcome = "Looks like catching a cab won't be an option.")
event_8 = Events(encounter = "You run into your old friend Riccardo!", outcome = "Lose twenty dollars.")
event_9 = Events(encounter = "You run into your brother while looking for a hiding place. He seems scared and confused.", outcome = "What would you like to do?")
event_10 = Events(encounter = "A television crew is filming accross the street.", outcome = "You think about taking a shot at fame and becoming an extra, but you realize you must keep moving.")
event_11 = Events(encounter = "Looks as though the cops have shutdown public transportation to help find the thief.", outcome = "Walking seems to be your only option.")
event_12 = Events(encounter = "You walk past the Trump Tower.", outcome= "You spit in its general direction.")

event_13 = Events(encounter = "You loook up to see that the cops have barricaded the street.", outcome = "What would you like to do?")
event_list = [event_1,
              event_2,
              event_3,
              event_6,
              event_7,
              event_8,
              event_9,
              event_10,
              event_11,
              event_12,
              event_13
              ]

ending_events = [event_4, event_5]

user_score = 0



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
            global user_score
            user_direction = self.request.get('user_direction')
            # story1 = "This is what happens when you go " + user_direction.lower() + ":"
            user_direction_template_vars = {"direction": user_direction, "event_encounter": ending_events[i].encounter, "event_outcome": ending_events[i].outcome, "user_score": user_score }
            if ending_events[i] != event_4:
                template = JINJA_ENVIRONMENT.get_template('templates/death.html')
                self.response.out.write(template.render(user_direction_template_vars))
                event_list.append(event_1)
                event_list.append(event_2)
                event_list.append(event_3)
                event_list.append(event_6)
                event_list.append(event_7)
                event_list.append(event_8)
                event_list.append(event_9)
                event_list.append(event_10)
                event_list.append(event_11)
                event_list.append(event_12)
                event_list.append(event_13)
                global user_score
                user_score = 0
            else:
                template = JINJA_ENVIRONMENT.get_template('templates/victory.html')
                self.response.out.write(template.render(user_direction_template_vars))
                event_list.append(event_1)
                event_list.append(event_2)
                event_list.append(event_3)
                event_list.append(event_6)
                event_list.append(event_7)
                event_list.append(event_8)
                event_list.append(event_9)
                event_list.append(event_10)
                event_list.append(event_11)
                event_list.append(event_12)
                event_list.append(event_13)
                global user_score
                user_score = 0

        else:
            i = random.randint(0,(len(event_list)-1))
            user_direction = self.request.get('user_direction')
            story1 = "Your choice was " + user_direction.capitalize() + ":"
            global user_score
            user_score += 1


            if event_list[i] == event_13:
                user_direction_template_vars = {"direction": user_direction, "story_text": story1, "event_encounter": event_list[i].encounter, "event_outcome": event_list[i].outcome, "user_score":user_score }
                event_list.remove(event_list[i])
                template = JINJA_ENVIRONMENT.get_template('templates/barricade.html')
                self.response.out.write(template.render(user_direction_template_vars))

            elif event_list[i]==event_9:
                user_direction_template_vars= {"direction": user_direction, "story_text": story1, "event_encounter": event_list[i].encounter, "event_outcome": event_list[i].outcome, "user_score":user_score }
                event_list.remove(event_list[i])
                template = JINJA_ENVIRONMENT.get_template('templates/findbrother.html')
                self.response.out.write(template.render(user_direction_template_vars))

            else:
                user_direction_template_vars = {"direction": user_direction, "story_text": story1, "event_encounter": event_list[i].encounter, "event_outcome": event_list[i].outcome, "user_score":user_score }
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
        if self.request.get('user_direction') == 'hide':
            global user_score
            user_score += 1
            start_text = "You chose to hide in the dumpster and, luckily, the store owner moved it to the other side of the street. You made it past the cops and into a safe alley, but you cannot stay for long. Where would you like to go from here?"
            beginning = {"story_text": start_text, "user_score": user_score}
            template = JINJA_ENVIRONMENT.get_template('templates/barricade_results.html')
            self.response.out.write(template.render(beginning))
        else:
            start_text = "Looks like you chose the wrong option. You are now dead. Oops..."
            beginning = {"story_text": start_text, "user_score": user_score}
            template = JINJA_ENVIRONMENT.get_template('templates/death.html')
            self.response.out.write(template.render(beginning))
            for event in event_list:
                event_list.remove(event)
            event_list.append(event_1)
            event_list.append(event_2)
            event_list.append(event_3)
            event_list.append(event_6)
            event_list.append(event_7)
            event_list.append(event_8)
            event_list.append(event_9)
            event_list.append(event_10)
            event_list.append(event_11)
            event_list.append(event_12)
            event_list.append(event_13)
            global user_score
            user_score = 0

class BrotherHandler(webapp2.RequestHandler):
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
        if self.request.get('user_direction') == 'hide':
            global user_score
            user_score += 1
            start_text = "You let your brother go. You may never see him again. That's pretty sad. Although, he did try to get you arrested so I guess all is fair... But the police are still looking, so you need to get moving."
            beginning = {"story_text": start_text, "user_score": user_score}
            template = JINJA_ENVIRONMENT.get_template('templates/brother_results.html')
            self.response.out.write(template.render(beginning))
        else:
            start_text = "Looks like you chose the wrong option. You are now dead. Oops..."
            beginning = {"story_text": start_text,"user_score": user_score}
            template = JINJA_ENVIRONMENT.get_template('templates/death.html')
            self.response.out.write(template.render(beginning))
            for event in event_list:
                event_list.remove(event)
            event_list.append(event_1)
            event_list.append(event_2)
            event_list.append(event_3)
            event_list.append(event_6)
            event_list.append(event_7)
            event_list.append(event_8)
            event_list.append(event_9)
            event_list.append(event_10)
            event_list.append(event_11)
            event_list.append(event_12)
            event_list.append(event_13)
            global user_score
            user_score = 0

class DeathHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/death.html')
        self.response.out.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/game', GameHandler),
    ('/barricaderesults', BarricadeHandler),
    ('/brotherresults', BrotherHandler),
    ('/death', DeathHandler)
], debug=True)
