from apps.blog.models import Category, Heading, Post, PostView
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug"]


class HeadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heading
        fields = ["title", "slug", "level", "order"]


class PostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostView
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    heading = HeadingSerializer(many=True)
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_view_count(self, obj):
        return obj.post_view.count()


class PostListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    # views = PostViewSerializer(many=True, source="post_view")
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "thumbnail",
            "category",
            # "views",
            "view_count",
        ]

    def get_view_count(self, obj):
        return obj.post_view.count()
