import django.shortcuts
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from cinema.forms import MovieForm, ReviewForm, UserRegistrationForm
from cinema.models import Movie, Session, Review

from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView

from django.contrib.auth.models import User, Group
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Create your views here.
def main_page(req):
    return render(req, 'cinema/pages/index.html')


def add_cinema_page(req):
    if req.method == 'POST':
        form = MovieForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    form = MovieForm()

    context = {
        'form': form,
    }

    return render(req, 'cinema/pages/movies/CRUD/add.html', context=context)


def movies_list_page(req):
    movies = Movie.objects.all()
    print(movies)

    context = {
        'movies': movies,
    }

    return render(req, 'cinema/pages/movies/movies.html', context=context)


class MovieDetailView(LoginRequiredMixin, DetailView):
    model = Movie
    template_name = 'cinema/pages/movies/CRUD/read.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(movie=self.object).order_by('-review_date')
        context['form'] = ReviewForm() if self.request.user.is_authenticated else None
        user = self.request.user
        if user.is_authenticated:
            groups = user.groups.values_list('name', flat=True)
            if user.is_staff:
                context['role'] = 'Staff'
            elif 'CEO' in groups:
                context['role'] = 'CEO'
            elif 'Employee' in groups:
                context['role'] = 'Employee'
            else:
                context['role'] = 'User'
        else:
            context['role'] = None
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect('login')
        form = ReviewForm(request.POST)
        if form.is_valid():
            existing_review = Review.objects.filter(movie=self.object, user=request.user).first()
            if existing_review:
                return redirect(reverse('movie_detail', kwargs={'pk': self.object.pk}))

            review = form.save(commit=False)
            review.movie = self.object
            review.user = request.user
            review.save()
            return redirect(reverse('movie_detail', kwargs={'pk': self.object.pk}))
        return self.get(request, *args, **kwargs)


class MovieUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Movie
    fields = '__all__'
    template_name = 'cinema/pages/movies/CRUD/update.html'
    context_object_name = 'movie'
    permission_required = 'cinema.change_movie'

    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.object.pk})


class MovieDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Movie
    template_name = 'cinema/pages/movies/CRUD/delete.html'
    context_object_name = 'movie'
    success_url = reverse_lazy('movies_list')
    permission_required = 'cinema.delete_movie'


class SessionCreateView(CreateView):
    model = Session
    fields = ['date', 'start_time', 'end_time', 'audience_number', 'is_active']

    template_name = 'cinema/pages/sessions/CRUD/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.movie = django.shortcuts.get_object_or_404(Movie, pk=kwargs['movie_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.movie.id})

    def form_valid(self, form):
        form.instance.movie = self.movie
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie'] = self.movie
        return context


class UserDetailView(DetailView):
    model = User
    template_name = 'cinema/pages/account/CRUD/read.html'
    context_object_name = 'user'


def logout_view(req):
    if req.method == 'POST':
        logout(req)
        return redirect('main')
    return render(req, 'cinema/pages/account/logout.html')


class UserRegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        context = {
            'form': form,
        }
        return render(request, 'cinema/pages/account/register.html', context=context)

    def post(self, request):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user_group = Group.objects.get(name='User')
            user.groups.add(user_group)

            login(request, user)
            return redirect('main')

        return render(request, "cinema/pages/account/register.html", {'form': form})


class ReviewDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Review
    template_name = 'cinema/pages/reviews/CRUD/delete.html'
    context_object_name = 'review'
    permission_required = 'cinema.delete_review'

    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.object.movie.id})


class ReviewUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Review
    template_name = 'cinema/pages/reviews/CRUD/update.html'
    context_object_name = 'review'
    permission_required = 'cinema.change_review'
    fields = ['review']

    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.object.movie.id})
