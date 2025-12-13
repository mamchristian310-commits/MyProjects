from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']
        widgets = {
            'title':forms.TextInput(),
            'description':forms.Textarea(),
            'completed':forms.CheckboxInput()
            }
        