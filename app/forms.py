from django import forms
from .models import AttendanceModels





class StartForm(forms.ModelForm):
    class Meta:
        model = AttendanceModels
        fields = ['start','days']
        widgets = {
            'start': forms.TimeInput(attrs={'type': 'time'}),
        }


class EndForm(forms.ModelForm):
    class Meta:
        model = AttendanceModels
        fields = ['end']
        widgets = {
            'end': forms.TimeInput(attrs={'type': 'time'}),
        }


class DaysForm(forms.ModelForm):
    class Meta:
        model = AttendanceModels
        fields = ['days']

    def __init__(self, *args, **kwargs):
        super(DaysForm, self).__init__(*args, **kwargs)
        self.fields['days'].widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        self.fields['days'].widget.attrs['placeholder'] = 'YYYY-MM-DD'
