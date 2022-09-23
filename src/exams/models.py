from django.db import models
from datetime import timedelta, datetime
from multiselectfield import MultiSelectField

# Create your models here.

class Exam(models.Model):
    exam_name     = models.CharField(max_length=50, unique=True)
    group         = models.CharField(max_length=50, default='group')
    date          = models.DateTimeField()
    created_date  = models.DateTimeField(default=datetime.now)
    created_by    = models.CharField(max_length=50)
    duration      = models.DurationField(default=timedelta(seconds=0))
    times = [
        (30,'30 Minutes'),
        (60,'1 Hour'),
        (90,'1 Hr 30 Mins'),
        (120,'2 Hours'),
        (150,'2 Hrs 30 Mins'),
        (180,'3 Hours')
    ]
    disp_duration = models.IntegerField(choices=times)
    mcq_questions = models.IntegerField()
    tf_questions = models.IntegerField()
    no_of_questions = models.IntegerField(default=0)
    exam_model = models.BooleanField(default=False)

    def __str__(self):
            return self.exam_name

class ExamMCQ(models.Model):
    exam    = models.ForeignKey(Exam, on_delete=models.CASCADE)
    title   = models.CharField(max_length=500)
    choice1 = models.CharField(max_length=50)
    choice2 = models.CharField(max_length=50)
    choice3 = models.CharField(max_length=50)
    choice4 = models.CharField(max_length=50)
    answers = [
        ('1',1),
        ('2',2),
        ('3',3),
        ('4',4),
    ]
    correct_answer = models.CharField(choices=answers, max_length=1)
    model   = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class ExamTF(models.Model):
    exam    = models.ForeignKey(Exam, on_delete=models.CASCADE)
    title   = models.CharField(max_length=500)
    answers  = [
        ('True',True),
        ('False',False),
    ]
    correct_answer = models.CharField(choices=answers , max_length=5)
    model   = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class MCQAnswerSheet(models.Model):
    exam    = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_title = models.ForeignKey(ExamMCQ, on_delete=models.CASCADE)
    # answers = [
    #     ('1','1'),
    #     ('2','2'),
    #     ('3','3'),
    #     ('4','4'),
    # ]
    answer = models.CharField(max_length=5)

    def __str__(self):
        return self.exam.exam_name

class TFAnswerSheet(models.Model):
    exam    = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_title = models.ForeignKey(ExamTF, on_delete=models.CASCADE)
    # answers = [
    #     ('True',True),
    #     ('False',False),
    # ]
    answer = models.CharField(max_length=5)

    def __str__(self):
        return self.exam.exam_name
