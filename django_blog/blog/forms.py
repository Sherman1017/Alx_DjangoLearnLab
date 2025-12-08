from django import forms
from taggit.forms import TagWidget

class PostForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(widget=TagWidget())
