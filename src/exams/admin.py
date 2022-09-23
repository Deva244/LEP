from django.contrib import admin
from .models import Exam, ExamMCQ, ExamTF, MCQAnswerSheet
# Register your models here.

admin.site.register(Exam)
admin.site.register(ExamMCQ)
admin.site.register(ExamTF)
admin.site.register(MCQAnswerSheet)