from django import forms


class PostCreateForm(forms.Form):
    text = forms.CharField(label="text", max_length=100)
    # image = forms.ImageField(label='image')
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class PostCommentCreateForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())

    def save(self, post, author):
        return post.postcomment_set.create(
            author=author,
            content=self.cleaned_data['content']
        )
