from django.contrib import admin
from .models import Question, Category, Room
# Register your models here.
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Room)