from django.contrib import admin
from .models import MyUser,Genre,Movie

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Genre)
admin.site.register(Movie)