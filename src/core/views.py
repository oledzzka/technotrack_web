from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.shortcuts import resolve_url
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from blogs.models import Blog, Post


class HomePageView(TemplateView):

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView,self).get_context_data(**kwargs)
        context['blogs_count'] = Blog.objects.all().count()
        context['posts_count'] = Post.objects.all().count()
        return context

class UserRegForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ("username",'avatar')
        field_classes = {'username': UsernameField}


class RegisterFormView(CreateView):
    form_class = UserRegForm
    template_name = "core/registration.html"

    def get_success_url(self):
        return resolve_url('home:home')

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)