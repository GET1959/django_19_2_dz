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


class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'price', 'created_at', 'updated_at')

    def clean_name(self):
        forbidden_list = ['казино', 'криптовалюта', 'крипта', 'биржа',
                  'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        cleaned_data = self.cleaned_data['name']

        if set(forbidden_list) & set(cleaned_data.split(' ')):
            raise forms.ValidationError('Добавлены недопустимые слова')

        return cleaned_data

    def clean_description(self):
        forbidden_list = ['казино', 'криптовалюта', 'крипта', 'биржа',
                          'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        cleaned_data = self.cleaned_data['description']

        if set(forbidden_list) & set(cleaned_data.split(' ')):
            raise forms.ValidationError('Добавлены недопустимые слова')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'

    def clean_version_sign(self):
        cleaned_data = self.cleaned_data['version_sign']
        print(cleaned_data)
        if cleaned_data != 'активна':
            raise forms.ValidationError('Данная версия не активна')
        return cleaned_data
