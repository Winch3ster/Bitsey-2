
from django.core.management.base import BaseCommand
from system.models import *
from user import models as usermodels
from datetime import date

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        # Your seeding logic goes here
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))

        #This is a seeding notification for DarrenLee
        user = usermodels.User.objects.get(pk=4)
        print(user)

        # Example seeding logic for MyModel
        notificationData = [
            {
                'user': user,
                'message': 'This is a notification for ' + user.first_name,
                'date': date.today(),
                'isRead': False   
            },
            {
                'user': user,
                'message': user.first_name + ", your favourite game is on offer!",
                'date': date.today(),
                'isRead': False   
            },
            {
                'user': user,
                'message': user.first_name + ", glad to see you again!",
                'date': date.today(),
                'isRead': False   
            },

            # Add more items as needed
        ]

        for data in notificationData:
            Notifications.objects.create(**data)