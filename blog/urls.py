from django.urls import path

from . import views

urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/remove/', views.PostDeleteView.as_view(), name='post_remove'),
    path('drafts/', views.PostDraftsList.as_view(), name='post_draft_list'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('comment/<int:pk>/approve/', views.approve_comment, name='approve_comment'),
    path('comment/<int:pk>/remove/', views.remove_comment, name='remove_comment')

]
