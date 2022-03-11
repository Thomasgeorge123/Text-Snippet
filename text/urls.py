from django.urls import path
from .views import *
from django.urls import re_path
from authentication import views
urlpatterns = [
    re_path('tag/',Tags.as_view(),name='tag'),
    re_path('snippet/',Snippets.as_view(),name='snippet'),
    re_path('snippetbytagid/(?P<tag_id>[0-9]+)/$',SnippetByTagId.as_view(),name='snippetbytagid'),
    re_path('snippentbyid/(?P<pk>[0-9]+)/$',SnippetById.as_view(),name='snippentbyid'),
    re_path('overview/',Overview.as_view(),name='overview'),
]