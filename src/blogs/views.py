from django.views.generic import ListView, DetailView
from models import Post, Blog
# Create your views here.

class PostListView(ListView):
    template_name = 'blogs/blog.html'
    queryset = Post.objects.all()

class PostView(DetailView):
    template_name = 'blogs/one_post.html'
    queryset = Post.objects.all()

class BlogView(DetailView):
    template_name = 'blogs/blog.html'
    queryset = Blog.objects.all()

class BlogListView(ListView):
    template_name = 'blogs/blog_list.html'
    queryset = Blog.objects.all()