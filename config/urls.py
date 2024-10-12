from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalog.urls", namespace='catalog')),
    path("users/", include("users.urls", namespace='users')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
