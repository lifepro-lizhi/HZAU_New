from django.contrib import admin
from .models import Paper, Multiple_Choice_Question, Essay_Question

# Register your models here.

admin.site.register(Paper)
admin.site.register(Multiple_Choice_Question)
admin.site.register(Essay_Question)