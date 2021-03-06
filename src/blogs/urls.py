from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from views import BlogListView, BlogView, PostDetail, CreateBlog
from views import UpdateBlog, CreatePost, UpdatePost, PostLikeAjaxView
from views import PostLikeCount, CommentsPostView

urlpatterns = [
    url(r'^$', BlogListView.as_view(), name='blog_list'),
    url(r'^(?P<pk>\d+)/$', BlogView.as_view(), name='blog'),
    url(r'^add_blog$', login_required(CreateBlog.as_view()), name='add_blog'),
    url(r'^edit_blog/(?P<pk>\d+)', login_required(UpdateBlog.as_view()), name='edit_blog'),
    url(r'^add_post', login_required(CreatePost.as_view()), name='add_post'),
    url(r'^edit_post/(?P<pk>\d+)', login_required(UpdatePost.as_view()), name='edit_post'),
    url(r'post/(?P<pk>\d+)/comments$', CommentsPostView.as_view(), name='post_comments'),
    url(r'post/(?P<pk>\d+)/likes$', PostLikeAjaxView.as_view(), name='post_ajax_like'),
    url(r'post/(?P<pk>\d+)$', PostDetail.as_view(), name='post'),
    url(r'post/likes$', PostLikeCount.as_view(), name='likecount'),

]
