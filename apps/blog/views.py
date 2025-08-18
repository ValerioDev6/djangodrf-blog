from apps.blog.models import Heading, Post, PostView
from apps.blog.serializers import HeadingSerializer, PostListSerializer, PostSerializer
from apps.blog.utils import get_client_ip
from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

#  Create your views here.
# class PostListView(ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer


class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.post_objects.all()
        serialized_post = PostListSerializer(posts, many=True).data
        return Response(serialized_post)


# class PostDetailView(RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     lookup_field = "slug"


class PostDetailView(APIView):
    def get(self, request, slug):
        post = Post.post_objects.get(slug=slug)
        serialized_post = PostSerializer(post).data

        client_ip = get_client_ip(request)
        if PostView.objects.filter(post=post, ip_address=client_ip).exists():
            return Response(serialized_post)

        PostView.objects.create(post=post, ip_address=client_ip)
        
        return Response(serialized_post)


class PostHeadingView(ListAPIView):
    serializer_class = HeadingSerializer

    def get_queryset(self):
        post_slug = self.kwargs.get("slug")
        return Heading.objects.filter(post__slug=post_slug)

    # def get_queryset(self):
    #     return Post.objects.all().order_by('-created_at')
