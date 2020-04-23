"""SoftwareEngineering URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from user import urls as user_urls
from owner import urls as owner_urls

admin.site.site_header = 'MunchBox Admin'
admin.site.site_title = 'MunchBox Site Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^owner/',
        include(owner_urls), name = 'owner'),
    url(r'^user/',
        include(user_urls)),
    url(r'',include('MunchBox.urls')),
    # Next to each url in user, we append dj-auth so that we don't hav problems with admin login and logout views.
]
