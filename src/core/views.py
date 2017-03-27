from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from blogs.models import Blog, Post
from core.models import User


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
    success_url = "/"
    template_name = "core/registration.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)