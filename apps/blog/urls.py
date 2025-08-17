from apps.blog.views import PostDetailView, PostHeadingView, PostListView
from django.urls import path

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<str:slug>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<slug>/headings/", PostHeadingView.as_view(), name="post-heading"),
]
