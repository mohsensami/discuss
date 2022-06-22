from django.urls import path
from . import views


app_name = 'post'
urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('<int:post_id>/<slug:post_slug>/', views.PostDetailView.as_view(), name='detail'),
]