from django import forms
from recipes.models import Author, User

class Add_Author(forms.Form):
    name = forms.CharField(max_length=60)
    bio = forms.CharField(widget=forms.Textarea)
    user = forms.ModelChoiceField(queryset=User.objects.all())

class Add_Recipe(forms.Form):
    title = forms.CharField(max_length=60)
    description = forms.CharField(widget=forms.Textarea)
    instructions = forms.CharField(widget=forms.Textarea)
    time_required = forms.IntegerField()
    author = forms.ModelChoiceField(queryset=Author.objects.all())
