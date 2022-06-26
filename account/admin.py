from atexit import register
from django.contrib import admin
from .models import Relation


admin.site.register(Relation)