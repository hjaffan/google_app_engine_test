from google.appengine.ext import ndb


class Student(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    name_lower = ndb.ComputedProperty(lambda self: self.name.lower())


    def get_student_by_name(self, name_to_search=""):
        student = Student.gql('WHERE name_lower = :1', name_to_search.lower()).get()
        return student

    def get_student_id(self, name_to_search=""):
        student = Student.gql('WHERE name_lower = :1', name_to_search.lower()).get()
        if student == None:
            return None
        else:
            return student.id

    def delete_student(self, id):
       conf = ndb.Key('category', int(id)).delete()
       return conf


class Instructor(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    name_lower = ndb.ComputedProperty(lambda self: self.name.lower())


    def get_instructor_by_name(self, name_to_search=""):
        instructor = Instructor.gql('WHERE name_lower = :1', name_to_search.lower()).get()
        return instructor

    def get_instructor_by_id(self, id_to_search=""):
        return self.id

    def delete_instructor(self, id):
       conf = ndb.Key('category', int(id)).delete()
       return conf


class ClassRoom(ndb.Model):
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

    def get_students_in_class_by_name(self, id_to_search):
        student_classes = ClassRoom.gql('WHERE students = :1', id_to_search)
        return student_classes

class Department(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    name_lower = ndb.StringProperty(indexed=True)
    classrooms = ndb.KeyProperty(ClassRoom, repeated=True)

    def get_dept_by_name(self, name_to_search=""):
        department = Department.gql('WHERE name_lower = :1', name_to_search.lower()).get()
        if department == None:
            return None
        else:
            return department