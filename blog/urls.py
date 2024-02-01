from django.urls import path
from django.views.decorators.cache import never_cache

from blog.apps import BlogConfig
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, published_toggle

app_name = BlogConfig.name

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('view/<int:pk>/', PostDetailView.as_view(), name='post_view'),
    path('create/', never_cache(PostCreateView.as_view()), name='post_create'),
    path('edit/<int:pk>/', PostUpdateView.as_view(), name='post_edit'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('published/<int:pk>', published_toggle, name='published_toggle'),
]