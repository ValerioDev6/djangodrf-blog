from apps.blog.models import Category, Heading, Post, PostAnalytics
from django import forms
from django.contrib import admin

# Register your models here.


# admin.site.register(Category)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "parent", "slug")
    search_fields = ("name", "title", "description", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("parent__name",)
    ordering = ("name",)


class HeadingInline(admin.TabularInline):
    model = Heading
    extra = 1
    fields = (
        "title",
        "level",
        "order",
        "slug",
    )
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "category", "created_at")
    search_fields = ("title", "slug")
    list_filter = ("category", "status")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)
    list_editable = ("status",)

    fieldsets = (
        (
            "General Information",
            {
                "fields": (
                    "title",
                    "description",
                    "content",
                    "thumbnail",
                    "keywords",
                    "slug",
                    "category",
                )
            },
        ),
        (
            "Status & Dates",
            {
                "fields": (
                    "status",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    inlines = [HeadingInline]


@admin.register(Heading)
class HeadingAdmin(admin.ModelAdmin):
    list_display = ("title", "post", "level", "order")
    search_fields = ("title", "post__title")
    list_filter = ("level", "post")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("post", "order")
    # list_editable = ("parent",)


# serial keygen: NAVJ-JE47-EQWB-PT2V
@admin.register(PostAnalytics)
class PostAnalyticsAdmin(admin.ModelAdmin):
    list_display = (
        "post_title",
        "views",
        "impressions",
        "clicks",
        "click_through_rate",
        "avg_time_on_page",
    )
    search_fields = ("post__title",)
    readonly_fields = (
        "views",
        "impressions",
        "clicks",  # Corregido
        "click_through_rate",  # Corregido
        "avg_time_on_page",
    )

    def post_title(self, obj):
        return obj.post.title

    post_title.short_description = "Post Title"
