from django import forms
from .models import Review
from django.forms import ModelForm

# class ReviewForm(forms.Form):
#     first_n = forms.CharField(label='First Name', max_length=100)
#     last_n = forms.CharField(label='Last Name', max_length=100)
#     email = forms.EmailField(label='Email')
#     review = forms.CharField(label='Please write your review here', widget=forms.Textarea())

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = "__all__"

        labels = {
            'first_n':"YOUR FIRST NAME",
            'last_n': 'Last Name',
            'stars':"rating"
            
        }