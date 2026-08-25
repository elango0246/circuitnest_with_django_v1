from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'contactName', 'placeholder': 'Your Name', 'required': True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'contactEmail', 'placeholder': 'Your Email', 'required': True}))
    message = forms.CharField(widget=forms.Textarea(attrs={'id': 'contactMessage', 'placeholder': 'Your Message', 'rows': 5, 'required': True}))

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']