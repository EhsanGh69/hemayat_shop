from django import forms

from .models import ContactUs



class ContactUsForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'subject', 'message']

