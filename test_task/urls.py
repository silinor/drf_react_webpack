from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers
from accounts.views import UserViewSet


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
]

router = routers.SimpleRouter()
router.register(r'user', UserViewSet, base_name='user')

urlpatterns += router.urls