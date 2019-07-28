"""Blogpost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.postListView, name='post_list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.postListView, name='post_list_by_tag_name'),
    url(r'^(?P<id>\d+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',views.postDetailsView, name='post_detail'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.postDetailsView, name='post_details_by_tag_name'),
    url(r'^(?P<id>\d+)/share/$', views.emailSendView, name='sendmail'),
    url(r'^create/', views.createPostView, name='create_blog'),
    url(r'^login/$', views.userLoginView, name='user_login'),
    url(r'^logout/$', views.userLogoutView, name='user_logout'),
    url(r'^registration/$', views.userRegistrationView, name='user_signup'),
    url(r'^edit_profile/$', views.editProfileView, name='edit_profile'),
    url(r'^like/(?P<post_id>\d+)', views.likePostView, name='like_post'),
    url(r'^myposts/$', views.myPostView, name='my_posts'),
    url(r'^myposts/edit/(?P<id>\d+)/$', views.postEditView, name='post_edit'),
    url(r'myposts/delete/(?P<id>\d+)/$', views.postDeleteView, name='post_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
