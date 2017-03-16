from django.conf.urls import url
from views import BlogListView, BlogView, PostView

urlpatterns = [
    url(r'^$', BlogListView.as_view(), name='blog_list'),
    url(r'^(?P<pk>\d+)/$', BlogView.as_view(), name='blog'),
    url(r'post/(?P<pk>\d+)$', PostView.as_view(), name='post'),
]
