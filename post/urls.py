from django.urls import path
from . import views


app_name = 'post'
urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('<int:post_id>/<slug:post_slug>/', views.PostDetailView.as_view(), name='detail'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('delete/<int:post_id>/', views.PostDeleteView.as_view(), name='delete'),
    path('update/<int:post_id>/', views.PostUpdateView.as_view(), name='update'),
    path('reply/<int:post_id>/<int:comment_id>/', views.PostAddReplyView.as_view(), name='add_reply'),
]