from django.urls import path
from .views import HomeView, PostDetailView, PostDeleteView, PostUpdateView, CreatePostView

app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<int:post_id>/<post_slug>/', PostDetailView.as_view(), name='detail'),
    path('delete/<int:post_id>/', PostDeleteView.as_view(), name='delete'),
    path('post/update/<int:post_id>/', PostUpdateView.as_view(), name='post_update'),
    path('post/create/', CreatePostView.as_view(), name='post_create'),
]