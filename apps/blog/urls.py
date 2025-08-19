from apps.blog.views import (
    IncrementPostClickView,
    PostDetailView,
    PostHeadingView,
    PostListView,
)
from django.urls import path

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/headings/", PostHeadingView.as_view(), name="post-heading"),
    path("posts/<str:slug>/", PostDetailView.as_view(), name="post-detail"),
    path(
        "posts/<slug:slug>/increment_clicks",
        IncrementPostClickView.as_view(),
        name="post-increment-clicks",
    ),
]
