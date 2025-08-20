from django.contrib import admin
from cinema.models import Movie, Review, User, Session

# Register your models here.
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Session)