from django.forms import ModelForm
from .models import Feeding

class FeedingForm(ModelForm):
    #meta: generates inputs for the fields we want
    class Meta:
        model = Feeding
        fields = ['date', 'meal']
