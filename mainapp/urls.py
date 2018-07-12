"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from mainapp.views import PostListView, TopPostListView, PostContentView

blog_urls = [
    url(r'^all/',PostListView.as_view(),name="all"),
    url(r'^top/',TopPostListView.as_view(),name="top"),
    url(r'^read/(?P<post_id>[0-9]+)',PostContentView.as_view(),name="read"),
]

urlpatterns = [
    url(r'^posts/',include(blog_urls,namespace="posts"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
