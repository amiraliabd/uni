from django.core.management.base import BaseCommand
from core.models import Answer, Question
import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display


class Command(BaseCommand):
    help = "migrate golestan file into users"

    def add_arguments(self, parser):
        parser.add_argument("question", nargs="+", type=int)
        parser.add_argument("section", nargs="+", type=int)

    def handle(self, *args, **options):
        question = options["question"][-1]
        section = options["section"][-1]
        answers = Answer.objects.filter(question__id=question, section__id=section).all().order_by('answer')

        if not answers:
            self.stdout.write(
                self.style.ERROR('no answers to such question for that section')
            )
        data = {}
        for ans in answers:
            if data.get(ans.answer):
                data[ans.answer] += 1
            else:
                data[ans.answer] = 1

        plt.bar(list(str(x) for x in data.keys()), list(data.values()))

        plt.xlabel("Answers")
        plt.ylabel("No. of students")
        question_title = Question.objects.filter(id=question).first().question
        question_title = arabic_reshaper.reshape(question_title)
        question_title = get_display(question_title)
        plt.title(question_title)
        plt.show()
