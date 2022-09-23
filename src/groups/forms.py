from django import forms
from .models import Group, GroupJoin, Teacher, Student

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name']

class GroupJoinForm(forms.ModelForm):
    class Meta:
        model = GroupJoin
        fields = ['group_code']

class GroupSettingsForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name']