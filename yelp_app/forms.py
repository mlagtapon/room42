from django import forms
from .models import User
from .models import Restaurant
from .models import Review

#DataFlair #File_Upload
class User_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = [
        'profile_image',
        ]
class Restaurant_Form(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
        'restaurant_image',
        ]
class Review_Form(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
        'review_image',
        ]