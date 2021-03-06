from django.forms import ModelForm
from .models import BookInstance
import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class RenewBookModelForm(ModelForm):

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        # Check if a date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_("Invalid date - renewal in the past"))

        # check if a date is in the allowed range ("About four weeks from today")
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal is more than four weeks ahead'))

        # Return cleaned data
        return data

    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('New renewal date')}
        help_texts = {'due_back': _(
            'Enter a date between now and 4 weeks (default 3).')}
