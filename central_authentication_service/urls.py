from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
import rest_framework.authtoken.views
import allauth.urls as allauth_urls

router = DefaultRouter()
# router.register(r'users', views.UserViewSet)

admin.autodiscover()

urlpatterns = patterns(
    '',
    # prevent the extra are-you-sure-you-want-to-logout step on logout
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

    url(r'^', include('casapp.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)