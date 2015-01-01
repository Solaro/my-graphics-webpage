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
# name: Terrence Kuo
# run locally: dev.appserver.py .


import os
import webapp2
import jinja2
from random import randint

# concat the current directory with the templates directory
# the templates directory contains all the the templates (html files)
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# create a jinja2 environment from the templates directory
# when we render templates, jinja is going to look for templates in the template_dir
jinja2_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
	# sends information to the browser
	# the *a is used to pass in a tuple. a stands for arguements
	# the **kw is used to pass in a dictionary. kw stands for keywords
	def write(self, *a, **kw):
		self.response.write(*a, **kw);

	def render_str(self, template, **params):
		# uses the created jinja2 enivronment and loads the template which is a html file
		t = jinja2_env.get_template(template)
		# provides the template (html file) with parameters
		# returns a string
		return t.render(params);

	def render(self, template, **kw):
		# calls redner_str and wraps it in self.write which actually sends it to browser
		self.write(self.render_str(template, **kw));

class MainHandler(Handler):
	def get(self):
		self.render("front.html", error = "");

	def post(self):
		graphic = self.request.get("graphic")

		if graphic == "box":
			self.redirect("/box_spinning");
		elif graphic == "sphere":
			self.redirect("/sphere_spinning");
		elif graphic == "sphere-wire":
			self.redirect("/sphere_wire");
		elif graphic == "suprise-me":
			random = randint(1,3);
			if random == 1:
				self.redirect("/box_spinning");
			elif random == 2:
				self.redirect("/sphere_spinning");
			else:
				self.redirect("/sphere_wire");
		else:
			error = "You didn't pick something to display!"
			self.render("front.html", error = error);

class BoxHandler(Handler):
	def get(self):
		self.render("box_spin.html");

class SphereHandler(Handler):
	def get(self):
		self.render("sphere_spin.html");

class SphereWireHandler(Handler):
	def get(self):
		self.render("wire_sphere.html")
		

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/box_spinning', BoxHandler),
    ('/sphere_spinning', SphereHandler),
    ('/sphere_wire', SphereWireHandler),
], debug=True)
