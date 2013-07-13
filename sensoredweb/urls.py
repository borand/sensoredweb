from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r"^$", views.HomepageView.as_view(), name="home"),
    url(r"^about/", views.AboutView.as_view(), name="about"),
        
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^sensordata/', include('sensordata.urls', namespace="sensordata")),
)

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)
# Add static server if required
# urlpatterns += patterns('',
#     (r'^static/(.*)$', 'django.views.static.serve', {
#         'document_root': settings.STATIC_ROOT
#     }),
# )