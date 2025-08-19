import uuid

from apps.blog.utils import get_client_ip
from ckeditor.fields import RichTextField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from model_utils.models import SoftDeletableModel


# Create your models here.
def blog_thumbnail_path(instance, filename):
    return "blog/{0}/{1}".format(instance.title, filename)


def category_thumbnail_path(instance, filename):
    return "blog_categories/{0}/{1}".format(instance.name, filename)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    name = models.CharField(max_length=255)
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to=category_thumbnail_path, blank=True, null=True
    )
    slug = models.CharField(max_length=120)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="published")

    status_options = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    content = RichTextField()
    thumbnail = models.ImageField(upload_to=blog_thumbnail_path, blank=True, null=True)
    keywords = models.CharField(max_length=150)
    slug = models.CharField(max_length=150)
    status = models.CharField(max_length=15, choices=status_options, default="draft")

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    objects = models.Manager()  # default manager
    post_objects = PostObjects()  # custom manager

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = (
            "status",
            "-created_at",
        )

    def __str__(self):
        return self.title


class PostView(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_view")
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)


class PostAnalytics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_analytics"
    )
    views = models.PositiveIntegerField(default=0)
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    click_through_rate = models.FloatField(default=0)
    avg_time_on_page = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def increment_click(self):
        self.clicks += 1
        self._update_click_through_rate()
        self.save()

    def _update_click_through_rate(self):
        if self.impressions > 0:
            self.click_through_rate = (self.clicks / self.impressions) * 100
        else:
            self.click_through_rate = 0
        self.save()

    def increment_impressions(self):
        self.impressions += 1
        self._update_click_through_rate()
        self.save()

    def increment_views(self, request):
        ip_address = get_client_ip(request)

        # Solo incrementar si es una IP nueva para este post
        if not PostView.objects.filter(post=self.post, ip_address=ip_address).exists():
            PostView.objects.create(post=self.post, ip_address=ip_address)
            self.views += 1
            self.save()


class Heading(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="heading")
    title = models.CharField(max_length=150)
    slug = models.CharField(max_length=150)

    level = models.IntegerField(
        choices=(
            (1, "h1"),
            (2, "h2"),
            (3, "h3"),
            (4, "h4"),
            (5, "h5"),
            (6, "h6"),
        ),
    )

    order = models.PositiveBigIntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]
        managed = True
        verbose_name = "Heading"
        verbose_name_plural = "Headings"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


@receiver(post_save, sender=Post)
def create_post_analytics(sender, instance, created, **kwargs):
    if created:
        PostAnalytics.objects.create(post=instance)
