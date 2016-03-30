"""colenso URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from web_views import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_letter$', views.add_letter),
    url(r'^search[/]$', views.search, name='search'),
    url(r'^search/large[/]$', views.large_search),
    url(r'^search/history[/]$', views.search_history),
    url(r'^search/history/mine[/]$', views.my_search_history),
    url(r'^letters/(?P<l_id>\w+)/edit[/]$', views.edit_letter),
    url(r'^letters/(?P<l_id>\w+)[/]$', views.letter_detail),
]
