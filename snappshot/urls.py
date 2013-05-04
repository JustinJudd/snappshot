from django.conf.urls import patterns, include, url

urlpatterns = patterns('snappshot.views',
    url(r'^$', 'index', name='home'),
    url(r'^upload/(?P<image_id>\d+)/$', 'upload_screenshot', name='upload'),
    url(r'^uploaded/(?P<image_id>\d+)/$', 'uploaded_screenshot', name='uploaded'),
    url(r'^image/(?P<image_id>\d+)/$', 'get_image', name='get_image'),
    url(r'^faq$', 'faq', name='faq'),
    url(r'^screenshot/(?P<width>\d+)x(?P<height>\d+)', 'get_screenshot', name='screenshot'),
)
