"""dataViz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from .admin import admin_site
from . import settings
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

wagtail_urlpatterns = [
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('', include(wagtail_urls)),
]

urlpatterns = [
    path('dashboard/', include("dashboard.urls")),
    #path("social/", include("blocks.urls")),
    path("data/", include("data.urls")),
    path('admin/', admin_site.urls),
    path("users/", include("users.urls")),
    path("energy/", include("energy_utils.urls")),
    path("api-v2/", include("study_notes.urls")),
    path("search/", include("wagtail_home.urls")),
    path("stocks/", include("stocks.urls")),
    path("time-booking/", include("time_booking.urls"))
]
urlpatterns.extend(wagtail_urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)