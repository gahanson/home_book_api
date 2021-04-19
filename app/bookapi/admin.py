from django.contrib import admin
from .models import bookapiUserSettings, bookapiSourceFiles, Book, AvailableBook

admin.site.register(bookapiUserSettings)
admin.site.register(bookapiSourceFiles)
admin.site.register(Book)
admin.site.register(AvailableBook)
