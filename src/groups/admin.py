from django.contrib import admin
from .models import Group, Student, Teacher, Manager
# Register your models here.

admin.site.register(Group)
admin.site.register(Manager)
admin.site.register(Student)
admin.site.register(Teacher)