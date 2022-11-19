from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, Search, CreatePost, UpdatePost, DeletePost, CategoryList, subscribe


urlpatterns = [
   path('', PostList.as_view(), name='news'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', Search.as_view()),
   path('create/', CreatePost.as_view(), name='post_create'),
   path('<int:pk>/edit/', UpdatePost.as_view(), name='post_update'),
   path('<int:pk>/delete/', DeletePost.as_view(), name='post_delete'),
   path('categories/<int:pk>', CategoryList.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe/', subscribe, name='subscribe')
]
