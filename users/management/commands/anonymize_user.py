from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('user-id', type=int)

    def handle(self, *args, **options):
        user = User.objects.get(id=options['user-id'])
        user.anonymize_me()

        self.stdout.write(self.style.SUCCESS(
            f"User has been anonymized (ID: {user.pk})"
        ))
