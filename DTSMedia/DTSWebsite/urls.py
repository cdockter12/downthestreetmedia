from . import views
from django.urls import path, include
from .views import book_now, AlbumDetail

urlpatterns = [
    path('', views.index, name='index'),
    path('book_now/', views.book_now, name='book-now'),
    path('captcha/', include('captcha.urls')),
    path('gallery/', views.gallery, name='gallery'),
    path('album/<int:pk>',
         views.AlbumDetail.as_view(), name='album-detail'),
]
