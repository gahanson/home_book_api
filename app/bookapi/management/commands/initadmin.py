import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        adminNameVariable = os.getenv("ADMIN_USER_NAME")
        adminEmailVariable = os.getenv("ADMIN_USER_EMAIL")
        adminPasswordVariable = os.getenv("ADMIN_USER_PASSWORD")
        if User.objects.filter(username=adminNameVariable).exists() != True:
            User.objects.create_superuser(adminNameVariable, adminEmailVariable, adminPasswordVariable)       
