from django.contrib import admin
from .models import (
    Section,
    Question,
    Evaluation,
    Answer,
)


class StudentSectionInline(admin.TabularInline):
    model = Section.students.through
    verbose_name = 'Section Student'


class AssistantSectionInline(admin.TabularInline):
    model = Section.assistants.through
    verbose_name = 'Section Assistant'


class EvaluationQuestionInline(admin.TabularInline):
    model = Evaluation.questions.through
    verbose_name = 'Evaluation Questions'


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
    list_display = ('question',)
    search_fields = ('question', )


class EvalAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'deadline')
    search_fields = ('section', )
    inlines = [EvaluationQuestionInline, ]
    exclude = ['questions']


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('evaluation', 'question', 'answer')
    exclude = ['student', ]


admin.site.register(Section, SectionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Evaluation, EvalAdmin)
admin.site.register(Answer, AnswerAdmin)
