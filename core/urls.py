from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("test/", TestView.as_view(), name="test"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
