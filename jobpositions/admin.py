# jobpositionsguide_project/jobpositions/admin.py
from django.contrib import admin
from .models import JobPosition,ContactMessage

admin.site.register(JobPosition)
admin.site.register(ContactMessage)

