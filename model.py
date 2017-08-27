from google.appengine.ext import ndb


class Student(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    name_lower = ndb.ComputedProperty(lambda self: self.name.lower())


    def get_student_by_name(self, name_to_search=""):
        student = Student.gql('WHERE name_lower = :1', name_to_search.lower()).get()
        return student

    def get_student_by_id(self, id_to_search=""):
        return self.id


class Instructor(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    name_lower = ndb.ComputedProperty(lambda self: self.name.lower())


    def get_instructor_by_name(self, name_to_search=""):
        instructor = Instructor.gql('WHERE name_lower = :1', name_to_search.lower()).get()
        return instructor

    def get_instructor_by_id(self, id_to_search=""):
        return self.id


class ClassRoom(ndb.Model):
    identity = ndb.IntegerProperty(indexed=True)
    name = ndb.StringProperty(indexed=True)
    name_lower = ndb.ComputedProperty(lambda self: self.name.lower())
    students = ndb.KeyProperty(Student, repeated=True)
    instructors = ndb.KeyProperty(Instructor, repeated=True)

    def get_class_by_name(self, name_to_search=""):
        class_room = ClassRoom.gql('WHERE name_lower = :1', name_to_search.lower()).get()
        if class_room == None:
            return None
        else:
            return class_room

    def get_class_by_id(self, id_to_search=""):
        return self.id
