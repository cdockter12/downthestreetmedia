import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField
from DTSWebsite.models import Album


class DateInput(forms.DateInput):
    input_type = 'date'


class SetupPhotoForm(forms.Form):
    SQFT_CHOICES = ((1, _('<2000')), (2, _('2001-3499')),
                    (3, _('3499-5000')), (4, _('>5000')),)

    contact_first_name = forms.CharField(
        label='First Name', max_length=100, required=True)
    contact_last_name = forms.CharField(
        label='Last Name', max_length=100, required=True)
    contact_email = forms.EmailField(
        label='Email Address', max_length=100, required=True)
    listing_address = forms.CharField(label="Listing Address")
    house_sqft = forms.ChoiceField(choices=SQFT_CHOICES,
                                   label="Listing Square Footage", required=True)
    photo_date = forms.DateField(
        label="Desired Photo Date:", widget=DateInput)
    captcha = CaptchaField()

    # adds a class 'form-control' to every input
    def __init__(self, *args, **kwargs):
        super(SetupPhotoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_photo_date(self):
        data = self.cleaned_data['photo_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(
                _('Invalid date - appointment is in the past'))

        # Returning cleaned data
        return data


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = []

    zip = forms.FileField(required=False)
