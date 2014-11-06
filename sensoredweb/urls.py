from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sensoredweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r"^$", views.HomepageView.as_view(), name="home"),    
	url(r'^admin/', include(admin.site.urls)),
    url(r"^about/", views.AboutView.as_view(), name="about"),
    url(r"^debug/", views.DebugView.as_view(), name="debug"),
    (r'^sensordata/', include('sensordata.urls', namespace="sensordata")),

    
)

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)

# Add static server if required
urlpatterns += patterns('',
    (r'^static/(.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT
    }),
)