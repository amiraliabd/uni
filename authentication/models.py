from django.db import models
from django.contrib.auth.models import User


User.add_to_class('national_id', models.CharField(
    max_length=10, blank=False, null=False, unique=True
))


def display_student_sections(self):
    return ', '.join(ss.__str__() for ss in self.student_sections.filter(
        is_active=True
    ).all())


User.add_to_class('display_student_sections', display_student_sections)
User.add_to_class('display_student_sections.short_description', 'Student Sections')


def display_assistant_sections(self):
    return ', '.join(a.__str__() for a in self.assistant_sections.filter(
        is_active=True
    ).all())


User.add_to_class('display_assistant_sections', display_assistant_sections)
User.add_to_class('display_assistant_sections.short_description', 'Assistant Sections')


def display_teaching_sections(self):
    return ', '.join(ts.__str__() for ts in self.teaching_sections.filter(
        is_active=True
    ).all())


User.add_to_class('display_teaching_sections', display_teaching_sections)
User.add_to_class('display_teaching_sections.short_description', 'Teaching Sections')


class GolestanUser(models.Model):
    student_number = models.CharField(max_length=9, null=False, blank=False, unique=True)
    national_id = models.CharField(max_length=10, null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
