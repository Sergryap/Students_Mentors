class Student:
    students = []

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        Student.students.append(self)

    @property
    def middle_grade(self):
        """
        метод для определения средней оценки
        """
        count = 0
        total = 0
        for j in self.grades.values():
            for i in j:
                count += 1
                total += i
        return round(total / count, 1)

    def __str__(self):
        return f'''
Имя: {self.name}
Фамилия: {self.surname}
Средняя оценка за домашние задания: {self.middle_grade}
Курсы в процессе изучения: {', '.join(self.courses_in_progress)}
Завершенные курсы: {', '.join(self.finished_courses)}
'''

    def rate_hw(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def __eq__(self, other):  # проверка на равенство
        if type(self) == type(other):
            return self.middle_grade == other.middle_grade

    def __lt__(self, other):  # сравнение на меньше
        if type(self) == type(other):
            return self.middle_grade < other.middle_grade

    def __le__(self, other):  # проверка на меньше или равно
        return self == other or self < other


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor, Student):
    """
    Класс лекторов.
    Для определения методов middle_grade и методов сравнения
    в качестве второго родителя принят класс Student
    """
    lecturers = []

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        Lecturer.lecturers.append(self)

    def __str__(self):
        return f'''
Имя: {self.name}
Фамилия: {self.surname}
Средняя оценка за лекции: {self.middle_grade}
'''
    rate_hw = property(doc='(!) Disallowed inherited')
    add_courses = property(doc='(!) Disallowed inherited')


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        return f'''Имя: {self.name}
Фамилия: {self.surname}
'''

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


def total_middle_grade(course, peoples):
    """
    Средняя оценка по всем д.з. студентов или лекторам по заданному курсу
    """
    count = 0
    total = 0
    if peoples == Student.students:
        row = 'по всем домашним заданиям cтудентов'
    else:
        row = 'по всем лекторам'

    for people in peoples:
        if course in people.grades:
            for grade in people.grades[course]:
                total += grade
                count += 1
    return f'Средняя оценка {row} по курсу "{course}": {round(total / count, 1)}'


# Полевые испытания

student1 = Student('Сергей', 'Агапов', 'муж')
student2 = Student('Светлана', 'Соколова', 'жен')
lector1 = Lecturer('Ирина', 'Сергеевна')
lector2 = Lecturer('Александр', 'Владимирович')
reviewer1 = Reviewer('Сергей', 'Николаевич')
reviewer2 = Reviewer('Антонина', 'Васильевна')

student1.courses_in_progress += ['Python', 'Java']
student1.finished_courses += ['Введение в программирование']
student2.courses_in_progress += ['Python', 'Java', 'Git']
student2.finished_courses += ['Введение в программирование']
lector1.courses_attached += ['Python', 'Java']
lector2.courses_attached += ['Python', 'Java', 'Git']
reviewer1.courses_attached += ['Python', 'Java']
reviewer2.courses_attached += ['Python', 'Java', 'Git']

reviewer1.rate_hw(student1, 'Python', 8)
reviewer1.rate_hw(student1, 'Java', 10)
reviewer2.rate_hw(student2, 'Python', 6)
reviewer2.rate_hw(student2, 'Java', 7)
reviewer2.rate_hw(student2, 'Git', 10)

student1.rate_hw(lector1, 'Python', 8)
student1.rate_hw(lector1, 'Java', 8)
student2.rate_hw(lector1, 'Python', 9)
student2.rate_hw(lector1, 'Java', 7)

student1.rate_hw(lector2, 'Python', 6)
student1.rate_hw(lector2, 'Java', 10)
student2.rate_hw(lector2, 'Python', 9)
student2.rate_hw(lector2, 'Java', 10)
student2.rate_hw(lector2, 'Git', 9)

print(student1)
print(student2)

print(lector1)
print(lector2)
print(reviewer1)
print(reviewer2)

print(total_middle_grade('Python', Student.students))
print(total_middle_grade('Java', Student.students))
print(total_middle_grade('Git', Lecturer.lecturers))
print(total_middle_grade('Java', Lecturer.lecturers))

print(lector1 < lector2)
print(student1 == student2)
