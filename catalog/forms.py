from random import choice, choices

from django import forms

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ContactForm(forms.Form):
    name = forms.CharField(label="Your name")
    phone = forms.CharField(label="Your phone")
    message = forms.CharField(widget=forms.Textarea)


FORBIDDEN_LIST = ['казино', 'криптовалюта', 'крипта', 'биржа',
                      'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'price',)

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']

        if set(FORBIDDEN_LIST) & set(cleaned_data.split(' ')):
            raise forms.ValidationError('Добавлены недопустимые слова')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']

        if set(FORBIDDEN_LIST) & set(cleaned_data.split(' ')):
            raise forms.ValidationError('Добавлены недопустимые слова')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'

    def clean_version_sign(self):
        cleaned_data = self.cleaned_data['version_sign']
        # if not cleaned_data:
        #     raise forms.ValidationError('Данная версия не активна')
        return cleaned_data
