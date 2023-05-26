from django.core.management.base import BaseCommand
from core.models import Answer, Question
import matplotlib.pyplot as plt
from django.db.models import Avg
import arabic_reshaper
from bidi.algorithm import get_display


class Command(BaseCommand):
    help = "migrate golestan file into users"

    def add_arguments(self, parser):
        parser.add_argument("section", nargs="+", type=int)

    def handle(self, *args, **options):
        section = options["section"][-1]
        answers = Answer.objects.filter(section__id=section).values("question").annotate(avg=Avg("answer")).all()

        if not answers:
            self.stdout.write(
                self.style.ERROR('no answers for that section')
            )
        data = {}
        for ans in answers:
            question_title = Question.objects.filter(id=ans['question']).first().question
            question_title = arabic_reshaper.reshape(question_title[:35] + "...")
            question_title = get_display(question_title)
            data[question_title] = ans['avg']

        plt.bar(list(str(x) for x in data.keys()), list(data.values()))

        plt.xlabel("Section Questions")
        plt.ylabel("Avg answers")
        plt.title("Section evaluation")
        plt.show()
