from django.core.management.base import BaseCommand, CommandError
from lessons.models import User, Term

# user objects are filtered such that only the test account of user_type = 0 is not deleted.
class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.filter(user_type=1).delete()
        User.objects.filter(user_type=2).delete()
        User.objects.filter(user_type=3).delete()
        Term.objects.all().delete()
        print('Database fully unseeded')
