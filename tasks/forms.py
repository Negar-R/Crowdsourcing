from django import forms
from django.db.models import fields

from tasks.models import TaskModel


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ['title', 'value', 'estimation', 'deadline', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control pull-right',
                                            'id': 'reservationtime'}),
            
            'description': forms.Textarea(attrs={'class': 'form-control pull-right',
                                                  'id': 'reservationtime'}),
            
            'deadline': forms.DateTimeInput(attrs={'placeholder': 'Enter a date',
                                                   'class': 'datetime-inputt-date',
                                                   'autocomplete': 'off'}),
        }
