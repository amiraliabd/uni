from django.core.management.base import BaseCommand, CommandError
from authentication.models import GolestanUser
import pandas as pds


class Command(BaseCommand):
    help = "migrate golestan file into users"

    def add_arguments(self, parser):
        parser.add_argument("file_name", nargs="+", type=str)

    def handle(self, *args, **options):
        path = options["file_name"][-1]
        excel = pds.read_excel(path)
        golestan_users = []
        for data in excel.iterrows():
            student_data = data[1]
            golestan_users.append(
                GolestanUser(
                    first_name=student_data['نام'],
                    last_name=student_data['نام خانوادگي'],
                    student_number=student_data['شماره دانشجو'],
                    national_id=student_data['شماره ملي'],
                )
            )
        GolestanUser.objects.bulk_create(golestan_users)

        self.stdout.write(
            self.style.SUCCESS('Successfull')
        )
