from django.core.management import base, utils


class Command(base.BaseCommand):
    help = 'Generate an APIKey'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS(utils.get_random_secret_key()))
