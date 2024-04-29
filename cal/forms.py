from django.forms import ModelForm, DateInput
from .models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time']
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

        def __init__(self, *args, **kwargs) -> None:
            super(EventForm, self).__init__(*args, **kwargs)
            self.fields['start_time'].input_formats = ['%Y-%m-%dT%H:%M']
            self.fields['end_time'].input_formats = ['%Y-%m-%dT%H:%M']