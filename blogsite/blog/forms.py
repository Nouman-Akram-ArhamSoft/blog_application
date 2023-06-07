from django import forms
from .models import Post, Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                            widget=forms.Textarea)




class CommentForm(forms.ModelForm):

    class Meta:
        mdoel = Comment
        fields = ["name", "email", "body"]