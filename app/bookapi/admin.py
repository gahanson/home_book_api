from django.contrib import admin
from .models import bookapiUserSettings, bookapiSourceFiles, Book

admin.site.register(bookapiUserSettings)
admin.site.register(bookapiSourceFiles)
admin.site.register(Book)
