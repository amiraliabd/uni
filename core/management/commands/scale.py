from django.core.management.base import BaseCommand
from core.models import Answer
import matplotlib.pyplot as plt
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display


class Command(BaseCommand):
    help = "migrate golestan file into users"

    def add_arguments(self, parser):
        parser.add_argument("question", nargs="+", type=int)
        parser.add_argument("section", nargs="+", type=int)

    def handle(self, *args, **options):
        question = options["question"]
        section = options["section"][-1]
        data = {}

        for q in question:
            answers = Answer.objects.filter(question__id=q, section__id=section).all().order_by('answer')

            if not answers:
                self.stdout.write(
                    self.style.ERROR('no answers to such question for that section')
                )

            data[answers[0].question.question] = sum([a.answer for a in answers]) / len(answers)

        plt.figure(figsize=(10, 6))
        plt.subplot(polar=True)

        expected = list(data.values())
        expected = [1.3, 3.2, 2.32, 4.1, 1.75]
        expected.append(expected[0])

        questions = list(data.keys())
        questions = ['تسلط علمی و توانایی انتقال مطالب', 'شیوه تعامل و همدلی با دانشجو', 'توانایی مدیریت فرایند آموزشی', ' برخورد حرفه‌ای، عادلانه و نمره‌دهی شفاف', ' مسئولیت‌پذیری و وقت‌گذاری منظم']
        persian_q = []
        for q in questions:
            question_title = arabic_reshaper.reshape(q[:18] + "...")
            question_title = get_display(question_title)
            persian_q.append(question_title)

        theta = np.linspace(0, 2 * np.pi, len(expected))
        lines, labels = plt.thetagrids(
            range(0, 360, int(360 / len(persian_q))),
                                       (persian_q))
        plt.plot(theta, expected)
        plt.title("Average answers spider graph")
        plt.show()
