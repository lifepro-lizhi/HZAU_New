from django.contrib import admin
from Student.models import Student, PaperResult, PaperAnswer, EssayAnswer, EssayComment, PaperToComment

# Register your models here.

admin.site.register(Student)
admin.site.register(PaperResult)
# admin.site.register(PaperAnswer)
# admin.site.register(EssayAnswer)
# admin.site.register(EssayComment)
# admin.site.register(PaperToComment)