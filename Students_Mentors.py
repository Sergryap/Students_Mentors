class MembersTraining:
    """
    Класс общих методов и свойств
    """

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        if type(self) == Student or type(self) == Lecturer:
            self.grades = {}
        if type(self) == Student:
            self.courses_in_progress = []
        if isinstance(self, Mentor):
            self.courses_attached = []

    @property
    def middle_grade(self):
        """
        метод (свойство) для определения средней оценки
        """
        gen = (i for j in self.grades.values() for i in j)
        count, total = 0, 0
        for i in gen:
            count += 1
            total += i
        return round(total / count, 1)

    def __eq__(self, other):
        """
        проверка на равенство
        """
        if type(self) == Reviewer:
            return 'Не поддерживается сравнение'
        elif type(self) == type(other):
            return self.middle_grade == other.middle_grade

    def __lt__(self, other):
        """
        проверка на меньше
        """
        if type(self) == Reviewer:
            return 'Не поддерживается сравнение'
        elif type(self) == type(other):
            return self.middle_grade < other.middle_grade

    def __le__(self, other):
        """
        проверка на меньше или равно
        """
        return self == other or self < other

    def __rate_true(self, people, course):
        """
        Проверка к методу rate_hw
        """
        if type(self) == Student:
            return isinstance(people,
                              Lecturer) and course in self.courses_in_progress and course in people.courses_attached
        elif type(self) == Reviewer:
            return isinstance(people,
                              Student) and course in self.courses_attached and course in people.courses_in_progress
        else:
            print('Нет прав для проставления оценки')

    def rate_hw(self, people, course, grade):
        """
        метод проставления оценок студентам или лекторам
        """
        if self.__rate_true(people, course):
            if course in people.grades:
                people.grades[course] += [grade]
            else:
                people.grades[course] = [grade]


class Student(MembersTraining):
    students = []

    def __init__(self, name, surname, gender):
        super().__init__(name, surname, gender)
        self.finished_courses = []
        Student.students.append(self)

    def __str__(self):
        return f'''
Имя: {self.name}
Фамилия: {self.surname}
Средняя оценка за домашние задания: {self.middle_grade}
Курсы в процессе изучения: {', '.join(self.courses_in_progress)}
Завершенные курсы: {', '.join(self.finished_courses)}
'''

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)


class Mentor(MembersTraining):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname, gender)


class Lecturer(Mentor):
    """
    Класс лекторов
    """
    lecturers = []

    def __init__(self, name, surname, gender):
        super().__init__(name, surname, gender)
        Lecturer.lecturers.append(self)

    def __str__(self):
        return f'''
Имя: {self.name}
Фамилия: {self.surname}
Средняя оценка за лекции: {self.middle_grade}
'''


class Reviewer(Mentor):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname, gender)

    def __str__(self):
        return f'''Имя: {self.name}
Фамилия: {self.surname}
'''


def total_middle_grade(course, peoples):
    """
    Средняя оценка по всем д.з. студентов или лекторам по заданному курсу
    """
    if peoples == Student.students:
        row = 'по всем домашним заданиям cтудентов'
    else:
        row = 'по всем лекторам'

    count, total = 0, 0
    for people in peoples:
        if course in people.grades:
            for grade in people.grades[course]:
                total += grade
                count += 1
    return f'Средняя оценка {row} по курсу "{course}": {round(total / count, 1)}'


# Полевые испытания

student1 = Student('Сергей', 'Агапов', 'муж')
student2 = Student('Светлана', 'Соколова', 'жен')
lector1 = Lecturer('Ирина', 'Сергеевна', 'жен')
lector2 = Lecturer('Александр', 'Владимирович', 'муж')
reviewer1 = Reviewer('Сергей', 'Николаевич', 'муж')
reviewer2 = Reviewer('Антонина', 'Васильевна', 'жен')

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
print(reviewer1 == reviewer2)
lector1.rate_hw(student2, 'Git', 10)
