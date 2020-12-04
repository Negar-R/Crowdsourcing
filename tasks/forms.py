from django import forms
from django.db.models import fields
# from django.core.exceptions import ValidationError

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
            
            'deadline': forms.DateTimeInput(attrs={'class': 'datetime-inputt-date',
                                                   'autocomplete': 'off',
                                                   'placeholder': '2021-01-18'}),
        }

    def clean(self):
        value = self.cleaned_data.get('value')
        estimation = self.cleaned_data.get('estimation')

        if value < 1000 or value > 50000:
            print("AVAL")
            raise forms.ValidationError("Value should be between 1000 and 50000")
        if estimation < 3 and value > 30000:
            print("DOYOM")
            raise forms.ValidationError(
                "Maximum value for tasks with estimation lower than \
                3 days is 30.000")
                
        return self.cleaned_data
