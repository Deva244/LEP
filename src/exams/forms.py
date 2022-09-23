from django import forms
from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from django.forms import widgets
from .models import Exam, ExamMCQ, ExamTF, MCQAnswerSheet, TFAnswerSheet

class ExamSettingsForm(forms.ModelForm):
    class Meta:
        model = Exam
        widgets = {
            'date': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        labels = {
            'disp_duration' : 'Duration',
            'mcq_questions' : 'Number of MCQs',
            'tf_questions' : 'Number of True or False Questions',
            'exam_model' : 'Extra Exam Model',
        }
        exclude = {'created_by', 'created_date', 'duration', 'group', 'no_of_questions'}

    def __init__(self, *args, **kwargs):
        super(ExamSettingsForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['date'].input_formats = ('%Y-%m-%dT%H:%M',)

class ExamMCQForm(forms.ModelForm):
    class Meta:
        model = ExamMCQ
        fields = ['title','choice1','choice2','choice3','choice4','correct_answer']
        widgets = {
            'choice1' : forms.TextInput(attrs={'placeholder' : '1st Choice'}),
            'choice2' : forms.TextInput(attrs={'placeholder' : '2nd Choice'}),
            'choice3' : forms.TextInput(attrs={'placeholder' : '3rd Choice'}),
            'choice4' : forms.TextInput(attrs={'placeholder' : '4th Choice'}),
        }
        labels = {
            'title'   : 'Question Title',
            'choice1' : '',
            'choice2' : '',
            'choice3' : '',
            'choice4' : '',
            'correct_answer' : 'Correct Answer',
        }

class ExamTFForm(forms.ModelForm):
    class Meta:
        model = ExamTF
        fields = ['title','correct_answer']
        labels = {
            'correct_answer' : 'Correct Answer',
        }

class ExamEditForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['exam_name', 'date', 'disp_duration']
        labels = {
            'disp_duration' : 'Duration',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(ExamEditForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['date'].input_formats = ('%Y-%m-%dT%H:%M',)

class MCQAnswerForm(forms.ModelForm):
    class Meta:
        model = MCQAnswerSheet
        fields = ['answer']
        labels = {
            'answer':''
        }
        widgets = {
            'answer': forms.TextInput(attrs={'placeholder' : "Input the answer's number"}),
        }

class TFAnswerForm(forms.ModelForm):
    class Meta:
        model = TFAnswerSheet
        fields = ['answer']
        labels = {
            'answer':''
        }
        widgets = {
            'answer': forms.TextInput(attrs={'placeholder' : "Input True or False"}),
        }
