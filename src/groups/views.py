from django.shortcuts import render, redirect
from .forms import GroupForm, GroupJoinForm, GroupSettingsForm
from .models import Student, Group, Teacher, Manager
from exams.models import Exam
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
# Create your views here.

@login_required
def group_create_view(request):
    form = GroupForm(request.POST or None)
    user = get_user_model()
    user_account_type = user.get_account_type(request.user)
    user_obj = request.user
    user_email = user_obj.email
    user_fullname = user.get_full_name(request.user)
    user_no_of_groups = user.get_no_of_groups(request.user)
    if form.is_valid():
        group_name = form.cleaned_data.get('group_name')
        if user_account_type == 'manager':
            if user_no_of_groups == 0:
                form.save()
                user_obj.no_of_groups += 1
                user_obj.save()
                group = Group.objects.get(group_name=group_name)
                group_owner = Manager(group=group, name= user_fullname, email=user_email)
                group_owner.save()
                group.group_owner = user_email
                group.member_count += 1
                group.save()
                messages.success(request, 'Group created successfully')
                return redirect('home-page')
            else:
                messages.error(request, "You cannot have more than one group")
        else:
            messages.error(request, "You don't have the permission to create a group")
            form = GroupForm()

    context = {
        'form' : form
    }
    return render(request, 'groups/group-create.html', context)

@login_required
def group_join_view(request):
    user = get_user_model()
    form = GroupJoinForm(request.POST or None)
    user_account_type = user.get_account_type(request.user)
    user_obj = request.user
    user_email = user_obj.email
    user_fullname = user.get_full_name(request.user)
    user_no_of_groups = user.get_no_of_groups(request.user)
    if form.is_valid():
        group_code = form.cleaned_data.get('group_code')
        group_obj = Group.objects.get(group_code=group_code)
        manager = Manager.objects.get(group=group_obj)
        if user_account_type == 'student':
            if user_no_of_groups == 0:
                user_obj.no_of_groups += 1
                user_obj.save()
                student_form = Student(id=None, student_email = user_email, student_name=user_fullname, group = group_obj, group_owner=manager)
                student_form.save()
                group_obj.member_count += 1
                group_obj.save()
                messages.success(request, 'Successfully joined the group')
                return redirect('home-page')
            else:
                messages.warning(request, "You cannot join more than one group")
                form = GroupJoinForm()
        elif user_account_type == 'teacher':
            if user_no_of_groups < 3:
                if user_no_of_groups >= 1:
                    teacher_query = Teacher.objects.filter(groups=group_obj)
                    if teacher_query:
                        messages.warning(request, "You are already a member of this group")
                        form = GroupJoinForm()
                    else:
                        user_obj.no_of_groups += 1
                        user_obj.save()
                        teacher_form = Teacher(teacher_email = user_email, teacher_name=user_fullname)
                        teacher_form.save()
                        teacher_form.groups.add(group_obj)
                        teacher_form.group_owner.add(manager)
                        group_obj.member_count += 1
                        group_obj.save()
                        messages.success(request, 'Successfully joined the group')
                        return redirect('home-page')
                else:
                    user_obj.no_of_groups += 1
                    user_obj.save()
                    teacher_form = Teacher(teacher_email = user_email, teacher_name=user_fullname)
                    teacher_form.save()
                    teacher_form.groups.add(group_obj)
                    teacher_form.group_owner.add(manager)
                    group_obj.member_count += 1
                    group_obj.save()
                    messages.success(request, 'Successfully joined the group')
                    return redirect('home-page')
            else:
                messages.warning(request, "You can only join 3 groups")
                form = GroupJoinForm()
        elif user_account_type == 'manager':
            messages.warning(request, "Managers can only create groups")
            form = GroupJoinForm()
    context = {
        'form' : form,      
    }
    return render(request, 'groups/group-join.html', context)

@login_required
def group_list_view(request):
    user = get_user_model()
    user_account_type = user.get_account_type(request.user)
    user_obj = request.user
    user_email = user_obj.email
    user_no_of_groups = user.get_no_of_groups(request.user)

    groups = "-"
    group_code = '-'
    group_owner = '-'
    group_query = []

    if user_account_type == 'manager':
        if user_no_of_groups == 1:
            group_owner = Manager.objects.get(email=user_email)
            group_code = group_owner.group.group_code
            groups = group_owner.group
    elif user_account_type == 'teacher':
        if user_no_of_groups >= 1:
            teacher = Teacher.objects.filter(teacher_email=user_email)
            groups = []
            for instance in teacher:
                group_name = instance.groups.get()
                groups.append(group_name)
            for group in groups:
                group_obj = Group.objects.get(group_name=group)
                group_query.append(group_obj)
    elif user_account_type == 'student':
        if user_no_of_groups == 1:
            student = Student.objects.get(student_email=user_email)
            group_owner = student.group_owner
            group_code = student.group.group_code
            groups = student.group
    
    context = {
        'group_name' : groups,
        'group_owner' : group_owner,
        'group_code' : group_code,
        'group_query' : group_query,
    }

    return render(request, 'groups/group-list.html', context)

@login_required
def group_manage_view(request, name):

    group_obj = Group.objects.get(group_name=name)
    group_name = group_obj.group_name
    group_code = group_obj.group_code
    group_owner = group_obj.group_owner
    member_count = group_obj.member_count

    manager_query = Manager.objects.get(email=group_owner)
    student_query = Student.objects.filter(group=group_obj)
    teacher_query = Teacher.objects.filter(groups=group_obj)
    exam_query = Exam.objects.filter(group=group_name)

    context = {
        'group_name'    : group_name,
        'group_owner'   : group_owner,
        'group_code'    : group_code,
        'manager'       : manager_query,
        'student'       : student_query,
        'teacher'       : teacher_query,
        'members'       : member_count,
        'exams'         : exam_query
    }

    return render(request, 'groups/group-manage.html', context)

@login_required
def group_settings_view(request, name):
    
    group_obj = Group.objects.get(group_name=name)
    group_code = group_obj.group_code
    group_name = group_obj.group_name
    group_owner = group_obj.group_owner
    member_count = group_obj.member_count
    teacher_query = Teacher.objects.filter(groups=group_obj)

    if request.method == "POST":
        settings_form = GroupSettingsForm(request.POST, request.FILES, instance=group_obj)
        if settings_form.is_valid():
            settings_form.save()
            messages.success(request, f'Info Updated Successfully!')
            return redirect('group-list')
    else:
        settings_form = GroupSettingsForm(instance=group_obj)

    context = {
        'settings_form' : settings_form,
        'group_code'    : group_code,
        'group_name'    : group_name,
        'members'       : member_count,
        'group_owner'   : group_owner,
        'teacher'       : teacher_query,
    }

    return render(request, 'groups/group-settings.html', context)

@login_required
def group_delete_view(request, name):

    group_obj = Group.objects.get(group_name=name)
    group_name = group_obj.group_name
    user = request.user

    if request.method == "POST":

        teacher_query = Teacher.objects.filter(groups=group_obj)
        student_query = Student.objects.filter(group=group_obj)

        for teacher in teacher_query:
            teacher_user = User.objects.get(email=teacher)
            teacher.delete()
            teacher_user.no_of_groups -= 1
            teacher_user.save()

        for student in student_query:
            student_user = User.objects.get(email=student)
            student_user.no_of_groups -= 1
            student_user.save()

        group_obj.delete()
        user.no_of_groups -= 1
        user.save()

        messages.success(request, 'Group Deleted Successfully!')
        return redirect('home-page')

    context = {
        'object' : group_obj,
        'group_name' : group_name,
    }

    return render(request, 'groups/group-delete.html', context)

@login_required
def group_leave_view(request, name):

    group_obj = Group.objects.get(group_name=name)
    group_name = group_obj.group_name
    user = get_user_model()
    user_email = user.get_email(request.user)
    user_account_type = user.get_account_type(request.user)

    if request.method == "POST":

        if user_account_type == 'teacher':
            teacher_query = Teacher.objects.filter(groups=group_obj)
            for teacher in teacher_query:
                if teacher.teacher_email == user_email:
                    teacher_user = User.objects.get(email=teacher)
                    teacher.delete()
                    teacher_user.no_of_groups -= 1
                    teacher_user.save()
                    group_obj.member_count -= 1
                    group_obj.save()
        elif user_account_type == 'student':
            student_query = Student.objects.filter(group=group_obj)
            for student in student_query:
                if student.student_email == user_email:
                    student_user = User.objects.get(email=student)
                    student.delete()
                    student_user.no_of_groups -= 1
                    student_user.save()
                    group_obj.member_count -= 1
                    group_obj.save()

        messages.success(request, 'Group Left Successfully!')
        return redirect('home-page')

    context = {
        'object' : group_obj,
        'group_name' : group_name,
    }

    return render(request, 'groups/group-leave.html', context)

@login_required
def group_kick_view(request, name, user):

    group_obj = Group.objects.get(group_name=name)
    member_obj = User.objects.get(email=user)
    group_name = group_obj.group_name
    user = get_user_model()

    if request.method == "POST":

        if member_obj.account_type == 'teacher':
            teacher_query = Teacher.objects.filter(groups=group_obj)
            for teacher in teacher_query:
                if teacher.teacher_email == member_obj.email:
                    teacher.delete()
                    member_obj.no_of_groups -= 1
                    member_obj.save()
                    group_obj.member_count -= 1
                    group_obj.save()
        elif member_obj.account_type == 'student':
            student_query = Student.objects.filter(group=group_obj)
            for student in student_query:
                if student.student_email == member_obj.email:
                    student.delete()
                    member_obj.no_of_groups -= 1
                    member_obj.save()
                    group_obj.member_count -= 1
                    group_obj.save()

        messages.success(request, f'{member_obj} Kicked!')
        return redirect('group-list')

    context = {
        'object' : group_obj,
        'group_name' : group_name,
        'member' : member_obj
    }

    return render(request, 'groups/group-kick.html', context)

@login_required
def group_perm_view(request, name, user):
    
    group_obj = Group.objects.get(group_name=name)
    member_obj = User.objects.get(email=user)
    group_name = group_obj.group_name
    user = get_user_model()
    teacher_query = Teacher.objects.filter(groups=group_obj)

    if request.method == "POST":

        for teacher in teacher_query:
            if teacher.teacher_email == member_obj.email:
                if teacher.exam_perm == False:
                    teacher.exam_perm = True
                    teacher.save()
                    messages.success(request, f'{member_obj} Has Exam Permissions Now')
                    return redirect('../../')
                else:
                    teacher.exam_perm = False
                    teacher.save()
                    messages.warning(request, f'{member_obj} No Longer Has Exam Permissions')
                    return redirect('../../')

    context = {
        'object' : group_obj,
        'group_name' : group_name,
        'member' : member_obj,
        'teacher_query' : teacher_query
    }

    return render(request, 'groups/group-perm.html', context)
