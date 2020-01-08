from django import forms


class PostCreateForm(forms.Form):
    text = forms.CharField(label="text", max_length=100)
    image = forms.ImageField(label='image')
