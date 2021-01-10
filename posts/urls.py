from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.post_new, name='post_new'),
    path('<str:username>/', views.profile, name='profile'),
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    path('about/', include('about.urls', namespace='about')),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path(
         '<str:username>/<int:post_id>/edit/',
         views.post_edit,
         name='post_edit'
         )
]
