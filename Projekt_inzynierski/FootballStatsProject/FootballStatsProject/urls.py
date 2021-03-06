"""FootballStatsProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from FootballStats import views

urlpatterns = [
    url(r"^index/$", views.index, name="index"),
    url(r"^admin/", admin.site.urls),
    url(r"^login/?$", views.login, name="login"),
    url(r"^register/?$", views.register, name="register"),
    url(r"^logout/?$", views.logout, name="logout"),
    url(r"^/?$", views.uploaded_files, name="uploaded_files"),
    url(r"^edit-user/(?P<user_id>\d+)/?$", views.edit_user, name="edit-user"),
    url(r"^info/?$", views.info, name="info"),
    url(r"^users/?$", views.users, name="users"),
    url(r"^users_files/?$", views.users_files, name="users_files"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)