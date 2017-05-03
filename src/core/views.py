from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.views import deprecate_current_app, _get_login_redirect_url
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from blogs.models import Blog, Post


class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['blogs_count'] = Blog.objects.all().count()
        context['posts_count'] = Post.objects.all().count()
        return context


class UserRegForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", 'avatar')
        field_classes = {'username': UsernameField}


class RegisterFormView(CreateView):
    form_class = UserRegForm
    template_name = "core/registration.html"

    def get_success_url(self):
        return resolve_url('home:home')

    def form_valid(self, form):
        form.save()
        super(RegisterFormView, self).form_valid(form)
        return HttpResponse("OK")


@deprecate_current_app
@sensitive_post_parameters()
@csrf_protect
@never_cache
def my_login_view(request, template_name='registration/login.html',
                  redirect_field_name=REDIRECT_FIELD_NAME,
                  authentication_form=AuthenticationForm,
                  extra_context=None, redirect_authenticated_user=False):
    redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))

    if redirect_authenticated_user and request.user.is_authenticated:
        redirect_to = _get_login_redirect_url(request, redirect_to)
        if redirect_to == request.path:
            raise ValueError(
                "Redirection loop for authenticated user detected. Check that "
                "your LOGIN_REDIRECT_URL doesn't point to a login page."
            )
        return HttpResponseRedirect(redirect_to)
    elif request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponse("OK")
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)
    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)
