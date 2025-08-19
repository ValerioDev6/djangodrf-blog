import redis
from apps.blog.models import Heading, Post, PostAnalytics, PostView
from apps.blog.serializers import HeadingSerializer, PostListSerializer, PostSerializer
from apps.blog.tasks import increment_post_impressions
from apps.blog.utils import get_client_ip
from core.permissions import HasValidApiKey
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions, status
from rest_framework.exceptions import APIException, NotFound
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api.views import StandardAPIView

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)

#  Create your views here.
# class PostListView(ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer


class PostListView(StandardAPIView):
    permission_classes = [HasValidApiKey]

    def get(self, request, *args, **kwargs):
        try:
            cached_posts = cache.get("post_list")
            if cached_posts:
                for post in cached_posts:
                    redis_client.incr(f"post:impressions:{post['id']}")
                return self.paginate(request, cached_posts)

            posts = Post.post_objects.all()

            if not posts.exists():
                raise NotFound(detail="Not posts found")

            serialized_post = PostListSerializer(posts, many=True).data

            cache.set("post_list", serialized_post, timeout=60 * 5)  # Cache

            for post in posts:
                redis_client.incr(f"post:impressions:{post.id}")
                # increment_post_impressions.delay(post.id)

        except Post.DoesNotExist:
            raise NotFound(detail="Not posts found")
        except Exception as e:
            raise APIException(
                detail=f"An unexpected error occurred: {str(e)}", code=500
            )

        return self.paginate(request, serialized_post)


# class PostDetailView(RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     lookup_field = "slug"


class PostDetailView(StandardAPIView):
    # @method_decorator(cache_page(60 * 2))
    def get(self, request, slug):
        try:
            post = Post.post_objects.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound(detail="the request post does not exist")
        except Exception as e:
            raise APIException(
                detail=f"An unexpected error occurred: {str(e)}", code=500
            )
        serialized_post = PostSerializer(post).data

        # increment post views count
        try:
            post_analytics, created = PostAnalytics.objects.get_or_create(post=post)
            post_analytics.increment_views(request)
        except PostAnalytics.DoesNotExist:
            raise NotFound(detail="the request post analytics does not exist")
        except Exception as e:
            raise APIException(
                detail=f"An error ocurred while updating post analytics: {str(e)}",
                code=500,
            )
        return self.response(serialized_post, status=status.HTTP_200_OK)


# class PostHeadingView(ListAPIView):
#     serializer_class = HeadingSerializer

#     def get_queryset(self):
#         post_slug = self.kwargs.get("slug")
#         return Heading.objects.filter(post__slug=post_slug)


class PostHeadingView(StandardAPIView):
    def get(self, request):
        post_slug = request.query_params.get("slug")

        if not post_slug:
            return self.response(
                {"detail": "Slug parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Buscar headings directamente
        heading_objects = Heading.objects.filter(post__slug=post_slug)

        # Si no hay headings, devolver lista vacía (no error)
        serialized_headings = HeadingSerializer(heading_objects, many=True).data

        return self.response(serialized_headings)


class IncrementPostClickView(APIView):
    permission_classes = [permissions.AllowAny]
    """Incrementa el contador de clics de un post basado en su slug"""

    def post(self, request, slug):
        try:
            post = Post.post_objects.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound(
                detail="The requested post does not exist increment clicks! "
            )
        except Exception as e:
            raise APIException(detail=f"Unexpected error: {str(e)}", code=500)

        try:
            # get_or_create devuelve una tupla (obj, created)
            post_analytics, created = PostAnalytics.objects.get_or_create(post=post)
            post_analytics.increment_click()
        except Exception as e:
            raise APIException(
                detail=f"Error while updating post analytics: {str(e)}",
                code=500,
            )

        return Response(
            {
                "message": "Click incremented successfully!",
                "clicks": post_analytics.clicks,
            }
        )
