"""hwserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from api import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.main),

    url(r'^api/v1/auth/', include('user_auth.urls')),

    url(r'^api/v1/vendors/', include('api.urls_set.vendors')),

    url(r'^api/v1/school/', include('api.urls_set.school')),
    url(r'^api/v1/classroom/', include('api.urls_set.classroom')),
    url(r'^api/v1/homework/', include('api.urls_set.homework')),
    url(r'^api/v1/comment/', include('api.urls_set.comment')),
    url(r'^api/v1/updates/', include('api.urls_set.updates')),

    url(r'^api/v1/qa/', include('api.urls_set.qa')),

]
