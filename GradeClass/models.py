from django.db import models

# Create your models here.

class GradeClass(models.Model):
    # grade = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


# class Major(models.Model):
#     major = models.CharField(max_length=255)

#     def __str__(self):
#         return self.major


# class Class(models.Model):
#     grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
#     major = models.ForeignKey(Major, on_delete=models.CASCADE)
#     class_number = models.CharField(max_length=255)

#     def __str__(self):
#         return self.grade.grade + "级" + self.major.major + "专业" + self.class_number + "班"

