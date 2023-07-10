from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView

)
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('my/', views.my_home, name='blog-my-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/schedule', views.schedule, name='post-schedule'),
    # not render
    path('save_tour_1/', views.save_tour_1, name='save-tour-1'),
    path('save_tour_2/', views.save_tour_2, name='save-tour-2'),
    path('save_tour_3/', views.save_tour_3, name='save-tour-3'),
    path('save_tour_4/', views.save_tour_4, name='save-tour-4'),
    path('save_tour_5/', views.save_tour_5, name='save-tour-5'),
    path('reset_1/', views.reset_1, name='reset-1'),
    path('reset_2/', views.reset_2, name='reset-2'),
    path('reset_3/', views.reset_3, name='reset-3'),
    path('reset_4/', views.reset_4, name='reset-4'),
    path('reset_5/', views.reset_5, name='reset-5'),
    path('new_files/', views.new_files, name='new-files')
]
