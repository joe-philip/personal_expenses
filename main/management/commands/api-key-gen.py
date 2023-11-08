from django.core.management.base import BaseCommand

from main.models import APIKey


class Command(BaseCommand):
    help = 'Generate an APIKey'

    def handle(self, *args, **kwargs):
        while True:
            try:
                label = input('Enter a label for API Key: ')
                if APIKey.objects.filter(label=label).exists():
                    print(self.style.ERROR(
                        'Key exists with that label, please retry'))
                    continue
                print(self.style.SUCCESS(APIKey.objects.create_key(label=label)))
                break
            except KeyboardInterrupt:
                print(self.style.ERROR('\nOperation aborted'))
                break
            except Exception as e:
                print(self.style.ERROR(str(e)))
                break
