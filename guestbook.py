#!/usr/bin/env python

# Copyright 2016 Google Inc.
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

# [START imports]
import os
import json
import urllib

from google.appengine.ext import ndb

import jinja2
import webapp2
from model import Student, Instructor, ClassRoom
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_NAME = 'default_name'
DEFAULT_CLASS = 'defaut_class'
# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def people_key(people_name=DEFAULT_NAME):
    return ndb.Key('People', people_name)

def class_key(class_name=DEFAULT_NAME):
    return ndb.Key('People', class_name)

# class People(ndb.Model):
#     name = ndb.TextProperty(indexed=True)
#     role = ndb.StringProperty()
#     phone_number = ndb.StringProperty(indexed=False)
#     date = ndb.DateTimeProperty(auto_now_add=True)
#
# class Classroom(ndb.Model):
#     name = ndb.StringProperty()
#     students = ndb.KeyProperty(kind=People, repeated=True)
#     instructor = ndb.StringProperty(indexed=False)

class People(webapp2.RequestHandler):


    def get(self):
        people = {}
        people['students'] = Student.query().fetch(10)
        people['instructors'] = Instructor.query().fetch(10)
        self.response.write([people])


    def post(self):
        class_found = False
        # Grab all the properties that are accepted via the API
        name = self.request.get('name', "")
        role = self.request.get('role', "student")
        class_name = self.request.get('class', "")
        # We first check to see if we are adding an Instructor or Student
        class_room_name = ClassRoom().get_class_by_name(name_to_search=class_name)
        if class_room_name != None:
            class_found = True
            class_room = class_room_name.key.get()
        if role == "instructor":
            instructor = Instructor().get_instructor_by_name(name_to_search=name)
            if instructor != None:
                print("Instructor Found")
                instructor_key = instructor.key
            else:
                new_instructor = Instructor(name=name)
                instructor = new_instructor.put()
                instructor_key = instructor
            if class_found:
                class_room.instructors.append(instructor_key)
                print("Class Already Exists and adding", instructor_key)
            else:
                class_room = ClassRoom(name=class_name, instructors=[instructor_key])
        elif role == "student":
            student = Student().get_student_by_name(name_to_search=name)
            if student != None:
                print("Student Found")
            else:
                new_student = Student(name=name)
                student = new_student.put()
                student_key = student
            if class_found:
                class_room.students.append(student_key)
                print("Class " + "Already Exists and adding", student_key, class_room)
            else:
                class_room = ClassRoom(name=class_name, students=[student_key])
                print("This is a new ClassRoom")
        class_room.put()
        self.redirect('/people')

# This class is used to Get a List of all the class Rooms out there.
#
class ClassRooms(webapp2.RequestHandler):

    def get(self):

        self.response.write([p.to_dict() for p in ClassRoom.query().fetch(10)])


# [START app]
app = webapp2.WSGIApplication([
    ('/people', People),
    ('/class', ClassRooms)
], debug=True)
# [END app]
