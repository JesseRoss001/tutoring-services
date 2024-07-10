from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('book/', views.book_session, name='book_session'),
    path('reviews/', views.reviews, name='reviews'),
    path('api/reviews/', views.reviews_api, name='reviews_api'),
]
