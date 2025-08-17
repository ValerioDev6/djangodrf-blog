from apps.blog.models import Category, Heading, Post
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


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    heading = HeadingSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "thumbnail",
            "category",
            "views",
        ]
