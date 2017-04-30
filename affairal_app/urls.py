from django.conf.urls import url, include

from rest_framework.authtoken import views as tokenview

from rest_framework.urlpatterns import format_suffix_patterns

import views

urlpatterns = [

    url(r'^user/$', views.AffairalUserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)$', views.AffairalUserDetail.as_view()),

    url(r'^event/$', views.EventList.as_view()),
    url(r'^event/(?P<pk>[0-9]+)$', views.EventDetail.as_view()),

    url(r'^token/', tokenview.obtain_auth_token),

]