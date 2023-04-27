from django.contrib import admin
from . import models

admin.site.register(models.Instructor)
admin.site.register(models.Course)
admin.site.register(models.Module)
admin.site.register(models.CourseCategory)
admin.site.register(models.Student)
admin.site.register(models.StudentCourseEnrollment)
admin.site.register(models.InstructorStudentChat)
admin.site.register(models.Assignments)
admin.site.register(models.AssignmentResponse)



# Register your models here.
