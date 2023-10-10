from django.db import models
from django.contrib.auth.models import User


class Section(models.Model):
    is_active = models.BooleanField(default=False)
    assistants = models.ManyToManyField(User,
                                        related_name='assistant_sections',
                                        blank=True)
    teacher = models.ForeignKey(to=User,
                                on_delete=models.CASCADE,
                                related_name='teaching_sections')
    students = models.ManyToManyField(User, related_name='student_sections', blank=True)

    class_number = models.CharField(max_length=2)
    lesson = models.CharField(max_length=2)
    group = models.CharField(max_length=2)
    semester = models.CharField(max_length=2)
    faculty = models.CharField(max_length=2)

    class Meta:
        unique_together = [['class_number', 'lesson', 'group', 'semester', 'faculty'], ]

    def display_students(self):
        return ', '.join(x.__str__() for x in self.students.all())

    display_students.short_description = 'Students'

    def display_assistants(self):
        return ', '.join(x.__str__() for x in self.assistants.all())

    display_assistants.short_description = 'Assistants'

    def __str__(self):
        return f'{self.class_number}{self.lesson}{self.group}{self.semester}{self.faculty}'


class Question(models.Model):
    question = models.CharField(max_length=200)

    def __str__(self):
        return self.question


class Evaluation(models.Model):
    title = models.CharField(max_length=100)
    section = models.ForeignKey(Section,
                                on_delete=models.CASCADE,
                                related_name='pending_eval')
    questions = models.ManyToManyField(Question)
    deadline = models.DateTimeField()

    class Meta:
        unique_together = ("section", 'deadline')

    def __str__(self):
        return self.title.__str__()


class Answer(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='answers')

    evaluation = models.ForeignKey(Evaluation,
                                   on_delete=models.PROTECT,
                                   related_name='answers')

    student = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='answers')

    answer = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("evaluation", "student", "question")
