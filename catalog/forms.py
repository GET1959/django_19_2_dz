from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label="Your name")
    phone = forms.CharField(label="Your phone")
    message = forms.CharField(widget=forms.Textarea)

