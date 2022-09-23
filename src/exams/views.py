from typing import Iterable
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.views import generic
from django.utils.safestring import mark_safe
from django.utils import timezone
from numpy import imag
from django.forms.models import modelformset_factory

from accounts.models import User
from groups.models import Group, Teacher, Manager, Student
from datetime import datetime, date
from .models import ExamMCQ, ExamTF, Exam, MCQAnswerSheet
from .forms import ExamEditForm, ExamMCQForm, ExamTFForm, ExamSettingsForm, MCQAnswerForm, TFAnswerForm
from datetime import timedelta
import calendar
from .utils import Calendar
from django.conf import settings

import face_recognition
import os
import cv2

# Create your views here.

user = get_user_model()

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class CalendarView(generic.ListView):
    model = Exam
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

@login_required
def exam_setup_view(request, name):

    form = ExamSettingsForm(request.POST or None)
    group_obj = Group.objects.get(group_name=name)
    group_name = group_obj.group_name
    user_obj = request.user
    user_email = user_obj.email
    exam_name = ''

    if request.POST and form.is_valid():
        exam_name = form.cleaned_data.get('exam_name')
        duration = form.cleaned_data.get('disp_duration')
        exam_model = form.cleaned_data.get('exam_model')

        mcq_count = form.cleaned_data.get('mcq_questions')
        tf_count = form.cleaned_data.get('tf_questions')
        if mcq_count == 0 and tf_count == 0:
            messages.warning(request, "You can't have an exam without questions!")
            return redirect('exam-setup' , name=group_name)

        form.save()
        exam_obj = Exam.objects.get(exam_name=exam_name)
        exam_obj.duration = timedelta(minutes=duration)
        exam_obj.created_by = user_email
        exam_obj.group = group_name
        exam_obj.no_of_questions = mcq_count + tf_count
        exam_obj.save()
        if exam_model == True:
            return redirect('exam-mcq' , name=group_name, exam=exam_name, exam_model=1)
        else:
            return redirect('exam-mcq' , name=group_name, exam=exam_name, exam_model=0)


    context = {
        'form' : form,
        'group_name' : group_name,
        'exam_name' : exam_name,
    }

    return render(request, 'exams/exam-setup.html', context)

@login_required
def exam_mcq_questions_view(request, name, exam, exam_model):

    exam_obj = Exam.objects.get(exam_name=exam)
    exam_name = exam_obj.exam_name
    mcq_questions = exam_obj.mcq_questions
    group_obj = Group.objects.get(group_name=name)
    group_name = group_obj.group_name
    tf_questions = exam_obj.tf_questions
    exam_model_on = exam_obj.exam_model
    question_count = ExamMCQ.objects.filter(exam=exam_obj).count()
    questions_1m = mcq_questions - 1
    questions_2m = (mcq_questions * 2) - 1
    exam_model_plus = exam_model + 1
    exam_model_minus = exam_model - 1
    question_number = question_count + 1

    if mcq_questions >= 1:
        form = ExamMCQForm(request.POST or None)

        if request.POST and form.is_valid():

            if exam_model_on:
                question_title = form.cleaned_data.get('title')
                choice1 = form.cleaned_data.get('choice1')
                choice2 = form.cleaned_data.get('choice2')
                choice3 = form.cleaned_data.get('choice3')
                choice4 = form.cleaned_data.get('choice4')
                correct_answer = form.cleaned_data.get('correct_answer')
                question_form = ExamMCQ(id=None, title = question_title, choice1=choice1, choice2=choice2, choice3=choice3, choice4=choice4, model=exam_model, correct_answer=correct_answer, exam=exam_obj)
                question_form.save()

            else:
                question_title = form.cleaned_data.get('title')
                choice1 = form.cleaned_data.get('choice1')
                choice2 = form.cleaned_data.get('choice2')
                choice3 = form.cleaned_data.get('choice3')
                choice4 = form.cleaned_data.get('choice4')
                correct_answer = form.cleaned_data.get('correct_answer')
                question_form = ExamMCQ(id=None, title = question_title, choice1=choice1, choice2=choice2, choice3=choice3, choice4=choice4, correct_answer=correct_answer, exam=exam_obj)
                question_form.save()
    else:
        return redirect('exam-tf' , name=group_name, exam=exam_name, exam_model=0)

    context = {
        'form' : form,
        'tf_questions' : tf_questions,
        'question_count' : question_count,
        'question_number' : question_number,
        'questions_1m' : questions_1m,
        'questions_2m' : questions_2m,
        'group_name' : group_name,
        'exam_name' : exam_name,
        'exam_model_on' : exam_model_on,
        'exam_model' : exam_model,
        'exam_model_plus' : exam_model_plus,
        'exam_model_minus' : exam_model_minus,
    }

    return render(request, 'exams/exam-mcq.html', context)

@login_required
def exam_tf_questions_view(request, name, exam, exam_model):

    form = ExamTFForm(request.POST or None)
    group_obj = Group.objects.get(group_name=name)
    group_name = group_obj.group_name
    exam_obj = Exam.objects.get(exam_name=exam)
    exam_name = exam_obj.exam_name
    exam_model_on = exam_obj.exam_model
    tf_questions = exam_obj.tf_questions
    question_count = ExamTF.objects.filter(exam=exam_obj).count()
    questions_1m = tf_questions - 1
    questions_2m = (tf_questions * 2) - 1
    exam_model_1 = exam_model + 1
    question_number = question_count + 1

    if request.POST and form.is_valid():

        if exam_model_on:
            question_title = form.cleaned_data.get('title')
            correct_answer = form.cleaned_data.get('correct_answer')
            question_form = ExamTF(id=None, title = question_title, model=exam_model, correct_answer=correct_answer, exam=exam_obj)
            question_form.save()

        else:
            question_title = form.cleaned_data.get('title')
            correct_answer = form.cleaned_data.get('correct_answer')
            question_form = ExamTF(id=None, title = question_title, correct_answer=correct_answer, exam=exam_obj)
            question_form.save()

    context = {
        'form' : form,
        'question_count' : question_count,
        'question_number' : question_number,
        'questions_1m' : questions_1m,
        'questions_2m' : questions_2m,
        'group_name' : group_name,
        'exam_name' : exam_name,
        'exam_model_on' : exam_model_on,
        'exam_model' : exam_model,
        'exam_model_plus' : exam_model_1,
    }

    return render(request, 'exams/exam-tf.html', context)

@login_required
def exam_settings_view(request, name, exam):

    group_obj = Group.objects.get(group_name=name)
    group_name = group_obj.group_name
    exam_obj = Exam.objects.get(exam_name=exam)

    exam_time = exam_obj.date
    time_now = datetime.now().replace(second=0, microsecond=0)
    exam_range = exam_time.time().replace(minute=exam_time.minute + 5)
    allowed = None

    exam_query = Exam.objects.filter(group=group_name)

    for exam_obj in exam_query:
        if exam_obj.exam_name == exam:
            exam_name = exam_obj.exam_name
            exam_object = Exam.objects.get(exam_name=exam_name)

    def time_in_range(start, end, x):
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    if time_now.date() == exam_time.date():

        if time_in_range(exam_time.time(), exam_range, time_now.time()):
            allowed = True
        else:
            allowed = False
    else:
        allowed == False

    context = {
        'group_name' : group_name,
        'exam' : exam_object,
        "allowed" : allowed,
    }

    return render(request, 'exams/exam-settings.html', context)

@login_required
def exam_delete_view(request, name, exam):

    group_obj = Group.objects.get(group_name=name)
    group_name = group_obj.group_name
    exam_obj = Exam.objects.get(exam_name=exam)

    exam_query = Exam.objects.filter(group=group_name)
    exam_name = ''

    if request.method == 'POST':

        for exam_obj in exam_query:
            if exam_obj.exam_name == exam:
                exam_name = exam_obj.exam_name
                exam_object = Exam.objects.get(exam_name=exam_name)
                exam_object.delete()

        messages.success(request, f'Successfully deleted {exam_name}')
        return redirect('../../../')

    context = {
        'exam' : exam_obj,
        'group' : group_obj
    }

    return render(request, 'exams/exam-delete.html', context)

@login_required
def exam_edit_view(request, name, exam):

    group_obj = Group.objects.get(group_name=name)
    group_name = group_obj.group_name
    exam_obj = Exam.objects.get(exam_name=exam)
    exam_name = exam_obj.exam_name

    if request.method == "POST":
        edit_form = ExamEditForm(request.POST, request.FILES, instance=exam_obj)
        if edit_form.is_valid():
            upd_exam_name = edit_form.cleaned_data.get('exam_name')
            duration = edit_form.cleaned_data.get('disp_duration')
            exam_obj.duration = timedelta(minutes=duration)
            exam_obj.save()
            edit_form.save()
            messages.success(request, f'Successfully edited {exam_name}')
            return redirect('group-manage' , name=group_name)
    else:
        edit_form = ExamEditForm(instance=exam_obj)

    context = {
        'edit_form' : edit_form,
        'exam' : exam_name
    }

    return render(request, 'exams/exam-edit.html', context)

@login_required
def exam_join_view(request, name, exam):

    group_obj = Group.objects.get(group_name=name)
    exam_obj = Exam.objects.get(exam_name=exam)

    context = {
        "group" : group_obj,
        "exam" : exam_obj,
    }

    return render(request, 'exams/exam-join.html', context)

@login_required
def face_view(request, name, exam):

    group_obj = Group.objects.get(group_name=name)
    exam_obj = Exam.objects.get(exam_name=exam)
    user_obj = request.user
    TOLERANCE = 0.5

    try:
        video = cv2.VideoCapture(0)

        ret, image = video.read()

        user_image = user_obj.image.name

        image_path = settings.MEDIA_ROOT + '\\' + user_image

        face_image = face_recognition.load_image_file(image_path)
        known_face_encoding = face_recognition.face_encodings(face_image)[0]

        locations = face_recognition.face_locations(image)
        face_encoding = face_recognition.face_encodings(image, locations)

        results = face_recognition.compare_faces(known_face_encoding, face_encoding, TOLERANCE)

    except ValueError:
        results = [False]
    except IndexError:
        results = [False]

    if False in results:
        for i in range(4):
            try:
                video = cv2.VideoCapture(0)
                ret, image = video.read()
                locations = face_recognition.face_locations(image)
                face_encoding = face_recognition.face_encodings(image, locations)
                results = face_recognition.compare_faces(known_face_encoding, face_encoding, TOLERANCE)

            except ValueError:
                results = [False]
            except IndexError:
                results = [False]

            if True in results:
                break

    context = {
        "group" : group_obj,
        "exam" : exam_obj,
        "result" : results
    }

    return render(request, 'exams/face-detect.html', context)

@login_required
def exam_view(request, name, exam):

    mcq_form = MCQAnswerForm(request.POST or None)
    tf_form = TFAnswerForm(request.POST or None)

    group_obj = Group.objects.get(group_name=name)
    exam_obj = Exam.objects.get(exam_name=exam)
    exam_date = exam_obj.date
    mcq_questions = exam_obj.mcq_questions
    tf_questions = exam_obj.tf_questions

    mcq_query = ExamMCQ.objects.filter(exam=exam_obj)
    tf_query = ExamTF.objects.filter(exam=exam_obj)

    # AnswerFormSet = modelformset_factory(MCQAnswerSheet, form=MCQAnswerForm, extra=0)
    # formset = AnswerFormSet(queryset=mcq_query)
    # if request.method == 'POST':
    #     formset = AnswerFormSet(request.POST or None)
    #     print(formset.errors)
    #     print(formset.is_valid())
    #     if formset.is_valid():
    #         print('here')
    #         for form in formset:
    #             form.save()
    #             answer = form.cleaned_data.get('answer')
    #             MCQAnswerSheet(id=None, exam=exam, question_title=mcq_query.title, answer=answer).save()

    context = {
        "exam" : exam_obj,
        "exam_date" : exam_date,
        "group" : group_obj,
        "mcq_query" : mcq_query,
        'tf_query' : tf_query,
        "mcq_form" : mcq_form,
        "tf_form" : tf_form,
    }

    return render(request, 'exams/exam.html', context)

@login_required
def exam_end_view(request, name, exam):

    group_obj = Group.objects.get(group_name=name)
    exam_obj = Exam.objects.get(exam_name=exam)

    context = {
        "exam" : exam_obj,
        "group" : group_obj,
    }

    return render(request, 'exams/exam-end.html', context)