from django import forms


class PostCreateForm(forms.Form):
    text = forms.CharField(label="text", max_length=100)
    # image = forms.ImageField(label='image')
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
