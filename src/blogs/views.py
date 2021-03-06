# -*- coding: utf-8 -*-
from datetime import date, datetime

from django import forms
from django.shortcuts import get_object_or_404, resolve_url
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.http import HttpResponse, JsonResponse

from comments.models import Comment
from models import Post, Blog, Category, LikePost


# Create your views here.

class BlogView(DetailView):
    template_name = 'blogs/blog.html'
    queryset = Blog.objects.all()


class SortForm(forms.Form):
    sort = forms.ChoiceField(
        choices=(
            ('title', u'Заголовок'),
            ('description', u'Описание'),
            ('id', u'id'),
        ),
        widget=forms.RadioSelect
    )
    search = forms.CharField(required=False, widget=forms.TextInput)


class BlogListView(ListView):
    template_name = 'blogs/blog_list.html'
    queryset = Blog.objects.all()
    sortform = None

    def dispatch(self, request, *args, **kwargs):
        self.sortform = SortForm(self.request.GET)
        return super(BlogListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(BlogListView, self).get_queryset()
        if self.sortform.is_valid():
            queryset = queryset.order_by(self.sortform.cleaned_data['sort'])
            if self.sortform.cleaned_data['search']:
                queryset = queryset.filter(title__icontains=self.sortform.cleaned_data['search'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data()
        context['sortform'] = self.sortform
        return context


class UpdateBlog(UpdateView):
    template_name = "blogs/edit_blog.html"
    model = Blog
    fields = ('title', 'description', 'category')

    def get_success_url(self):
        return resolve_url('blogs:blog', pk=self.object.id)

    def get_queryset(self):
        return super(UpdateBlog, self).get_queryset().filter(author=self.request.user)

    def form_valid(self, form):
        response = super(UpdateBlog, self).form_valid(form)
        return HttpResponse('OK')


class CreateBlog(CreateView):
    template_name = "blogs/add_blog.html"
    model = Blog
    fields = ('title', 'description', 'category')

    def get_success_url(self):
        return resolve_url('blogs:blog', pk=self.object.id)

    def get_form(self, form_class=None):
        form = super(CreateBlog, self).get_form()
        form.fields['category'].queryset = Category.objects.all()
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateBlog, self).form_valid(form)


class UpdatePost(UpdateView):
    template_name = "blogs/edit_post.html"
    model = Post
    fields = ('title', 'description')

    def get_success_url(self):
        return resolve_url('blogs:post', pk=self.object.id)

    def get_queryset(self):
        return super(UpdatePost, self).get_queryset().filter(blog__author=self.request.user)

    def form_valid(self, form):
        super(UpdatePost, self).form_valid(form)
        return HttpResponse('OK')


class CreatePost(CreateView):
    template_name = "blogs/add_post.html"
    model = Post
    fields = ('title', 'description', 'blog')

    def get_success_url(self):
        return resolve_url('blogs:post', pk=self.object.id)

    def get_form(self, form_class=None):
        form = super(CreatePost, self).get_form()
        form.fields["blog"].queryset = Blog.objects.all().filter(author=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreatePost, self).form_valid(form)


class PostDetail(CreateView):
    model = Comment
    template_name = 'blogs/one_post.html'
    fields = ('text',)

    def get_success_url(self):
        return resolve_url('blogs:post', pk=self.postobject.id)

    def form_valid(self, form):
        form.instance.post = self.postobject
        form.instance.author = self.request.user
        return super(PostDetail, self).form_valid(form)

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.postobject = get_object_or_404(Post, id=pk)
        return super(PostDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['post'] = self.postobject
        return context


class PostLikeAjaxView(View):
    post_object = None

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.post_object = get_object_or_404(Post, id=pk)
        return super(PostLikeAjaxView, self).dispatch(request, *args, **kwargs)

    def post(self, data):
        if self.post_object.likes.filter(author=self.request.user).exists():
            self.post_object.likes.filter(author=self.request.user).delete()
        else:
            like = LikePost()
            like.post = self.post_object
            like.author = self.request.user
            like.save()
        return HttpResponse(LikePost.objects.filter(post=self.post_object).count())


class PostLikeCount(View):

    def get(self, request):
        postids = request.GET.get('posts', '')
        postids = postids.split(',')
        dict_like = {}
        for ids in postids:
            dict_like[ids] = LikePost.objects.filter(post=ids).count()
        return JsonResponse(dict_like)


class CommentsPostView(DetailView):
    template_name = 'blogs/comment.html'
    queryset = Post.objects.all()