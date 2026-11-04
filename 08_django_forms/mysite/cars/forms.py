from django import forms

class ReviewForm(forms.Form):
    first_n = forms.CharField(label='First Name', max_length=100)
    last_n = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email')
    review = forms.CharField(label='Please write your review here', widget=forms.Textarea())