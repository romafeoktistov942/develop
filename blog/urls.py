from django.urls import path
from django.conf.urls.static import static
from blog.apps import BlogConfig
from blog.views import (
    BlogCreateView,
    BlogListView,
    BlogDetailView,
    BlogUpdateView,
    BlogDeleteView,
)
from config import settings

app_name = BlogConfig.name

urlpatterns = [
    path("blog/create/", BlogCreateView.as_view(), name="blog_create"),
    path("", BlogListView.as_view(), name="blog_list"),
    path("blog/<str:slug>/", BlogDetailView.as_view(), name="blog_detail"),
    path("blog/<str:slug>/delete/", BlogDeleteView.as_view(), name="blog_delete"),
    path("blog/<str:slug>/update/", BlogUpdateView.as_view(), name="blog_update"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
