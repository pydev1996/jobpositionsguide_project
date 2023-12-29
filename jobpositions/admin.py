# jobpositionsguide_project/jobpositions/admin.py
from django.contrib import admin
from .models import JobPosition,ContactMessage,Institution,Billing,Institutor

admin.site.register(JobPosition)
admin.site.register(ContactMessage)
admin.site.register(Billing)
admin.site.register(Institution)
admin.site.register(Institutor)

