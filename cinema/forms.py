from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from cinema.models import Movie, Review


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'company', 'description', 'year_released', 'length', 'genre', 'thumbnail']

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['review']

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']