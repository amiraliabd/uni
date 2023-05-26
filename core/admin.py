from django.contrib import admin
from .models import (
    Section,
    Question,
    PendingEvaluation,
)


class StudentSectionInline(admin.TabularInline):
    model = Section.students.through
    verbose_name = 'Section Student'


class AssistantSectionInline(admin.TabularInline):
    model = Section.assistants.through
    verbose_name = 'Section Assistant'


class SectionAdmin(admin.ModelAdmin):
    list_display = ('is_active',
                    'class_number',
                    'lesson',
                    'group',
                    'semester',
                    'faculty',
                    'teacher',
                    'display_assistants',
                    'display_students',
                    )
    readonly_fields = ('assistants', 'students')
    list_filter = ('is_active', )
    search_fields = ('class_number', 'lesson', 'group', 'semester', 'faculty')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'comment')
    search_fields = ('question', )
    list_filter = ('comment', )


class PendingEvalAdmin(admin.ModelAdmin):
    list_display = ('question', 'section')
    search_fields = ('question', 'section')


admin.site.register(Section, SectionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(PendingEvaluation, PendingEvalAdmin)
